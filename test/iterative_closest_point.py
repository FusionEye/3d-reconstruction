# -*- coding: utf-8 -*-
# How to use iterative closest point
# http://pointclouds.org/documentation/tutorials/iterative_closest_point.php#iterative-closest-point

import pcl
import random
import numpy as np

# from pcl import icp, gicp, icp_nl

cloud_in = pcl.load('/home/fred/Documents/task00/shanghai/pcd/20181007.pcd')
cloud_out = pcl.load('/home/fred/Documents/task00/shanghai/pcd/2018100800.pcd')

# std::cout << "Transformed " << cloud_in->points.size () << " data points:" << std::endl;
print('Transformed ' + str(cloud_in.size) + ' data points:')


# pcl::IterativeClosestPoint<pcl::PointXYZ, pcl::PointXYZ> icp;
# icp.setInputCloud(cloud_in);
# icp.setInputTarget(cloud_out);
# pcl::PointCloud<pcl::PointXYZ> Final;
# icp.align(Final);
icp = cloud_in.make_IterativeClosestPoint()
# Final = icp.align()
converged, transf, estimate, fitness = icp.icp(cloud_in, cloud_out)

# std::cout << "has converged:" << icp.hasConverged() << " score: " << icp.getFitnessScore() << std::endl;
# std::cout << icp.getFinalTransformation() << std::endl;
# print('has converged:' + str(icp.hasConverged()) + ' score: ' + str(icp.getFitnessScore()) )
# print(str(icp.getFinalTransformation()))
print('has converged:' + str(converged) + ' score: ' + str(fitness) )
pcl.save(estimate, '/home/fred/Documents/task00/shanghai/pcd/20181007_icp.pcd')
print(str(transf))
