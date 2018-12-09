class Syllabator():
    def __init__(self):
        self.consonants = 'bcdfghjklmnpqrstvwxz'

        self.consonant_pairs = [
            'bl', 'br', 'ch', 'ck', 'cl', 'cr', 'ct', 'dg', 'dr', 'fl',
            'fr', 'ft', 'gh', 'gl', 'gr', 'hr', 'ht', 'kh', 'ld', 'lf',
            'lv', 'nc', 'nd', 'ng', 'nk', 'ns', 'nt', 'ph', 'pl', 'pr',
            'rd', 'rd', 'rg', 'rh', 'sc', 'sh', 'sk', 'sl', 'sm', 'sn',
            'sp', 'st', 'sw', 'th', 'tr', 'ts', 'tw', 'tz', 'wh', 'wr',
            'hr', 'tc']

        self.vowels = 'aeiouy'

        self.word_parts = [""]

    def split_consonants(self):
        """
        make a split where there are 2 consonants next to
        eachother if the 2 consonants are not at the end of the word
        and they aren't in the consonant pairs
        example:
        pizzazz --> piz, zazz
        """

        i = 0
        while i < len(self.word_parts):
            for x in range(1, len(self.word_parts[i])):
                a = self.word_parts[i][x - 1]
                b = self.word_parts[i][x]
                if (a in self.consonants and
                        b in self.consonants and not
                        a + b in self.consonant_pairs and not
                        x == len(self.word_parts[i]) - 1):
                    part1 = self.word_parts[i][0:x]
                    part2 = self.word_parts[i][x::]
                    self.word_parts.pop(i)
                    self.word_parts.insert(i, part2)
                    self.word_parts.insert(i, part1)
                    break
            i += 1

    def handle_ckle(self):
        """
        make a split between ck and le
        """

        i = 0
        while i < len(self.word_parts):
            if self.word_parts[i].endswith('ckle'):
                part1 = self.word_parts[i][0:-2]
                part2 = 'le'
                self.word_parts.pop(i)
                self.word_parts.insert(i, part2)
                self.word_parts.insert(i, part1)
            i += 1

    def handle_le(self):
        """
        make a split between word part and 'le' if it ends with le and the
        3rd to last character is not a vowel.
        """
        i = 0
        while i < len(self.word_parts):
            if self.word_parts[i].endswith('le') and len(self.word_parts[i]) > 3:
                if len(self.word_parts[i]) > 3 and not self.word_parts[i][-3] in self.vowels:
                    part1 = self.word_parts[i][0:-3]
                    part2 = self.word_parts[i][-3::]
                    self.word_parts.pop(i)
                    self.word_parts.insert(i, part2)
                    self.word_parts.insert(i, part1)
            i += 1


    def split_surrounded_consonant(self, position='BEFORE'):
        """
        make a split when there is a consonant that is surrounded by vowels
        """

        i = 0
        while i < len(self.word_parts):
            for x in range(1, len(self.word_parts[i]) - 1):
                a = self.word_parts[i][x - 1]
                b = self.word_parts[i][x]
                c = self.word_parts[i][x + 1]
                if a in self.vowels and c in self.vowels and b in self.consonants:

                    # mATE
                    if x == len(self.word_parts[i]) - 2 and self.word_parts[i].endswith('e'):
                        pass

                    # cURE, cURED
                    elif a == 'u' and b == 'r' and c == 'e' and self.word_parts[i].endswith('e') or self.word_parts[i].endswith('ed'):
                        pass

                    # brACElet
                    elif a == 'a' and b == 'c' and c == 'e':
                        pass

                    else:
                        if position == 'BEFORE':
                            part1 = self.word_parts[i][0:x+1]
                            part2 = self.word_parts[i][x+1::]

                        else:
                            part1 = self.word_parts[i][0:x+1]
                            part2 = self.word_parts[i][x+1::]

                        self.word_parts.pop(i)
                        self.word_parts.insert(i, part2)
                        self.word_parts.insert(i, part1)
                        break

            i += 1

    def split_surrounded_consonant_triples(self):
        """
        make a split where there are 2 consonant pairs back to back
        as in amaziNGLy
        """

        i = 0
        while i < len(self.word_parts):
            for x in range(1, len(self.word_parts[i]) - 3):
                a = self.word_parts[i][x - 1]
                b = self.word_parts[i][x]
                c = self.word_parts[i][x + 1]
                d = self.word_parts[i][x + 2]
                e = self.word_parts[i][x + 3]
                if a in self.vowels and b + c in self.consonant_pairs and c + d in self.consonant_pairs and e in self.vowels:
                    part1 = self.word_parts[i][0:x]
                    part2 = self.word_parts[i][x::]
                    self.word_parts.pop(i)
                    self.word_parts.insert(i, part2)
                    self.word_parts.insert(i, part1)
                    break
            i += 1

    def split_surrounded_consonant_pairs(self, position='BEFORE'):
        """
        make a split when there is a consonant pair surrounded by vowels
        """

        i = 0
        while i < len(self.word_parts):
            for x in range(1, len(self.word_parts[i]) - 2):
                a = self.word_parts[i][x - 1]
                b = self.word_parts[i][x]
                c = self.word_parts[i][x + 1]
                d = self.word_parts[i][x + 2]
                if a in self.vowels and b + c in self.consonant_pairs and d in self.vowels:
                    if x == len(self.word_parts[i]) - 3 and self.word_parts[i].endswith('e'):
                        pass

                    else:
                        if position == 'BEFORE':
                            part1 = self.word_parts[i][0:x+2]
                            part2 = self.word_parts[i][x+2::]
                        elif position == 'AFTER':
                            part1 = self.word_parts[i][0:x+2]
                            part2 = self.word_parts[i][x+2::]
                        elif position == 'MIDDLE':
                            part1 = self.word_parts[i][0:x+1]
                            part2 = self.word_parts[i][x+1::]

                        self.word_parts.pop(i)
                        self.word_parts.insert(i, part2)
                        self.word_parts.insert(i, part1)
                        break
            i += 1


    def syllabify(self, word, pos1="BEFORE", pos2="BEFORE"):
        """Splits a word up into syllables"""
        self.word_parts = [word]
        self.split_consonants()
        self.handle_ckle()
        self.handle_le()

        self.split_surrounded_consonant_pairs(position=pos1)
        self.split_surrounded_consonant(position=pos2)
        self.split_surrounded_consonant_triples()
        return self.word_parts

