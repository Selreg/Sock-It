import socket
import sys
import os

def send_command(sock, command):
    sock.send(command.encode())
    if command.lower().startswith(("get","put")):
        #Server sends message saying ready to transfer files
        response = sock.recv(4096).decode()
        print(response)

        #Create data socket for transferring files
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.bind(('', 0))
        data_socket.listen(1)
        #Send the data port number to the server
        sock.send(str(data_socket.getsockname()[1]).encode())
        data_transfer_socket, _ = data_socket.accept()
        if command.lower().startswith("get"):
            #Code to receive file
            with open(command.split()[1], 'wb') as f:
                while True:
                    bytes_read = data_transfer_socket.recv(4096)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
            print("File downloaded successfully.")
        elif command.lower().startswith("put"):
            #Code to send file
            with open(command.split()[1], 'rb') as f:
                bytes_sent = f.read(4096)
                while bytes_sent:
                    data_transfer_socket.send(bytes_sent)
                    bytes_sent = f.read(4096)
            print("File uploaded successfully.")
        data_transfer_socket.close()
        data_socket.close()
    else:
        #For non-transfer commands, receive normal response
        response = sock.recv(4096).decode()
        print(response)

def main(server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))

    try:
        while True:
            command = input("ftp> ")
            if command.upper().startswith('QUIT'):
                send_command(sock, 'QUIT')
                break
            else:
                send_command(sock, command)
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <server machine> <server port>")
        sys.exit(1)
    server = sys.argv[1]
    port = int(sys.argv[2])
    main(server, port)