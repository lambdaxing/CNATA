#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a server socket
serverSocket.bind(('', 80))
serverSocket.listen(1)
while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
        #Send one HTTP header line into socket
        outputdata = 'HTTP/1.1 200 Ok\r\nConnection: close\r\n\r\n' + outputdata
        #Send the content of the requested file to client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
        print("OK!")
    except IOError:
        #Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n'.encode())
        #Close client socket
        connectionSocket.close()
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data