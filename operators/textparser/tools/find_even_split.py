def make_lines(line, space):
    """
    Make a list of lines that are less than or equal to space long
    """
    word_list = line.split(' ')
    lines = []
    growing_string = ''
    while len(word_list) > 0:
        if len((growing_string + ' ' + word_list[0]).strip()) <= space:
            growing_string += ' ' + word_list[0]
            growing_string = growing_string.strip()
        else:
            lines.append(growing_string.strip())
            growing_string = word_list[0]
        word_list.pop(0)
    lines.append(growing_string)
    return lines

def find_even_split(line):
    max_line_length = 31
    output = make_lines(line, max_line_length)
    max_lines = len(output)
    space = max_line_length - 1
    while len(make_lines(line, space)) == max_lines:
        space -= 1
    lines = make_lines(line, space + 1)
    return '\n'.join(make_lines(line, space + 1))