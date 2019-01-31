import socket
import FileDirectory
port = 50000                    # Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket()             # Create a socket object
host = ""   # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print('Server listening....')


conn, addr = s.accept()     # Establish connection with client.
print('Got connection from', addr)
path = FileDirectory.main()
if path == "":
    print("No file was selected. Closing Send")
    conn.close()
    exit()
try:
    name = str(path).rsplit("/", 1)[1]
    name = name.encode("utf-8")
    conn.send(name)
    with open(path, 'rb') as f:
        print('read')
        l = f.read(1024)
        while l:
            conn.send(l)
            l = f.read(1024)
    print('Done sending')
    conn.close()
except:
    print("Could not open file please try again")