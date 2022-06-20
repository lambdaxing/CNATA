 #改为Python3格式
from socket import *
import sys
import os

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerPort = int(sys.argv[1])
tcpSerSock.bind(("", tcpSerPort))
print(tcpSerPort)
tcpSerSock.listen(10)
while 1:
	# Strat receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
	message = tcpCliSock.recv(1024)
	message = message.decode()
	print("message:\n", message)
	if(message == ''):
		continue
	# Extract the filename from the given message
	print("message.split()[1]:", message.split()[1])
	filename = message.split()[1].partition("/")[2]
	print("filename:", filename)
	fileExist = "false"
	filetouse = "/" + filename
	print("filetouse:", filetouse)
	try:
		# Check wether the file exist in the cache
		f = open("WEB/" + filetouse[1:], "rb")
		outputdata = f.read()
		f.close()
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
		tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
		tcpCliSock.send(outputdata)
		print('Read from cache')
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false":
			# Create a socket on the proxyserver
			c = socket(AF_INET, SOCK_STREAM)
			hostn = filename.replace("www.","",1)
			print("hostn:", hostn)
			try:
				# Connect to the socket to port 80
				serverName = filename.partition("/")[0]
				serverPort = 80
				print((serverName, serverPort))
				c.connect((serverName, serverPort))
				askFile = ''.join(filename.partition('/')[1:])
				print("askFile:", askFile)
				# Create a temporary file on this socket and ask port 80
				# for the file requested by the client
				reH = "GET " + askFile + " HTTP/1.1\r\nHost: " + serverName + "\r\n\r\n"
				print("reH:", reH)
				c.send(reH.encode())
				print("ok")
				serverResponse = c.recv(1024)
				print(serverResponse.decode())
				tmpFile = open('WEB/' + filename, "wb")
				print("ok1")
				tmpFile.write(serverResponse)
				print("ok2")
				tmpFile.close()
				print("ok3")
				tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
				print("ok4")
				tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
				print("ok5")
				tcpCliSock.send(serverResponse)
				print("ok6")
			except:
				print("Illegal request")
			c.close()
		else:
			# HTTP response message for file not found
			print("NET ERROR")
	# Close the client and the server sockets
	tcpCliSock.close()
tcpSerSock.close()