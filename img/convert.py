#! /usr/bin/env python

import sys

from PIL import Image

file_name = sys.argv[1]
im = Image.open(file_name)

im = im.resize((512, 512), Image.NEAREST)
im = im.convert("1").transpose(Image.FLIP_TOP_BOTTOM)

im.save("{}.bmp".format(file_name.split(".")[0]))
