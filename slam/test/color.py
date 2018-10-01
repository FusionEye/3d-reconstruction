# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pcl
import readyaml
from PIL import Image

CalibrationDataFile = '../camera.yml'
OriginCloudFilename = '/home/fred/git/3d-reconstruction/pcd/home/cloud.pcd'
RGBFileNamePath = '/home/fred/git/3d-reconstruction/images/pcd_on_color/20181001161152.JPG'
OutputCloudFilename = './cloud.pcd'

CameraIntrinsicData, DistortionCoefficients = readyaml.parseYamlFile(CalibrationDataFile)

# 点云数据
# 空调右下角靠墙 1.46 0.46 -0.41
# 空调右下角外面 1.40 0.40 -0.00
# 空调右上角外面 1.99 0.67 -0.20
# 灯右下角 1.88 -0.42 0.49
# 灯右上角 1.90 -0.40 0.86
pts_obj = np.array([
    (1.46, 0.46, -0.41),
    (1.40, 0.40, -0.00),
    (1.99, 0.40, -0.20),
    (1.88, -0.42, 0.49),
    (1.90, -0.40, 0.86)

], dtype=np.float32)

# 照片数据
# 空调右下角靠墙
# 空调右下角外面
# 空调右上角外面
# 灯右下角
# 灯右上角
pts_img = np.array([
    (1284, 894),
    (1239, 774),
    (1251, 693),
    (1836, 291),
    (1842, 153)
], dtype=np.float32)
pts_img = np.ascontiguousarray(pts_img[:, :2]).reshape((5, 1, 2))

# 畸变参数
DistortionCoefficients = np.zeros((4, 1))

cameraMatrix = np.matrix(CameraIntrinsicData)
rvec = None
tvec = None
inliers = None
retval, rvec, tvec, inliers = cv2.solvePnPRansac(pts_obj, pts_img, cameraMatrix, DistortionCoefficients,
                                                 useExtrinsicGuess=False, iterationsCount=100, reprojectionError=1)

print "旋转矩阵： "
print(rvec)
print "平移矩阵： "
print(tvec)
print(inliers)
print "pnp结果： "
print(retval)

# (end_point_2d, jacobian) = cv2.projectPoints(np.array([(1.90, -0.40, 0.86)]), rvec, tvec, cameraMatrix, DistortionCoefficients)

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

print('pcd lines: ' + str(len(lines)))

# 加载图像
img_src = Image.open(RGBFileNamePath)
# img_src = img_src.convert('RGBA')
pix = img_src.load()

# 遍历点云
for i in range(11, totalLine):
    p1 = float(lines[i].split(' ')[0])
    p2 = float(lines[i].split(' ')[1])
    p3 = float(lines[i].split(' ')[2].replace('\n', ''))
    # 获取3d对应的2d坐标
    (end_point_2d, jacobian) = cv2.projectPoints(np.array([(p1, p2, p3)]), rvec, tvec, cameraMatrix,
                                                 DistortionCoefficients)
    print end_point_2d
    # 获得2d坐标对应的颜色
    x = end_point_2d[0][0][0]
    y = end_point_2d[0][0][1]
    if x > 2895:
        x = 2895
    if x <= 0:
        x = 0
    if y > 2895:
        y = 2895
    if y <= 0:
        y = 0
    print x
    print y
    r, g, b = pix[x, y]
    print r
    print g
    print b
    lines[i] = lines[i].split('\n')[0] + ' ' + str((r << 16) | (g << 8) | b) + '\n'

with open(OutputCloudFilename, 'wb') as fw:
    fw.writelines(lines[:totalLine])
