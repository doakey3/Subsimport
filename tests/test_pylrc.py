import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

from operators.pylrc.parser import parse
from operators.pysrt.srtfile import SubRipFile
from operators.pysrt.convert_enhanced import convert_enhanced

class TestPyLRC(unittest.TestCase):
    def setUp(self):
        self.static_path = os.path.join(file_path, 'tests', 'static')
        lyrics_path = os.path.join(self.static_path, 'I Move On.lrc')
        f = open(lyrics_path)
        self.lyrics = parse(f.read())
        f.close()

        lyrics_path = os.path.join(self.static_path, 'I Move On_bases.srt')
        f = open(lyrics_path)
        self.base_comparison = f.read()
        f.close()

        lyrics_path = os.path.join(self.static_path, 'I Move On_tops.srt')
        f = open(lyrics_path)
        self.tops_comparison = f.read()
        f.close()

        lyrics_path = os.path.join(self.static_path, 'non_subsimport.lrc')
        f = open(lyrics_path)
        self.non_subsimport = parse(f.read())
        f.close()

    def test_parsing(self):
        self.maxDiff = None
        srt_string = self.lyrics.to_SRT()
        subs = SubRipFile().from_string(srt_string)
        bases, tops, color = convert_enhanced(subs)
        self.assertEqual(1, 1)
        self.assertEqual(self.base_comparison, bases.to_string())
        self.assertEqual(self.tops_comparison, tops.to_string())

        srt_string = self.non_subsimport.to_SRT()
        subs = SubRipFile().from_string(srt_string)
        bases, tops, color = convert_enhanced(subs)


if __name__ == '__main__':
    unittest.main()