import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

from operators.pysrt.srtfile import SubRipFile
from operators.pysrt.convert_enhanced import convert_enhanced

class TestPySRT(unittest.TestCase):
    def setUp(self):
        self.static_path = os.path.join(file_path, 'tests', 'static')

        lyrics_path = os.path.join(self.static_path, 'I Move On.srt')
        f = open(lyrics_path)
        self.lyrics = SubRipFile.from_string(f.read())
        f.close()

        lyrics_bases = os.path.join(
            self.static_path, 'I Move On_bases.srt')
        f = open(lyrics_bases, 'r')
        self.lyrics_bases = f.read()
        f.close()

        lyrics_tops = os.path.join(
            self.static_path, 'I Move On_tops.srt')
        f = open(lyrics_tops, 'r')
        self.lyrics_tops = f.read()
        f.close()

    def test_parsing(self):
        self.maxDiff = None
        bases, tops, color = convert_enhanced(self.lyrics)
        self.assertEqual(bases.to_string(), self.lyrics_bases)
        self.assertEqual(tops.to_string().rstrip(), self.lyrics_tops.rstrip())
        self.assertEqual(color, "#ff8800")
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()