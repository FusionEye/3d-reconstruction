# -*- coding: utf-8 -*-

import sys
from util.image_util import spliteRicohImages

if __name__ == '__main__':
    # 分割图片
    if sys.argv[1] == 'imageSplit':
        spliteRicohImages(sys.argv[2], sys.argv[3])
