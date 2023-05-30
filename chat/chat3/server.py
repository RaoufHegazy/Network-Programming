import datetime
import threading
from socket import *
from tkinter import *

host = '127.0.0.1'
port = 8888
s = socket(AF_INET, SOCK_STREAM)
s.bind((host,port))
s.listen()
clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)

def receive():
    while True:
        client,add = s.accept()
        clients.append(client)
        dateAsString = str(datetime.datetime.now())
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        client.send(('you connected at:'+ dateAsString).encode('utf-8'))
        aliases.append(alias)
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

def handle_client(client):
    while True:
        try:
            m = client.recv(1024)
            broadcast(m)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

if __name__ == "__main__":
    receive()