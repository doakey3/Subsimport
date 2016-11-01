import bpy

class ShiftFrameStart(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_text_frame_start"
    bl_label = "Shift Frame Start of Next Text Strip"
    bl_description = "Shifts the frame start of text strip to the current frame"
    
    def execute(self, context):
        scene = context.scene
        current_frame = scene.frame_current
        seq = bpy.context.scene.sequence_editor
        if not seq == None:
            all_strips = list(sorted(seq.sequences_all,
                key=lambda x: x.frame_start))
            text_strips = []
            for strip in all_strips:
                if strip.type == "TEXT":
                    text_strips.append(strip)
            if not len(text_strips) == 0:
                for i in range(len(text_strips)):
                    if (text_strips[i].frame_final_start < current_frame and 
                    text_strips[i].frame_final_end > current_frame):
                        text_strips[i].frame_final_start = current_frame
                        return {"FINISHED"}
                    elif (text_strips[i].frame_final_start >= current_frame and 
                    text_strips[i].frame_final_end > current_frame and
                    i < len(text_strips)):
                        text_strips[i].frame_final_start = current_frame
                        return {"FINISHED"}
                        
            else:
                return {"FINISHED"}
        else:
            return {"FINISHED"}
            
        return {"FINISHED"}

class ShiftFrameEnd(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_text_frame_end"
    bl_label = "Shift Frame End of Next Text Strip"
    bl_description = "Shifts the frame end of text strip to the current frame"
    
    def execute(self, context):
        scene = context.scene
        current_frame = scene.frame_current
        seq = bpy.context.scene.sequence_editor
        if not seq == None:
            all_strips = list(sorted(seq.sequences_all,
                key=lambda x: x.frame_start))
            text_strips = []
            for strip in all_strips:
                if strip.type == "TEXT":
                    text_strips.append(strip)
            if not len(text_strips) == 0:
                for i in range(len(text_strips)):
                    if i == 0 and text_strips[i].frame_final_start > current_frame:
                        return {"FINISHED"}
                    elif (text_strips[i].frame_final_start < current_frame and 
                    text_strips[i].frame_final_end > current_frame):
                        text_strips[i].frame_final_end = current_frame
                        return {"FINISHED"}
                    elif (text_strips[i].frame_final_start >= current_frame and 
                    text_strips[i].frame_final_end > current_frame):
                        text_strips[i-1].frame_final_end = current_frame
                        return {"FINISHED"}
                    elif i == len(text_strips) - 1:
                        text_strips[i].frame_final_end = current_frame
                        return {"FINISHED"}
                        
                return {"FINISHED"}
            else:
                return {"FINISHED"}
        else:
            return {"FINISHED"}
            
        return {"FINISHED"}
