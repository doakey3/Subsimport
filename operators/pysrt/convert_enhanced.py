from .srtfile import SubRipFile
from .srtitem import SubRipItem

def get_all_bases(temp_subs):
    """Get the bases (whole sentences) from the enhanced subs"""

    subs = []
    for temp in temp_subs:
        sub = SubRipItem(
                index = temp.index, start=temp.start, end=temp.end, 
                text=temp.text)
        subs.append(sub)

    subs[0].text = subs[0].text_without_tags
    sub_items = [subs[0]]
    subs.pop(0)

    i = 0
    while i < len(subs):
        subs[i].text = subs[i].text.split('</font>')[0]
        subs[i].text = subs[i].text_without_tags

        base_text = str()
        strip_text = str(subs[i].text)
        if sub_items[-1].text.startswith(subs[i].text): 
            sub_items[-1].end = subs[i].end
            i += 1
            
        else:
            sub_items.append(subs[0])
            subs.pop(0)

    bases = SubRipFile(sub_items)
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
            
    print(start, end, b_start, b_end)

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
    
    return bases, tops, color

