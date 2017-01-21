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
        print ("Got a request of: %s\n" % self.data)
        self.request.sendall("OK")

        # split the requset
        method = self.data.split()[0]
        abs_path = self.data.split()[1]

        response = self.ifMethod(method)

    def ifMethod(self, method):
        if(method != 'GET'):
            status = "HTTP/1.1 405 Method Not Allowed\r\n"
            response = "content-type: text/html\r\n" + \
                        "content-length: +  \r\n" + \
                        "contents"
            return response
        else:
            pass

    def getPath(self, path):
        dir = os.path.abspath("www")

        # if this is a GET method
        if not response:
            #print "aaaa"
            if not abs_path.startswith(dir):
                print ("not this dir")
                # handle 404 Error
            elif:
            elif "/../" in abs_path:
                # handle 404 Error
            else:
                # handle 404 Error
            if not os.path.exists(dir):
                # handle 404 Error
        print (dir)



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
