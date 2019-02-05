import socket
from threading import Thread
import time
import pyautogui
from pyautogui import press, typewrite, hotkey
import selectors
import types
import os
import sys
import csv
import FileDirectory
import uuid
sel = selectors.DefaultSelector()
pyautogui.FAILSAFE = False


global connected
global started
global dict
global IP
global a
global b
global conn
global sock1
global sock2
global In_Messaging
global enter
global back_message
global back
global message
global go_back
global key
global break_all


started = False

break_all = False

back = False
message = False

show_ls = True


go_back = False

dict = {}

results = []

sock1 = None

connected = False
enter = False


def accept_wrapper(sock):
    global break_all
    global conn
    if not str(sock).__contains__('[closed]'):
        conn, addr = sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
        if break_all == True:
            print('breaking')
            return



def service_connection(key, mask):
    global sock
    global sock1
    global dictList
    global Position
    global IP
    global connected
    global In_Messaging
    global new_client
    global enter
    global back
    global show_ls
    global dict
    global break_all
    sock = key.fileobj
    data = key.data
    if break_all == True:
        return
    if not str(sock).__contains__('[closed]'):
        if not str(sock).__contains__('[closed]'):
            if sock not in dict.values():
                if not str(sock).__contains__('[closed]'):
                    new_client = True
                    random = str(uuid.uuid4())
                    random = random[:4]
                    random = 'temporary' + str(random)
                    dict[str(random)] = sock
                    print(dict)
                    if len(dict) > 1:
                        with open('Profiles.csv', 'r') as f:
                            print("Please wait for system to configure new computer...")
                            if break_all == True:
                                return
                            try:
                                time.sleep(1)
                                Computer_Name = sock.recv(1024).decode()
                            except:
                                Computer_Name = "failed"
                            results = f.readlines()
                            mystring = ''.join(results)
                            newstring = mystring.split(',')
                            length = len(newstring)
                            length = length - 1
                            i = 0
                            detected = False
                            while i != length:
                                Name = newstring[i]
                                i += 1
                                PC_Name = newstring[i]
                                i += 1
                                print("Computer profile list: ")
                                print('\t' + Name + " - " + PC_Name)
                                if Computer_Name == PC_Name:
                                    print('detected -> ' + Name + " -> Hostname -> " + PC_Name)
                                    detected = True
                                    print(dict)
                                    del dict[random]
                                    if Name in dict:
                                        print("Computer with same hostname found. Creating temporary name for client...")
                                        random = str(uuid.uuid4())
                                        random = random[:4]
                                        Name = Name + str(random)
                                    dict[Name] = sock
                                    ls_func()
                                    print(dict)
                                    new_client = False
                                    if In_Messaging == True:
                                        back_func()
                                    else:
                                        enter_func()
                                    i = length

                                if Computer_Name == "failed":
                                    if not str(sock).__contains__('[closed]'):
                                        print('could not get hostname. Assigning random value for computer')
                                        detected = True
                                        print(dict)
                                        try:
                                            del dict[random]
                                            random = str(uuid.uuid4())
                                            random = random[:4]
                                            Name = "COMPUTER" + str(random)
                                            show_ls = True
                                            if show_ls == True:
                                                dict[Name] = sock
                                                show_ls = False
                                                ls_func()
                                            print(dict)
                                            new_client = False
                                            if In_Messaging == True:
                                                back_func()
                                            else:
                                                enter_func()
                                            i = length
                                        except:
                                            print('Error connecting. Device may need to restart')
                                    else:
                                        print('Closed socket... Removing from system')
                                        detected = True
                                        enter_func()


                            if detected == False:
                                print('New computer detected. Please wait for system to configure')
                                time.sleep(1)
                                enter = True
                                one = input("What is the name of this computer: ")
                                del dict[random]
                                dict[one] = sock
                                print(dict)
                                new_client = False
                                with open(""
                                          "Profiles.csv", 'a', newline='') as resultFile:
                                    wr = csv.writer(resultFile, delimiter=',', lineterminator='\r')
                                    comma = ''
                                    row = [one, Computer_Name, comma]
                                    wr.writerow(row)
                                if In_Messaging == True:
                                    back_func()
                                else:
                                    enter_func()
                    else:
                        with open('Profiles.csv', 'r') as f:
                            print("Please wait for system to configure new computer...")
                            try:
                                time.sleep(1)
                                Computer_Name = sock.recv(1024).decode()
                            except:
                                Computer_Name = "failed"
                            results = f.readlines()
                            mystring = ''.join(results)
                            newstring = mystring.split(',')
                            length = len(newstring)
                            length = length - 1
                            i = 0
                            detected = False
                            while i != length:
                                Name = newstring[i]
                                i += 1
                                PC_Name = newstring[i]
                                i += 1
                                print("Computer profile list: ")
                                print('\t' + Name + " - " + PC_Name)
                                if Computer_Name == PC_Name:
                                    print('detected -> ' + Name + " -> Hostname -> " + PC_Name)
                                    detected = True
                                    del dict[random]
                                    dict[Name] = sock
                                    ls_func()
                                    print(dict)
                                    new_client = False
                                    i = length
                                    if started == True:
                                        enter_func()

                                try:
                                    if Computer_Name == "failed":
                                        if not str(sock).__contains__('[closed]'):
                                            print('could not get hostname. Assigning random value for computer')
                                            detected = True
                                            print(dict)
                                            try:
                                                del dict[random]
                                                random = str(uuid.uuid4())
                                                random = random[:4]
                                                Name = "COMPUTER" + str(random)
                                                show_ls = True
                                                if show_ls == True:
                                                    dict[Name] = sock
                                                    show_ls = False
                                                    ls_func()
                                                print(dict)
                                                new_client = False
                                                if In_Messaging == True:
                                                    back_func()
                                                else:
                                                    enter_func()
                                                i = length
                                            except:
                                                print('Error connecting. Device may need to restart')
                                        else:
                                            print('Closed socket... Removing from system')
                                            detected = True
                                            enter_func()
                                except:
                                    print("UNEXPECTED ERROR: This could probably be ignored")


                            if detected == False:
                                one = input("What is the name of this computer: ")
                                del dict[random]
                                dict[one] = sock
                                new_client = False
                                print("Adding " + one + "to computer profiles")
                                with open(""
                                          "Profiles.csv", 'a', newline='') as resultFile:
                                    wr = csv.writer(resultFile, delimiter=',', lineterminator='\r')
                                    comma = ''
                                    row = [one, Computer_Name, comma]
                                    wr.writerow(row)

    else:
        print("declined" + str(sock))


    if connected == False:
        connected = True

    try:
        got = True
        if mask & selectors.EVENT_READ:
            recv_data2 = sock.recv(1024).decode()
            got = False
            if recv_data2 != "--quit--":
                if recv_data2.__contains("--TEST--"):
                    dictList = []
                    [dictList.extend([k, v]) for k, v in dict.items()]
                    Position = dictList.index(sock) - 1
                    if str(recv_data2) == "--SENDING_FILE--":
                        print(recv_data2)
                        print('recieving file...')
                        sock3 = str(sock).rsplit("raddr=('", 1)[1]
                        sock3 = str(sock3).rsplit("',", 1)[0]
                        ip_to_send = sock3
                        print(ip_to_send)
                        with open("IP.txt", 'w', newline='') as resultFile:
                            resultFile.write(ip_to_send)
                            press('enter')

                        os.system('Get.py')
                        recv_data2 = sock.recv(1024).decode()

                elif str(recv_data2) == "--RM--":
                    print('Device requested remote connection... Entering remote status')
                    rm_func()

                else:
                    print('\n' + "Recieved message from -> " + dictList[Position] + " -> " + recv_data2)
                    enter = True
                    recv_data2 = sock.recv(1024).decode()

            else:
                print(dict)
                print('closing connection to', data.addr)
                sel.unregister(sock)
                sock.close()
                for x, y in dict.items():
                    if y == sock:
                        del dict[x]
                        break
                print(dict)
                if In_Messaging == True:
                    back_func()
                else:
                    enter_func()
    except:
        pass


