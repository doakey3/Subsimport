import bpy
from bpy_extras.io_utils import ExportHelper
from .pylrc.classes import Lyrics, LyricLine

def toTimecode(sec):
    """Makes a timecode of the format [MM:SS.ff]"""
    minutes = "%02d" % int(sec / 60)
    seconds = "%02d" % int(sec % 60)
    millis = ("%03d" % ((sec % 1) * 1000))[0:2]
    
    return ''.join(['[', minutes, ':', seconds, '.', millis, ']'])

class ExportLRC(bpy.types.Operator, ExportHelper):
    bl_label = 'Export LRC'
    bl_idname = 'sequencerextra.export_lrc'
    bl_description = 'Export Subtitles'
    
    filename_ext = ".lrc"
    
    def execute(self, context):
        scene = context.scene
        edit_channel = scene.subtitle_edit_channel
        fps = scene.render.fps/scene.render.fps_base
        
        all_strips = list(sorted(
            scene.sequence_editor.sequences_all,
            key=lambda x: x.frame_start))
        
        text_strips = []
        for x in range(len(all_strips)):
            if (all_strips[x].type == "TEXT" and
                    all_strips[x].channel == edit_channel):
                text_strips.append(all_strips[x])
                
        lyrics_list = []
        for i in range(len(text_strips)):
            strip = text_strips[i]
            if (strip.frame_start / fps) < 3600:
                start = toTimecode(strip.frame_start / fps)
                text = strip.text.replace('\n', ' ')
                lyrics_list.append(LyricLine(start, text))
                if i < len(text_strips) - 1:
                    if text_strips[i + 1].frame_start > strip.frame_final_end:
                        start = toTimecode(strip.frame_final_end / fps)
                        lyrics_list.append(LyricLine(start, ""))
                
                elif i == len(text_strips):
                    start = toTimecode(strip.frame_final_end / fps)
                    lyrics_list.append(LyricLine(start, ""))
        
        lyrics = Lyrics(lyrics_list)
            
        
        output = lyrics.toLRC()
        
        outfile = open(self.filepath, 'w')
        outfile.write(output)
        outfile.close()
        
        return {"FINISHED"}

