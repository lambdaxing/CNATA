# UDPPingerClient.py
from socket import *
import time

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
minRtt,maxRtt,sumRtt = 1.0,0.0,0.0
num = 0
for i in range(10):
    start = time.time()
    clientSocket.sendto('ping'.encode(), (serverName, serverPort))
    clientSocket.settimeout(1.0)
    try:
        pongmessage, sa = clientSocket.recvfrom(1024)
        t = (time.time() - start) * 1000
        minRtt = min(minRtt, t)
        maxRtt = max(maxRtt, t)
        sumRtt = sumRtt + t
        num = num + 1
        print(pongmessage.decode(), i, t)
    except:
        print("Request timed out")
    finally:
        clientSocket.settimeout(None)
clientSocket.close()
print("10 packets transmitted, %s packets received, %.1f%% packet loss" % (num, (num/10)*100))
print("round-trip min/avg/max = %.3f/%.3f/%.3f ms" % (minRtt, sumRtt/num, maxRtt))
