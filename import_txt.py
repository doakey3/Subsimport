import bpy
from .funcs import *
from .import_srt import Segment
from bpy_extras.io_utils import ImportHelper

class ImportTXT(bpy.types.Operator, ImportHelper):
    bl_label = 'Import Text'
    bl_idname = 'sequencerextra.import_txt'
    bl_description = ''.join(['Import .txt as text strips.\nEach line will be a text strip. \nLimit your line lengths to 74 characters.'])
    
    filter_glob = bpy.props.StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            maxlen=255,
            )
    
    def execute(self, context):
        scene = context.scene
        fps = scene.render.fps/scene.render.fps_base
        
        path = self.filepath.replace('\\','/')
        
        f = open(path,'r')
        lines = f.readlines()
        f.close()
        current_step = scene.frame_start
        segments = []
        for i in range(len(lines)):
            segments.append(Segment())
            segments[-1].segment_number = i+1
            line = lines[i].rstrip()
            length = len(line)
            if length > 37:
                words = line.split(' ')
                line1, line2 = find_even_split(words)
                segments[-1].topline = line1
                segments[-1].bottomline = line2
            else:
                segments[-1].bottomline = line
            segments[-1].start_time = current_step/fps + (1.000000001/fps)
            current_step += fps
            segments[-1].end_time = current_step/fps
        
        add_segments(scene,segments)
            
        return {'FINISHED'}
