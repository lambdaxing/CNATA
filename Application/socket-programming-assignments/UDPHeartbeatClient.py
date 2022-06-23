from socket import *
import time

serverName = 'localhost'
serverPort = 12000
number = 1
clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    message = str(number) + " " + str(time.time())
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    number = number + 1
    time.sleep(5)
