import bpy
from .tools.get_base_strip import get_base_strip
from .tools.get_text_strips import get_text_strips

class SEQUENCER_OT_shift_frame_start(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_frame_start"
    bl_label = "Shift Frame Start of Next Text Strip"
    bl_description = "Shifts frame start of text strip to the current frame"

    def execute(self, context):
        scene = context.scene

        try:
            text_strips = get_text_strips(scene)

            if len(text_strips) == 0:
                return {"FINISHED"}
        except AttributeError:
            return {"FINISHED"}

        current_frame = scene.frame_current
        base_channel = text_strips[0].channel - 1
        base_strips = get_text_strips(scene, channel=base_channel)

        for i in range(len(text_strips)):
            strip = text_strips[i]
            start = strip.frame_final_start
            end = strip.frame_final_end

            if current_frame >= start and current_frame < end:
                strip.frame_final_start = current_frame
                return {"FINISHED"}

            elif current_frame < start:
                if not strip.name.startswith('[locked start]'):
                    strip.frame_final_start = current_frame
                    return {"FINISHED"}

                elif len(base_strips) == 0:
                    strip.frame_final_start = current_frame
                    return {"FINISHED"}

                else:
                    base = get_base_strip(strip, base_strips)
                    try:
                        if base.frame_final_start <= current_frame:
                            strip.frame_final_start = current_frame
                            return {"FINISHED"}
                        else:
                            strip.frame_final_start = base.frame_final_start
                            return {"FINISHED"}
                    except AttributeError:
                        strip.frame_final_start = current_frame
                        return {"FINISHED"}

        return {"FINISHED"}


class SEQUENCER_OT_shift_frame_end(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_frame_end"
    bl_label = "Shift Frame End of Next Text Strip"
    bl_description = "Shifts the frame end of text strip to the current frame"

    def execute(self, context):
        scene = context.scene

        try:
            text_strips = list(reversed(get_text_strips(scene)))

            if len(text_strips) == 0:
                return {"FINISHED"}
        except AttributeError:
            return {"FINISHED"}

        current_frame = scene.frame_current
        base_channel = text_strips[0].channel - 1
        base_strips = get_text_strips(scene, channel=base_channel)

        for i in range(len(text_strips)):
            strip = text_strips[i]
            start = strip.frame_final_start
            end = strip.frame_final_end

            if current_frame > start and current_frame <= end:
                strip.frame_final_end = current_frame
                return {"FINISHED"}

            elif current_frame > end:
                if not strip.name.endswith('[locked end]'):
                    strip.frame_final_end = current_frame
                    return {"FINISHED"}

                elif len(base_strips) == 0:
                    strip.frame_final_end = current_frame
                    return {"FINISHED"}

                else:
                    base = get_base_strip(strip, base_strips)
                    try:
                        if base.frame_final_end >= current_frame:
                            strip.frame_final_end = current_frame
                            return {"FINISHED"}
                        else:
                            strip.frame_final_end = base.frame_final_end
                            return {"FINISHED"}
                    except AttributeError:
                        strip.frame_final_end = current_frame
                        return {"FINISHED"}

        return {"FINISHED"}


class SEQUENCER_OT_shift_frame_start_end(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_frame_start_end"
    bl_label = "Shift Frame End then Frame start of next"
    bl_description = "Like pressing D then F"

    def execute(self, context):
        bpy.ops.sequencerextra.shift_frame_start()
        bpy.ops.sequencerextra.shift_frame_end()

        return {"FINISHED"}


class SEQUENCER_OT_shift_frame_end_start(bpy.types.Operator):
    bl_idname = "sequencerextra.shift_frame_end_start"
    bl_label = "Shift Frame End then Frame start of next"
    bl_description = "Like pressing F then D"

    def execute(self, context):
        bpy.ops.sequencerextra.shift_frame_end()
        bpy.ops.sequencerextra.shift_frame_start()

        return {"FINISHED"}

class SEQUENCER_OT_reset_children(bpy.types.Operator):
    bl_idname = "sequencerextra.reset_children"
    bl_label = "Send the children to the final frames of the parent"
    bl_description = "Press Z while the current time indicator is on a parent and the upper strips will be sent to the end of the parent"

    def execute(self, context):
        scene = context.scene

        try:
            text_strips = get_text_strips(scene)
            low_channel = scene.subtitle_edit_channel - 1
            parents = get_text_strips(scene, low_channel)
            current_frame = scene.frame_current

            if len(text_strips) > 0 and len(parents) > 0:
                go = False
                for base in parents:
                    b_start = base.frame_final_start
                    b_end = base.frame_final_end
                    if current_frame >= b_start and current_frame <= b_end:
                        go = True
                        break
                if not go:
                    return {"FINISHED"}

            else:
                return {"FINISHED"}
        except AttributeError:
            return {"FINISHED"}

        for parent in parents:
            p_start = parent.frame_final_start
            p_end = parent.frame_final_end

            if current_frame >= p_start and current_frame <= p_end:
                current_parent = parent
                break

        p_start = current_parent.frame_final_start
        p_end = current_parent.frame_final_end

        maybe_children = get_text_strips(scene)

        children = []
        for maybe_child in maybe_children:
            m_start = maybe_child.frame_final_start
            m_end = maybe_child.frame_final_end

            if p_start <= m_start and p_end >= m_end:
                children.append(maybe_child)

        children = list(reversed(children))
        for i in range(len(children)):
            if children[i].frame_final_end > current_frame:
                children[i].frame_final_end = p_end - i
                children[i].frame_final_start = p_end - (i + 1)

        return {"FINISHED"}
