# This script was used to get the hyphenator patterns from https://github.com/mnater/Hyphenopoly

import os
import ntpath

def remove_punctuation(word):
    """Remove punctuation from the beginning and end of a word"""

    puncs = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\n', '(',
             ')', '!', '@', '#', '$', '%', '^', '-', '+', '=', "'",
             ';', ',', '.', '{', '}','[', ']']

    while word[0] in puncs:
        word = word[1::]

    while word[-1] in puncs:
        word = word[0:-1]

    return word

def extract_patterns(path):
    patterns = []

    f = open(path, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()

    important_lines = []
    for i in range(len(lines)):
        try:
            step = int(remove_punctuation(lines[i].strip().split(':')[0]))
            important_lines.append(lines[i])
        except:
            pass

    for i in range(len(important_lines)):
        step = int(remove_punctuation(important_lines[i].strip().split(':')[0]))
        text = remove_punctuation(important_lines[i].split(':')[-1].strip())
        while len(text) > 0:
            patterns.append(text[0:step].replace('_', '.'))
            text = text[step::]

    return patterns

if __name__ == '__main__':
    files = os.listdir(os.getcwd())

    for file in files:
        if file.endswith('.js'):
            patterns = list(sorted(extract_patterns(file)))
        fname = os.path.splitext(ntpath.basename(file))[0]

        f = open(os.path.join('/home/doakey/Desktop/new_patterns', fname + '.txt'), 'w', encoding='utf-8')
        f.write('\n'.join(patterns))
        f.close()