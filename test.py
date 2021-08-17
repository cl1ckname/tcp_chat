from sys import stdin, stdout
from time import sleep
import threading

def message():
    while True:
        print('\033[s \033[F ivan-9 \033[u', end='')
        # print('ivan - 8')
        # print('\033[u',end='')
        sleep(5)


t = threading.Thread(target=message, daemon=True)
t.start()
print()
while True:
    input('>>')

