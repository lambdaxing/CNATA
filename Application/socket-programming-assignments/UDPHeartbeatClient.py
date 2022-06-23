from socket import *
import time

serverName = '112.74.41.43'
serverPort = 12000
number = 1
clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    message = str(number) + " " + str(time.time())
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    number = number + 1
    time.sleep(5)
