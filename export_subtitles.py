import bpy
from bpy_extras.io_utils import ExportHelper

class ExportLRC(bpy.types.Operator, ExportHelper):
    bl_label = 'Export LRC'
    bl_idname = 'sequencerextra.export_lrc'
    bl_description = 'Export Subtitles'
    
    filename_ext = ".lrc"
    
    def execute(self, context):
        scene = context.scene
        
        return {"FINISHED"}
