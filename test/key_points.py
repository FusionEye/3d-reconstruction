import numpy as np
import pcl


cloud = pcl.load('../input/pointCloud.pcd')
detector = cloud.make_HarrisKeypoint3D()
keypoints = detector.compute()
print(keypoints)
pcl.save(keypoints, '../input/pointCloud_keypoints.pcd')
