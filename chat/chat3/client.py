import threading
from socket import *
from tkinter import *

host = '127.0.0.1'
port = 8888
r=3
s = socket(AF_INET, SOCK_STREAM)
s.connect((host,port))

wind = Tk()
wind.title('client')
wind.geometry('1000x500')

en=Entry(wind,width=100)
en.grid(column=3,row=1)
en.config(state=DISABLED)

btn=Button(wind,width=3,height=1,text="send")
btn.grid(column=3,row=2)
btn.config(state=DISABLED)

en2=Entry(wind,width=20)
en2.grid(column=1,row=1)

btn2=Button(wind,width=6,height=1,text="connect")
btn2.grid(column=1,row=2)

l = Label(wind, text = 'alais')
l.grid(column=0,row=1)

alias = StringVar

def client_receive():
    global r,alias
    while True:
        try:
            message = s.recv(1024).decode('utf-8')
            Label(wind, text = message).grid(column=3,row=r)
            r=r+1
            print(message)
        except:
            print('Error!')
            s.close()
            break

def clicked():
    global r
    message = f'{alias}: {en.get()}'
    s.send(message.encode('utf-8'))
    en.delete(0,'end')

def clicked2():
    global r, alias
    try:
        message = s.recv(1024).decode('utf-8')
        if message == "alias?":
            s.send((en2.get()).encode('utf-8'))
            alias = en2.get()
            en2.config(state=DISABLED)
            en.config(state=NORMAL)
            btn2.config(state=DISABLED)
            btn.config(state=NORMAL)
            receive_thread = threading.Thread(target=client_receive)
            receive_thread.start()
    except:
        print('Error!')
        s.close()

btn["command"]=clicked
btn2["command"]=clicked2
wind.mainloop()

