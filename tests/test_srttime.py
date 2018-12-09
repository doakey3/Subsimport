import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

from operators.pysrt.srttime import SubRipTime

x = SubRipTime()
x.from_millis(500000)
# 00:08:20,000
print(x)