import socket
import sys
import os

def send_command(sock, command):
    sock.send(command.encode())
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