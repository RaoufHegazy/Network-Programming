import socket
import threading
import tkinter as tk

host = '127.0.0.1'
port = 8888
alias = input('alais:')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

def client_receive():
    while True:
        try:
            message = s.recv(1024).decode('utf-8')
            if message == "alias?":
                s.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            s.close()
            break


def client_send():
    while True:
        message = f'{alias}: {input("")}'
        s.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
