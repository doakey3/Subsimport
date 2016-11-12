import bpy
from .funcs import parse_txt, parse_srt, parse_lrc, add_segments
from bpy_extras.io_utils import ImportHelper

class ImportSubtitle(bpy.types.Operator, ImportHelper):
    bl_label = 'Import Subtitle'
    bl_idname = 'sequencerextra.import_subtitle'
    bl_description = ''.join(['Import subtitles as text strips.'])
    
    filter_glob = bpy.props.StringProperty(
            default="*.srt;*.lrc;*.txt",
            options={'HIDDEN'},
            maxlen=255,
            )
    
    def execute(self, context):
        scene = context.scene
        path = self.filepath.replace('\\','/')
        
        if path.endswith('.txt'):
            segments = parse_txt(path, scene)
        elif path.endswith('.srt'):
            segments = parse_srt(path)
        elif path.endswith('.lrc'):
            segments = parse_lrc(path)
        add_segments(scene, segments)
        
        return {'FINISHED'}
