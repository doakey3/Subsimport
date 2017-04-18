import bpy

def get_parent(child, parents):
    """
    Returns the text strip from the base channel from which the child
    text strip originated.
    """
    start = child.frame_start
    end = child.frame_final_end
    
    for i in range(len(parents)):
        pstart = parents[i].frame_start
        pend = parents[i].frame_final_end
        
        if pstart <= start and pend >= end:
            return parents[i]

def get_child_number(child, children, parent):
    """Gets the child's place among all the parent's children"""
    
    pkids = []
    
    pstart = parent.frame_start
    pend = parent.frame_final_end
    
    for kid in children:
        start = kid.frame_start
        end = kid.frame_final_end
        
        if pstart <= start and pend >= end:
            pkids.append(kid)
    
    for i in range(len(pkids)):
        if pkids[i] == child:
            return i

def combine_child_and_parent(child, children, parents, color):
    parent = get_parent(child, parents)
    child_number = get_child_number(child, children, parent)
    color_list = list(color)
    for i in range(len(color_list)):
        color_list[i] = int(color_list[i] * 256)
        if color_list[i] == 256:
            color_list[i] -= 1
    r, g, b = color_list
    
    hexcode = '#%02x%02x%02x' % (r, g, b)
    ctext = '<font color="' + hexcode + '">' + child.text.strip() + '</font>'
    pmatrix = parent.text.split('\n')
    for i in range(len(pmatrix)):
        pmatrix[i] = pmatrix[i].split(' ')
    
    count = 0
    for row in range(len(pmatrix)):
        for column in range(len(pmatrix[row])):
            if count == child_number:
                pmatrix[row][column] = ctext
            count += 1
    
    new_text = []
    lines = []
    for row in range(len(pmatrix)):
        for column in range(len(pmatrix[row])):
            new_text.append(pmatrix[row][column])
        lines.append(' '.join(new_text))
        new_text = []
    child.text = '\n'.join(lines)
    child.color = parent.color

class CombineWords(bpy.types.Operator):
    bl_label = 'Combine Words'
    bl_idname = 'sequencerextra.combine_words'
    bl_description = "Combine 2 channels of text strips to create enhanced subtitles"
    
    def execute(self, context):
        scene = context.scene
        
        edit_channel = scene.subtitle_edit_channel
        color = scene.enhanced_subs_color
        fps = scene.render.fps/scene.render.fps_base
        
        
        all_strips = list(sorted(
            scene.sequence_editor.sequences_all,
            key=lambda x: x.frame_start))
        
        base_strips = []
        for x in range(len(all_strips)):
            if (all_strips[x].type == "TEXT" and
                    all_strips[x].channel == edit_channel - 1):
                base_strips.append(all_strips[x])
        
        word_strips = []
        for x in range(len(all_strips)):
            if (all_strips[x].type == "TEXT" and
                    all_strips[x].channel == edit_channel):
                word_strips.append(all_strips[x])
        
        for i in range(len(word_strips)):
            combine_child_and_parent(word_strips[i], word_strips, base_strips, color)
        
        return {"FINISHED"}
