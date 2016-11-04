bl_info = {
    "name": "Subsimport",
    "description": "Import subtitles into blender",
    "author": "doakey3",
    "version": (1, 0, 2),
    "blender": (2, 7, 8),
    "wiki_url": "",
    "tracker_url":"",
    "category": "Sequencer"}

import bpy
from .import_srt import ImportSRT
from .import_lrc import ImportLRC
from .import_txt import ImportTXT
from .shortcut_functions import ShiftFrameStart
from .shortcut_functions import ShiftFrameEnd
    
class subsimport_UI(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Subtitles"
    
    def draw(self, context):
        layout = self.layout
        channel = layout.row()
        channel.prop(context.scene, 'subtitle_channel',
            text='Subtitle Channel')
        font_size = layout.row()
        font_size.prop(context.scene,'subtitle_font_size',
            text='Subtitle Font Size')
        srow = layout.row()
        srow.operator('sequencerextra.import_srt',icon="WORDWRAP_ON")
        lrow = layout.row()
        lrow.operator('sequencerextra.import_lrc',icon="LONGDISPLAY")
        trow = layout.row()
        trow.operator('sequencerextra.import_txt',icon="TEXT")
            
def register():
    bpy.utils.register_module(__name__)
    
    bpy.types.Scene.subtitle_channel = bpy.props.IntProperty(
        description="The channel where subtitles will be added",
        default=3,
        min=1)
    bpy.types.Scene.subtitle_font_size = bpy.props.IntProperty(
        description="The font_size of the added text strips after import",
        default=70,
        min=1)
    
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="Sequencer", space_type="SEQUENCE_EDITOR")
    kmi = km.keymap_items.new("sequencerextra.shift_text_frame_start", "D", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_text_frame_end", "F", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_both", "S", 'PRESS')
    
def unregister():
    bpy.utils.unregister_module(__name__)
    
    del bpy.types.Scene.subtitle_channel
    
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps["Sequencer"] 
    for kmi in km.keymap_items:
        if kmi.idname in ["sequencerextra.shift_text_frame_start",
                          "sequencerextra.shift_text_frame_end",
                          "sequencerextra.shift_both"]:
            km.keymap_items.remove(kmi)

if __name__ == "__main__":
    register()
