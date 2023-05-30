import socket
import threading
import tkinter as tk

host = '127.0.0.1'
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen()

client,add = s.accept()

while True:
    x = client.recv(1024)
    print('Client:',x.decode('utf-8'))
    y = input('Server:')
    client.send(y.encode('utf-8'))