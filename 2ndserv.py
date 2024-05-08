# server.py
import socket
import os
import sys

def list_files(connection):
    files = os.listdir('.')
    files_str = '\n'.join(files)
    connection.sendall(files_str.encode())
    print("Sent list of files to client.")

def get_file(connection, filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
          filecontent = f.read()
        connection.sendall(filecontent)
        print(f"File {filename} sent successfully to client.")
    else:
        connection.sendall('File not found'.encode())
        print(f"File {filename} not found on server.")
    
def put_file(connection, filename, data_socket):
    with open(filename, 'wb') as f:
        while True:
            file_data = data_socket.recv(1024)
            if not file_data:
                break
            f.write(file_data)
    print(f"File {filename} received successfully from client.")

def handle_client(connection, client_address):
    print(f"Connection established with {client_address}")
    try:
        while True:
            command = connection.recv(1024).decode()
            if not command:
                break  # Client disconnected
            print(f"Received command: {command}")
            cmd_parts = command.split()
            action = cmd_parts[0].upper()

            if action == 'GET' and len(cmd_parts) > 1:
                get_file(connection, cmd_parts[1])
            elif action == 'PUT' and len(cmd_parts) > 1:
                data_port = int(connection.recv(1024).decode())
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect((client_address[0], data_port))
                put_file(connection, cmd_parts[1], data_socket)
                data_socket.close()
            elif action == 'LIST':
                list_files(connection)
            elif action == 'QUIT':
                print("Client requested to quit.")
                connection.close()
                break
            else:
                connection.sendall('Invalid command'.encode())
    finally:
        connection.close()
        print(f"Connection with {client_address} closed")


def main(port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', port))
    server_sock.listen(1)
    print(f"Server is listening on port {port}")

    try:
        while True:
            client_sock, client_address = server_sock.accept()
            handle_client(client_sock, client_address)
    finally:
        server_sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <port number>")
        sys.exit(1)
    port_num = int(sys.argv[1])
    main(port_num)