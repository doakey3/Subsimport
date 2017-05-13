from .classes import Lyrics, LyricLine
from .utilities import validateTimecode, unpackTimecode

def parse(lrc):
    
    lines = lrc.split('\n')
    lyrics = Lyrics()
    items = []
    
    for i in range(len(lines)):
        if lines[i].startswith('[ar:'):
            lyrics.artist = lines[i].rstrip()[4:-1].lstrip()
            
        elif lines[i].startswith('[ti:'):
            lyrics.title = lines[i].rstrip()[4:-1].lstrip()
        
        elif lines[i].startswith('[al:'):
            lyrics.album = lines[i].rstrip()[4:-1].lstrip()
        
        elif lines[i].startswith('[by:'):
            lyrics.author = lines[i].rstrip()[4:-1].lstrip()
        
        elif lines[i].startswith('[length:'):
            lyrics.length = lines[i].rstrip()[8:-1].lstrip()
        
        elif lines[i].startswith('[offset:'):
            lyrics.offset = lines[i].rstrip()[8:-1].lstrip()
        
        elif lines[i].startswith('[re:'):
            lyrics.editor = lines[i].rstrip()[4:-1].lstrip()
        
        elif lines[i].startswith('[ve:'):
            lyrics.version = lines[i].rstrip()[4:-1].lstrip()
        
        elif len(lines[i].split(']')[0]) >= len('[0:0:0]'):
            if validateTimecode(lines[i].split(']')[0] + ']'):
                while validateTimecode(lines[i].split(']')[0] + ']'):
                    timecode = lines[i].split(']')[0] + ']'
                    text = ''.join(lines[i].split(']')[-1]).rstrip()
                    lyric_line = LyricLine(timecode, text=text)
                    items.append(lyric_line)
                    
                    lines[i] = lines[i][len(timecode)::]
    
    lyrics.extend(sorted(items))
    
    if not lyrics.offset == "":
        offset_mins, offset_secs, offset_millis = unpackTimecode(lyrics.offset)
        for i in range(len(lyrics)):
            lyrics[i].shift(minutes=offset_mins, seconds=offset_secs, 
                milliseconds=offset_millis)
    
    return lyrics