def send_func(Q):
    global IP
    global In_Messaging
    length = len(dict)
    if length == 1:
        try:
            print('sending file to only connected client')
            for x in dict.values():
                message = "--SENDING_FILE--"
                message = message.encode("utf-8")
                sock1 = x
                sock1.send(message)
                print(" Please select file...")
                os.system('File_Sender.py')
        except:
            pass
    else:
        try:
            Q = Q.split('/send ', 1)[1]
            print(Q)
            if Q in str(dict):
                message = "--SENDING_FILE--"
                message = message.encode("utf-8")
                sock1 = dict[Q]
                sock1.send(message)
                print(" Please select file to send to -> " + Q)
                os.system('File_Sender.py')
            else:
                print("Computer not found. Please reference the computer list:")
                ls_func()
        except:
            print("Here is the list of computers:")
            ls_func()


def rm_func():
    message = ""
    while message != "/back":
        message = input(" -> ")
        if message == "/send":
            pass
        if message == "/get":
            pass
        if message == "/view":
            pass
    return

def view_func():
    global dict
    Q = input("Would you like to send or get?")
    if Q == "get":
        Q = input('On which computer would you like to view:\n')
        ls_func()
        print('Server')
    elif Q =="send":
        Q = input('On which computer would you like to view:\n')
        ls_func()
        print('Server')
    else:
        print('exiting program please try again with a proper input')
        return


    file = FileDirectory.main()




