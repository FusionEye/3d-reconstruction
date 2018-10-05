# -*- coding: utf-8 -*-

import sys
from util.image_util import split_ricoh_images
from lidar.hokuyo.pcl_tools import merge_point_cloud_to_pcd
from lidar.color_point_cloud import color_pcd


def test_split_image():
    split_ricoh_images('test/*.JPG', 'output/test')


def test_merge_pcd():
    merge_point_cloud_to_pcd('/home/fred/Documents/task00/shanghai/bagfiles/2018-10-03-09-10-19/',
                             '/home/fred/Documents/task00/shanghai/pcd/2018-10-03-09-10-19.pcd')


def test_color_pcd():
    color_pcd('/home/fred/Documents/task00/shanghai/pcd/2018-10-03-09-10-19.pcd',
              '/home/fred/git/3d-reconstruction/images/pcd_on_color/right/20181001161152.JPG',
              '/home/fred/Documents/task00/shanghai/pcd/2018-10-03-09-10-19_colorful.pcd')


if __name__ == '__main__':
    if sys.argv[1] == 'image_split':
        test_split_image()
    if sys.argv[1] == 'merge_pcd':
        test_merge_pcd()
    if sys.argv[1] == 'color_pcd':
        test_color_pcd()
