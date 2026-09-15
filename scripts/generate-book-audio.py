#!/usr/bin/env python3
"""Generate or prepare every chapter, reusing cached Azure synthesis."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('book', type=Path)
    parser.add_argument('--casting', type=Path, required=True)
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--credentials', type=Path)
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    book = json.loads(args.book.read_text())
    casting = json.loads(args.casting.read_text())
    if not all(c['id'] in casting.get('chapters', {}) for c in book['chapters']):
        parser.error('Every chapter needs a reviewed casting plan')
    generator = Path(__file__).with_name('generate-chapter-audio.py')
    for n in range(1, len(book['chapters']) + 1):
        command = [sys.executable, str(generator), str(args.book), '--chapter', str(n),
                   '--casting', str(args.casting), '--work-dir', str(args.work_dir / f'chapter-{n}')]
        if args.credentials:
            command += ['--credentials', str(args.credentials)]
        if args.prepare_only:
            command.append('--prepare-only')
        subprocess.run(command, check=True)


if __name__ == '__main__':
    main()
