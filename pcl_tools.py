# -*- coding: utf-8 -*-

import os
import numpy as np
import pcl


def mergePointcloud(path):
    # 初始化矩阵大小
    pathDir = os.listdir(path)
    shape = (9999999, 3)
    points = np.zeros(shape, dtype=np.float32)

    row = 0
    for allDir in pathDir:
        pcdFile = os.path.join('%s%s' % (path, allDir))
        print(pcdFile)
        tmp_cloud = pcl.load(pcdFile)
        print('cloud(size) = ' + str(tmp_cloud.size))

        for i in range(0, tmp_cloud.size):
            x = tmp_cloud[i][0]
            y = tmp_cloud[i][1]
            z = tmp_cloud[i][2]

            # 过滤无用的点
            if (abs(x) > 10 or abs(y) > 10 or abs(z) > 10):
                continue

            points[row][0] = x
            points[row][1] = y
            points[row][2] = z
            row += 1

    # 重置矩阵大小
    points.resize(row, 3)
    return points


def outPointCloud(points, out):
    cloud = pcl.PointCloud()
    cloud.from_array(points)
    pcl.save(cloud, out)


if __name__ == '__main__':
    # 这个目录由ros命令生成， rosrun pcl_ros bag_to_pcd xxx.bag /hokuyo_points pcd
    points = mergePointcloud("/home/fred/Documents/bagfiles/pcd/")
    # 输出
    outPointCloud(points, "/home/fred/Documents/pcd/cloud.pcd")
