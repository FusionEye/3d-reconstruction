# 3d重建

点云可视化: 

pcl_viewer xxx.pcd -use_point_picking

shift + 鼠标左键点击可以获取点云坐标

---

图像坐标和点云坐标文件:

input/imageAndPcd.txt

图像文件:

input/image.JPG

点云文件:

input/pointCloud.pcd

输出有色点云:

output/colourfulPointCloud.pcd

上色命令:

python fusioneye.py color_pcd
