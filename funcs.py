import bpy
import datetime

class Segment():
    """Holds the information in an SRT segment"""
    def __init__(self):
        self.segment_number = 0
        self.start_time = 0.0
        self.end_time = 0.0
        self.topline = ''
        self.bottomline = ''

def parse_srt(file):
    """
    Open an srt file and convert its sections into a list of segments
    """
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    separated = []
    temp = []
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()
        if not lines[i] == '':
            temp.append(lines[i])
        else:
            separated.append(temp)
            temp = []
    separated.append(temp)

    for s in separated:
        if s == []:
            separated.pop(separated.index([]))
            
    segments = []
    for i in range(len(separated)):
        seg = i + 1
        try:
            try:
                start = convert_to_seconds(
                    separated[i][1].split(' --> ')[0])
            except ValueError:
                start = convert_to_seconds('23:59:59,999')
            try:
                end = convert_to_seconds(
                    separated[i][1].split(' --> ')[1])
            except ValueError:
                end = convert_to_seconds('23:59:59,999')
            try:
                line_1 = separated[i][2]
            except IndexError:
                line_1 = ''
            if len(separated[i]) > 3:
                line_2 = separated[i][3]
            segments.append(Segment())
            segments[i].segment_number = seg
            segments[i].start_time = start
            segments[i].end_time = end
            
            if len(separated[i]) > 3:
                segments[i].topline = line_1
                segments[i].bottomline = line_2
            else:
                segments[i].bottomline = line_1
        except IndexError:
            pass
    return segments

class lrc_segment():
    """
    A class to hold the segments of an lrc file
    """
    def __init__(self):
        self.time = 0.0
        self.line = ''

def parse_lrc(file):
    """
    Open an lrc file and convert it's sections into srt segments
    """
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    lrc_segs = []
    for i in range(len(lines)):
        try:
            t = datetime.datetime.strptime(lines[i].split(']')[0][1::],"%M:%S.%f")
            words = lines[i].rstrip().split(']')
            for x in range(len(words)):
                if words[x].startswith('['):
                    words[x] = convert_to_seconds('00:' + words[x][1::].replace('.', ','))
                    lrc_segs.append(lrc_segment())
                    lrc_segs[-1].time = words[x]
                    lrc_segs[-1].line = words[-1]
        except ValueError:
            #The line doesn't start with [mm:ss.xx] format, skip it
            pass
    lrc_segs.sort(key=lambda x: x.time, reverse=False)

    srt_segments = []
    for i in range(len(lrc_segs)):
        if not lrc_segs[i].line.lstrip() == '':
            srt_segments.append(Segment())
            srt_segments[-1].segment_number = i + 1
            srt_segments[-1].start_time = lrc_segs[i].time
            if i < len(lrc_segs) - 1:
                srt_segments[-1].end_time = lrc_segs[i+1].time
            else:
                srt_segments[-1].end_time = srt_segments[-1].start_time
            if len(lrc_segs[i].line) > 37:
                line1, line2 = find_even_split(lrc_segs[i].line.split(' '))
                srt_segments[-1].topline = line1
                srt_segments[-1].bottomline = line2
            else:
                srt_segments[-1].bottomline = lrc_segs[i].line
        
    return srt_segments
    
def parse_txt(path, scene):
    f = open(path,'r')
    lines = f.readlines()
    f.close()
    current_step = scene.frame_start
    segments = []
    fps = scene.render.fps/scene.render.fps_base
    for i in range(len(lines)):
        segments.append(Segment())
        segments[-1].segment_number = i+1
        line = lines[i].rstrip()
        length = len(line)
        if length > 37:
            words = line.split(' ')
            line1, line2 = find_even_split(words)
            segments[-1].topline = line1
            segments[-1].bottomline = line2
        else:
            segments[-1].bottomline = line
        segments[-1].start_time = current_step/fps + (1.000000001/fps)
        current_step += fps
        segments[-1].end_time = current_step/fps
    
    return segments

def convert_to_seconds(timecode):
    """convert a timecode '00:00:00,000' to seconds"""
    t = datetime.datetime.strptime(timecode, "%H:%M:%S,%f")
    seconds = (60 * t.minute) + (3600 * t.hour) + t.second
    fraction = t.microsecond/1000000
    combo = seconds + fraction
    return combo
    
def find_sequencer_area():
    screens = list(bpy.data.screens)
    for screen in screens:
        for area in screen.areas:
            if area.type == 'SEQUENCE_EDITOR':
                return screen, area

def find_even_split(word_list):
    """
    Given a list of words, attempts to split the word list
    into 2 evenly sized strings
    """
    differences = []
    for i in range(len(word_list)):
        group1 = ' '.join(word_list[0:i+1])
        group2 = ' '.join(word_list[i+1::])
        differences.append(abs(len(group1) - len(group2)))
    index = differences.index(min(differences))
    for i in range(len(word_list)):
        if i == index:
            group1 = ' '.join(word_list[0:i+1])
            group2 = ' '.join(word_list[i+1::])
    return group1, group2
    
def get_open_channel(scene):
    channels = []
    try:
        for strip in scene.sequence_editor.sequences_all:
            channels.append(strip.channel)
        if len(channels) > 0:
            return max(channels) + 1
        else:
            return 1
    except AttributeError:
        return 1

def add_segments(scene, segments):
    """Given a list of segments, adds them to the sequencer"""
    fps = scene.render.fps/scene.render.fps_base
    open_channel = get_open_channel(scene)
    try:
        
        for strip in scene.sequence_editor.sequences_all:
            strip.select = False
    except AttributeError:
        pass
    for i in range(len(segments)):
        if not segments[i].topline == '':
            line = segments[i].topline +' \n' + segments[i].bottomline
        else:
            line = segments[i].bottomline
        segment_start = segments[i].start_time * fps
        segment_end = segments[i].end_time * fps 

        screen, area = find_sequencer_area()
        window = bpy.context.window
        bpy.ops.sequencer.effect_strip_add(
            {'window':window,
            'scene':scene,
            'area':area,
            'screen':screen,
            'region':area.regions[0]},
            frame_start=segment_start, 
            frame_end=segment_end,
            channel=open_channel,
            type="TEXT")
            
        all_strips = list(sorted(
            scene.sequence_editor.sequences_all,
            key=lambda x: x.frame_start))
        text_strips = []
        for x in range(len(all_strips)):
            if (all_strips[x].type == "TEXT" and 
            all_strips[x].channel == open_channel):
                text_strips.append(all_strips[x])
        strip = text_strips[-1]
        strip.name = line
        strip.text = line
        strip.font_size = scene.subtitle_font_size
        strip.use_shadow = True
        
    for strip in text_strips:
        strip.select = True
