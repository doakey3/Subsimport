from .srtfile import SubRipFile
from .srtitem import SubRipItem
import re

def get_all_bases(temp_subs):
    """Get the bases (whole sentences) from the enhanced subs"""

    subs = []
    for temp in temp_subs:
        sub = SubRipItem(
                index = temp.index, start=temp.start, end=temp.end,
                text=temp.text)
        subs.append(sub)

    sub_items = []

    while len(subs) > 0:

        if subs[0].text == subs[0].text_without_tags:

            sub_items.append(subs[0])
            subs.pop(0)
            if len(subs) > 0:
                go = True
                while go:
                    lesser = subs[0].text.split('</font>')[0]
                    lesser = re.compile(r'<[^>]*?>').sub('', lesser)
                    if (len(lesser.rstrip()) <= len(sub_items[-1].text) and
                            lesser in sub_items[-1].text):
                        sub_items[-1].end = subs[0].end
                        subs.pop(0)
                    else:
                        go = False

        if len(sub_items) == 0:
            sub_items.append(subs[0])
            sub_items[-1].text = sub_items[-1].text.split('</font>')[0]
            sub_items[-1].text = sub_items[-1].text_without_tags
            subs.pop(0)

        if len(subs) > 0:

            subs[0].text = subs[0].text.split('</font>')[0]
            subs[0].text = subs[0].text_without_tags

            if subs[0].text.startswith(sub_items[-1].text):
                sub_items[-1].end = subs[0].end
                sub_items[-1].text = subs[0].text
                subs.pop(0)

            else:
                sub_items.append(subs[0])
                subs.pop(0)

    bases = SubRipFile(sub_items)
    bases.clean_indexes()
    return bases

def get_base(sub, bases):
    """Get the base that corresponds with a sub"""

    start = sub.start.to_millis()
    end = sub.end.to_millis()

    for base in bases:
        b_start = base.start.to_millis()
        b_end = base.end.to_millis()

        if b_start <= start and b_end >= end:
            return base

def get_children(base, tops):
    """Get all of the children of a base"""

    children = []

    start = base.start.to_millis()
    end = base.end.to_millis()

    for i in range(len(tops)):
        t_start = tops[i].start.to_millis()
        t_end = tops[i].end.to_millis()

        if start <= t_start and end >= t_end:
            children.append(i)

        elif start < t_end:
            return children

    return children

def make_locks(tops, bases):
    """Add [locked start] and [locked end] to appropriate tops"""

    for base in bases:
        children = get_children(base, tops)
        tops[children[0]].name = '[locked start]'
        tops[children[-1]].name = '[locked end]'

    return tops


def get_all_tops(subs, bases):
    """Get the top subs (syllable/word splits)"""

    sub_items = []

    i = 0
    while i < len(subs):
        if subs[i].text == subs[i].text_without_tags:
            subs.pop(i)

        elif i > 0:
            base = get_base(subs[i], bases)
            old_base = get_base(subs[i - 1], bases)

            if subs[i].text == subs[i - 1].text and base == old_base:
                subs.pop(i)

            else:
                i += 1
        else:
            i += 1

    for i in range(len(subs)):
        subs[i].text = subs[i].text.split('</font>')[0]
        subs[i].text = subs[i].text_without_tags

        base = get_base(subs[i], bases)
        empty = empty_text(base.text)
        subs[i].text = subs[i].text + empty[len(subs[i].text)::]

        sub_items.append(subs[i])

    tops = SubRipFile(sub_items)
    tops.clean_indexes()
    return tops

def empty_text(text):
    """
    Creates a string from text where each character (except newline)
    is a space
    """
    lines = text.split('\n')
    empty_text = ''
    for x in range(len(lines)):
        for char in range(len(lines[x])):
            empty_text += ' '
        empty_text += '\n'

    return empty_text[0:-1]

def retrieve_color(subs):
    for sub in subs:
        if sub.text.startswith('<font color='):
            hexcode = sub.text[len('<font color="')::]
            hexcode = hexcode.split('>')[0][0:-1]
            return hexcode

def convert_enhanced(subs):
    """
    Convert an enhanced SRT to 2 standard SRT files
    One on top and the other on bottom
    also retrieves the color of the enhancement

    """

    color = retrieve_color(subs)
    bases = get_all_bases(subs)
    tops = get_all_tops(subs, bases)
    tops = make_locks(tops, bases)

    return bases, tops, color