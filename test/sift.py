import pcl
import numpy as np


def Surface_normals(cloud):
    ne = cloud.make_NormalEstimation()
    tree = cloud.make_kdtree()
    ne.set_SearchMethod(tree)
    ne.set_RadiusSearch(0.5)
    # NG
    print('test - a')
    print(ne)
    cloud_normals = ne.compute()
    print('test - b')
    return cloud_normals


def Extract_SIFT(cloud, cloud_normals):
    min_scale = 0.01
    n_octaves = 3
    n_scales_per_octave = 4
    min_contrast = 0.001

    sift = cloud_makeSIFTKeypoint()
    sift.set_SearchMethod(tree)
    sift.set_Scales(min_scale, n_octaves, n_scales_per_octave)
    sift.set_MinimumContrast(0.00)
    result = sift.compute()
    print('No of SIFT points in the result are ' + str(result.size))
    return result
