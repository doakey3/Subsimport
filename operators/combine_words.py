import bpy
from .common.get_text_strips import get_text_strips
from .common.subtitles_to_sequencer import subtitles_to_sequencer

from .pysrt.srtitem import SubRipItem
from .pysrt.srtfile import SubRipFile

def get_base(strip, base_strips):
    """Get the strip's base strip"""
    for i in range(len(base_strips)):
        if base_strips[i].frame_start <= strip.frame_start:
            if base_strips[i].frame_final_end >= strip.frame_final_end:
                return base_strips[i]

def color_to_hexcolor(base_color):
    """convert float color to hexcode color"""
    color = [base_color[0], base_color[1], base_color[2]]
    for i in range(len(color)):
        color[i] = int(color[i] * 256)
        if color[i] == 256:
            color[i] -= 1
    return '#%02x%02x%02x' % tuple(color)
    

class CombineWords(bpy.types.Operator):
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
        text_strips = get_text_strips(scene)
        low_channel = scene.subtitle_edit_channel - 1
        bottom_text_strips = get_text_strips(scene, low_channel)
        
        hexcolor = color_to_hexcolor(scene.enhanced_subs_color)

        sub_list = []
        for strip in text_strips:
            base = get_base(strip, bottom_text_strips)
            
            text = '<font color="' + hexcolor + '">'
            text += strip.text.rstrip()
            text += '</font>'
            text += base.text[len(strip.text.rstrip())::]
            
            sub_item = SubRipItem()
            
            fps = scene.render.fps/scene.render.fps_base
            start = strip.frame_final_start / fps
            end = strip.frame_final_end / fps
            
            sub_item.start.from_millis((start * 1000))
            sub_item.end.from_millis((end * 1000))
            sub_item.text = text
            
            sub_list.append(sub_item)
        
        subs = SubRipFile(sub_list)
        
        bpy.ops.sequencer.select_all(action="DESELECT")
        for strip in text_strips:
            strip.select = True
            bpy.ops.sequencer.delete()
        
        for strip in bottom_text_strips:
            strip.select = True
            bpy.ops.sequencer.delete()
        
        subtitles_to_sequencer(context, subs)
        
        return {"FINISHED"}
