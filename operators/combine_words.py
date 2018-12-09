import bpy
from .tools.get_text_strips import get_text_strips
from .tools.get_base_strip import get_base_strip
from .tools.subtitles_to_sequencer import subtitles_to_sequencer
from .tools.color_to_hexcode import color_to_hexcode

from .pylrc.tools.timecode import seconds_to_timecode

from .pysrt.srtitem import SubRipItem
from .pysrt.srtfile import SubRipFile

def check_bases(top_strips, bases):
    """
    Check to make sure that each top strip is within the start and end
    points of a base strip.
    """

    for strip in top_strips:
        base = get_base_strip(strip, bases)
        if base == None:
            return strip
    return True

def combine_esrt(fps, text_strips, bottom_text_strips, hexcolor):
    """
    Combine the text_strips with the bottom_strips into a SubRipFile
    """
    sub_list = []
    old_base_strip = ''
    for i in range(len(text_strips)):
        strip = text_strips[i]
        base_strip = get_base_strip(strip, bottom_text_strips)

        if not base_strip == old_base_strip:
            if len(sub_list) > 0:
                old_end = old_base_strip.frame_final_end
                old_strip = text_strips[i - 1]
                if not old_strip.frame_final_end == old_end:
                    start = old_strip.frame_final_end / fps
                    end = old_end / fps
                    text = '<font color="' + hexcolor + '">'
                    text += old_base_strip.text.rstrip()
                    text += '</font>'

                    sub_item = SubRipItem()
                    sub_item.start.from_millis((start * 1000))
                    sub_item.end.from_millis((end * 1000))
                    sub_item.text = text
                    sub_list.append(sub_item)

            start = base_strip.frame_final_start
            if not strip.frame_final_start == start:
                start = start / fps
                end = strip.frame_final_start / fps
                text = base_strip.text.rstrip()

                sub_item = SubRipItem()
                sub_item.start.from_millis((start * 1000))
                sub_item.end.from_millis((end * 1000))
                sub_item.text = text
                sub_list.append(sub_item)

            old_base_strip = base_strip

        start = strip.frame_final_start / fps
        end = strip.frame_final_end / fps
        text = '<font color="' + hexcolor + '">'
        text += strip.text.rstrip()
        text += '</font>'
        text += base_strip.text[len(strip.text.rstrip())::]

        sub_item = SubRipItem()
        sub_item.start.from_millis((start * 1000))
        sub_item.end.from_millis((end * 1000))
        sub_item.text = text
        sub_list.append(sub_item)

    old_end = old_base_strip.frame_final_end
    old_strip = text_strips[-1]
    if not old_strip.frame_final_end == old_end:
        start = old_strip.frame_final_end / fps
        end = old_end / fps
        text = '<font color="' + hexcolor + '">'
        text += old_base_strip.text.rstrip()
        text += '</font>'

        sub_item = SubRipItem()
        sub_item.start.from_millis((start * 1000))
        sub_item.end.from_millis((end * 1000))
        sub_item.text = text
        sub_list.append(sub_item)

    subs = SubRipFile(sub_list)

    return subs

def combine_elrc(fps, text_strips, bottom_text_strips):
    """
    Combine the text_strips with the bottom_strips into a SubRipFile
    """
    sub_list = []
    old_base_strip = ''
    for i in range(len(text_strips)):
        strip = text_strips[i]
        base_strip = get_base_strip(strip, bottom_text_strips)

        if not base_strip == old_base_strip:
            old_base_strip = base_strip
            start = base_strip.frame_final_start / fps
            end = base_strip.frame_final_end / fps

            sub_item = SubRipItem()
            sub_item.start.from_millis((start * 1000))
            sub_item.end.from_millis((end * 1000))

            start = strip.frame_final_start / fps
            time_code = seconds_to_timecode(start, '<>')
            text = time_code + strip.text.rstrip()
            sub_item.text = text

            if len(sub_list) > 0:
                end = text_strips[i - 1].frame_final_end / fps
                time_code = seconds_to_timecode(end, '<>')
                sub_list[-1].text += time_code

            sub_list.append(sub_item)

        else:
            start = strip.frame_final_start / fps
            time_code = seconds_to_timecode(start, '<>')
            text = strip.text[len(text_strips[i - 1].text.rstrip())::]
            text = time_code + text.rstrip()
            sub_list[-1].text += text

            if i == len(text_strips) - 1:
                end = text_strips[i].frame_final_end / fps
                time_code = seconds_to_timecode(end, '<>')
                sub_list[-1].text += time_code

    subs = SubRipFile(sub_list)

    return subs


class SEQUENCER_OT_combine_words(bpy.types.Operator):
    bl_label = 'Combine'
    bl_idname = 'sequencerextra.combine_words'
    bl_description = 'Combine subtitles from edit channel with the subtitles in the channel below.'

    @classmethod
    def poll(self, context):
        scene = context.scene
        try:
            text_strips = get_text_strips(scene)
            low_channel = scene.subtitle_edit_channel - 1
            bottom_text_strips = get_text_strips(scene, low_channel)

            if len(text_strips) > 0 and len(bottom_text_strips) > 0:
                return True
            else:
                return False
        except AttributeError:
            return False

    def execute(self, context):
        scene = context.scene
        fps = scene.render.fps / scene.render.fps_base
        text_strips = get_text_strips(scene)
        low_channel = scene.subtitle_edit_channel - 1
        bottom_text_strips = get_text_strips(scene, low_channel)

        c = scene.enhanced_subs_color
        color = [c[0], c[1], c[2]]
        hexcolor = color_to_hexcode(color)

        base_check = check_bases(text_strips, bottom_text_strips)
        if not base_check == True:
            frame = str(base_check.frame_final_start)
            channel = str(base_check.channel)
            message = ' '.join([
                'The strip at frame', frame, ', channel ', channel,
                'has no base strip.', '\n', 'Correct this and try again.'])
            self.report(set({'ERROR'}), message)
            return {"FINISHED"}

        if scene.subtitle_combine_mode == 'esrt':
            subs = combine_esrt(fps, text_strips, bottom_text_strips, hexcolor)


        elif scene.subtitle_combine_mode == 'elrc':
            subs = combine_elrc(fps, text_strips, bottom_text_strips)

        bpy.ops.sequencer.select_all(action="DESELECT")
        for strip in text_strips:
            strip.select = True
            bpy.ops.sequencer.delete()

        for strip in bottom_text_strips:
            strip.select = True
            bpy.ops.sequencer.delete()

        text_strips = subtitles_to_sequencer(context, subs)
        scene.subtitle_edit_channel = text_strips[0].channel

        return {"FINISHED"}
