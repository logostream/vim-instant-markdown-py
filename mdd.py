#!/usr/bin/env python
# coding: utf-8
import socket
import threading
import os
from os import path
import sys
from bottle import *
from markdown import markdown
from ws import *

markdown_options = [
  'extra', 'mathjax', 'topen', 'preview', 'tag', 'anchor',
  'poptoc(title=Table of Content (Beta),maxlevel=2)',
  'wikilinks(base_url=http://en.wikipedia.org/wiki/, end_url=)',
  'highlight', 'githubcss', 'codehilite']
client = None


def startServer():
    global client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 9998))
    sock.listen(1)
    html = os.path.join(sys.path[0], 'index.html')
    if sys.platform.startswith('darwin'):
        os.system('open -g {}'.format(html))
    elif sys.platform.startswith('win'):
        os.system('start {}'.format(html))
    else:
        print 'Please open ./index.html'
    try:
      while True:
          conn, addr = sock.accept()
          if handshake(conn):
              client = conn
    finally:
      sock.close()


@route('/<path:path>')
def server_static(path):
    return static_file(path, root='/')

@post('/')
def convert():
    html = markdown(request.forms['md'].decode('utf-8'), markdown_options)
    if client:
        SendData(html, client)
    return 'OK'

@get('/')
def start():
    print 'Welcome!!!'
    return static_file('index.html', root=path.dirname(__file__))

if __name__ == '__main__':
    t = threading.Thread(target=startServer)
    t.daemon = True
    t.start()
    run(host='localhost', port=9999)
