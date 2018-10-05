# -*- coding: utf-8 -*-

import cv2
import numpy as np
from util import read_yaml

CalibrationDataFile = 'config/camera.yml'
OriginCloudFilename = '/home/fred/git/3d-reconstruction/pcd/home/cloud.pcd'
RGBFileNamePath = '/home/fred/git/3d-reconstruction/images/pcd_on_color/20181001161152.JPG'
OutputCloudFilename = './cloud.pcd'

CameraIntrinsicData, DistortionCoefficients = read_yaml.parseYamlFile(CalibrationDataFile)

# 点云数据
# 螂头左下角
# 螂头夹角
# 空调右下角靠墙
# 灯右下角
# 灯右上角
# 房间右上角
pts_obj = np.array([
    (0.23, -0.50, -0.57),
    (0.28, -0.62, -0.52),
    (0.98, 0.63, -0.67),
    (1.43, -0.28, 0.23),
    (1.44, -0.25, 0.61),
    (1.42, -1.86, -0.64)
], dtype=np.float32)

# 照片数据
# 螂头左下角
# 螂头夹角
# 空调右下角靠墙
# 灯右下角
# 灯右上角
# 房间右上角
pts_img = np.array([
    (2154, 1284),
    (2211, 1220),
    (1274, 886),
    (1842, 294),
    (1824, 147),
    (2301, 807)
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

print("旋转矩阵： ")
print(rvec)
print("平移矩阵： ")
print(tvec)
print(inliers)
print("pnp结果： ")
print(retval)

for pt_obj in pts_obj:
    (end_point_2d, jacobian) = cv2.projectPoints(np.array([(pt_obj[0], pt_obj[1], pt_obj[2])]), rvec, tvec,
                                                 cameraMatrix, DistortionCoefficients)
    print(end_point_2d)
