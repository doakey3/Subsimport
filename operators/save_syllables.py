import bpy
from .hyphenator.get_dictionary import get_dictionary
import os

class SEQUENCER_OT_save_syllables(bpy.types.Operator):
    bl_label = 'Save'
    bl_idname = 'sequencerextra.save_syllables'
    bl_description = "Add the syllables to the default syllable dictionary"

    @classmethod
    def poll(self, context):
        scene = context.scene
        path = bpy.path.abspath(scene.syllable_dictionary_path)

        if os.path.isfile(path):
            return True
        else:
            return False

    def execute(self, context):
        scene = context.scene
        dictionary = get_dictionary(
                lang=scene.syllabification_language)

        path = bpy.path.abspath(scene.syllable_dictionary_path)
        f = open(path, 'r')
        words = f.readlines()
        f.close()

        for i in range(len(words)):
            words[i] = words[i].rstrip()
            word = words[i].replace(' ', '')
            dictionary[word] = words[i]

        values = sorted(list(dictionary.values()))

        module_path = os.path.dirname(__file__)
        dic_path = os.path.join(
            module_path, 'hyphenator', 'dictionaries',
            scene.syllabification_language + '.txt')

        f = open(dic_path, 'w')
        f.write('\n'.join(values))
        f.close()

        return {"FINISHED"}
