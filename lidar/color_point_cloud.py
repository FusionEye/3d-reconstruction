# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np
from util import read_yaml
from PIL import Image


def color_pcd(OriginCloudFilename, RGBFileNamePath, OutputCloudFilename):
    CalibrationDataFile = 'config/camera.yml'
    CameraIntrinsicData, DistortionCoefficients = read_yaml.parseYamlFile(CalibrationDataFile)

    # 点云数据
    pts_obj = np.array([
        (1.265592, 1.910337, 0.082096),
        (1.248772, 1.920148, 0.682424),
        (-0.262132, 3.050739, 1.336622),
        (1.486778, 0.630351, 1.128295),
        (1.161838, 3.230030, 1.407530),
        (0.919682, -1.172692, 1.557984)
    ], dtype=np.float32)

    # 照片数据
    pts_img = np.array([
        (1040, 1308),
        (1020, 1144),
        (832, 1180),
        (1340, 964),
        (804, 1056),
        (2048, 788)
    ], dtype=np.float32)
    pts_img = np.ascontiguousarray(pts_img[:, :2]).reshape((6, 1, 2))

    # 畸变参数
    DistortionCoefficients = np.zeros((4, 1))

    cameraMatrix = np.matrix(CameraIntrinsicData)
    rvec = None
    tvec = None
    inliers = None
    retval, rvec, tvec, inliers = cv2.solvePnPRansac(pts_obj, pts_img, cameraMatrix, DistortionCoefficients,
                                                     useExtrinsicGuess=False, iterationsCount=100, reprojectionError=1)

    print("旋转矩阵：\n{0}\n平移矩阵：\n{1}\ninliers:\n{2}\npnp结果:\n{3}".format(rvec, tvec, inliers, retval))

    # 获取点云数据
    with open(OriginCloudFilename, 'rb') as f:
        lines = f.readlines()

    totalLine = len(lines)
    # totalLine = 20000

    lines[2] = lines[2].split('\n')[0] + ' rgb\n'
    lines[3] = lines[3].split('\n')[0] + ' 4\n'
    lines[4] = lines[4].split('\n')[0] + ' I\n'
    lines[5] = lines[5].split('\n')[0] + ' 1\n'
    lines[6] = 'WIDTH ' + str(totalLine - 11) + '\n'
    lines[9] = 'POINTS ' + str(totalLine - 11) + '\n'

    print('pcd lines: {0}'.format(totalLine))

    # 加载图像
    img_src = Image.open(RGBFileNamePath)
    # img_src = img_src.convert('RGBA')
    pix = img_src.load()

    # 遍历点云
    prev_progress = 0.00
    for i in range(11, totalLine):
        p1 = float(lines[i].split(' ')[0])
        p2 = float(lines[i].split(' ')[1])
        p3 = float(lines[i].split(' ')[2].replace('\n', ''))
        # 获取3d对应的2d坐标
        (end_point_2d, jacobian) = cv2.projectPoints(np.array([(p1, p2, p3)]), rvec, tvec, cameraMatrix,
                                                     DistortionCoefficients)

        # 显示进度
        current_progress = ((i + 1.0) * 100 / totalLine)
        if current_progress >= (prev_progress + 10):
            prev_progress = current_progress
            print('%s, 进度： %.2f%%' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), current_progress))

        # 获得2d坐标对应的颜色
        x = end_point_2d[0][0][0]
        y = end_point_2d[0][0][1]
        if x > 5375:
            x = 5375
        if x <= 0:
            x = 0
        if y > 2687:
            y = 2687
        if y <= 0:
            y = 0
        r, g, b = pix[x, y]
        lines[i] = lines[i].split('\n')[0] + ' ' + str((r << 16) | (g << 8) | b) + '\n'

    with open(OutputCloudFilename, 'wb') as fw:
        fw.writelines(lines[:totalLine])
