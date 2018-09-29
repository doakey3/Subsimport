from .tools.find_even_split import find_even_split
from .tools.seconds_to_srt_timecode import seconds_to_srt_timecode

def text_to_srt(text, fps, reflow_long_lines=False):
    """
    Creates an SRT string out of plain text, with 1 second for each
    segment
    """
    text = text.strip()
    lines = text.split('\n')

    output = []
    sec_time = 0
    for i in range(len(lines)):
        seg = str(i + 1) + '\n'

        start = seconds_to_srt_timecode(i + 0.00000001)
        sec_time = i + 1.00000001
        end = seconds_to_srt_timecode(sec_time)
        seg += start + ' --> ' + end + '\n'

        if len(lines[i].rstrip()) > 31 and reflow_long_lines:
            lines[i] = find_even_split(lines[i].rstrip())

        seg += lines[i] + '\n'
        output.append(seg)

    return '\n'.join(output).rstrip()
