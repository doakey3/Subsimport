import bpy

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

def addSubs(scene, subs):
    """Given a list of subs, adds them to the sequencer"""
    try:

        for strip in scene.sequence_editor.sequences_all:
            strip.select = False
    except AttributeError:
        pass
    
    fps = scene.render.fps/scene.render.fps_base
    open_channel = getOpenChannel(scene)
    
    for i in range(len(subs)):
        hrs = subs[i].start.hours
        mins = subs[i].start.minutes
        secs = subs[i].start.seconds
        millis = subs[i].start.milliseconds
        start_time = sum([(hrs * 3600), 
                          (mins * 60), secs, (millis / 1000)])
                          
        strip_start = start_time * fps
        
        hrs = subs[i].end.hours
        mins = subs[i].end.minutes
        secs = subs[i].end.seconds
        millis = subs[i].end.milliseconds
        end_time = sum([(hrs * 3600), 
                          (mins * 60), secs, (millis / 1000)])
                          
        strip_end = end_time * fps

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
        strip.name = subs[i].text
        strip.text = subs[i].text
        strip.font_size = scene.subtitle_font_size
        strip.use_shadow = True
        strip.select = True  