def enter_func():
    global enter
    press('enter')
    enter = False


def back_func():
    global back_message
    global back
    global In_Messaging
    print("Returning to main screen. Please hold")
    time.sleep(1)
    press('enter')
    time.sleep(1)
    back_message = "/back"
    back = True
    press('enter')
    In_Messaging = False
    go_back = False

def message_func(Q):
    global In_Messaging
    global back_message
    global back
    back = False
    back_message = ""
    length = len(dict)
    if length == 1:
        try:
            print('sending message to only connected client')
            for x in dict.values():
                while back_message != "/back":
                    if back == False:
                        In_Messaging = True
                        message = input(" -> ")
                        back_message = message
                        message = message.encode("utf-8")
                        sock1 = x
                        sock1.send(message)
                    else:
                        back_message = "/back"
                In_Messaging = False
        except:
            pass
    else:
        try:
            Q = Q.split('/m ', 1)[1]
            if Q in str(dict):
                back_message = ""
                while back_message != "/back":
                    if back == False:
                        In_Messaging = True
                        message = input("Sending message to -> " + Q + " -> ")
                        back_message = message
                        message = message.encode("utf-8")
                        sock1 = dict[Q]
                        sock1.send(message)
                    else:
                        back_message = "/back"
                In_Messaging = False
            else:
                print("Computer not found. Please reference the computer list:")
                ls_func()
        except:
            print("Here is the list of computers:")
            ls_func()


def ls_func():
    global dict
    for x in dict:
        print(x)
    #enter_func()


def help_func():
    print("/m - 'DEVICE NAME' --> Sends message to device, \n"
          "/m - all --> Sends message to all devices, \n"
          "/power 'DEVICE NAME' --> Turns on device, \n"
          "/shutdown 'DEVICE NAME' --> Shutsdown device, \n"
          "/ls --> Shows connected devices, \n"
          "/back --> Exists messaging menu, \n")


