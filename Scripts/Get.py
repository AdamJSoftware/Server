import pyautogui
from pyautogui import press
import sys
import socket
import os
import time
global can_connect
pyautogui.FAILSAFE = False


def error_log(error):
    with open("Resources/ErrorLog.txt", 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")


def error_print(error_message, error):
    print("SYSTEM ERROR - " + error_message + ": " + str(error))


def main(port, ip_to_send):
    global can_connect
    press('enter')
    print('started get.py')

    s = socket.socket()
    print("PORT: {}".format(port))
    print("host", ip_to_send)

    host = ip_to_send  # Ip address that the TCPServer  is there

    try:
        s.settimeout(10)
        s.connect((host, port))
        print('Connected to server')
    except Exception as error:
        error_log(error)
        error_print("Get.py - error while connecting to server", error)
        press('enter')
        sys.exit()
    name = s.recv(1024)
    print('received name {}'.format(name.decode()))
    try:
        with open(name, 'wb') as f:
            print('Receiving data...')
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
    except Exception as e:
        print(e)
    f.close()
    print('Successfully got the file')
    s.close()
    print('connection closed')



def backup(host, port):
    s = socket.socket()


    try:
        s.settimeout(10)
        s.connect((host, port))
        print('started receiver')
    except Exception as error:
        print(error)
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
        os.mkdir("Resources/Backups/" + name)
    except:
        pass
    with open("Resources/Backups/" + name + "/Received_Backup.txt", 'wb') as f:
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


    return name


def write_backup_file(pc, host, port):
    global can_connect
    s = socket.socket()

    print('socket binded')

    try:
        s.settimeout(10)
        s.connect((host, port))
        print('started Receiver')
    except Exception as error:
        print(error)
        press('enter')
        sys.exit()
    name = s.recv(1024)
    name = name.decode("utf-8")
    print("NAME " + name)
    time.sleep(1)
    path = "Resources/Backups/" + pc + "/" + name
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