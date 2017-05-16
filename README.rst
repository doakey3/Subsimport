.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=QA2T7WG47UTCL

.. image:: http://i.imgur.com/8XoKdam.png
    :align: center

.. contents::

Installation
============

1. Download the repository. 
2. Open Blender. 
3. Go to File > User Preferences > Addons
4. Click "Install From File" and navigate to the downloaded release
5. Check the box next to "Subsimport"

You will see the user interface on the right side of the sequencer.

Usage
=====

The user interface is located to the right side of the video sequencer.

.. image:: http://i.imgur.com/he5yfp4.png
    :align: left

.. image:: http://i.imgur.com/0vIHtfE.png
    :align: right

Set the font size of the text that will be imported. Click the import
button and navigate to the .txt/.lrc/.srt file you would like to import
and click import.

Ensure the subtitle edit channel is set to the channel where your text
strips have been imported.

Keyboard Shortcuts
------------------

Make sure the "Subtitle Edit Channel" property is set to the channel 
where your subtitle strips have been imported.

Note that syllabified strips are set to not respond to these 4 shortcuts 
if it means going outside the bounds of their base strips.

:D: 
    Set the start of a text strip.
    
:F: 
    Set the end of a text strip.
    
:S: 
    (like pressing F, then D rapidly)

:W: 
    (like pressing D, then F rapidly)

.. image:: http://i.imgur.com/t9ahMhV.gif

:Z: 
    Send top strips to the end of the base strip. Useful for resetting
    the position of syllabified lyrics. 
    
    You must be within the start and end points of a base strip and the 
    "Subtitle Edit Channel" must be set to the top strips channel for 
    this to work.
    
.. image:: http://i.imgur.com/JhGzLmo.gif

Use the Split words function to split words so they can be timed 
individually.

Use the Combine words function to recombine highlighted words into 
sentences. (for making enhanced SRT). For now, combining only works as
enhanced SRT, but other options are coming.

The Export LRC function does not work at this point, but coming soon.

