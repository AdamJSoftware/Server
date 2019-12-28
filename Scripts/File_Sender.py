import socket
import time
from Scripts import FileDirectory
import os
import sys


def main(sock, port):

    print('USING PORT: {}'.format(port))

    s = socket.socket()  # Create a socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = ""  # Get local machine name
    try:
        s.bind((host, port))  # Bind to the port
    except Exception as e:
        print(e)
        return False
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')
    sock.send('--SENDING_FILE--'.encode("utf-8"))

    connection, address = s.accept()  # Establish connection with client.
    print('Got connection from', address)
    path = FileDirectory.main()
    if path == "":
        print("No file was selected. Closing Send")
        connection.close()
        exit()
    try:
        print(path)
        name = str(path).rsplit("/", 1)[1]
        name = name.encode("utf-8")
        connection.send(name)
        with open(path, 'rb') as f:
            print('Sending...')
            l = f.read(1024)
            while l:
                connection.send(l)
                l = f.read(1024)
        print('Finished sending')
        connection.close()
    except:
        print("Could not open file please try again")

    return True


def files_to_send(client_sock, name, port, path):
    print("PORT: {}".format(port))
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.settimeout(5)
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.
    message_to_send = "--GETFILES--"
    message_to_send = message_to_send.encode("utf-8")
    client_sock.sendall(message_to_send)

    print('Server listening....')

    conn, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    try:
        print(f"PATH: {path}")
        name = 'FTS.json'
        name = name.encode("utf-8")
        conn.send(name)
        time.sleep(1)  # Fix this
        with open(path, 'rb') as f:
            print('Sending...')
            l = f.read(1024)
            while l:
                conn.send(l)
                l = f.read(1024)
        print('Finished Sending sending')
        conn.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))

def get_ip_from_sock(sock):
    sock = str(sock).rsplit("raddr=('", 1)[1]
    sock = str(sock).rsplit("',", 1)[0]
    return sock


# if __name__ == '__main__':
#     main()
