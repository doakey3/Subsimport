import bpy

import sys
import os

modules_path = os.path.dirname(__file__)

if not modules_path in sys.path:
    sys.path.append(os.path.dirname(__file__))

import subsutils
import pysrt

from aeneas.executetask import ExecuteTask
from aeneas.task import Task

def write_word_level(text, txt_path):
    """
    Writes each word of text on a separate line inside the .txt file
    """
    words = []
    text = text.split('\n')
    for line in text:
        split = line.split(' ')
        for word in split:
            words.append(word)

    txt_file = open(txt_path, 'w')
    txt_file.write('\n'.join(words))
    txt_file.close()

def make_subs(wav_path, txt_path, srt_path, start):
    """Gets the subtitles with the correct timing based on the wav file"""

    config_string = "task_language=eng|is_text_type=plain|os_task_file_format=srt"

    task = Task(config_string=config_string)
    task.audio_file_path_absolute = wav_path
    task.text_file_path_absolute = txt_path
    task.sync_map_file_path_absolute = srt_path

    ExecuteTask(task).execute()
    task.output_sync_map_file()

    subs = pysrt.open(srt_path)

    subs.shift(seconds=start)

    return subs


class SplitWords(bpy.types.Operator):
    bl_label = 'Split Words'
    bl_idname = 'sequencerextra.split_words'
    bl_description = "Split each strip word by word. Needed for making enhanced subtitles"

    def execute(self, context):
        scene = context.scene
        edit_channel = scene.subtitle_edit_channel

        fps = scene.render.fps/scene.render.fps_base

        original_start = scene.frame_start
        original_end = scene.frame_end

        all_strips = list(sorted(
            scene.sequence_editor.sequences_all,
            key=lambda x: x.frame_start))

        text_strips = []
        for x in range(len(all_strips)):
            if (all_strips[x].type == "TEXT" and
                    all_strips[x].channel == edit_channel):
                text_strips.append(all_strips[x])

        wav_path = os.path.join(os.path.dirname(__file__), 'temp.wav')
        txt_path = os.path.join(os.path.dirname(__file__), 'temp.txt')
        srt_path = os.path.join(os.path.dirname(__file__), 'temp.srt')

        subs = pysrt.SubRipFile()

        for i in range(len(text_strips)):
            frame_start = text_strips[i].frame_start
            frame_end = text_strips[i].frame_final_end - 1
            start = (frame_start + 1) / fps
            text = text_strips[i].text

            scene.frame_start = frame_start
            scene.frame_end = frame_end

            bpy.ops.sound.mixdown(filepath=wav_path, container="WAV", codec="PCM")
            write_word_level(text, txt_path)
            subs.extend(make_subs(wav_path, txt_path, srt_path, start))


        subsutils.addSubs(context, subs, use_color=True)

        return {"FINISHED"}