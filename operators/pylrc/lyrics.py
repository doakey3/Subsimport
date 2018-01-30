from .tools.timecode import is_timecode, timecode_to_srt
from .tools.find_even_split import find_even_split

class Lyrics(list):
    """A list that holds the contents of the lrc file"""
    def __init__(self, items=[]):

        self.artist = ""
        self.album = ""
        self.title = ""
        self.author = ""
        self.length = ""
        self.offset = ""

        self.extend(items)

    def is_enhanced_lrc(self):
        """
        Checks if the subs is an enhanced lrc
        """
        for sub in self:
            word = '<' + sub.text.split('<')[-1]
            if is_timecode(word[0:10]):
                return True
        return False

    def to_SRT(self):
        """Returns an SRT string of the LRC data"""

        if not self[-1].text.rstrip() == "":
            timecode = self[-1].lrc_timecode
            end_line = LyricLine(timecode, "")
            end_line.shift(seconds=5)
            self.append(end_line)

        if self.is_enhanced_lrc():
            return self.to_ESRT()

        output = []
        srt = ""
        for i in range(len(self) - 1):
            if not self[i].text == '':
                srt = str(i + 1) + '\n'
                start_timecode = self[i].srt_time
                end_timecode = self[i + 1].srt_time

                srt = srt + start_timecode + ' --> ' + end_timecode + '\n'
                if len(self[i].text) > 31:
                    srt = srt + find_even_split(self[i].text) + '\n'
                else:
                    srt = srt + self[i].text + '\n'
                output.append(srt)

        return '\n'.join(output).rstrip()

    def to_ESRT(self):
        """Convert ELRC to ESRT"""
        output = []
        for i in range(len(self) - 1):
            sub_list = []
            if not self[i].text == '':
                text = self[i].text
                base_text = self[i].text_without_tags

                if len(base_text) > 31:
                    base_text = find_even_split(base_text)

                if not is_timecode(text[0:10]):
                    time = self[i].lrc_time
                    time = time.replace('[', '<').replace(']', '>')
                    text = time + text

                if not is_timecode(text[-10::]):
                    time = self[i + 1].lrc_time
                    time = time.replace('[', '<').replace(']', '>')
                    text = text + time

                if not text[0:10].replace('<', '[').replace('>', ']') == self[i].lrc_time:
                    start = self[i].srt_time
                    end = timecode_to_srt(text[0:10])
                    body = base_text

                    segment = ''.join(
                        ['0\n', start, ' --> ', end, '\n', body, '\n'])
                    sub_list.append(segment)

                growing = ""
                while len(text) > 10:
                    start = timecode_to_srt(text[0:10])
                    for c in range(1, len(text)):
                        if text[c] == '<' and is_timecode(text[c:c + 10]):
                            end = timecode_to_srt(text[c: c + 10])
                            body = text[10:c]
                            text = text[c::]
                            break

                    if growing.endswith('\n'):
                        growing += body.lstrip()

                    else:
                        growing += body

                    try:
                        if base_text[len(growing)] == '\n':
                            growing = growing + '\n'
                    except IndexError:
                        pass

                    body = ''.join(
                        ['<font color="#ff8800">', growing, '</font>',
                         base_text[len(growing)::]])

                    segment = ''.join(
                        ['0\n', start, ' --> ', end, '\n', body, '\n'])
                    sub_list.append(segment)

                if not text[0:10].replace('<', '[').replace('>', ']') == self[i + 1].lrc_time:
                    start = timecode_to_srt(text[0:10])
                    end = self[i + 1].srt_time
                    body = '<font color="#ff8800">' + base_text + '</font>'

                    segment = ''.join(
                        ['0\n', start, ' --> ', end, '\n', body, '\n'])
                    sub_list.append(segment)

                output.extend(sub_list)

        for i in range(len(output)):
            output[i] = str(i + 1) + output[i][1::]

        return '\n'.join(output).rstrip()


    def to_LRC(self):
        output = []
        if not self.artist == "":
            output.append('[ar:' + self.artist + ']')
        if not self.album == "":
            output.append('[al:' + self.album + ']')
        if not self.title == "":
            output.append('[ti:' + self.title + ']')
        if not self.author == "":
            output.append('[au:' + self.author + ']')
        if not self.length == "":
            output.append('[length:' + self.length + ']')
        if not self.offset == "":
            output.append('[offset:' + self.offset + ']')

        if len(output) > 0:
            output.append('')

        lrc = ""
        for i in range(len(self)):
            lrc = self[i].lrc_time + self[i].text
            output.append(lrc)
        return '\n'.join(output).rstrip()