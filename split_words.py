import bpy

import sys
import os

modules_path = os.path.dirname(__file__)

if not modules_path in sys.path:
    sys.path.append(os.path.dirname(__file__))
    
import subsutils
import pysrt

def fillWordSpace(word):
    """Replaces all characters in a word with space"""
    growing_space = ''
    for char in word:
        growing_space += ' '
    return growing_space


def makePaddedParagraph(position, words_list):
    """Makes a padded paragraph"""
    words = []
    for i in range(len(words_list)):
        words.append(list(words_list[i]))
        
    for x in range(len(words)):
        for y in range(len(words[x])):
            if not [x, y] == position:
                words[x][y] = fillWordSpace(words[x][y])
    
    for i in range(len(words)):
        words[i] = ' '.join(words[i])
    return '\n'.join(words)


def paragraphDivider(text):
    """
    split each word in text, then pad it with spaces/newlines so
    the word appears in the same spot (in a monospace font)
    """
    words = []
    lines = text.split('\n')

    for i in range(len(lines)):
        words.append([])
        split = lines[i].split(' ')
        for word in split:
            words[i].append(word)
    
    padded_paragraphs = []
    for x in range(len(words)):
        for y in range(len(words[x])):
            
            pp = makePaddedParagraph([x, y], words)
            padded_paragraphs.append(pp)
    return padded_paragraphs     
                
class SplitWords(bpy.types.Operator):
    bl_label = 'Split Words'
    bl_idname = 'sequencerextra.split_words'
    bl_description = "Split each strip word by word. Needed for making enhanced subtitles"
    
    def execute(self, context):
        scene = context.scene
        edit_channel = scene.subtitle_edit_channel
        
        fps = scene.render.fps/scene.render.fps_base
        
        
        all_strips = list(sorted(
            scene.sequence_editor.sequences_all,
            key=lambda x: x.frame_start))
        
        text_strips = []
        for x in range(len(all_strips)):
            if (all_strips[x].type == "TEXT" and
                    all_strips[x].channel == edit_channel):
                text_strips.append(all_strips[x])
        
        sub_list = []
        index_count = 1
        
        if len(text_strips) == 0:
            return {"FINISHED"}
        
        for strip in text_strips:
            start = strip.frame_final_start / fps
            end = strip.frame_final_end / fps
            duration = strip.frame_final_duration / fps
            
            text = strip.text
            word_count = len(text.replace('\n', ' ').split(' '))
            piece_duration = duration / word_count
            padded_paragraphs = paragraphDivider(text)
            
            for i in range(len(padded_paragraphs)):
                dialogue = padded_paragraphs[i]    
                start_time = start + (piece_duration * i)
                end_time = start_time + piece_duration
                sub_item = pysrt.SubRipItem()
                
                sub_item.start.from_millis((start_time * 1000) + 1)
                sub_item.end.from_millis((end_time * 1000) + 1)
                sub_item.text = dialogue
                sub_item.index = index_count
                if len(dialogue.replace(dialogue.lstrip(), '')) == 0:
                    sub_item.name = '[locked start]'
                elif len(dialogue.replace(dialogue.rstrip(), '')) == 0:
                    sub_item.name = '[locked end]'
                sub_list.append(sub_item)
                index_count += 1
        
        subs = pysrt.SubRipFile(sub_list)
        subsutils.addSubs(context, subs, use_color=True)
            
        
        return {"FINISHED"}
