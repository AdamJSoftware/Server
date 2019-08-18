import socket
from Scripts import FileDirectory


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


def get_files(path, port):
    print("PORT: {}".format(port))
    s = socket.socket()  # Create a socket object
    host = ""  # Get local machine name
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    print('Server listening....')

    conn, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    try:
        print(path)
        name = str(path).rsplit("/", 1)[1]
        name = name.encode("utf-8")
        conn.send(name)
        with open(path, 'rb') as f:
            print('Sending...')
            l = f.read(1024)
            while l:
                conn.send(l)
                l = f.read(1024)
        print('Finished Sending sending')
        conn.close()
    except Exception as e:
        print("Could not open file please try again")
        print(e)

    return True


def get_ip_from_sock(sock):
    sock = str(sock).rsplit("raddr=('", 1)[1]
    sock = str(sock).rsplit("',", 1)[0]
    return sock




# if __name__ == '__main__':
#     main()