#!/usr/bin/env python
# coding: utf-8
import socket
import threading
import os
import sys
from bottle import *
from markdown import markdown
from ws import *

markdown_options = ['extra', 'codehilite']
client = None


def startServer():
    global client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 9998))
    sock.listen(1)
    if sys.platform.startswith('darwin'):
        os.system('open -g index.html')
    else:
        print 'Please open ./index.html'
    while True:
        conn, addr = sock.accept()
        if handshake(conn):
            client = conn


@route('/<path:path>')
def server_static(path):
    return static_file(path, root='.')

@post('/')
def convert():
    html = markdown(request.forms['md'].decode('utf-8'), markdown_options)
    if client:
        SendData(html, client)
    return 'OK'

if __name__ == '__main__':
    t = threading.Thread(target=startServer)
    t.daemon = True
    t.start()
    run(host='localhost', port=9999)
