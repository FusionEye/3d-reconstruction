# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi

PORT_NUMBER = 8080


class myHandler(BaseHTTPRequestHandler):
    # Handler for the POST requests
    def do_POST(self):
        if self.path == "/color_pcd":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'
                         })

            print "Your name is: %s" % form["your_name"].value
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Thanks %s !" % form["your_name"].value)
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
