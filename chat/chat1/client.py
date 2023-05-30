import socket
import threading
import tkinter as tk

host = '127.0.0.1'
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:
    y = input('Client:')
    s.send(y.encode('utf-8'))
    x = s.recv(1024)
    print('Server:',x.decode('utf-8'))