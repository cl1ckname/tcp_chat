import argparse
from server import Server
from client import Client
from time import sleep

parser = argparse.ArgumentParser(description='')
parser.add_argument('side', type=str, help='client or server')
parser.add_argument('-a', '--adress', help='IP of your server', default='localhost')
parser.add_argument('-p', '--port', help='Port of your server', default='8888')
args = parser.parse_args()

if args.side == 'server':
    serv = Server(args.adress, int(args.port))
    serv.start()
    pass
elif args.side == 'client':
    cl = Client()
    cl.connect(args.adress, int(args.port))
    try:
        while True:
                cl.send(bytes(input('>> ').encode('utf-8')))
                cl.receive()
    except KeyboardInterrupt:
        print(' - you tab CTRL-C')
    finally:
        print('Closing...')
        cl.close()
else:
    print('ERROR ARGUMENT')