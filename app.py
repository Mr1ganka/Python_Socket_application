
import socket
import threading
from flask import Flask
from datetime import datetime
import time


# app=Flask(__name__)

PORT=5050
# PORT=5000
# SERVER='192.168.0.1'
# SERVER ='127.0.0.1'
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
HEADER=64 
FORMAT='utf-8'

DISCONN ="!DISCONNECT"
TOTAL="!CLIENTS"
TIMESTAMP="!CURRENT"
ELAPSED="!ELAPSED"

All_connections=[]

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

#socket created
#getting socket ready for listening

def handle_client(conn,addr):
    try:
        CONNECTION_ESTABLISHED=datetime.now() #current time when the conection was established

        print(f"[NEW CONNECTION] {addr} ESTABLISHED \n")
        All_connections.append([conn,addr])
        print(f"[ACTIVE CONNECTIONS] {len(All_connections)}\n")
        
        connected=True
        while connected:
            msg_length=conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length=int (msg_length)
                msg=conn.recv(msg_length).decode(FORMAT)

                if msg == DISCONN:
                    connected = False
                    conn.close()
                    print(f'[{addr}] "[!!HAS DISCONNETED!!]"')
                    All_connections.remove([conn,addr])
                    print(f"[ACTIVE CONNECTIONS] {len(All_connections)}\n")
                
                elif msg == TOTAL:          #total number of connections that are there
                    # print(f"[ACTIVE CONNECTIONS] {len(All_connections)}\n")
                    conn.send(f"NUMBER OF CONNECTED CLIENTS: {len(All_connections)}".encode(FORMAT))

                elif msg == TIMESTAMP:      #current time on the server
                    now_time = str(datetime.now())
                    # current_time = now.strftime("%H:%M:%S")
                    conn.send(f'THE SERVER TIME STAMP IS: {now_time} \n'.encode(FORMAT))

                elif msg == ELAPSED:        #time elapsed on the server since then
                    now_time = datetime.now()
                    elapsed_time=str(now_time-CONNECTION_ESTABLISHED)
                    conn.send(f'TIME ELAPSED SINCE THE CONNECTION WAS ESTABLISHED: {elapsed_time} \n'.encode(FORMAT))
                    
                else:                       #else we just print the address
                    # print(f'[{addr}] SAYS: {msg}')
                    conn.send("\n".encode(FORMAT))
    except Exception:                   #exception added just in case the client is closed suddenly
        All_connections.remove([conn,addr])
        print(f'[{addr}] [CONNECTION ERROR] "!!HAS BEEN TERMINATED!!" ')
        # print("CONNECTION ERROR")
    
def sleeping():     #function to send the connected message to all clients every one minute
    while True:
        if len(All_connections)>0:
            time.sleep(60)
            for i in All_connections:
                i[0].send(f"\nCONNECTED\nenter your message here: ".encode(FORMAT))
        # print("CONNECTED")


def start():
    server.listen()
    print(f"[STARTED]:LISTENING FOR CONNECTIONS on {SERVER}...")

    while True:

        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        # print("Connection list",All_connections)

print("[STARTING]...")
newthread=threading.Thread(target=sleeping) #a new thread to send the connected message
newthread.start()
start()