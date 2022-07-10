import socket
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(str):
    csum = 0
    countTo = (len(str) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = str[count+1] * 256 + str[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
        
    if countTo < len(str):
        csum = csum + str[len(str) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        
        #Fill in start
        #Fetch the ICMP header from the IP packet
        header = recPacket[20:28]
        header_type, header_code, header_checksum, header_id, header_sequence = struct.unpack("bbHHh", header)
        if header_type != 0 or header_code != 0 or header_id != ID or header_sequence != 1:
            if header_type == 3 and header_code == 0:
                return "目的网络不可达。"
            if header_type == 3 and header_code == 1:
                return "目的主机不可达。"
            if header_type == 3 and header_code == 2:
                return "目的协议不可达。"
            if header_type == 3 and header_code == 3:
                return "目的端口不可达。"
            if header_type == 3 and header_code == 6:
                return "目的网络未知。"
            if header_type == 3 and header_code == 7:
                return "目的主机未知。"
            if header_type == 4 and header_code == 0:
                return "源抑制。"
            if header_type == 12 and header_code == 0:
                return "IP首部损坏。"
            return "Receive error."
        #Fill in end
        
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."
        #return timeLeft        # timeLeft is not delay
        return howLongInSelect  # This is delay


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    
    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
        #Convert 16-bit integers from host to network byte order.
    else:
        myChecksum = socket.htons(myChecksum)
    
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    #Both LISTS and TUPLES consist of a number of objects
    #which can be referenced by their position number within the object

def doOnePing(destAddr, timeout):
    icmp = socket.getprotobyname("icmp")

    #SOCK_RAW is a powerful socket type. For more details see: http://sock-raw.org/papers/sock_raw
    
    #Fill in start
    #Create Socket here
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    #Fill in end

    myID = os.getpid() & 0xFFFF #Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    #timeout=1 means: If one second goes by without a reply from the server,
    #the client assumes that either the client’s ping or the server’s pong is lost
    dest = socket.gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    #Send ping requests to a server separated by approximately one second
    num, lost, sumRtt, maxRtt, minRtt = 10, 0, 0, 0, 1.0
    for i in range(num):
        delay = doOnePing(dest, timeout)
        print(str(i) + ": " + str(delay))
        if type(delay) == str:
            lost = lost + 1
        else:
            maxRtt = max(maxRtt, delay)
            minRtt = min(minRtt, delay)
            sumRtt = sumRtt + delay
        time.sleep(1)# one second
    if lost != num:
        print("%d packets transmitted, %d packets received, %.2f%% packet loss" % (num, num - lost, lost/num))
        print("round-trip min/avg/max = %.3f/%.3f/%.3f ms" % (minRtt, sumRtt/(num-lost), maxRtt))

ping("www.cppreference.com")