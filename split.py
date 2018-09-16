from PIL import Image
import os
import glob

# 图片路径
images = glob.glob('images/201809162257_with_button/origin/*.JPG')

for fname in images:
    im = Image.open(fname)
    img_size = im.size
    print("图片宽度和高度分别是{}".format(img_size))

    x = 0
    y = 0
    w = img_size[0] / 2.0
    h = img_size[1]
    box = (x, y, x + w, y + h)

    region = im.crop(box)
    region = region.transpose(Image.ROTATE_270)

    filepath = os.path.dirname(fname)
    filename = os.path.basename(fname)
    print(filepath + '/../left/' + filename)
    region.save(filepath + '/../left/' + filename)
