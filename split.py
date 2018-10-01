# -*- coding: utf-8 -*-

from PIL import Image
import os
import glob

# 图片路径
images = glob.glob('images/pcd_on_color/*.JPG')

for fname in images:
    im = Image.open(fname)
    img_size = im.size
    print("图片宽度和高度分别是{}".format(img_size))

    x = img_size[0] / 2.0
    y = 0
    w = img_size[0] / 2.0
    h = img_size[1]
    box = (x, y, x + w, y + h)

    region = im.crop(box)
    region = region.transpose(Image.ROTATE_90)

    filepath = os.path.dirname(fname)
    filename = os.path.basename(fname)
    region.save(filepath + '/right/' + filename)
