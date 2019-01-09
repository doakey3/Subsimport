.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=QA2T7WG47UTCL

.. image:: http://i.imgur.com/KxRENJr.png

.. contents::

About
=====

Subs import is an addon for Blender_ that allows users to create and
edit subtitles for movies or music. The keyboard shortcuts and automatic
syllable separation tools make it a very fast tool.

.. image:: http://i.imgur.com/CLDXWRd.gif

.. _Blender: https://www.blender.org/

Installation
============

1. Download the repository.
2. Open Blender.
3. Go to File > User Preferences > Addons
4. Click "Install From File" and navigate to the downloaded zip file and
   install.
5. Check the box next to "Subsimport"

Use the correct release for your Blender version. Add-ons for Blender 2.80 and above will not work for Blender 2.79

Usage
=====

A `video tutorial`_ is available.

The user interface is located to the right side of the video sequencer.

.. image:: http://i.imgur.com/nNchW3Z.png

.. _video tutorial: https://www.youtube.com/watch?v=R-jis3S6dxU

Subtitle Edit Channel
---------------------

.. image:: http://i.imgur.com/fgXDH1C.png

The sequencer channel where The addon will have effect. Keyboard
shortcuts, duration changing, exporting, syllabifying, splitting, and
combining subtitles all depends on this value.

Importing, splitting, and combining subtitles will automatically adjust
the subtitle edit channel.

Subtitle Font Size
------------------

.. image:: http://i.imgur.com/PNFAW5x.png

The font size that will be applied to imported strips. You may change
this value and refresh using the button to the right. (Changes only
applied to the Subtitle Edit Channel)

.. image:: http://i.imgur.com/sC6xx0n.gif

Importing
---------

.. image:: http://i.imgur.com/x93jx4s.png

.. image:: http://i.imgur.com/8MM08X5.gif

3 filetypes may be imported with this addon: .txt, .lrc, and .srt files.

.txt files do not contain any timing info. The text is imported so that
each line of the text file becomes a strip in the sequencer. It is
recommended that each line of text be no longer than **62** characters
long.

.lrc files are used with programs like MiniLyrics_ for displaying
subtitles with music.

.. _MiniLyrics: http://www.crintsoft.com/

.srt files are the standard subtitle filetype for movies. They work well
with the VLC_ media player.

.. _VLC: https://www.videolan.org/vlc/index.html

Subsimport also supports "Enhanced" .srt and .lrc files. These are
special subtitles that highlight parts of the subtitles at a time.

On import, AV sync, scrubbing, and frame drop will be enabled.

It is recommended that if you're making lyrics for songs that you
increase the scene FPS to 100 or even 1000 frames per second before
importing. The reason is that .srt files support time data down to the
millisecond, but strips must conform to the scene's FPS value. If a low
FPS is used, then the minimum timing difference will be limited by the
scene FPS.

Furthermore, if you attempt to import strips and one or more strips has
a duration that is less than 1 / the scene fps, you will create an
error.

Subimport does not allow any subtitles to overlap times and will
automatically remove overlaps on import.

.. _Bligify's: https://github.com/doakey3/Bligify

Dur x 2 and Dur / 2
-------------------

.. image:: http://i.imgur.com/BmEDQiH.png

.. image:: http://i.imgur.com/ZywhLfB.gif

Doubles or halfs the duration of the strips in the
"Subtitle Edit Channel".

These buttons allow you to edit subtitles with a song playing at 50%
speed, then convert the subtitles to normal speed.

When making subtitles for music, I like to use Audacity_ to slow the
music down by 50% and export it as a .wav file. I then use this in
Blender for matching the lyrics to the song.

.. _Audacity: http://www.audacityteam.org/

Exporting
---------

.. image:: http://i.imgur.com/MzNk9S6.png

Export the subtitles from the "Subtitle Edit Channel" as either .lrc
or .srt file.

Syllabify
---------

.. image:: http://i.imgur.com/sjKYWt8.png

After subtitles have been imported, you can separate words by syllables.
Before splitting the syllables, you should create a syllabification
dictionary for your subtitles that defines how each word should be
broken up.

Subsimport has a dictionary of words and an algorithm for splitting
words. Both are enabled by default. The algorithm's accuracy depends
on which language is set.

After clicking the "Syllabify" button, you'll create a .txt file
containing all of the words of the song. Subsimport will try to split
them up into separate syllables. You should read through the .txt file
and make any corrections as necessary before you split your words.

After syllabifying words, you may save your dictionary to the default
dictionary that Subsimport uses. This way, any words you may have needed
to edit will be correctly syllabified the next time Subsimport
encounters them.

Split
-----

.. image:: http://i.imgur.com/XKJfMb3.png

.. image:: http://i.imgur.com/9gAon9U.gif

After defining how words should be separated, you can split them apart
and create individually colored text strips that will highlight
sequentially as your audio plays. You can set the timing of each
syllable in the song.

Text strip color can be changed with the highlight property and the
refresh button to the right.

Combine
-------

.. image:: http://i.imgur.com/4LJ3fQe.png

.. image:: http://i.imgur.com/5lUFAt8.gif

After synchronizing the syllables to the music, you can recombine
the strips into enhanced strips prior to exporting the subtitles.

The method used for combining the strips (ESRT or ELRC) depends on
what kind of subtitles you would like to export.

Keyboard Shortcuts
------------------

Make sure the "Subtitle Edit Channel" property is set to the channel
where your subtitle strips have been imported.

Note that splitted strips are set to not respond to these 4 shortcuts
if it means going outside the bounds of their base strips.

:D:
    Set the start of a text strip.

:F:
    Set the end of a text strip.

:S:
    (like pressing F, then D rapidly)

:W:
    (like pressing D, then F rapidly)

.. image:: http://i.imgur.com/D38fvvU.gif

:Z:
    Send top strips to the end of the base strip. Useful for resetting
    the position of syllabified lyrics.

    You must be within the start and end points of a base strip and the
    "Subtitle Edit Channel" must be set to the top strips channel for
    this to work.

.. image:: http://i.imgur.com/XoxELtD.gif

:Ctrl + Shift + Right:
    Select all strips in the Subtitle Edit Channel to the right of the
    current time indicator.

:Ctrl + Shift + Left:
    Select all strips in the Subtitle Edit Channel to the left of the
    current time indicator

Contributing
============

Pull requests, feature requests, donations, and example song .srt files
are welcome! Also, adding syllabified words to the default dictionary is
encouraged.
