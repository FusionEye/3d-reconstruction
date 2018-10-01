# -*- coding: utf-8 -*-

import cv2
import numpy as np

# 点数据
# 空调右下角靠墙 1.46 0.46 -0.41
# 空调右下角外面 1.40 0.40 -0.00
# 空调右上角外面 1.99 0.67 -0.20
# 灯右下角 1.88 -0.42 0.49
# 灯右上角 1.90 -0.40 0.86

retval, rvec, tvec, inliers = cv2.solvePnPRansac
