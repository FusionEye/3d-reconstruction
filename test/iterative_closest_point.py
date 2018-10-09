# -*- coding: utf-8 -*-
# How to use iterative closest point
# http://pointclouds.org/documentation/tutorials/iterative_closest_point.php#iterative-closest-point

import pcl
import numpy as np


cloud_in = pcl.load('/home/fred/Documents/task00/shanghai/pcd/20181007.pcd')
cloud_out = pcl.load('/home/fred/Documents/task00/shanghai/pcd/2018100800.pcd')

print('Transformed ' + str(cloud_in.size) + ' data points:')

icp = cloud_in.make_IterativeClosestPoint()
converged, transf, estimate, fitness = icp.icp(cloud_in, cloud_out)

print('has converged:' + str(converged) + ' score: ' + str(fitness))
print(str(transf))

pointcloud = []
for item in cloud_in:
    a = list(item)
    a.append(1)
    a = np.matrix(a)
    a = a.reshape((-1, 1))
    temp = transf * a
    temp = temp.reshape((1, -1))
    temp = np.array(temp)
    temp = list(temp[0])
    pointcloud.append(temp[0:3])

cloud = pcl.PointCloud()
cloud.from_array(np.array(pointcloud, dtype=np.float32))
pcl.save(cloud, '/home/fred/Documents/task00/shanghai/pcd/20181007_trans.pcd')
