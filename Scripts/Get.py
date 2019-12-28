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
    print("CONNECTING TO " + host + " " + str(port))
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
    with open("Resources/Backups/" + name + "/received_backup.json", 'wb') as f:
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

    return


def write_backup_file(pc, host, port, backup_directory):
    try:
        global can_connect
        s = socket.socket()

        print('socket binded')

        try:
            s.settimeout(10)
            s.connect((host, port + 2))
            print('started Receiver')
        except Exception as error:
            print(error)
            press('enter')
            sys.exit()
        name = s.recv(1024)
        name = name.decode("utf-8")
        name = name.split("\\")
        new_name = ""
        for item in name:
            new_name = os.path.join(new_name, item)
        name = new_name
        print("FILE NAME: " + name)
        time.sleep(1)
        path = os.path.join(backup_directory, name)
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
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))