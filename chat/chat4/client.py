import threading
from socket import *
from tkinter import *

wind = Tk()
wind.title('client')
wind.geometry('860x420')

Frame1 = Frame(wind)
Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 1,sticky = S+E+W)

Frame2 = Frame(wind)
Frame2.grid(row = 0, column = 1, rowspan = 5, columnspan = 3,sticky = S+E+W)

Frame3 = Frame(wind)
Frame3.grid(row = 5, column = 1, rowspan = 1, columnspan = 3,sticky = S+E+W)
# set up connection part
a_label=Label(Frame1, text="alais")
user = Entry(Frame1)
a_label.grid(row=2,column=0)
user.grid(row=2,column=1,columnspan=2)
# set up chat area
chat = Text(Frame2)
chat.pack(side="left")
# set up message area
msg = Entry(Frame3)
msg.pack(side="left",expand=1,fill="both")
msg.config(state=DISABLED)
#------------------------------------------------------------------------------
def connect():
    global alias,s
    host = '127.0.0.1'
    port = 8888
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host,port))
    try:
        message = s.recv(1024).decode('utf-8')
        if message == "alias?":
            s.send((user.get()).encode('utf-8'))
            alias = user.get()
            user.config(state=DISABLED)
            connect.config(state=DISABLED)
            msg.config(state=NORMAL)
            send.config(state=NORMAL)
            receive_thread = threading.Thread(target=client_receive)
            receive_thread.start()
    except:
        print('Error!')
        s.close()
        
connect = Button(Frame1,text="Connect",command=connect)
connect.grid(row=3,column=1)
#send button function
def sendButton():
     global alias
     message = msg.get()
     finMessage =alias + "-> " + message
     s.send(finMessage.encode('utf-8'))
     msg.delete(0, END)

send = Button(Frame3,text="send",bg="Aqua", fg="Black",width=2,height=1,font=('courier','12'),command=sendButton )
send.config(state=DISABLED)
send.pack(side="left",expand=1,fill="x")
#------------------------------------------------------------------------------

def client_receive():
    global alias
    while True:
        try:
            message = s.recv(1024).decode('utf-8')
            finrecievedMsg = message + "\n"
            chat.insert(END,finrecievedMsg)
        except:
            print('Error!')
            s.close()
            break



wind.mainloop()

