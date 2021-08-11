from socket import socket
import threading

class Connection(threading.Thread):
    active = True

    def __init__(self, sock):
        super (Connection, self).__init__()
        self.sock = sock

    def echo(self, sock: socket):
        try:
            while self.active:
                data = sock.recv(1024)
                if data:
                    print('Recieved',data.decode('utf-8'),'|', len(data))
                    sock.send(data.upper())
            sock.close()
        finally:
            sock.close()

    def run(self):
        self.echo(self.sock)

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

    def start(self):
        print('Start server')
        self.socket.listen(5)
        try:
            while True:
                sock, addr = self.socket.accept()
                print("Connected to", addr)
                thread = Connection(sock)
                self.threads.append(thread)
                print('Num of connections:', len(self.threads))
                thread.start()
        except KeyboardInterrupt:
            print(' - you tab CTRL-C')
        finally:
            print('Stop server')
            for thread in self.threads:
                thread.stop()
            self.socket.close()
# HOST = '192.168.0.53'
# PORT = 8888

# s = socket.socket()
# s.bind((HOST, PORT))
# s.listen(True)

# conn, addr = s.accept()
# print(addr)

# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     conn.send(data.upper())
# conn.close()