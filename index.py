# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import os
from lidar.color_point_cloud import color_pcd

PORT_NUMBER = 3000


class myHandler(BaseHTTPRequestHandler):
    # Handler for the POST requests
    def do_POST(self):
        if self.path == "/color_pcd":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'})

            # txt
            field_item = form['txt']
            filevalue = field_item.value
            with open('./input/imageAndPcd.txt', 'wb') as f:
                f.write(filevalue)

            # image
            field_item = form['image']
            filevalue = field_item.value
            with open('./input/image.JPG', 'wb') as f:
                f.write(filevalue)

            # pcd
            field_item = form['pcd']
            filevalue = field_item.value
            with open('./input/pointCloud.pcd', 'wb') as f:
                f.write(filevalue)

            # 点云上色
            color_pcd('./input/pointCloud.pcd', './input/image.JPG', './output')

            # 转ply
            os.system('pcl_pcd2ply ./output/colourfulPointCloud.pcd ./input/colourfulPointCloud.ply')

            # 删除文件
            os.system('rm -rf /var/www/html/*')

            # 转potree
            os.system('../potree/PotreeConverter ./output/colourfulPointCloud.ply -o /var/www/html -p index')

            self.send_response(200)
            self.end_headers()
            self.wfile.write(1)
            return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
