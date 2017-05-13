import bpy
from bpy_extras.io_utils import ExportHelper
from .hyphenator.hyphenator import Hyphenator
from .hyphenator.get_dictionary import get_dictionary
from .common.get_text_strips import get_text_strips
from .common.remove_punctuation import remove_punctuation

def collect_words(scene):
    """Collect, clean, and alphabetize the words in the subtitles"""
    
    words = []
        
    text_strips = get_text_strips(scene)
    for strip in text_strips:
        strip_words = strip.text.lower().replace('\n', ' ').split(' ')
        words.extend(strip_words)
    
    i = 0
    while i < len(words):
        if words[i].rstrip() == '':
            words.pop(i)
        else:
            i += 1
            
    words = set(words)
    words = list(sorted(words))
    
    for i in range(len(words)):
        words[i] = remove_punctuation(words[i])
    
    return words


class Syllabify(bpy.types.Operator, ExportHelper):
    bl_label = 'Syllabify'
    bl_idname = 'sequencerextra.syllabify'
    bl_description = "Create a list of words, separated by syllables.\nNeeded for splitting words with accurate syllable differentiation"
    
    filename_ext = ".txt"
    
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
        
        words = collect_words(scene)
        
        found_words = []
        if scene.use_dictionary_syllabification:
            dictionary = get_dictionary()
            for i in range(len(words)):
                try:
                    words[i] = dictionary[words[i]]
                    found_words.append(words[i])
                except KeyError:
                    pass
                    
        if scene.use_algorithmic_syllabification:
            hyphenator = Hyphenator()
            for i in range(len(words)):
                if not words[i] in found_words:
                    words[i] = hyphenator.hyphenate_word(words[i])
                    words[i] = ' '.join(words[i])
        
        f = open(self.filepath, 'w')
        f.write('\n'.join(words))
        f.close()
        
        scene.syllable_dictionary_path = self.filepath
        
        return {"FINISHED"}
