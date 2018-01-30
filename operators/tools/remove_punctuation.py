def remove_punctuation(word):
    """Remove punctuation from the beginning and end of a word"""

    puncs = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '\n', '(',
             ')', '!', '@', '#', '$', '%', '^', '-', '+', '=', "'",
             ';', ',', '.', '{', '}','[', ']']

    while len(word) > 0 and word[0] in puncs:
        word = word[1::]

    while len(word) > 0 and word[-1] in puncs:
        word = word[0:-1]

    return word

if __name__ == '__main__':
    print(remove_punctuation('...'))