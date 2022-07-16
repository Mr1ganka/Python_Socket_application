from email import message
from multiprocessing import connection
import socket
import threading
import sys


# PORT=5000
# SERVER='127.0.0.1'

SERVER=socket.gethostbyname(socket.gethostname())
PORT=5050
# ADDR=(SERVER,PORT)
HEADER=64
FORMAT='utf-8'
# SET=True
connection=True

DISCONN ="!DISCONNECT"
TOTAL_CLIENTS="!CLIENTS"
TIMESTAMP="!CURRENT"
ELAPSED="!ELAPSED"

ADDR=(SERVER,PORT)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length=len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length +=b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    # if client.recv(2048):
    # print(client.recv(2048).decode(FORMAT))

def recievemsg():
    while connection:
        print(client.recv(2048).decode(FORMAT))
    sys.exit()

newthread=threading.Thread(target=recievemsg)
newthread.start()


while connection:
    
    message=input("enter your message here: ")
    if message.upper()==DISCONN:
        send(DISCONN)
        connection=False
        print("Connection was terminated ")
        sys.exit()
    elif message.upper()==TOTAL_CLIENTS:
        send(TOTAL_CLIENTS)

    elif message.upper()==TIMESTAMP:
        send(TIMESTAMP)

    elif message.upper()==ELAPSED:
        send(ELAPSED)

    else:
        send(message)
