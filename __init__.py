import bpy
from bpy.props import FloatVectorProperty

from .import_subtitles import ImportSubtitles
from .export_subtitles import ExportLRC
from .split_words import SplitWords
from .combine_words import CombineWords
from .shortcut_functions import ShiftFrameStart
from .shortcut_functions import ShiftFrameEnd
from .shortcut_functions import ShiftFrameStartEnd
from .shortcut_functions import ShiftFrameEndStart


bl_info = {
    "name": "Subsimport",
    "description": "Import subtitles into blender",
    "author": "doakey3",
    "version": (1, 1, 3),
    "blender": (2, 7, 8),
    "wiki_url": "https://github.com/doakey3/subsimport",
    "tracker_url": "https://github.com/doakey3/subsimport/issues",
    "category": "Sequencer"}


class subsimport_UI(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Subsimport"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, 'subtitle_font_size',
                 text='Subtitle Font Size')
        row = layout.row()
        row.operator('sequencerextra.import_subtitles', icon="TEXT")
        row = layout.row()
        row.prop(context.scene, 'subtitle_edit_channel', 
            text="Subtitle Edit Channel")
        row = layout.row()
        row.operator('sequencerextra.split_words')
        row.prop(context.scene, 'enhanced_subs_color',
            text='')
        row = layout.row()
        row.operator('sequencerextra.combine_words')
        row.prop(context.scene, 'subtitle_combine_method', text="")
        row = layout.row()
        row.operator('sequencerextra.export_lrc', icon="GO_LEFT")


def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.subtitle_font_size = bpy.props.IntProperty(
        description="The font size of the added text strips after import",
        default=70,
        min=1)
        
    bpy.types.Scene.subtitle_edit_channel = bpy.props.IntProperty(
        description="The channel where keyboard shortcuts will act on text strips",
        default=1,
        min=1)
    
    bpy.types.Scene.enhanced_subs_color = FloatVectorProperty(  
       subtype='COLOR_GAMMA',
       description="Highlighted word color",
       size=3,
       default=(1.0, 0.5, 0.0),
       min=0.0, max=1.0,)
    
    combine_methods = [
        #(identifier, name, description, icon, number)
        ("E SRT", "Enhanced SubRip Text", "Combine as enhanced SRT"),
        ("E LRC", "Enhanced Lyrics", "Combine as enhanced LRC"),
        ("EM SRT", "Enhanced Monomer SubRip Text", "Combine as SRT with one word highlighted at a time"),
        ]
    
    bpy.types.Scene.subtitle_combine_method = bpy.props.EnumProperty(
        items=combine_methods,
        description="Combination Method",
        default="E SRT"
        )
    

    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="Sequencer", space_type="SEQUENCE_EDITOR")
    kmi = km.keymap_items.new("sequencerextra.shift_frame_start",
                              "D", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_frame_end",
                              "F", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_frame_start_end", "W", "PRESS")
    kmi = km.keymap_items.new("sequencerextra.shift_frame_end_start", "S", 'PRESS')


def unregister():
    del bpy.types.Scene.subtitle_edit_channel
    del bpy.types.Scene.subtitle_font_size
    del bpy.types.Scene.enhanced_subs_color
    del bpy.types.Scene.subtitle_combine_method

    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps["Sequencer"]
    for kmi in km.keymap_items:
        if kmi.idname in ["sequencerextra.shift_frame_start",
                          "sequencerextra.shift_frame_end",
                          "sequencerextra.shift_frame_start_end",
                          "sequencerextra.shift_frame_end_start"]:
            km.keymap_items.remove(kmi)

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
