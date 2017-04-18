import bpy
from bpy_extras.io_utils import ImportHelper

import sys
import os

modules_path = os.path.dirname(__file__)

if not modules_path in sys.path:
    sys.path.append(os.path.dirname(__file__))

import pysrt
import subsutils
import pylrc

class ImportSubtitles(bpy.types.Operator, ImportHelper):
    bl_label = 'Import'
    bl_idname = 'sequencerextra.import_subtitles'
    bl_description = 'Import subtitles as text strips. (.txt, .lrc, or .srt)'

    filter_glob = bpy.props.StringProperty(
            default="*.srt;*.lrc;*.txt",
            options={'HIDDEN'},
            maxlen=255,
            )

    def execute(self, context):
        scene = context.scene
        path = self.filepath.replace('\\', '/')
        
        text_file = open(path, 'r', encoding='utf-8', errors='ignore')
        text = ''.join(text_file.readlines()).rstrip()
        text_file.close()
        
        if path.endswith('.lrc'):
            subs = pylrc.parse(text)
            text = subs.toSRT()
        
        elif path.endswith('.txt'):            
            text = subsutils.text2srt(text)
        
        srt = pysrt.from_string(text)
        
        srt.remove_overlaps()

        subsutils.addSubs(context, srt)
        
        return {"FINISHED"}
