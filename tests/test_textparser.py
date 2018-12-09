import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

from operators.textparser.parser import text_to_srt

class TestTextParser(unittest.TestCase):
    def setUp(self):
        self.static_path = os.path.join(file_path, 'tests', 'static')

        lyrics_path = os.path.join(self.static_path, 'I Move On.txt')
        f = open(lyrics_path)
        self.lyrics = f.read()
        f.close()

        lyrics_output_path = os.path.join(
            self.static_path, 'I Move On_unsynchronized.srt')
        f = open(lyrics_output_path)
        self.output = f.read().rstrip()
        f.close()

    def test_parsing(self):
        self.maxDiff = None
        self.assertEqual(text_to_srt(self.lyrics), self.output)

if __name__ == '__main__':
    unittest.main()