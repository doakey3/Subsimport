import bpy
from bpy_extras.io_utils import ImportHelper

from .pylrc.parser import parse as lrc_parse
from .pysrt.srtfile import SubRipFile
from .pysrt.srtfile import SubRipItem
from .textparser.parser import text_to_srt

from .common.subtitles_to_sequencer import subtitles_to_sequencer

def is_enhanced_srt(subs):
    """Checks if the subs is an enhanced srt"""
    for sub in subs:
        if not sub.text.startswith('<font color="'):
            return False
    return True

def parse_enhanced_srt(subs):
    """
    Parses an enhanced srt as 2 groups, 1 for the highlighted subs and
    1 for the base subs
    """

    base_subs = [SubRipItem()]
    base_subs[-1].text = subs[0].text
    base_subs[-1].start = subs[0].start
    base_subs[-1].end = subs[0].end
    
    starts = [0]
    ends = []
    
    for i in range(1, len(subs)):
        if base_subs[-1].text.split('</font>')[0] in subs[i].text:
            base_subs[-1].text = subs[i].text
            base_subs[-1].end = subs[i].end
        else:
            ends.append(i - 1)
            starts.append(i)
            base_subs[-1].text = base_subs[-1].text[len('<font color="#000000">')::]
            base_subs[-1].text = base_subs[-1].text.replace('</font>', '')
            
            base_subs.append(SubRipItem())
            base_subs[-1].text = subs[i].text
            base_subs[-1].start = subs[i].start
            base_subs[-1].end = subs[i].end
    
    base_subs[-1].text = base_subs[-1].text[len('<font color="#000000">')::]
    base_subs[-1].text = base_subs[-1].text.replace('</font>', '')
    ends.append(len(subs) - 1)
    base_subs = SubRipFile(base_subs)
    
    top_subs = []
    for i in range(len(subs)):
        text = str(subs[i].text)
        text = text[len('<font color="#000000">')::].replace('</font>', '')
        lines = text.split('\n')
        empty_text = ''
        for x in range(len(lines)):
            for char in range(len(lines[x])):
                empty_text += ' '
            empty_text += '\n'
        
        text = str(subs[i].text)
        text = text[len('<font color="#000000">')::].split('</font>')[0]
        text = text + empty_text[len(text)::]
        
        top_subs.append(SubRipItem())
        top_subs[-1].text = text
        top_subs[-1].start = subs[i].start
        top_subs[-1].end = subs[i].end
        
        top_subs[-1].name = ''
        if i in starts:
            top_subs[-1].name = '[locked start]'
        if i in ends:
            top_subs[-1].name += '[locked end]'
                
    top_subs = SubRipFile(top_subs)
    
    return base_subs, top_subs

class ImportSubtitles(bpy.types.Operator, ImportHelper):
    bl_label = 'Import Subtitles'
    bl_idname = 'sequencerextra.import_subtitles'
    bl_description = 'Import subtitles as text strips. (.txt, .lrc, or .srt)'

    filter_glob = bpy.props.StringProperty(
            default="*.srt;*.lrc;*.txt",
            options={'HIDDEN'},
            maxlen=255,
            )
    
    def execute(self, context):
        scene = context.scene
        
        file = open(self.filepath, encoding='utf-8', errors='ignore')
        text = file.read()
        file.close()
        
        if self.filepath.endswith('.txt'):
            text = text_to_srt(text)
        
        elif self.filepath.endswith('.lrc'):
            lrc = lrc_parse(text)
            text = lrc.toSRT()
            
        subs = SubRipFile().from_string(text)
        subs.remove_overlaps()
        
        if is_enhanced_srt(subs):
            base_subs, top_subs = parse_enhanced_srt(subs)
            subtitles_to_sequencer(context, base_subs)
            top_strips = subtitles_to_sequencer(context, top_subs)
            
            for strip in top_strips:
                strip.color[0] = scene.enhanced_subs_color[0]
                strip.color[1] = scene.enhanced_subs_color[1]
                strip.color[2] = scene.enhanced_subs_color[2]
            
            scene.subtitle_edit_channel = top_strips[0].channel
        
        else:
            subtitles_to_sequencer(context, subs)
        
        return {"FINISHED"}
