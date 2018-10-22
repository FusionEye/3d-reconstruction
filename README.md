# 3d重建

### USAGE
 
Use pcd file with panoramic image to colorize the point cloud to realistic 3D rendering. 

you will need: 
* a panoramic photo
* a pointcloud file
* relating point cloud (x,y,z) positions
* correlating pixel position (x,y) in the same scene

### PROCEDURE

0. Converting ros bag to pcd:
    
    ``` rosrun pcl_ros bag_to_pcd xxx.bag /hokuyo_points input/pointCloud ```
    
0. Merging pcd files to one:

    ``` python fusioneye.py merge_pcd ```
    
1. Picking (x,y,z) from point cloud:

    ``` pcl_viewer input/pointCloud.pcd -use_point_picking ```

    shift + 鼠标左键点击可以获取点云坐标

2. Picking relative image pixel (x,y) from image file:

    use a gimp or equivalent image software

3. Prepare source data folder:

    * 图像坐标和点云坐标文件: input/imageAndPcd.txt
    * 图像文件: input/image.JPG

4. Run coloring command: 

    ``` python fusioneye.py color_pcd ```
    
5. Output colorful pcd file:

    输出有色点云: output/colourfulPointCloud.pcd
