import pyautogui
from pyautogui import press
import sys
import socket
import os
pyautogui.FAILSAFE = False


def main():
    press('enter')
    print('started get.py')
    with open("Resources/IP.txt", 'r') as f:
        IP_TO_SEND = f.read()
        if IP_TO_SEND == "":
            print('Started twice... exiting')
            sys.exit()
        else:
            # Import socket module
            import time

            s = socket.socket()

            host = IP_TO_SEND  # Ip address that the TCPServer  is there
            port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

            try:
                s.connect((host, port))
                print('started reciever')
            except:
                print('Started twice... exiting')
                press('enter')
                sys.exit()
            name = s.recv(1024)
            with open(name, 'wb') as f:
                print('receiving data...')
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    f.write(data)

            f.close()
            print('Successfully got the file')
            s.close()
            print('connection closed')
            with open("IP.txt", 'w') as f:
                f.write("")

def backup():
    with open("IP.txt", 'r') as f:
        IP_TO_SEND = f.read()
        if IP_TO_SEND == "":
            print('Started twice... exiting')
            sys.exit()
        else:
            # Import socket module

            s = socket.socket()

            host = IP_TO_SEND  # Ip address that the TCPServer  is there
            port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

            try:
                s.connect((host, port))
                print('started reciever')
            except:
                print('Started twice... exiting')
                press('enter')
                sys.exit()
            name = s.recv(1024)
            name = name.decode("utf-8")
            print("NAME " + str(name))
            try:
                name = name.split("||")[0]
            except:
                pass
            try:
                os.mkdir("Resources\\Backups\\" + name)
            except:
                pass
            with open("Resources\\Backups\\" + name + "\\Received_Backup.txt", 'wb') as f:
                print('receiving data...')
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    f.write(data)

            f.close()
            print('Successfully got the file')
            s.close()
            print('connection closed')
            with open("IP.txt", 'w') as f:
                f.write("")

    return name

def write_backup_file(PC):
    with open("Resources/IP.txt", 'r') as f:
        IP_TO_SEND = f.read()
        if IP_TO_SEND == "":
            print('Started twice... exiting')
            sys.exit()
        else:
            # Import socket module
            import time

            s = socket.socket()

            host = IP_TO_SEND  # Ip address that the TCPServer  is there
            port = 50000  # Reserve a port for your service every new transfer wants a new port or you must wait.

            try:
                s.connect((host, port))
                print('started reciever')
            except:
                print('Started twice... exiting')
                press('enter')
                sys.exit()
            name = s.recv(1024)
            name = name.decode("utf-8")
            print("NAME " + name)
            time.sleep(1)
            path = "Resources\\Backups\\" + PC + "\\" + name
            try:
                path = path.split("\n")[0]
            except:
                pass
            print(path)
            with open(path, 'wb') as f:
                print('receiving data...')
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    f.write(data)
            f.close()
            print('Successfully got the file')
            s.close()
            print('connection closed')
            with open("IP.txt", 'w') as f:
                f.write("")



if __name__ == '__main__':
    main()
