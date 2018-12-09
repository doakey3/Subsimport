import bpy
import codecs
from bpy_extras.io_utils import ExportHelper

from .pylrc.lyrics import Lyrics
from .pylrc.lyricline import LyricLine
from .pylrc.tools.timecode import seconds_to_timecode

from .tools.get_text_strips import get_text_strips

class SEQUENCER_OT_export_lrc(bpy.types.Operator, ExportHelper):
    bl_label = 'Export LRC'
    bl_idname = 'sequencerextra.export_lrc'
    bl_description = 'Export subtitles as LRC\n\nThis format is usually used for music.'

    filename_ext = ".lrc"

    @classmethod
    def poll(self, context):
        scene = context.scene
        try:
            text_strips = get_text_strips(scene)

            if len(text_strips) > 0:
                return True
            else:
                return False
        except AttributeError:
            return False

    def execute(self, context):
        scene = context.scene
        fps = scene.render.fps/scene.render.fps_base
        text_strips = get_text_strips(scene)

        lyric_list = []
        for i in range(len(text_strips)):
            strip = text_strips[i]
            if (strip.frame_final_start / fps)  >= 3600:
                message = ".lrc files cannot store subtitles longer than 59:59.99"
                self.report(set({'ERROR'}), message)
                return {"FINISHED"}

            start = seconds_to_timecode(strip.frame_final_start / fps)

            text_lines = strip.text.split('\n')
            text = ''
            for line in text_lines:
                text += line.strip() + ' '
            text = text.rstrip()

            lyric_list.append(LyricLine(start, text))

            if i < len(text_strips) - 1:
                if text_strips[i + 1].frame_start > strip.frame_final_end:
                    start = seconds_to_timecode(strip.frame_final_end / fps)
                    lyric_list.append(LyricLine(start, ""))

            elif i == len(text_strips) - 1:
                start = seconds_to_timecode(strip.frame_final_end / fps)
                lyric_list.append(LyricLine(start, ""))

        output = Lyrics(lyric_list).to_LRC()
        outfile = codecs.open(self.filepath, 'w', 'utf-8')
        outfile.write(output)
        outfile.close()

        return {"FINISHED"}
