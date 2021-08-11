import socket
import threading
from time import sleep

class Client:
    host = None
    port = None
    connected = False
    def __init__(self, username):
        self.socket = socket.socket()
        self.username = username

    def connect(self, host, port):
        self.host = host
        self.port = port
        try:
            self.socket.connect((host,port))
            self.send(self.username)
            answer = self.receive()
            assert answer == '200'
            self.connected = True
            print('Connected!')
            listen_thread = threading.Thread(target=self.listen, daemon=True)
            listen_thread.start()
        except:
            print('Connection error')
            self.socket.close()

    def shell(self):
        try:
            while True:
                sleep(0.2)
                message = input('>> ')
                if not message:
                    print('I can`t send empty message')
                elif message == '/exit':
                    print('Exit!')
                    break
                elif message == '/down':
                    self.socket.shutdown(socket.SHUT_RDWR)
                    break
                else:
                    self.send(message)
        except KeyboardInterrupt:
            print(' - you tab CTRL-C')
        finally:
            print('Closing...')
            self.close()
    
    def listen(self):
        print()
        try:
            while self.connected:
                data = self.socket.recv(1024)
                if len(data) > 0:
                    message = data.decode("utf-8")
                    print(message)
                else:
                    self.connected = False
        finally:
            print('Stop listening...')
            self.close()

    def send(self, message: str):
        self.socket.send(message.encode('utf-8'))
    
    def receive(self):
        data = self.socket.recv(1024)
        return data.decode('utf-8')
    

    def close(self):
        self.connected = False
        self.socket.close()


