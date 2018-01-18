import bpy

from .operators.shortcuts import ShiftFrameStart
from .operators.shortcuts import ShiftFrameEnd
from .operators.shortcuts import ShiftFrameStartEnd
from .operators.shortcuts import ShiftFrameEndStart
from .operators.shortcuts import ResetChildren

from .operators.duration_adjust import DurationXTwo
from .operators.duration_adjust import DurationXHalf

from .operators.refresh_font_size import RefreshFontSize
from .operators.import_subtitles import ImportSubtitles
from .operators.export_srt import ExportSRT
from .operators.export_lrc import ExportLRC
from .operators.refresh_highlight import RefreshHighlight
from .operators.syllabify import Syllabify
from .operators.save_syllables import SaveSyllables
from .operators.split_words import SplitWords
from .operators.combine_words import CombineWords

from .operators.select import SelectChannelRight, SelectChannelLeft

bl_info = {
    "name": "Subsimport",
    "description": "Import subtitles into blender",
    "author": "doakey3",
    "version": (1, 2, 8),
    "blender": (2, 7, 8),
    "wiki_url": "https://github.com/doakey3/subsimport",
    "tracker_url": "https://github.com/doakey3/subsimport/issues",
    "category": "Sequencer"
    }

class subsimport_UI(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Subsimport"
    bl_category = "Tools"
    
    @classmethod
    def poll(cls, context):
        return context.space_data.view_type == 'SEQUENCER'

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        row = layout.row()
        row.prop(scene, 'subtitle_edit_channel', 
            text="Subtitle Edit Channel")
        
        box = layout.box()
        row = box.row(align=False)
        row.prop(scene, 'subtitle_font_size',
                 text='Subtitle Font Size')
        row.operator('sequencerextra.refresh_font_size', 
            icon="FILE_REFRESH")
        row = box.row()
        row.operator('sequencerextra.import_subtitles', icon='ANIM')
        row = box.row()
        row.operator('sequencerextra.duration_x_two', icon='PREVIEW_RANGE')
        row.operator('sequencerextra.duration_x_half', icon='RECOVER_LAST')
        row = box.row()
        row.operator('sequencerextra.export_srt', icon='RENDER_ANIMATION')
        row.operator('sequencerextra.export_lrc', icon='FILE_SOUND')
        box = layout.box()
        row = box.row()
        row.prop(scene, 'use_dictionary_syllabification', text="Dictionary Syllabification")
        row = box.row()
        row.prop(scene, 'use_algorithmic_syllabification', text="Algorithm")
        row.prop(scene, 'syllabification_language', text='')
        row = box.row()
        row.operator('sequencerextra.syllabify', icon="ALIGN")
        row.operator('sequencerextra.save_syllables', icon="DISK_DRIVE")
        row = box.row()
        row.prop(scene, 'syllable_dictionary_path', icon='TEXT', text="Syll Dict")
        
        row = box.row()
        row.prop(scene, 'enhanced_subs_color',
            text='Highlight')
        row.operator('sequencerextra.refresh_highlight', 
            icon='FILE_REFRESH')
        row = box.row()
        row.operator('sequencerextra.split_words', icon="MOD_EXPLODE")
        row = box.row()
        row.operator('sequencerextra.combine_words', icon="MOD_BUILD")
        row.prop(scene, 'subtitle_combine_mode', text='')

def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.subtitle_edit_channel = bpy.props.IntProperty(
        description="The channel where keyboard shortcuts will act on text strips",
        default=1,
        min=0)

    bpy.types.Scene.subtitle_font_size = bpy.props.IntProperty(
        description="The font size of the added text strips after import",
        default=70,
        min=1)
    
    bpy.types.Scene.syllable_dictionary_path = bpy.props.StringProperty(
        name="Syllable Dictionary Path",
        description="Path to the text file containing words separated by syllables.\nNeeded for accurate splitting of subtitles by syllable.",
        subtype="FILE_PATH",
        )
    
    bpy.types.Scene.enhanced_subs_color = bpy.props.FloatVectorProperty(  
       subtype='COLOR_GAMMA',
       description="Highlight color of the subtitles in the edit channel",
       size=3,
       default=(1.0, 0.5, 0.0),
       min=0.0, max=1.0,)
    
    bpy.types.Scene.use_dictionary_syllabification = bpy.props.BoolProperty(
        description="Use (Less-Error-Prone) algorithm to syllabify words.",
        default=True
    )
    
    bpy.types.Scene.use_algorithmic_syllabification = bpy.props.BoolProperty(
        description="Use (imperfect) algorithm to syllabify words.\nIf dictionary method is enabled, the algorithm is used for words not found in the dictionary.",
        default=True
    )
    
    language_options = [
        # probably don't need this
        #('grc', 'Ancient Greek', ''),
        ('hy', 'Armenian', ''),
        ('be', 'Belarusian', ''),
        ('bn', 'Bengali', ''),
        ('ca', 'Catalan', ''),
        ('cs', 'Czech', ''),
        ('da', 'Danish', ''),
        ('nl', 'Dutch', ''),
        # Better off using en-us until I have a better dictionary
        #('en-gb', 'English-Great Britain', ''), 
        ('en-us', 'English-U.S.', ''),
        ('eo', 'Esperanto', ''),
        ('et', 'Estonian', ''),
        ('fi', 'Finnish', ''),
        ('fr', 'French', ''),
        ('de', 'German', ''),
        ('gu', 'Gujarati', ''),
        ('hi', 'Hindi', ''),
        ('hu', 'Hungarian', ''),
        ('ga', 'Irish', ''),
        ('it', 'Italian', ''),
        ('lv', 'Latvian', ''),
        ('ml', 'Malayalam', ''),
        ('el-monoton', 'Monotonic Greek', ''),
        ('nb-no', 'Norwegian', ''),
        ('or', 'Oriya', ''),
        ('pl', 'Polish', ''),
        # Probably don't need this
        #('el-polyton', 'Polytonic Greek', ''),
        ('pt', 'Portuguese', ''),
        ('pa', 'Punjabi', ''),
        ('ro', 'Romanian', ''),
        ('ru', 'Russian', ''),
        ('sr-cyrl', 'Serbian Cyrillic', ''),
        ('sr-latn', 'Serbian Latin', ''),
        ('sk', 'Slovak', ''),
        ('sl', 'Slovene', ''),
        ('es', 'Spanish', ''),
        ('sv', 'Swedish', ''),
        ('ta', 'Tamil', ''),
        ('te', 'Telugu', ''),
        ('tr', 'Turkish', ''),
        ('uk', 'Ukrainian', ''),
        ]
    
    bpy.types.Scene.syllabification_language = bpy.props.EnumProperty(
        name="Syllabification Language",
        items=language_options,
        description="Set the language to use when syllabifying",
        default="en-us"
        )
    
    combine_modes = [
        ('esrt', 'ESRT', 'Combine subtitles as enhanced SRT strips'),
        ('elrc', 'ELRC', 'Combine subtitles as enhanced LRC strips')
    ]
    
    bpy.types.Scene.subtitle_combine_mode = bpy.props.EnumProperty(
        name="Subtitle Combine Mode",
        items=combine_modes,
        description="How to combine the subtitles",
        default="esrt"
        )

    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="Sequencer", space_type="SEQUENCE_EDITOR")
    kmi = km.keymap_items.new("sequencerextra.shift_frame_start",
                              "D", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_frame_end",
                              "F", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_frame_start_end", "W", "PRESS")
    kmi = km.keymap_items.new("sequencerextra.shift_frame_end_start", "S", 'PRESS')
    
    kmi = km.keymap_items.new("sequencerextra.reset_children", "Z", 'PRESS')

    kmi = km.keymap_items.new(
        "sequencerextra.select_channel_right", "RIGHT_ARROW", "PRESS", alt=False,
        ctrl=True, shift=True
        )
    kmi = km.keymap_items.new(
        "sequencerextra.select_channel_left", "LEFT_ARROW", "PRESS", alt=False,
        ctrl=True, shift=True
        )

def unregister():
    del bpy.types.Scene.subtitle_edit_channel
    del bpy.types.Scene.subtitle_font_size
    del bpy.types.Scene.enhanced_subs_color
    del bpy.types.Scene.syllable_dictionary_path
    del bpy.types.Scene.use_dictionary_syllabification
    del bpy.types.Scene.use_algorithmic_syllabification
    del bpy.types.Scene.syllabification_language
    del bpy.types.Scene.subtitle_combine_mode
    
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps["Sequencer"]
    for kmi in km.keymap_items:
        if kmi.idname in ["sequencerextra.shift_frame_start",
                          "sequencerextra.shift_frame_end",
                          "sequencerextra.shift_frame_start_end",
                          "sequencerextra.shift_frame_end_start",
                          "sequencerextra.select_channel_right",
                          "sequencerextra.select_channel_left"]:
            km.keymap_items.remove(kmi)

    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
