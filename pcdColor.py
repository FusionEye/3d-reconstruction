# -*- coding: utf-8 -*-

import cv2
import pcl
import numpy as np
import pcl.pcl_visualization


class CameraIntrinsicParameters(object):
    """docstring for CameraIntrinsicParameters"""

    def __init__(self, cx, cy, fx, fy, scale):
        super(CameraIntrinsicParameters, self).__init__()
        self.cx = cx
        self.cy = cy
        self.fx = fx
        self.fy = fy
        self.scale = scale


# 点云展示
def pcdViewer(filename):
    cloud = pcl.load_XYZRGB(filename)
    print("cloud points : " + str(cloud.size))
    visual = pcl.pcl_visualization.CloudViewing()

    # PointXYZ
    # visual.ShowMonochromeCloud(cloud)

    visual.ShowColorCloud(cloud, b'cloud')

    flag = True
    while flag:
        flag != visual.WasStopped()
    end


# 图片转点云
def point2dTo3d(n, m, d, camera):
    z = float(d) / camera.scale
    x = (n - camera.cx) * z / camera.fx
    y = (m - camera.cy) * z / camera.fy
    point = np.array([x, y, z], dtype=np.float32)
    return point


# 点云上色
def AddColorToPCDFile(filename):
    with open(filename, 'rb') as f:
        lines = f.readlines()
    lines[2] = lines[2].split('\n')[0] + ' rgb\n'
    lines[3] = lines[3].split('\n')[0] + ' 4\n'
    lines[4] = lines[4].split('\n')[0] + ' I\n'
    lines[5] = lines[5].split('\n')[0] + ' 1\n'
    with open(filename, 'wb') as fw:
        fw.writelines(lines)


# 灰度图转pcd
def imageToPointCloud(RGBFilename, DepthFilename, CloudFilename, camera):
    rgb = cv2.imread(RGBFilename)
    depth = cv2.imread(DepthFilename, cv2.COLOR_BGR2GRAY)
    # ROS中rqt保存的深度摄像头的图片是rgb格式，需要转换成单通道灰度格式
    if len(depth[0][0]) == 3:
        depth = cv2.cvtColor(depth, cv2.COLOR_BGR2GRAY)

    cloud = pcl.PointCloud()
    rows = len(depth)
    cols = len(depth[0])
    pointcloud = []
    colors = []
    for m in range(0, rows):
        for n in range(0, cols):
            d = depth[m][n]
            if d == 0:
                pass
            else:
                point = point2dTo3d(n, m, d, camera)
                pointcloud.append(point)
                b = rgb[m][n][0]
                g = rgb[m][n][1]
                r = rgb[m][n][2]
                color = (r << 16) | (g << 8) | b
                colors.append(int(color))
    pointcloud = np.array(pointcloud, dtype=np.float32)
    cloud.from_array(pointcloud)
    pcl.save(cloud, CloudFilename, format='pcd')


pcdViewer('./pcd/cloud.pcd')
camera = CameraIntrinsicParameters(3.6927587384670619e+02, 2.0049685183455608e+02,
                                   6.0782982475382448e+02, 6.0782982475382448e+02, 1000.0)
# imageToPointCloud('slam/rgb.png', 'slam/depth.png', 'pcd/cloud.pcd', camera)
