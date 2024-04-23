from socket import *

serverPort = 12000 #port number to listen on

serverSocket = socket(AF_INET, SOCK_STREAM) #create TCP socket

serverSocket.bind(('localhost', serverPort)) #bind socket to port

serverSocket.listen(1) #listen for incoming connections

print('The server is ready to receive from:', serverSocket.getsockname())

data = b"" #buffer for incoming data, to store the recieved data

while 1:
  connectionSocket, addr = serverSocket.accept() #accept incoming connection
  
  #modifcations ----
  tmpBuffer = "" 
  while len(data) != 40: # if data is not 40 bytes
    tmpBuffer = connectionSocket.recv(40) #recieve data
    # data += tmpBuffer
    if not tmpBuffer:
      break
    # data += tmpBuffer # add data to buffer
    data += tmpBuffer

  
  # data = connectionSocket.recv(40) #recieve data

  
  print("Received:", data.decode())
  
  
  # connectionSocket.sendall(data.upper()) #send data in uppercase
  # if not data:
  #   break #end of connection
  # connectionSocket.send(data.upper()) #send data in uppercase
  # connectionSocket.close()

connectionSocket.close()

print ("Connection closed")