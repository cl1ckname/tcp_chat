# Tcp_chat
[![PyPI version](https://badge.fury.io/py/cn-tcp-server.svg)](https://badge.fury.io/py/cn-tcp-server)  
A simple tcp chat on python
## Installing

Using pip:

```
$ pip3 install cn-tcp-server
```

Using git:
```
$ git clone https://github.com/cl1ckname/tcp_chat.git
$ mv tcp_chat <path_to_your_python_packeges_folder>/tcp_chat
```

## Usage
The chat works on a room system. Any names consisting of symbols of the Latin alphabet, numbers and slashes are acceptable. Chats are not password protected, so anyone can join any room, or create their own.  
How it look like:
>_Clickname_ - Hay, is this chat empty?  
>_BigJoe2008_ - No, the guys and I are here discussing isomorphism problems in topologically compact manifolds  
>_Clickname_ - Oh...  
### Commands
To start the __server__ write:  
```
python3 -m tcp_chat server -a <IP> -p <PORT>
```
* IP - Your IP address where the server will run. The default is `localhost`.  
* PORT - The port that the server will listen on. The default is `8888`.  
  
To start __client__ write:
```
python3 -m tcp_chat start client -a <IP> -p <PORT> -u <USERNAME> -c <CHAT_ID>
```
* IP - Your IP address of server. The default is `localhost`.  
* PORT - The port of that server. The default is `8888`.  
* USERNAME - The name with which your chat messages will be shown.  
* CHAT_ID - The name of the chat room. If such exists, the application will add you to it, if not, it will create.
### Close application
To close server tap CTR+C  
To stop client tap CTR+C or write `/exit`
## For custom clients
You can use any tcp client to connect, you should only follow the authentication system:
* The first message must match the pattern `<USERNAME>_<CHAT_ID>`
* There are three response codes
  * __200__ - Authentication passed
  * __400__ - Invalid first message
  * __403__ - User with this username already connected  

Messages are sent as plain text in UTF-8 encoding.
