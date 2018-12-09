import bpy
import os

from .tools.get_text_strips import get_text_strips
from .tools.subtitles_to_sequencer import subtitles_to_sequencer
from .tools.remove_punctuation import remove_punctuation

from .pysrt.srtitem import SubRipItem
from .pysrt.srtfile import SubRipFile

from .hyphenator.get_dictionary import get_dictionary


def break_strip(scene, strip):
    """
    Break a strip into it's words/syllables and
    return a list of the pieces
    """

    dic_path = bpy.path.abspath(scene.syllable_dictionary_path)
    if os.path.isfile(dic_path):
        dictionary = get_dictionary(dic_path)
    else:
        dictionary = {}

    words = strip.text.replace('\n', ' ').split(' ')
    i = 0
    while i < len(words):
        if words[i].rstrip() == '':
            words.pop(i)
        else:
            i += 1

    finished_pieces = []

    for i in range(len(words)):
        words[i] = words[i].strip()

        try:
            key = remove_punctuation(words[i].lower())
            pieces = dictionary[key].split(' ')
        except KeyError:
            pieces = [words[i]]

        for x in range(len(pieces)):
            string = ''
            while len(pieces[x]) > 0:

                if words[i][0].lower() == pieces[x][0]:
                    pieces[x] = pieces[x][1::]
                string += words[i][0]
                words[i] = words[i][1::]

                if x == len(pieces) - 1:
                    string += words[i]
                    pieces[x] = ''

            finished_pieces.append(string)

    return finished_pieces


def form_items(scene, strip, pieces):
    """
    Create SubRipItems for each piece
    """

    fps = scene.render.fps / scene.render.fps_base
    start = strip.frame_final_start / fps
    end = strip.frame_final_end / fps

    text = strip.text
    lines = text.split('\n')
    empty_text = ''
    for i in range(len(lines)):
        for char in range(len(lines[i])):
            empty_text += ' '
        empty_text += '\n'

    new_pieces = []
    for i in range(len(pieces)):
        if i == 0:
            string = ''
        else:
            string = new_pieces[i - 1].rstrip()
        while len(pieces[i]) > 0:
            if text[0] == pieces[i][0]:
                pieces[i] = pieces[i][1::]
            string += text[0]
            text = text[1::]
        string = string + empty_text[len(string)::]
        new_pieces.append(string)

    new_pieces = list(reversed(new_pieces))
    sub_list = []
    step = 1 / fps

    for i in range(len(new_pieces)):
        if not i == len(new_pieces) - 1:
            start_time = end - (step * i) - step
            end_time = start_time + step
        else:
            end_time = end - (step * i)
            start_time = start

        sub_item = SubRipItem()
        sub_item.start.from_millis(start_time * 1000)
        sub_item.end.from_millis(end_time * 1000)
        sub_item.text = new_pieces[i]
        sub_item.name = ''

        if i == 0:
            sub_item.name = '[locked end]'
        if i == len(new_pieces) - 1:
            sub_item.name += '[locked start]'

        sub_list.append(sub_item)

    return sub_list


class SEQUENCER_OT_split_words(bpy.types.Operator):
    bl_label = 'Split'
    bl_idname = 'sequencerextra.split_words'
    bl_description = 'Create new subtitles where each word is separated.\n\nIf a syllable dictionary is provided, words will be further split by their syllables'

    @classmethod
    def poll(self, context):
        scene = context.scene
        try:
            text_strips = get_text_strips(scene)

            if len(text_strips) > 0:
                return True
            else:
                return False
        except AttributeError:
            return False

    def execute(self, context):

        scene = context.scene
        text_strips = get_text_strips(scene)

        sub_list = []
        for strip in text_strips:
            pieces = break_strip(scene, strip)
            sub_list.extend(form_items(scene, strip, pieces ))

        for i in range(len(sub_list)):
            sub_list[i].index = i + 1

        subs = SubRipFile(sub_list)

        new_strips = subtitles_to_sequencer(context, subs)

        for strip in new_strips:
            strip.color[0] = scene.enhanced_subs_color[0]
            strip.color[1] = scene.enhanced_subs_color[1]
            strip.color[2] = scene.enhanced_subs_color[2]

        scene.subtitle_edit_channel = new_strips[0].channel

        return {"FINISHED"}
