import bpy
from bpy_extras.io_utils import ImportHelper
import sys
import os

from .shortcut_functions import ShiftFrameStart
from .shortcut_functions import ShiftFrameEnd
from .shortcut_functions import ShiftBoth

modules_path = os.path.dirname(__file__)

if not modules_path in sys.path:
    sys.path.append(os.path.dirname(__file__))

import pysrt
import subsutils
import pylrc

bl_info = {
    "name": "Subsimport",
    "description": "Import subtitles into blender",
    "author": "doakey3",
    "version": (1, 1, 2),
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
        row.operator('sequencerextra.import_subtitle', icon="TEXT")
        

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
        path = self.filepath.replace('\\', '/')
        
        if path.endswith('.lrc'):
            lrc_file = open(path, 'r', encoding='utf-8', errors='replace') #surrogateescape?
            text = ''.join(lrc_file.readlines()).rstrip()
            lrc_file.close()
            
            subs = pylrc.parse(text)
            text = subs.toSRT()
        
        elif path.endswith('.srt'):
            srt_file = open(path, 'r', encoding='utf-8', errors='replace')
            text = ''.join(srt_file.readlines()).rstrip()
            srt_file.close()
        
        else:
            txt_file = open(path, 'r', encoding='utf-8', errors='replace')
            text = ''.join(txt_file.readlines()).rstrip()
            txt_file.close()
            
            text = subsutils.text2srt(text)
        
        srt = pysrt.from_string(text)
        
        subsutils.addSubs(scene, srt)
        
        return {"FINISHED"}


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
    kmi = km.keymap_items.new("sequencerextra.shift_text_frame_start",
                              "D", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_text_frame_end",
                              "F", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_both", "S", 'PRESS')


def unregister():
    del bpy.types.Scene.subtitle_channel

    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps["Sequencer"]
    for kmi in km.keymap_items:
        if kmi.idname in ["sequencerextra.shift_text_frame_start",
                          "sequencerextra.shift_text_frame_end",
                          "sequencerextra.shift_both"]:
            km.keymap_items.remove(kmi)

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
