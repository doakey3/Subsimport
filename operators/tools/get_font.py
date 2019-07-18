import bpy

import os.path

def get_font(font_path):

	if os.path.isfile(font_path):
		return bpy.data.fonts.load(font_path, check_existing=True)
	else:
		return None