#  coding: utf-8
import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Jinzhu Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall("OK")

        # split the requset
        method = self.data.split()[0]
        abs_path = self.data.split()[1]
        #print "aaaaaaaaaa"
        #print abs_path
        #print os.path.abspath('www'+abs_path)

        response = self.ifMethod(method)

        # if this is a GET method
        if not response:
            self.getPath(abs_path)

    def ifMethod(self, method):
        if(method != 'GET'):
            status = "405 Method Not Allowed"
            mime_type = "text/html"
            contents = "<html><head>\r\n" + \
                        "<title>405 Method Not Allowed</title>\r\n" + \
                        "</head><body>\r\n" + \
                        "<h1>405 Method Not Allowed</h1>\r\n" + \
                        "</body></html>"
            response = False
            self.respond(status, mime_type, contents)
            return response
        else:
            pass

    def getPath(self, path):
        dir = os.path.abspath("www")
        #print (path)
        full_path = os.path.abspath('www'+path)

        types = path.split(".")
        if types[-1] == 'css':
            mime_type = "css"
        elif types[-1] == 'html':
            mime_type = "html"
        else:
            mime_type = "html"

        if not full_path.startswith(dir): # ONLY files in ./www and deeper to be served
            #print ("not this dir")
            # handle 404 Error
            self.error_404()
        elif "/../" in full_path:
            # handle 404 Error
            self.error_404()
        elif not os.path.exists(full_path):
            # handle 404 Error
            #print ("not exists uri")
            self.error_404()
        #print (dir)
        # return index.html from directories
        # TODO: handle 302 error
        elif os.path.isdir(full_path):
            # paths that end in /
            if path[-1] == '/':
                full_path = full_path + "/index.html"
            # if path not ending with '/', redirect it
            else:
                self.handle_302(full_path)

        # try open the file
        try:
            file = open(full_path, "r")
            contents = file.read()
        except IOError, e:
            self.error_404()
        else:
            status = "200 OK"
            self.respond(status, mime_type, contents)

    def respond(self, status, mime_type, contents):
        response = "HTTP/1.1 " + status + "\r\n" + \
                    "Content-type: text/" + mime_type + "\r\n" + \
                    "Content-length: " + str(len(contents)) + "\r\n\r\n" + \
                    contents + "\r\n"
        #print response
        self.request.sendall(response)

    def error_404(self):
        status = "404 Not Found"
        mime_type = "html"
        contents = "<html><head>\r\n" + \
                    "<title>404 Not Found</title>\r\n" + \
                    "</head><body>\r\n" + \
                    "<h1>Nothing matches the given URI</h1>\r\n" + \
                    "</body></html>"
        self.respond(status, mime_type, contents)

    def handle_302(self,path):
        status = "302 Found"
        mime_type = "html"
        contents = "<HTML><HEAD>\r\n" + \
                    "<TITLE>302 Moved</TITLE></HEAD><BODY>\r\n" + \
                    "<H1>302 Moved</H1>\r\n" + \
                    "The document has moved\r\n" + \
                    "<A HREF=" + path + "/index.html>here</A>.\r\n" + \
                    "</BODY></HTML>"
        location = "Location: " + path + "/index.html"
        self.respond(status, mime_type, contents)
        self.request.sendall(location)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
