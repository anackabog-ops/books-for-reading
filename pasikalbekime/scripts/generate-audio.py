#!/usr/bin/env python3
"""Generate cached, static Lithuanian MP3s. Never call Azure from the browser.

Uses the same private F0 credentials file as the repository's chapter generator.
API reference: https://learn.microsoft.com/azure/ai-services/speech-service/rest-text-to-speech
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]


def duration(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                             '-of', 'default=noprint_wrappers=1:nokey=1', str(path)],
                            capture_output=True, text=True, check=True)
    seconds = float(result.stdout.strip())
    if seconds <= 0:
        raise ValueError('Empty audio')
    return seconds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--credentials', type=Path, default=Path.home() / '.azure/lietuviskos-knygos-speech.json')
    parser.add_argument('--voice', choices=['lt-LT-OnaNeural', 'lt-LT-LeonasNeural'], default='lt-LT-OnaNeural')
    parser.add_argument('--limit', type=int, default=100)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error('--limit must be from 1 to 100')
    source = (ROOT / 'questions.json').read_bytes()
    questions = json.loads(source)['questions'][:args.limit]
    print(f'{len(questions)} questions; {sum(len(q["lt"]) for q in questions)} characters; {args.voice}')
    if args.check_only:
        return
    if not args.credentials.exists():
        raise SystemExit('Speech credentials are not configured. Keep the private credentials file outside the repository.')
    if not shutil.which('ffprobe'):
        raise SystemExit('ffprobe is required to validate MP3 recordings.')
    credentials = json.loads(args.credentials.read_text())
    if credentials.get('sku') != 'F0':
        raise SystemExit('Expected the configured F0 resource; refusing to switch to a paid resource.')
    region = credentials['SPEECH_REGION']
    if not re.fullmatch('[a-z0-9]+', region):
        raise SystemExit('Invalid Speech region')
    endpoint = f'https://{region}.tts.speech.microsoft.com/cognitiveservices/v1'
    manifest_path = ROOT / 'audio.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    output = ROOT / 'assets/audio'
    output.mkdir(parents=True, exist_ok=True)
    for q in questions:
        ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="lt-LT"><voice name="{args.voice}">{escape(q["lt"])}</voice></speak>'
        digest = hashlib.sha256(ssml.encode()).hexdigest()[:16]
        relative = f'assets/audio/{q["id"]}-{digest}.mp3'
        target = ROOT / relative
        if not target.exists():
            request = urllib.request.Request(endpoint, data=ssml.encode(), headers={
                'Ocp-Apim-Subscription-Key': credentials['SPEECH_KEY'],
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3',
                'User-Agent': 'AnackaConversationCards'
            }, method='POST')
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    content = response.read()
            except urllib.error.HTTPError as error:
                raise SystemExit(f'Azure returned HTTP {error.code}. Generation stopped; existing audio retained. Check credentials or F0 quota.') from None
            except urllib.error.URLError:
                raise SystemExit('Unable to reach Azure. Generation stopped; existing audio retained.') from None
            temporary = target.with_suffix('.tmp.mp3')
            temporary.write_bytes(content)
            duration(temporary)
            temporary.replace(target)
        seconds = duration(target)
        if (ROOT / 'questions.json').read_bytes() != source:
            raise SystemExit('Questions changed during synthesis. Audio is cached; manifest left unchanged for this question.')
        manifest[q['id']] = dict(file=relative, text=q['lt'], voice=args.voice, duration=seconds)
        temporary_manifest = manifest_path.with_suffix('.tmp.json')
        temporary_manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        temporary_manifest.replace(manifest_path)
        print(f'{q["id"]}: {seconds:.1f}s ready', flush=True)
    print('Review recordings, then commit assets/audio and audio.json. No key belongs in a commit.')


if __name__ == '__main__':
    main()
