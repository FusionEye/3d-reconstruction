# -*- coding: utf-8 -*-

import os
import numpy as np
import pcl


def get_cloud(pcd_file):
    tmp_cloud = pcl.load(pcd_file)
    return tmp_cloud


def split_cloud(in_path, out_path):
    # 读取点云
    origin_cloud = get_cloud(in_path)
    outputCloud = pcl.PointCloud()

    # 配置剪刀
    points = np.array([
        [1.942357, -1.290997, -1.428566],
        [1.877337, -1.313471, 1.738325],
        [-0.782346, -0.630484, 1.685191],
        [1.679406, 6.726147, 1.921501]
    ], dtype=np.float32)
    filterCloud = pcl.PointCloud()
    filterCloud.from_array(points)

    vt = pcl.Vertices()
    vertices_point_1 = np.array([1, 2, 3, 4], dtype=np.int)
    vt.from_array(vertices_point_1)

    crophull = origin_cloud.make_crophull()
    crophull.SetParameter(filterCloud, vt)
    crophull.Filtering(outputCloud)

    # 保存点云
    pcl.save(outputCloud, out_path)


split_cloud('../input/pointCloud.pcd', '../input/pointCloud_split.pcd')