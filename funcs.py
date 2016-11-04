import bpy
import datetime

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

def add_segments(scene, segments):
    """Given a list of segments, adds them to the sequencer"""
    fps = scene.render.fps/scene.render.fps_base
    
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
            channel=scene.subtitle_channel,
            type="TEXT",)
        all_strips = list(sorted(
            scene.sequence_editor.sequences_all,
            key=lambda x: x.frame_start))
        text_strips = []
        for x in range(len(all_strips)):
            if (all_strips[x].type == "TEXT" and 
            all_strips[x].channel == scene.subtitle_channel):
                text_strips.append(all_strips[x])
        strip = text_strips[-1]
        strip.name = line
        strip.text = line
        strip.font_size = scene.subtitle_font_size
        strip.use_shadow = True
        
    for strip in text_strips:
        strip.select = True
