from socket import socket
import threading

from time import sleep


class Connection(threading.Thread):
    ''' Thread of user connection to server '''
    active = True

    def __init__(self, sock, server, username):
        super (Connection, self).__init__(daemon=True)
        self.sock = sock
        self.server = server
        self.username = username

    def mainloop(self):
        try:
            while self.active:
                data = self.sock.recv(1024)
                if len(data) > 0:
                    message = f'{self.username}: {data.decode("utf-8")}'
                    print(message)
                    self.sock.send(message.encode('utf-8'))
                else:
                    self.active = False
        finally:
            self.sock.close()

    def run(self):
        self.mainloop()
        self.server.members -= 1
        print(self.username, 'disconnected')

    def stop(self):
        self.active = False

class Server:
    ''' Server for multithreading TCP connections '''
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.socket = socket()
        self.socket.bind((host, port))
        self.threads = []
        self.members = 0

    def recive_decoded(self, n=1024, encoding = 'utf-8'):
        return self.socket.recv(n).decode(encoding)

    def start(self):
        print('Start server')
        self.socket.listen(5)
        try:
            while True:
                sock, addr = self.socket.accept()
                username = sock.recv(1024).decode('utf-8')
                print(122, username)
                if username:
                    sock.send(b'200')
                    print("Connected to", addr, 'as', username)
                    thread = Connection(sock, self, username)
                    self.threads.append(thread)
                    self.members += 1
                    print('Num of connections:', len(self.threads))
                    thread.start()
                else:
                    sock.send(b'401')
                    sock.close()
                    print('Authentificated error with', addr)
        except KeyboardInterrupt:
            print(' - you tab CTRL-C')
        finally:
            print('Stop server')
            for thread in self.threads:
                thread.stop()
            self.socket.close()
