import bpy
from .funcs import *
from bpy_extras.io_utils import ImportHelper

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

class ImportSRT(bpy.types.Operator, ImportHelper):
    bl_label = 'Import SRT'
    bl_idname = 'sequencerextra.import_srt'
    bl_description = ''.join(['Import .srt as text strips.'])
    
    filter_glob = bpy.props.StringProperty(
            default="*.srt",
            options={'HIDDEN'},
            maxlen=255,
            )
    
    def execute(self, context):
        scene = context.scene
        path = self.filepath.replace('\\','/')
        segments = parse_srt(path)
        add_segments(scene,segments)
        return {'FINISHED'}
