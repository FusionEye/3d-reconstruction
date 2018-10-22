# -*- coding: utf-8 -*-

import sys
from util.image_util import split_ricoh_images
from lidar.hokuyo.pcl_tools import merge_point_cloud_to_pcd
from lidar.color_point_cloud import color_pcd

if __name__ == '__main__':
    argvLen = len(sys.argv)

    # 分割图片
    if sys.argv[1] == 'image_split':
        split_ricoh_images(sys.argv[2], sys.argv[3])

    # 点云合成
    if sys.argv[1] == 'merge_pcd':
        if argvLen == 2:
            merge_point_cloud_to_pcd('./input/pointCloud/', './input/pointCloud.pcd')
        if argvLen == 4:
            merge_point_cloud_to_pcd(sys.argv[2], sys.argv[3])

    # 点云上色
    if sys.argv[1] == 'color_pcd':
        if argvLen == 2:
            color_pcd('./input/pointCloud.pcd', './input/image.JPG', './output')
        if argvLen == 5:
            color_pcd(sys.argv[2], sys.argv[3], sys.argv[4])
