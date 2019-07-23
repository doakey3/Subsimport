import bpy
from .operators import *

bl_info = {
    "name": "Subsimport",
    "description": "Import subtitles into blender",
    "author": "doakey3",
    "version": (1, 3, 1),
    "blender": (2, 80, 0),
    "wiki_url": "https://github.com/doakey3/subsimport",
    "tracker_url": "https://github.com/doakey3/subsimport/issues",
    "category": "Sequencer"
    }


class SEQUENCER_PT_subsimport(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Subsimport"
    bl_category = "Tools"
    bl_options = {"DEFAULT_CLOSED"}

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
        row.prop(scene, 'subtitle_font',
                 text='Font')
        row = box.row()
        row.prop(scene, 'subtitle_font_size',
                 text='Font Size')
        row = box.row()
        row.prop(scene, 'subtitle_font_height',
                 text='Font Height')
        row = box.row()
        row.operator('sequencerextra.refresh_font_data',
            icon="FILE_REFRESH")
        box = layout.box()
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
        row.operator('sequencerextra.syllabify', icon="ALIGN_FLUSH")
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


def init_prop():
    bpy.types.Scene.subtitle_edit_channel = bpy.props.IntProperty(
        description="The channel where keyboard shortcuts will act on text strips",
        default=1,
        min=0)

    bpy.types.Scene.subtitle_font = bpy.props.StringProperty(
        description="The font of the added text strips after import",
        subtype="FILE_PATH")

    bpy.types.Scene.subtitle_font_size = bpy.props.IntProperty(
        description="The font size of the added text strips after import",
        default=70,
        min=1)

    bpy.types.Scene.subtitle_font_height = bpy.props.FloatProperty(
        description="The height of the added text strips after import",
        default=0.0,
        min=0.0,
        max=1.0)

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

classes = [
    SEQUENCER_PT_subsimport,
    SEQUENCER_OT_combine_words,
    SEQUENCER_OT_duration_x_2,
    SEQUENCER_OT_duration_x_half,
    SEQUENCER_OT_export_lrc,
    SEQUENCER_OT_export_srt,
    SEQUENCER_OT_import_subtitles,
    SEQUENCER_OT_refresh_font_data,
    SEQUENCER_OT_refresh_highlight,
    SEQUENCER_OT_save_syllables,
    SEQUENCER_OT_select_channel_right,
    SEQUENCER_OT_select_channel_left,
    SEQUENCER_OT_shift_frame_start,
    SEQUENCER_OT_shift_frame_end,
    SEQUENCER_OT_shift_frame_start_end,
    SEQUENCER_OT_shift_frame_end_start,
    SEQUENCER_OT_reset_children,
    SEQUENCER_OT_split_words,
    SEQUENCER_OT_syllabify,
]
addon_keymaps = []

def register():
    init_prop()
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Sequencer", space_type="SEQUENCE_EDITOR", region_type="WINDOW")

    kmi = km.keymap_items.new("sequencerextra.shift_frame_start", "D", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_frame_end", "F", 'PRESS')
    kmi = km.keymap_items.new("sequencerextra.shift_frame_start_end", "W", "PRESS")
    kmi = km.keymap_items.new("sequencerextra.shift_frame_end_start", "S", 'PRESS')

    kmi = km.keymap_items.new("sequencerextra.reset_children", "Z", 'PRESS')

    kmi = km.keymap_items.new("sequencerextra.select_channel_right", "RIGHT_ARROW", "PRESS", alt=False, ctrl=True, shift=True)
    kmi = km.keymap_items.new("sequencerextra.select_channel_left", "LEFT_ARROW", "PRESS", alt=False, ctrl=True, shift=True)

    addon_keymaps.append(km)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
