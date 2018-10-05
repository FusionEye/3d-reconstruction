# -*- coding: utf-8 -*-

import sys
from util.image_util import split_ricoh_images
from lidar.hokuyo.pcl_tools import merge_point_cloud_to_pcd

if __name__ == '__main__':
    # 分割图片
    if sys.argv[1] == 'image_split':
        split_ricoh_images(sys.argv[2], sys.argv[3])
    # 点云合成
    if sys.argv[1] == 'merge_pcd':
        merge_point_cloud_to_pcd(sys.argv[2], sys.argv[3])
