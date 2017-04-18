import bpy
import time
import sys

def find_sequencer_area():
    """Locate the sequencer area"""
    screens = list(bpy.data.screens)
    for screen in screens:
        for area in screen.areas:
            if area.type == 'SEQUENCE_EDITOR':
                return screen, area

def getOpenChannel(scene):
    """Get a channel with nothing in it"""
    channels = []
    try:
        for strip in scene.sequence_editor.sequences_all:
            channels.append(strip.channel)
        if len(channels) > 0:
            return max(channels) + 1
        else:
            return 1
    except AttributeError:
        return 1

def update_progress(job_title, progress):
    length = 20
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title,
                                     "#" * block + "-" * (length-block),
                                     "%.2f" % (progress * 100))
    if progress >= 1:
        msg += " DONE\r\n"
    sys.stdout.write(msg)
    sys.stdout.flush()


def addSubs(context, subs, use_color=False):
    """Given a list of subs, adds them to the sequencer"""
    scene = context.scene
    try:

        for strip in scene.sequence_editor.sequences_all:
            strip.select = False
    except AttributeError:
        pass
    
    fps = scene.render.fps/scene.render.fps_base
    

    open_channel = getOpenChannel(scene)
    
    scene.subtitle_edit_channel = open_channel
    
    wm = context.window_manager
    wm.progress_begin(0, 100.0)
        
    for i in range(len(subs)):
        start_time = subs[i].start.to_millis() / 1000
        strip_start = start_time * fps
        
        end_time = subs[i].end.to_millis() / 1000
        strip_end = end_time * fps
        
        """if i > 0:
            previous_strip_end = subs[i - 1].strip_end
            while round(previous_strip_end) >= round(strip_start) + 1:
                strip_start += 1
        
        while round(strip_start) >= round(strip_end):
            strip_end += 1
        
        subs[i].strip_end = strip_end"""
        
        #if strip_start - strip_end <= 0.5:
        #    strip_end += 0.5
        
        #print(strip_start, strip_end)

        screen, area = find_sequencer_area()
        window = bpy.context.window
        location = {
            'window': window,
            'scene': scene,
            'area': area,
            'screen': screen,
            'region': area.regions[0]
            }

        bpy.ops.sequencer.effect_strip_add(
            location,
            frame_start=strip_start,
            frame_end=strip_end,
            channel=open_channel,
            type="TEXT")
        
        all_strips = list(sorted(
            scene.sequence_editor.sequences_all,
            key=lambda x: x.frame_start))
        
        text_strips = []
        for x in range(len(all_strips)):
            if (all_strips[x].type == "TEXT" and
                    all_strips[x].channel == open_channel):
                text_strips.append(all_strips[x])
                
        strip = text_strips[-1]
        try:
            strip.name = subs[i].name
        except AttributeError:
            strip.name = ""
        strip.name += subs[i].text
        strip.text = subs[i].text
        strip.font_size = scene.subtitle_font_size
        strip.use_shadow = True
        strip.select = True
        if use_color:
            strip.color[0] = scene.enhanced_subs_color[0]
            strip.color[1] = scene.enhanced_subs_color[1]
            strip.color[2] = scene.enhanced_subs_color[2]
            
        wm.progress_update((i / len(subs)) * 100)
        #update_progress("Adding Subs", i/len(subs))
    wm.progress_update(100)
    #update_progress("Adding Subs", 1)
