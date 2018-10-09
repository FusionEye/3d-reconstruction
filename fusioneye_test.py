# -*- coding: utf-8 -*-

import sys
from util.image_util import split_ricoh_images
from lidar.hokuyo.pcl_tools import merge_point_cloud_to_pcd
from lidar.color_point_cloud import color_pcd


def test_split_image():
    split_ricoh_images('test/*.JPG', 'output/test')


def test_merge_pcd():
    merge_point_cloud_to_pcd('/mnt/hgfs/PycharmProjects/ml/input/2018-10-08-29/',
                             '/mnt/hgfs/PycharmProjects/ml/input/2018-10-08-29.pcd')


def test_color_pcd():
    color_pcd('/mnt/hgfs/PycharmProjects/ml/input/2018-10-08-29.pcd',
              '/mnt/hgfs/下载/R0010034.JPG',
              '/mnt/hgfs/PycharmProjects/ml/output/colorful.pcd')


if __name__ == '__main__':
    if sys.argv[1] == 'image_split':
        test_split_image()
    if sys.argv[1] == 'merge_pcd':
        test_merge_pcd()
    if sys.argv[1] == 'color_pcd':
        test_color_pcd()
