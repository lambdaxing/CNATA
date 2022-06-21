from http import server
from socket import *
import sys
import os

if len(sys.argv) <= 3:
    print('Usage : "Client.py server_host server_port filename"')
    sys.exit(2)
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
askFile = sys.argv[3]
tcpSocket = socket(AF_INET, SOCK_STREAM)
tcpSocket.connect((serverName, serverPort))
tcpSocket.send("GET ".encode() + askFile.encode() + " HTTP/1.1\r\nHost: ".encode() + serverName.encode() + "\r\n\r\n".encode())
message = 1
while message:
    message = tcpSocket.recv(1024)
    print(message.decode(), end = '')
tcpSocket.close()