class Starter(Thread):
    global soc
    global data
    global new_data
    global enter
    global break_all

    def __init__(self):
        global soc
        global new_data
        global enter
        global break_all
        Thread.__init__(self)
        print("Starting server")
        self.running = True
        self.new_data = False

        host = ''
        port = 8888

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            lsock.bind((host, port))
        except:
            print("Bind failed. Error : " + str(sys.exc_info()))
            sys.exit()

        lsock.listen(5)
        print("Socket created")
        lsock.setblocking(False)
        sel.register(lsock,selectors.EVENT_READ, data=None)
        self.running = True


    def run(self):
        global enter
        global break_all
        while self.running:
            if break_all == True:
                print('breaking main')
                press('enter')
                return
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    if break_all == True:
                        print('breaking main')
                        return
                    accept_wrapper(key.fileobj)
                else:
                    if break_all == True:
                        print('breaking main')
                        return
                    service_connection(key, mask)


    def stop(self):
        self.running = False


class Send(Thread):
    global In_Messaging

    def __init__(self):
        Thread.__init__(self)
        global In_Messaging


    def run(self):
        global In_Messaging
        while True:
            In_Messaging = False
            Q = input(' -> ')
            self.Q = Q
            if Q == "":
                pass
            if Q == "/ls":
                ls_func()
            if Q.__contains__('/send'):
                send_func(Q)
            if Q == "/help":
                help_func()
            if Q.__contains__('/m'):
                message_func(Q)
            if Q == 'test':
                 i = len(dict)
                 i = 0
                 while i < len(dict):
                    check = list(dict.values())[i]
                    if str(check).__contains__('[closed]'):
                        print('problem found')
            if break_all == True:
                print('breaking Send')
                return


class Check(Thread):
    global enter
    global back
    global message
    global go_back
    global break_all
    global dict

    def __init__(self):
        global enter
        global back
        global message
        global break_all
        global dict
        Thread.__init__(self)
        print("Check thread started")

    def run(self):
        global enter
        global back
        global message
        global go_back
        global dict
        global break_all
        while True:
            if enter == True:
                enter_func()
            if go_back == True:
                back_func()
            if message == True:
                message_func()
            if break_all == True:
                print('breaking Check')
                return

class Check2(Thread):
    def __init__(self):
        global enter
        global back
        global message
        global dict
        global new_client
        global break_all
        Thread.__init__(self)
        print("Check thread started")

    def run(self):
        global new_client
        global break_all
        global dict
        while True:
            i = 0
            while i < len(dict):
                time.sleep(.5)
                if len(dict) != 0:
                    try:
                        soc = list(dict.values())[i]
                        message = "--TEST--"
                    except:
                        print('index error. Resetting check')
                        i = 0
                    try:

                        soc.send(message.encode("utf-8"))
                    except:
                        #new_client = False
                        print(dict)
                        print('closing connection to ' + str(list(dict.keys())[i]))
                        key = list(dict.keys())[i]
                        sock = list(dict.values())[i]
                        del dict[key]
                        print(dict)
                        try:
                            if not str(sock).__contains__('[closed]'):
                                sel.unregister(sock)
                                sock.close()
                                i = 0
                        except:
                            print('unable to close sock' + str(sock))
                        if In_Messaging == True:
                            back_func()
                        else:
                            enter_func()
                    i += 1


try:
    fh = open('Profiles.csv', 'r')
except:
    fh = open('Profiles.csv',"w+")
    print('creating profile database...')

try:
    fh = open('IP.txt', 'r')
except:
    fh = open('IP.txt',"w+")
    print('creating IP database...')


def getIpAddresses():
    addrList = socket.getaddrinfo(socket.gethostname(), None)

    ipList = []
    for item in addrList:
        print
        "Item:", item
        ipList.append(item[4][0])

    num = len(ipList)
    i = 0
    while i != num:
        if str(ipList[i]).__contains__("::"):
            ipList.remove(ipList[i])
            num = num-1
        print(ipList[i])
        i +=1
    return ipList


a = Starter()
getIpAddresses()
b = Send()
c = Check()
d = Check2()
a.start()

while connected == False:
    time.sleep(.1)

if connected == True:
    print("Send started")
    b.start()
    started = True
    c.start()
    d.start()