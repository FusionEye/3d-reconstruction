pcd转ply:
pcl_pcd2ply xxx.pcd xxx.ply

分割图片:
python fusioneye.py images_plit test/*.JPG output

bag生成pcd:
rosrun pcl_ros bag_to_pcd xxx.bag /hokuyo_points pcd_folder

合成点云:
python fusioneye.py merge_pcd pcd_folder xxx.pcd

点云图片坐标系校准:


点云上色:
python fusioneye.py color_pcd input.pcd xxx.JPG output.pcd
