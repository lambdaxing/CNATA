from socket import *
import time

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", 12000))
number = 1
serverSocket.settimeout(10)
while True:
    try:
        message, addr = serverSocket.recvfrom(2048)
        t = time.time()
        message = message.decode()
        n = int(message.split()[0])
        t = t - float(message.split()[1])
        while n > number:
            print('%d package lost...' % number)
            number = number + 1
        print('%d package difftime is %.3f ms' % (n, t*1000))
        number = number + 1
    except:
        print("Clietn stopped!")
        break
serverSocket.close()