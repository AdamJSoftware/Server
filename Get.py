print('started get.py')
import pyautogui
from pyautogui import press
pyautogui.FAILSAFE = False
press('enter')
import sys
with open("IP.txt", 'r') as f:
    IP_TO_SEND = f.read()
    if IP_TO_SEND == "":
        print('Started twice... exiting')
        sys.exit()
    else:
        # Import socket module
        import socket

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

                # write data to a file
                f.write(data)

        f.close()
        print('Successfully got the file')
        s.close()
        print('connection closed')
        with open("IP.txt", 'w') as f:
            f.write("")