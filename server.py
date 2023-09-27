#  coding: utf-8 
import socketserver
import os 

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        # Decode data from bytestring to string
        decoded = self.data.decode("utf-8")
        # Split into words to check for methods that can be handled
        words = decoded.split()
        # Check if method is not get and if so return 405 status code and prevent rest from running
        if words[0] != "GET":
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\nContent-Type: text/plain; charset=utf-8\n", 'utf-8'))
            return   
        # Read the path and use the os library to check if it exists or needs redirect
        path = words[1] 
        folder = "www"
        if os.path.isdir(folder + path + "/") and not path.endswith("/"):
            actual_path = path + "/"
            self.request.sendall(bytearray(f"HTTP/1.1 301 Moved Permanently\nLocation: {actual_path}\nContent-Type: text/plain; charset=utf-8\n", 'utf-8'))
            return
        # Noe check if path to file or directory is valid, using exists instead to check for files
        if os.path.exists(folder + path):
            # Check if path ends with "/", in which case add index.html as per requirements, save www in actual path to open file
            actual_path = folder + path
            if actual_path.endswith("/"):
                actual_path += "index.html"
            content_type = ""
            # Check if html file or css file asked for and save content type to have mime support
            if actual_path.endswith(".html"):
                content_type = "text/html"
            elif actual_path.endswith(".css"):
                content_type = "text/css"
            # Check if file that does not exist
            if content_type == "":
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\nContent-Type: text/plain; charset=utf-8\n", 'utf-8'))
                return
            # Open the file     
            file = open(actual_path).read()
            self.request.sendall(bytearray(f"HTTP/1.1 200 OK\nContent-Type: {content_type}; charset=utf-8\n\n{file}\n", 'utf-8'))
        # If path not found, then return 404
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\nContent-Type: text/plain; charset=utf-8\n", 'utf-8'))
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
