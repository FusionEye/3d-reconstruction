import numpy as np
import pcl


cloud = pcl.load('/home/fred/Documents/task00/shanghai/pcd/2018-10-03-09-10-19.pcd')
detector = cloud.make_HarrisKeypoint3D()
keypoints = detector.compute()
print(keypoints)
pcl.save(keypoints, '/home/fred/Documents/task00/shanghai/pcd/2018-10-03-09-10-19_keypoints.pcd')
