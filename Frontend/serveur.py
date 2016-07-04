#! /usr/bin/env python2
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer
import SocketServer


class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
	PORT = 80
	Handler = CORSRequestHandler
	httpd = SocketServer.TCPServer(("", PORT), Handler)

	print "http://localhost:" + str(PORT)
	httpd.serve_forever()







