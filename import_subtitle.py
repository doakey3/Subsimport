import bpy
from bpy_extras.io_utils import ImportHelper
import datetime


class ImportSubtitle(bpy.types.Operator, ImportHelper):
    bl_label = 'Import Subtitle'
    bl_idname = 'sequencerextra.import_subtitle'
    bl_description = ''.join(['Import subtitles as text strips.'])

    filter_glob = bpy.props.StringProperty(
            default="*.srt;*.lrc;*.txt",
            options={'HIDDEN'},
            maxlen=255,
            )

    def execute(self, context):
        scene = context.scene
        path = self.filepath.replace('\\', '/')

        if path.endswith('.txt'):
            segments = parseTXT(path, scene)
        elif path.endswith('.srt'):
            segments = parseSRT(path)
        elif path.endswith('.lrc'):
            segments = parseLRC(path)
        addSegments(scene, segments)

        return {'FINISHED'}


class Segment():
    """Holds the information in an SRT segment"""
    def __init__(self):
        self.segment_number = 0
        self.start_time = 0.0
        self.end_time = 0.0
        self.topline = ''
        self.bottomline = ''


def parseTXT(path, scene):
    """Read a .txt file, split lines where necessary"""
    f = open(path, 'r')
    lines = f.readlines()
    f.close()

    max_characters_per_line = 37

    current_step = scene.frame_start
    segments = []
    fps = scene.render.fps/scene.render.fps_base
    for i in range(len(lines)):
        segments.append(Segment())
        segments[-1].segment_number = i + 1
        line = lines[i].rstrip()
        length = len(line)
        if length > max_characters_per_line:
            words = line.split(' ')
            line1, line2 = findEvenSplit(words)
            segments[-1].topline = line1
            segments[-1].bottomline = line2
        else:
            segments[-1].bottomline = line
        segments[-1].start_time = current_step / fps + (1.000000001/fps)
        current_step += fps
        segments[-1].end_time = current_step / fps

    return segments


def parseSRT(file):
    """
    Open an srt file and convert its sections into a list of segments
    """
    f = open(file, 'r')
    lines = f.readlines()
    f.close()

    separated = []
    temp = []
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip()
        if not lines[i] == '':
            temp.append(lines[i])
        else:
            separated.append(temp)
            temp = []
    separated.append(temp)

    for s in separated:
        if s == []:
            separated.pop(separated.index([]))

    segments = []
    for i in range(len(separated)):
        seg = i + 1
        try:
            try:
                start = convert2Seconds(
                    separated[i][1].split(' --> ')[0])
            except ValueError:
                start = convert2Seconds('23:59:59,999')
            try:
                end = convert2Seconds(
                    separated[i][1].split(' --> ')[1])
            except ValueError:
                end = convert2Seconds('23:59:59,999')
            try:
                line_1 = separated[i][2]
            except IndexError:
                line_1 = ''
            if len(separated[i]) > 3:
                line_2 = separated[i][3]
            segments.append(Segment())
            segments[i].segment_number = seg
            segments[i].start_time = start
            segments[i].end_time = end

            if len(separated[i]) > 3:
                segments[i].topline = line_1
                segments[i].bottomline = line_2
            else:
                segments[i].bottomline = line_1
        except IndexError:
            pass
    return segments


class LRC_Segment():
    """
    A class to hold the segments of an lrc file
    """
    def __init__(self):
        self.time = 0.0
        self.line = ''


def parseLRC(file):
    """
    Open an lrc file and convert it's sections into srt segments
    """
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    lrc_segs = []
    max_characters_per_line = 37
    
    for i in range(len(lines)):
        try:
            given_time = lines[i].split(']')[0][1::]
            t = datetime.datetime.strptime(given_time, "%M:%S.%f")
            words = lines[i].rstrip().split(']')
            for x in range(len(words)):
                if words[x].startswith('['):
                    no_period = words[x][1::].replace('.', ',')
                    words[x] = convert2Seconds('00:' + no_period)
                    lrc_segs.append(LRC_Segment())
                    lrc_segs[-1].time = words[x]
                    lrc_segs[-1].line = words[-1]
        except ValueError:
            # The line doesn't start with [mm:ss.xx] format, skip it
            pass
    lrc_segs.sort(key=lambda x: x.time)

    srt_segments = []
    for i in range(len(lrc_segs)):
        if not lrc_segs[i].line.lstrip() == '':
            srt_segments.append(Segment())
            srt_segments[-1].segment_number = i + 1
            srt_segments[-1].start_time = lrc_segs[i].time
            if i < len(lrc_segs) - 1:
                srt_segments[-1].end_time = lrc_segs[i+1].time
            else:
                end = srt_segments[-1].start_time + 10
                srt_segments[-1].end_time = end
            if len(lrc_segs[i].line) > max_characters_per_line:
                split = lrc_segs[i].line.split(' ')
                line1, line2 = find_even_split(split)
                srt_segments[-1].topline = line1
                srt_segments[-1].bottomline = line2
            else:
                srt_segments[-1].bottomline = lrc_segs[i].line

    return srt_segments


def findEvenSplit(word_list):
    """
    Given a list of words, attempts to split the word list
    into 2 evenly sized strings
    """
    differences = []
    for i in range(len(word_list)):
        group1 = ' '.join(word_list[0:i+1])
        group2 = ' '.join(word_list[i+1::])
        differences.append(abs(len(group1) - len(group2)))
    index = differences.index(min(differences))
    for i in range(len(word_list)):
        if i == index:
            group1 = ' '.join(word_list[0:i+1])
            group2 = ' '.join(word_list[i+1::])
    return group1, group2


def convert2Seconds(timecode):
    """convert a timecode '00:00:00,000' to seconds"""
    t = datetime.datetime.strptime(timecode, "%H:%M:%S,%f")
    seconds = (60 * t.minute) + (3600 * t.hour) + t.second
    fraction = t.microsecond/1000000
    combo = seconds + fraction
    return combo


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


def addSegments(scene, segments):
    """Given a list of segments, adds them to the sequencer"""
    fps = scene.render.fps/scene.render.fps_base
    open_channel = getOpenChannel(scene)
    try:

        for strip in scene.sequence_editor.sequences_all:
            strip.select = False
    except AttributeError:
        pass
    for i in range(len(segments)):
        if not segments[i].topline == '':
            line = segments[i].topline + ' \n' + segments[i].bottomline
        else:
            line = segments[i].bottomline
        segment_start = segments[i].start_time * fps
        segment_end = segments[i].end_time * fps

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
            frame_start=segment_start,
            frame_end=segment_end,
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
        strip.name = line
        strip.text = line
        strip.font_size = scene.subtitle_font_size
        strip.use_shadow = True
        strip.select = True
