# -*- coding: utf-8 -*-

import math
import numpy as np
import pcl


sphericalFilePath = '/home/fred/Documents/task00/chengdu/pcd_origin_data_txt/data2.txt'
cloudFilename = '/home/fred/Documents/task00/chengdu/pcd/data2.pcd'

with open(sphericalFilePath, 'rb') as f:
    lines = f.readlines()

pointcloud = []
for i in range(0, len(lines)):
    # print i
    sphericalData = lines[i].split('\t')
    # print sphericalData
    if sphericalData[0] != '\r\n':
        r = float(sphericalData[2].replace('\r\r\n', ''))

        if r > 0:
            r = r * 100

            theta = float(sphericalData[1])
            if theta <= 90:
                theta = 90.0 - theta
            if theta > 90 and theta <= 180:
                theta = theta - 90
            if theta > 180 and theta <= 270:
                theta = theta - 90
            if theta > 270:
                theta = (360 - theta) + 90
            theta = math.radians(theta)
            phi = math.radians(float(sphericalData[0]))

            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)

            if theta > 180:
                print 'theta: {0}, phi: {1}, r: {2}'.format(theta, phi, r)
                print 'x: {0}, y: {1}, z: {2}'.format(x, y, z)

            point = np.array([x, y, z], dtype=np.float32)
            pointcloud.append(point)

print len(pointcloud)
pointcloud = np.array(pointcloud, dtype=np.float32)
cloud = pcl.PointCloud()
cloud.from_array(pointcloud)
pcl.save(cloud, cloudFilename, format='pcd')

