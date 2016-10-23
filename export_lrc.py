import datetime
import bpy
from bpy_extras.io_utils import ExportHelper
from .import_srt import Segment

class ExportLRC(bpy.types.Operator, ExportHelper):
    bl_idname = "sequencerextra.export_lrc"
    bl_label = "Export LRC"
    bl_description = "Export text strips from VSE to LRC text file."
    filename_ext = ".lrc"
    filter_glob = bpy.props.StringProperty(
            default="*.lrc",
            options={'HIDDEN'},
            maxlen=255,
            )
    def execute(self, context):
        scene = context.scene
        fps = scene.render.fps/scene.render.fps_base
        path = self.filepath
        seq = bpy.context.scene.sequence_editor
        if not seq == None:
            all_strips = list(sorted(seq.sequences_all,
                key=lambda x: x.frame_start))
            segments = []
            for strip in all_strips:
                if strip.type == 'TEXT':
                    segments.append(Segment())
                    segments[-1].segment_number = 0
                    segments[-1].start_time = strip.frame_final_start/fps
                    segments[-1].end_time = strip.frame_final_end/fps
                    segments[-1].topline = strip.text.replace('\n',' ')
        else:
            segments = []
        write_lrc(segments,path)
        return {'FINISHED'}

def sec_to_msf(seconds):
    """Convert seconds to '[00:00.00] format"""
    if seconds > 3600:
        return '[59:59.99]'
    m = str(int(seconds / 60)).zfill(2)
    s = str(int(seconds % 60)).zfill(2)
    ms = str(int(round(seconds - int(seconds), 2) * 100)).zfill(2)
    output = ''.join(['[',m,':', s,'.',ms,']'])
    return output
    
def write_lrc(segments, path):
    """Write segments into an lrc file"""
    output_string = ''
    count = 0
    while count < len(segments):
        if count < len(segments) - 1:
            if segments[count].end_time != segments[count + 1].start_time:
                segments.insert(count + 1, Segment())
                segments[count + 1].start_time = segments[count].end_time
                segments[count + 1].end_time = segments[count + 2].start_time
                segments[count + 1].topline = ''
                segments[count + 1].bottomline = ''
        count += 1
    lines = []
    for seg in segments:
        lines.append((seg.topline + ' ' + seg.bottomline).rstrip())
    
    count = 0
    while count < len(segments):
        start = ""
        line = (segments[count].topline + ' ' + segments[count].bottomline).rstrip()
        while line in lines:
            index = lines.index(line)
            start += sec_to_msf(segments[index].start_time) 
            lines.pop(index)
            segments.pop(index)
        output_string += ''.join([start,line,'\n'])
        count += 1
    f = open(path, 'w', encoding='utf-8')
    f.write(output_string)
    f.close()