if __name__ == '__main__':

    count_dictionary = {}
    f = open('syllable_counts.txt', 'r')
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        if not lines[i].rstrip() == '':
            word = lines[i].split(' ')[0]
            count = int(lines[i].split(' ')[1].rstrip())
            count_dictionary[word] = count

    syllable_dictionary = {}
    f = open('syllable_splits.txt', 'r')
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        word = lines[i].rstrip()
        syllable_dictionary[word] = lines[i].rstrip()

    old_words = list(syllable_dictionary.keys())
    words = list(count_dictionary.keys())

    syllabator = Syllabator()
    hyphenator = Hyphenator()

    confirmed_words = []
    syl_splits = []
    for i in range(len(words)):
        syl_splits.append(syllabator.syllabify(words[i]))
        syl_splits.append(syllabator.syllabify(words[i], pos1='AFTER', pos2='BEFORE'))
        syl_splits.append(syllabator.syllabify(words[i], pos1='MIDDLE', pos2='BEFORE'))
        syl_splits.append(syllabator.syllabify(words[i], pos1='BEFORE', pos2='AFTER'))
        syl_splits.append(syllabator.syllabify(words[i], pos1='AFTER', pos2='AFTER'))
        syl_splits.append(syllabator.syllabify(words[i], pos1='MIDDLE', pos2='AFTER'))

        hyp_split = hyphenator.hyphenate_word(words[i])

        for x in range(len(syl_splits)):
            if len(syl_splits[x]) == count_dictionary[words[i]] and syl_splits[x] == hyp_split:
                w = ' '.join(syl_splits[x])
                if not w in old_words:
                    confirmed_words.append(w)
                    break

    lines = []
    for i in range(len(confirmed_words)):
        lines.append(confirmed_words[i] + '\n')
    f = open('new_splits.txt', 'w')
    f.write(''.join(lines))
    f.close()