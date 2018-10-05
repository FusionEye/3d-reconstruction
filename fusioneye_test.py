# -*- coding: utf-8 -*-

import sys
from util.image_util import spliteRicohImages


def test_split_image():
    spliteRicohImages('test/*.JPG', 'output/test')


if __name__ == '__main__':
    if sys.argv[1] == 'imageSplit':
        test_split_image()
