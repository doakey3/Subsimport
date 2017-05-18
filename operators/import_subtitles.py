import bpy
from bpy_extras.io_utils import ImportHelper

from .pylrc.parser import parse as lrc_parse

from .pysrt.srtfile import SubRipFile
from .pysrt.convert_enhanced import convert_enhanced

from .textparser.parser import text_to_srt

from .tools.subtitles_to_sequencer import subtitles_to_sequencer
from .tools.hexcode_to_color import hexcode_to_color

class ImportSubtitles(bpy.types.Operator, ImportHelper):
    bl_label = 'Import'
    bl_idname = 'sequencerextra.import_subtitles'
    bl_description = 'Import subtitles (.txt, .lrc, or .srt) as text strips.'

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
            text = lrc.to_SRT()

        subs = SubRipFile().from_string(text)
        subs.remove_overlaps()
        
        scene.use_audio_scrub = True
        scene.use_audio_sync = True
        scene.use_frame_drop = True

        if scene.subs_adjust_fps:
            scene.render.fps = 100
            scene.render.fps_base = 0.1
        
        try:
            all_strips = list(sorted(scene.sequence_editor.sequences,
                key=lambda x: x.frame_start))
            
            for strip in all_strips:
                strip.select = False
        
        except AttributeError:
            pass

        if subs.is_enhanced:
            
            bases, tops, color = convert_enhanced(subs)
            color = hexcode_to_color(color)
            
            scene.enhanced_subs_color[0] = color[0]
            scene.enhanced_subs_color[1] = color[1]
            scene.enhanced_subs_color[2] = color[2]
            
            subtitles_to_sequencer(context, bases)
            
            strips = subtitles_to_sequencer(context, tops)
            
            for strip in strips:
                strip.color[0] = scene.enhanced_subs_color[0]
                strip.color[1] = scene.enhanced_subs_color[1]
                strip.color[2] = scene.enhanced_subs_color[2]
            
        else:
            strips = subtitles_to_sequencer(context, subs)

        scene.subtitle_edit_channel = strips[0].channel
        
        bpy.ops.sequencer.view_selected()
        
        return {"FINISHED"}
