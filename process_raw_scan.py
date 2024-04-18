#!/usr/bin/python

import os
from gimpfu import *

def process_raw_scan(_a, _b, image, drawable):
    _selection, x1, y1, x2, y2 = pdb.gimp_selection_bounds(image)
    width = x2 - x1
    height = y2 - y1

    original_filename = pdb.gimp_image_get_filename(image)
    filename = original_filename.replace('\\raw\\', '\\processed\\')
    directory = os.path.dirname(filename)


    # # Ensure the directory exists
    if not os.path.exists(directory):
        os.mkdir(directory)

    # TODO: Automatically create selection on edges of scanned image.
    # 1. Deskew the image
    # pdb.gimp_deskew_plugin(image, drawable, 0, 0, 0, 0, 0, run_mode=0)
    # 2. Try Colors > Curves method to remove edges.
    # 3. Use known dimensions of 750 x 1050 to crop area appropriately

    pdb.script_fu_selection_rounded_rectangle(image, drawable, 8, 0)
    pdb.gimp_selection_invert(image)
    pdb.gimp_drawable_edit_clear(drawable)

    pdb.gimp_selection_none(image) # This speeds up the subsequent crop
    pdb.gimp_image_crop(image, width, height, x1, y1)

    pdb.gimp_image_set_resolution(image, 300, 300)
    pdb.gimp_image_scale(image, 750, 1050)

    pdb.file_png_save_defaults(image, drawable, filename, filename)


register(
	"python_fu_process_raw_scan",
	"Take a raw scan and export a processed image",
	"Take a raw scan and export a processed image",
	"Steven Hamilton",
	"Steven Hamilton",
	"2024",
	"<Image>/Tools/Process raw scan",
	"RGB*, GRAY*",
	[
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],
	[],
	process_raw_scan
)

main()
