import bpy

from .get_open_channel import get_open_channel
from .get_font import get_font

def subtitles_to_sequencer(context, subs):
    """Add subtitles to the video sequencer"""

    scene = context.scene
    fps = scene.render.fps / scene.render.fps_base
    open_channel = get_open_channel(scene)

    if not scene.sequence_editor:
        scene.sequence_editor_create()

    wm = context.window_manager
    wm.progress_begin(0, 100.0)

    added_strips = []

    for i in range(len(subs)):
        start_time = subs[i].start.to_millis() / 1000
        strip_start = round(start_time * fps, 0)

        end_time = subs[i].end.to_millis() / 1000
        strip_end = round(end_time * fps, 0)
        sub_name = str(open_channel) + '_' + str(i + 1)
        try:
            if '[locked start]' in subs[i].name:
                sub_name = '[locked start]' + sub_name
            if '[locked end]' in subs[i].name:
                sub_name += '[locked end]'
        except AttributeError:
            pass

        text_strip = scene.sequence_editor.sequences.new_effect(
            name=sub_name,
            type='TEXT',
            channel=open_channel,
            frame_start=strip_start,
            frame_end=strip_end
            )

        text_strip.font = get_font(scene.subtitle_font)
        text_strip.font_size = scene.subtitle_font_size
        text_strip.location[1] = scene.subtitle_font_height
        text_strip.text = subs[i].text
        text_strip.use_shadow = True
        text_strip.select = True
        text_strip.blend_type = 'ALPHA_OVER'

        added_strips.append(text_strip)

    return added_strips