import bpy
import datetime
from .funcs import *
from .import_srt import Segment
from bpy_extras.io_utils import ImportHelper

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
    
class ImportLRC(bpy.types.Operator, ImportHelper):
    bl_label = 'Import LRC'
    bl_idname = 'sequencerextra.import_lrc'
    bl_description = ''.join(['Import .lrc as text strips.'])
    
    filter_glob = bpy.props.StringProperty(
            default="*.lrc",
            options={'HIDDEN'},
            maxlen=255,
            )
    
    def execute(self, context):
        scene = context.scene
        
        path = self.filepath.replace('\\','/')
        segments = parse_lrc(path)
        add_segments(scene, segments)
        return {'FINISHED'}
