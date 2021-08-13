import threading
from abc import ABC, abstractmethod
from socket import socket
from typing import MutableSet

class LoopThread(ABC, threading.Thread):
    ''' LoopThread runs on a separate thread and includes an infinite loop that executes `main` and calls `final` upon completion. '''
    active = True
    def run(self):
        try:
            while self.active:
                self.main()
        finally:
            self.final()

    @abstractmethod
    def main(self):
        ''' The function to be called in the loop until the loop is stopped '''
        pass

    @abstractmethod
    def final(self):
        ''' Сalled after the end of the loop '''
        pass

    def stop(self):
        ''' Stops the loop '''
        self.active = False

class Connection(LoopThread):
    ''' Thread of user connection to server '''
    def __init__(connection, sock: socket, username:str, chat_id:str):
        super().__init__(daemon=True)
        connection.sock = sock
        connection.username = username
        connection.chat_id = chat_id
    
    def receive(connection) -> str:
        ''' Receives and decodes data '''
        return connection.sock.recv(1024).decode('utf-8')

    def send(connection, message: str):
        ''' Encode and send message to client '''
        connection.sock.send(message.encode('utf-8'))

class Server:
    ''' Server for multithreading TCP connections '''
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.socket:socket = socket()
        self.socket.bind((host, port))
        self.connections = {}
        self.chats = {}

        class Connection_(Connection):
            def main(connection):
                data = connection.receive()
                if len(data) > 0:
                    message = f'{connection.username}: {data}'
                    connection.send(message)
                else:
                    connection.stop()

            def final(connection):
                connection.sock.close()
                del self.connections[connection.username]
                print(connection.username, 'disconnected')

        self.Connection = Connection_ 

    def recive(self, n=1024, encoding = 'utf-8'):
        return self.socket.recv(n).decode(encoding)

    def auth(self ,sock: socket, addr):
        data = sock.recv(1024).decode('utf-8')
        username, chat_id  = data.split('_')
        if username and chat_id and username not in self.connections.keys():
            print("Connected to", addr, 'as', username)
            sock.send(b'200')
            connection = self.Connection(sock = sock, username = username, chat_id = chat_id)
            connection.start()
            self.connections[username] = connection
            print('Num of connections:', len(self.connections))
            return connection

        elif username in self.connections.keys():
            sock.send(b'403')
            sock.close()
            return None
        else:
            sock.send(b'401')
            sock.close()
            print('Authentificated error with', addr)
            return None

    def join_chat(self, chat_id, username):
        user = self.connections[username]
        if chat_id in self.chats.keys():
            self.chats[chat_id].join(user)
        else:
            chat = Chat(chat_id)
            self.chats[chat_id] = chat
            chat.join(user)

    def start(self):
        print('Start server')
        self.socket.listen(5)
        try:
            while True:
                sock, addr = self.socket.accept()
                conn = self.auth(sock, addr)
                if conn:
                    self.join_chat(conn.chat_id, conn.username)
        except KeyboardInterrupt:
            print(' - you tab CTRL-C')
        finally:
            print('Stop server')
            for connection in self.connections.values():
                connection.stop()
            self.socket.close()


class Chat(LoopThread):
    active = True
    id: int = None
    def __init__(self, id:int):
        self.id = id
        self.members:MutableSet[Connection] = set()
    
    def join(self, conn: Connection):
        self.members.add(conn)

    def main(self):
        for conn_sender in self.members:
            data = conn_sender.receive()
            if len(data):
                for conn_receiver in self.members:
                    conn_receiver.send(data)

    def final(self):
        print('Chat error, chat failed')
        for conn in self.members:
            conn.stop()            
