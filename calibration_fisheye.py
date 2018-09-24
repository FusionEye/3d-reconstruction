# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
import glob

assert cv2.__version__[0] == '3'


def get_K_and_D(checkerboard, imgsPath):
    CHECKERBOARD = checkerboard

    # 迭代终止条件
    # cv2.TERM_CRITERIA_EPS 精度满足epsilon时，终止迭代
    # 24 最大迭代次数
    # 0.1 精度
    subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 24, 0.1)
    calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW

    # 初始化角点数组
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

    # 图片角点存储
    _img_shape = None
    objpoints = []
    imgpoints = []

    # 读取图片
    images = glob.glob(imgsPath)
    for fname in images:
        img = cv2.imread(fname)
        # 判断图片大小是否一致
        if _img_shape == None:
            _img_shape = img.shape[:2]
        else:
            assert _img_shape == img.shape[:2], "所有图片必须要有一样的尺寸"

        # 转换灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 找到图片棋盘的角点
        # CALIB_CB_ADAPTIVE_THRESH 自适应阀值
        # CALIB_CB_FAST_CHECK 快速检查
        # CALIB_CB_NORMALIZE_IMAGE 均衡图像亮度
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
        if ret == True:
            objpoints.append(objp)
            # 角点坐标二次查找
            corners2 = cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), subpix_criteria)
            # 记录角点坐标
            imgpoints.append(corners)

            # 给图片画上角点
            img = cv2.drawChessboardCorners(img, (checkerboard[0], checkerboard[1]), corners2, ret)
            # cv2.imwrite('images/201809162257_with_button/out/' + os.path.basename(fname), img)

    N_OK = len(objpoints)
    K = np.zeros((3, 3))
    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)]

    # 鱼眼标定
    # InputArrayOfArrays objectPoints
    # InputArrayOfArrays imagePoints
    # const Size & image_size
    # InputOutputArray K 内参
    # InputOutputArray D 矫正参数
    # OutputArrayOfArrays rvecs 旋转矩阵
    # OutputArrayOfArrays tvecs 平移矩阵
    # int flags = 0,
    # TermCriteria criteria = TermCriteria(TermCriteria::COUNT + TermCriteria::EPS, 100, DBL_EPSILON)
    rms, _, _, _, _ = cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        gray.shape[::-1],
        K,
        D,
        rvecs,
        tvecs,
        calibration_flags,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 24, 1e-6)
    )
    DIM = _img_shape[::-1]
    print("Found " + str(N_OK) + " valid images for calibration")
    print("DIM=" + str(_img_shape[::-1]))
    print("K=np.array(" + str(K.tolist()) + ")")
    print("D=np.array(" + str(D.tolist()) + ")")

    return DIM, K, D


# 计算内参和矫正系数
'''
# checkerboard： 棋盘格的格点数目
# imgsPath: 存放鱼眼图片的路径
'''
# get_K_and_D((6, 8), 'images/out_no_button/*.JPG')
get_K_and_D((6, 8), 'images/201809162223_no_button/right/*.JPG')
