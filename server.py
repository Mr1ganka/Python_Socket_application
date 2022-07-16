import socket
import threading
from flask import Flask

app=Flask(__name__)

PORT=5050
# SERVER='192.168.0.1'
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
HEADER=64 
FORMAT='utf-8'

DISCONN ="!DISCONNECT"
TOTAL_CLIENTS='!CLIENTS'

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

#socket created
#getting socket ready for listening
All_connections = []

def handle_client(conn,addr):
    print(f"[New Connection] {addr} connected \n")
    
    connected=True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int (msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONN:
                connected = False
            print(f'[{addr}] {msg}')
    conn.close()
    print(f'[{addr}] "!!HAS DISCONNETED!!"')
    print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}\n")


def start():
    server.listen()
    print(f"[STARTED]:LISTENING FOR CONNECTIONS on {SERVER}...")
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}\n")
    
print("[STARTING]...")
start()