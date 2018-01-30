def get_text_strips(scene, channel=None):
    """Get all the text strips in the edit channel"""

    if channel == None:
        channel = scene.subtitle_edit_channel

    all_strips = list(sorted(scene.sequence_editor.sequences,
            key=lambda x: x.frame_start))

    text_strips = []
    for strip in all_strips:
        if (strip.channel == channel and
                strip.type == 'TEXT'):
            text_strips.append(strip)

    return text_strips