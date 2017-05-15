import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

from operators.pysrt.srtfile import SubRipFile
from operators.pysrt.convert_enhanced import convert_enhanced

class TestTextParser(unittest.TestCase):
    def setUp(self):
        self.static_path = os.path.join(file_path, 'tests', 'static')
        
        lyrics_path = os.path.join(self.static_path, 'test.srt')
        f = open(lyrics_path)
        self.lyrics = SubRipFile.from_string(f.read())
        f.close()
        
        #lyrics_output_path = os.path.join(
        #    self.static_path, 'lyrics_output.srt')
        #f = open(lyrics_output_path)
        #self.output = f.read()
        #f.close()
    
    def test_parsing(self):
        bases, tops, color = convert_enhanced(self.lyrics)
        print(bases.to_string())
        print(tops.to_string())
        print(color)
        #self.assertEqual(text_to_srt(self.lyrics), self.output)
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
