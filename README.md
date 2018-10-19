# 3d重建

### USAGE
 
Use pcd file with panoramic image to colorize the point cloud to realistic 3D rendering. 

you will need: 
* a panoramic photo
* a pointcloud file
* relating point cloud (x,y,z) positions
* correlating pixel position (x,y) in the same scene

### PROCEDURE

1. Picking (x,y,z) from point cloud:

    ``` pcl_viewer xxx.pcd -use_point_picking ```

    shift + 鼠标左键点击可以获取点云坐标

2. Picking relative image pixel (x,y) from image file:

    use a gimp or equivalent image software

3. Prepare source data folder:

    * 图像坐标和点云坐标文件: input/imageAndPcd.txt
    * 图像文件: input/image.JPG
    * 点云文件夹: input/pointCloud

4. Run coloring command: 

    ``` python fusioneye.py color_pcd ```
    
5. Output colorful pcd file:

    输出有色点云: output/colourfulPointCloud.pcd
