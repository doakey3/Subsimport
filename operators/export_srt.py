import bpy
import codecs
from bpy_extras.io_utils import ExportHelper

from .pysrt.srtitem import SubRipItem
from .pysrt.srtfile import SubRipFile

from .tools.get_text_strips import get_text_strips

class SEQUENCER_OT_export_srt(bpy.types.Operator, ExportHelper):
    bl_label = 'Export SRT'
    bl_idname = 'sequencerextra.export_srt'
    bl_description = 'Export subtitles as SRT\n\nThis format is usually used for movies.'

    filename_ext = ".srt"

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

        sub_lines = []
        for i in range(len(text_strips)):
            strip = text_strips[i]

            start = (strip.frame_start / fps) * 1000
            end = (strip.frame_final_end / fps) * 1000
            text = strip.text

            item = SubRipItem()
            item.text = text
            item.start.from_millis(start)
            item.end.from_millis(end)
            item.index = i + 1
            sub_lines.append(item)

        output = SubRipFile(sub_lines).to_string()

        outfile = codecs.open(self.filepath, 'w', 'utf-8')
        outfile.write(output)
        outfile.close()

        return {"FINISHED"}
