import asyncio
import websockets
import socket
from time import sleep

class Client:
    host = None
    port = None
    def __init__(self):
        self.socket = socket.socket()

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.socket.connect((host,port))
    
    def send(self, message):
        self.socket.send(message)
    
    def receive(self):
        data = self.socket.recv(1024)
        print(data)
    
    def close(self):
        self.socket.close()

