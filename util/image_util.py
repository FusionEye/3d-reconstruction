# -*- coding: utf-8 -*-

from PIL import Image
import os
import glob


def spliteRicohImages(inputPath, outPath):
    # 图片路径
    images = glob.glob(inputPath)

    for fname in images:
        im = Image.open(fname)
        img_size = im.size
        print("图片宽度和高度分别是{0}".format(img_size))

        # 右边
        x = img_size[0] / 2.0
        y = 0
        w = img_size[0] / 2.0
        h = img_size[1]
        box = (x, y, x + w, y + h)

        region = im.crop(box)
        region = region.transpose(Image.ROTATE_90)

        # 创建目录
        right_folder = os.path.exists(outPath + '/right')
        if not right_folder:
            os.makedirs(outPath + '/right')

        filename = os.path.basename(fname)
        region.save(outPath + '/right/' + filename)

        # 左边
        x = 0
        y = 0
        w = img_size[0] / 2.0
        h = img_size[1]
        box = (x, y, x + w, y + h)

        region = im.crop(box)
        region = region.transpose(Image.ROTATE_270)

        # 创建目录
        right_folder = os.path.exists(outPath + '/left')
        if not right_folder:
            os.makedirs(outPath + '/left')

        filename = os.path.basename(fname)
        region.save(outPath + '/left/' + filename)
