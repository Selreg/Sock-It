from socket import *

serverName = 'localhost' #name of server
serverPort = 12000 #port number

clientSocket = socket(AF_INET, SOCK_STREAM) #create TCP socket

clientSocket.connect((serverName, serverPort))

try:
  data = "Hello World ! This is a very long string" #data to send
  clientSocket.send(data.encode())

  #modified code
  bytesSent = 0
  while bytesSent != len(data): # keep sending data until all data is sent

    bytesSent += clientSocket.send(data[bytesSent:].encode())
  # bytesSent += clientSocket.send(data[bytesSent:]) #This has the str error

  data = clientSocket.recv(40) #recieve data

  print("Received:", data.decode())

finally:
  clientSocket.close()
  print('Connection closed')

# clientSocket.connect((serverName, serverPort)) #connect to server

# clientSocket.send(data) #send data

# clientSocket.close()
