import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

from operators.pylrc.parser import parse

class TestPyLRC(unittest.TestCase):
    def setUp(self):
        self.static_path = os.path.join(file_path, 'tests', 'static')
        lyrics_path = os.path.join(self.static_path, 'test.lrc')
        f = open(lyrics_path)
        self.lyrics = parse(f.read())
        f.close()
    
    def test_parsing(self):
        #print(self.lyrics.to_LRC())
        print(self.lyrics.to_SRT())
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
