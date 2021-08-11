import argparse
from server import Server
from client import Client
from time import sleep

parser = argparse.ArgumentParser(description='')
parser.add_argument('side', type=str, help='client or server')
parser.add_argument('-a', '--adress', help='IP of your server', default='localhost')
parser.add_argument('-p', '--port', help='Port of your server', default='8888')
parser.add_argument('-u', '--username', help='Your name in the chats', default='Anon')
args = parser.parse_args()

if args.side == 'server':
    serv = Server(args.adress, int(args.port))
    serv.start()
elif args.side == 'client':
    cl = Client(args.username)
    cl.connect(args.adress, int(args.port))
    if cl.connected:
        cl.shell()
else:
    print('ERROR ARGUMENT')