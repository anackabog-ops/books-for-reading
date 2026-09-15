import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location('chapter_audio', Path(__file__).resolve().parents[1] / 'scripts/generate-chapter-audio.py')
audio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio)


class CastingTest(unittest.TestCase):
    def test_bookmark_offsets_include_every_voice_switch_gap(self):
        phrases = [
            {'mark': 'a', 'voice': 'lt-LT-LeonasNeural'},
            {
                'mark': 'b',
                'voice': 'lt-LT-OnaNeural',
                'segments': [
                    {'text': 'one', 'voice': 'lt-LT-OnaNeural'},
                    {'text': 'two', 'voice': 'lt-LT-LeonasNeural'},
                    {'text': 'three', 'voice': 'lt-LT-OnaNeural'},
                ],
            },
            {'mark': 'c', 'voice': 'lt-LT-OnaNeural'},
            {'mark': 'd', 'voice': 'lt-LT-LeonasNeural'},
        ]
        offsets = {'a': 0.1, 'b': 1.0, 'c': 2.0, 'd': 3.0}

        self.assertEqual(
            [0, 1.0625, 2.1875, 3.25],
            audio.correct_bookmark_offsets(phrases, offsets),
        )

    def test_narrator_inside_female_dialogue_keeps_text_and_one_bookmark(self):
        self.assertTrue(hasattr(audio, 'build_ssml'), 'reviewed mixed-voice casting is missing')
        text = '— Ačiū. Aš Ieva, — pasakė ji.'
        chapter = {'blocks': [{'type': 'dialogue', 'items': [{'text': text}]}]}
        ssml, phrases = audio.build_ssml(chapter, [1], {'1:1': ['— pasakė ji.']})
        root = ET.fromstring(ssml)
        ns = {'s': 'http://www.w3.org/2001/10/synthesis'}
        voices = root.findall('s:voice', ns)
        self.assertEqual(['lt-LT-OnaNeural', 'lt-LT-LeonasNeural'], [v.attrib['name'] for v in voices])
        self.assertEqual(text, ''.join(root.itertext()).strip())
        self.assertEqual(1, len(root.findall('.//s:bookmark', ns)))
        self.assertEqual(text, ''.join(s['text'] for s in phrases[0]['segments']))
        self.assertIn('pasakė ji', ''.join(voices[1].itertext()))

    def test_narration_can_precede_resumed_female_speech(self):
        self.assertTrue(hasattr(audio, 'build_ssml'))
        text = '— pasakė Ieva. — Taip buvo parašyta.'
        chapter = {'blocks': [{'type': 'dialogue', 'items': [{'text': text}]}]}
        _, phrases = audio.build_ssml(chapter, [1], {'1:1': ['— pasakė Ieva.']})
        self.assertEqual(['lt-LT-LeonasNeural', 'lt-LT-OnaNeural'], [s['voice'] for s in phrases[0]['segments']])

    def test_female_narrator_and_male_dialogue_preserve_speaker_insertions(self):
        text = '– Taip, – atsakė jis.'
        chapter = {'blocks': [{'type': 'paragraph', 'items': [{'text': text}]}]}
        ssml, phrases = audio.build_ssml(chapter, [], {'1:1': [', – atsakė jis.']},
                                        'lt-LT-OnaNeural', {'1': 'lt-LT-LeonasNeural'})
        ET.fromstring(ssml)
        self.assertEqual(['lt-LT-LeonasNeural', 'lt-LT-OnaNeural'],
                         [segment['voice'] for segment in phrases[0]['segments']])
        self.assertEqual(text, ''.join(segment['text'] for segment in phrases[0]['segments']))
        with self.assertRaises(ValueError):
            audio.build_ssml(chapter, [], {}, 'lt-LT-OnaNeural', {'2': 'lt-LT-LeonasNeural'})

    def test_reference_numbers_are_not_spoken(self):
        chapter = {'blocks': [{'type': 'paragraph', 'items': [{'text': 'Žodis. [3]'}]}]}
        ssml, phrases = audio.build_ssml(chapter, [], {})
        self.assertEqual('Žodis.', phrases[0]['text'])
        self.assertNotIn('[3]', ssml)

    def test_stale_casting_is_rejected_before_synthesis(self):
        self.assertTrue(hasattr(audio, 'build_ssml'))
        chapter = {'blocks': [{'type': 'dialogue', 'items': [{'text': '— Ačiū.'}]}]}
        with self.assertRaises(ValueError):
            audio.build_ssml(chapter, [1], {'1:1': ['missing words']})
        with self.assertRaises(ValueError):
            audio.build_ssml(chapter, [1], {'2:1': ['— Ačiū.']})


if __name__ == '__main__':
    unittest.main()

