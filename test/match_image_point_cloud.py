# -*- coding: utf-8 -*-

import cv2
import numpy as np
import yaml, sys


def parseYamlFile(filename):
    f = open(filename)
    x = yaml.load(f)
    f.close()
    CameraIntrinsicData = np.array(x['camera_matrix']['data'], dtype=np.float32)
    DistortionCoefficients = np.array(x['distortion_coefficients']['data'], dtype=np.float32)
    return (CameraIntrinsicData.reshape(3, 3), DistortionCoefficients)


CalibrationDataFile = 'config/camera.yml'
OutputCloudFilename = './cloud.pcd'

CameraIntrinsicData, DistortionCoefficients = parseYamlFile(CalibrationDataFile)

# 获取点云照片标定点
with open('./input/imageAndPcd.txt', 'rb') as f:
    img_pcd_points = f.readlines()

real_points_len = 1
for i in range(1, len(img_pcd_points)):
    if len(img_pcd_points[i].split(',')) > 4:
        real_points_len = real_points_len + 1

print(real_points_len)

real_points_num = real_points_len - 1
# 点云数据
pts_obj = np.zeros((real_points_num, 3), dtype=np.float32)
# 照片数据
pts_img = np.zeros((real_points_num, 2), dtype=np.float32)

for i in range(1, real_points_len):
    pos_list = img_pcd_points[i].split(',')

    pts_obj[i - 1] = (float(pos_list[0].strip()), float(pos_list[1].strip()), float(pos_list[2].strip()))
    pts_img[i - 1] = (float(pos_list[3].strip()), float(pos_list[4].strip()))

print(pts_img)
print(pts_obj)

pts_img = np.ascontiguousarray(pts_img[:, :2]).reshape((real_points_num, 1, 2))

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
print("pnp结果： ")
print(retval)

for pt_obj in pts_obj:
    (end_point_2d, jacobian) = cv2.projectPoints(np.array([(pt_obj[0], pt_obj[1], pt_obj[2])]), rvec, tvec,
                                                 cameraMatrix, DistortionCoefficients)
    print(end_point_2d)
