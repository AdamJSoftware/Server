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

global accepted
global recv_computername
global waiting_on_server
global done
global test_computername
global connected
global started
global key
global replacing_dict
global dict
global IP
global a
global b
global conn
global sock1
global sock2
global got
global In_Messaging
global enter
global back_message
global back
global message
global go_back
global key
global break_all

replacing_dict = False
waiting_on_server = False
started = False
break_all = False
back = False
message = False
got = False
show_ls = True
go_back = False
dict = {}
results = []
sock1 = None
connected = False

sel = selectors.DefaultSelector()
pyautogui.FAILSAFE = False


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


def get_ip_addresses_func():
    addrList = socket.getaddrinfo(socket.gethostname(), None)

    ipList = []
    for item in addrList:
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


def enter_func():
    press('enter')


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


def help_func():
    print("/m - 'DEVICE NAME' --> Sends message to device, \n"
          "/m - all --> Sends message to all devices, \n"
          "/power 'DEVICE NAME' --> Turns on device, \n"
          "/shutdown 'DEVICE NAME' --> Shutsdown device, \n"
          "/ls --> Shows connected devices, \n"
          "/back --> Exists messaging menu, \n")


def ls_func():
    global dict
    for x in dict:
        print(x)


def send_func(Q, rm):
    global IP
    global In_Messaging
    global soc
    rm = rm
    length = len(dict)
    if length == 1:
        try:
            if rm is True:
                message = 'sending file to only connected client'
                print(message)
                soc.sendall(message.encode(1024))
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
    rm = True
    message = ""
    length = len(dict)
    while message != "/back":
        message = input(" -> ")
        if message.__contains__("/send"):
            send_func(message, rm)
        if message.__contains__("/get"):
            pass
        if message.__contains__("/view"):
            pass
    return


def accept_wrapper(sock):
    global break_all
    global conn
    global accepted
    if not str(sock).__contains__('[closed]'):
        print('SOCK DOES NOT CONTAIN STRING')
        conn, addr = sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
        accepted = True


def service_connection(key, mask):
    global sock
    global recv_computername
    global selectors
    global sock1
    global dictList
    global Position
    global replacing_dict
    global IP
    global connected
    global In_Messaging
    global new_client
    global enter
    global back
    global show_ls
    global dict
    global waiting_on_server
    global got
    global break_all
    global done
    global accepted
    sock = key.fileobj
    done = True
    if accepted is True:
        if not str(sock).__contains__('[closed]'):
            if not str(sock).__contains__('[closed]'):
                if sock not in dict.values():
                    if not str(sock).__contains__('[closed]'):
                        if replacing_dict is False:
                            done = False
                            new_client = True
                            random = str(uuid.uuid4())
                            random = random[:4]
                            random = 'temporary' + str(random)
                            dict[str(random)] = sock
                            print(dict)
                            if len(dict) > 1:
                                with open('Profiles.txt', 'r') as f:
                                    print("Please wait for system to configure new computer...")
                                    if break_all == True:
                                        return
                                    try:
                                        got = False
                                        waiting_on_server = True
                                        print('waiting to recieve computer name')
                                        time.sleep(2)
                                        Computer_Name = recv_computername
                                        waiting_on_server = False
                                        got = True
                                    except:
                                        Computer_Name = "failed"
                                    results = f.read().split(',')
                                    print(results)
                                    length = len(results)
                                    length = length - 1
                                    i = 0
                                    detected = False
                                    while i != length:
                                        Name = results[i]
                                        i += 1
                                        PC_Name = results[i]
                                        i += 1
                                        print("Computer profile list: ")
                                        print('\t' + Name + " - " + PC_Name)
                                        if Computer_Name == PC_Name:
                                            try:

                                                print('detected -> ' + Name + " -> Hostname -> " + PC_Name)
                                                detected = True
                                                print(dict)
                                                del dict[random]
                                                if Name in dict:
                                                    print(
                                                        "Computer with same hostname found. Creating temporary name for client...")
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
                                            except:
                                                print('an unknown error occured')

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
                                                    print('Error connecting. Device may need to restart (006)')
                                            else:
                                                print('Closed socket... Removing from system')
                                                detected = True
                                                enter_func()

                                    if detected == False:
                                        try:
                                            print('New computer detected. Please wait for system to configure')
                                            enter_func()
                                            time.sleep(1)
                                            one = input("What is the name of this computer: ")
                                            print("Naming this computer " + one)
                                            del dict[random]
                                            dict[one] = sock
                                            print(dict)
                                            new_client = False
                                            comma = ","
                                            with open("Profiles.txt", 'a', newline='') as resultFile:
                                                resultFile.write(one + comma + Computer_Name + comma)
                                            if In_Messaging == True:
                                                back_func()
                                            else:
                                                enter_func()
                                        except:
                                            print("Error adding new computer. Check delete (005)")
                            else:
                                with open('Profiles.txt', 'r') as f:
                                    print("Please wait for system to configure new computer...")
                                    try:
                                        got = False
                                        waiting_on_server = True
                                        print('waiting to recieve computer name')
                                        try:
                                            c.start()
                                        except:
                                            pass
                                        time.sleep(4)
                                        Computer_Name = recv_computername
                                        waiting_on_server = False
                                        got = True
                                    except:
                                        Computer_Name = "failed"
                                    results = f.read().split(',')
                                    print(results)
                                    length = len(results)
                                    length = length - 1
                                    i = 0
                                    detected = False
                                    while i != length:
                                        Name = results[i]
                                        i += 1
                                        PC_Name = results[i]
                                        i += 1
                                        print("Computer profile list: ")
                                        print('\t' + Name + " - " + PC_Name)
                                        try:
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
                                        except:
                                            print(
                                                'Error while adding computer to current database. Program may need to restart (004)')

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
                                                        print('Error connecting. Device may need to restart (003)')
                                                else:
                                                    print('Closed socket... Removing from system')
                                                    detected = True
                                                    enter_func()
                                        except:
                                            print("UNEXPECTED ERROR: This could probably be ignored (002)")

                                    if detected == False:
                                        try:
                                            one = input("What is the name of this computer: ")
                                            del dict[random]
                                            dict[one] = sock
                                            new_client = False
                                            print("Adding " + one + " to computer profiles")
                                            comma = ","
                                            with open("Profiles.txt", 'a', newline='') as resultFile:
                                                resultFile.write(one + comma + Computer_Name + comma)
                                        except:
                                            print("Error while adding computer to profile list (001)")
                        else:
                            print("declined" + str(sock))
                if connected == False:
                    connected = True
        done = True
        accepted = False


class Starter(Thread):
    global soc
    global data
    global new_data
    global enter
    global break_all
    global key

    def __init__(self):
        global soc
        global new_data
        global enter
        global break_all
        global key
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
        global key
        while self.running:
            events = sel.select()
            for key, mask in events:
                if key.data is None:
                    if not str(key.fileobj).__contains__("[closed]"):
                        accept_wrapper(key.fileobj)
                        print("FILEOBJECT" + str(key.fileobj))
                    else:
                        print('rejected closed socket')
                else:
                    if not str(key.fileobj).__contains__("[closed]"):
                        service_connection(key, mask)


class Send(Thread):
    global In_Messaging

    def __init__(self):
        Thread.__init__(self)
        global In_Messaging

    def run(self):
        global In_Messaging
        rm = False
        while True:
            In_Messaging = False
            Q = input(' -> ')
            self.Q = Q
            if Q == "":
                pass
            if Q == "/ls":
                ls_func()
            if Q.__contains__('/send'):
                send_func(Q, rm)
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


class Recieve(Thread):
    global enter
    global back
    global message
    global go_back
    global got
    global recv_computername
    global sock
    global waiting_on_server
    global break_all
    global key
    global dict

    def __init__(self):
        global enter
        global waiting_on_server
        global back
        global message
        global sock
        global break_all
        global dict
        global got
        global recv_computername
        global key
        Thread.__init__(self)
        print("Receive thread initiallized")

    def run(self):
        print('Recieve thread started')
        time.sleep(2)
        global recv_computername
        global key
        global enter
        global back
        global message
        global sock
        global got
        global go_back
        global dict
        global break_all
        global waiting_on_server
        while True:
            try:
                recv_data = sock.recv(1024).decode()
                if str(recv_data).__contains__("--PCNAME--||"):
                    test_computername = str(recv_data).split("||")[1]
                    print("received computer name -> " + test_computername)
                    recv_computername = str(test_computername)
                else:
                    if recv_data != "--quit--":
                        if str(recv_data) == "--SENDING_FILE--":
                            print(recv_data)
                            print('recieving file...')
                            sock3 = str(sock).rsplit("raddr=('", 1)[1]
                            sock3 = str(sock3).rsplit("',", 1)[0]
                            ip_to_send = sock3

                            print(ip_to_send)
                            with open("IP.txt", 'w', newline='') as resultFile:
                                resultFile.write(ip_to_send)
                                press('enter')
                            os.system('Get.py')
                            # recv_data = sock.recv(1024).decode()
                        elif str(recv_data) == "--RM--":
                            print('Device requested remote connection... Entering remote status')
                            rm_func()
                        else:
                            dictList = []
                            [dictList.extend([k, v]) for k, v in dict.items()]
                            Position = dictList.index(sock) - 1
                            print('\n' + "Recieved message from -> " + dictList[Position] + " -> " + recv_data)
                            enter_func()
                            # recv_data = sock.recv(1024).decode()
            except:
                pass

                '''print(dict)
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
                        '''

                '''else:
                    if got is False:
                        recv_data = sock.recv(1024).decode()
                        if str(recv_data).__contains__("--PCNAME--||"):
                            test_computername = str(recv_data).split("||")[1]
                            print("recieved computer name -> hey" + test_computername)
                            recv_computername = str(test_computername)
                        time.sleep(.1)
                        '''



class Check2(Thread):
    def __init__(self):
        global done
        global enter
        global back
        global message
        global dict
        global new_client
        global break_all
        global replacing_dict
        Thread.__init__(self)
        print("Check thread started")

    def run(self):
        global new_client
        global break_all
        global dict
        global done
        global replacing_dict
        while True:
            i = 0
            if done is True:
                for x in dict:
                    if str(x).__contains__("\n"):
                        replacing_dict = False
                        print('replacing dict')
                        oldkey = x
                        oldvalue = dict[x]
                        del dict[x]
                        newx = str(x).split("\n")[0]
                        print(newx)
                        if newx == "":
                            print('switching')
                            newx = str(x).split("\n")[1]
                        dict[newx] = oldvalue
                        replacing_dict = True
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
    fh = open('Profiles.txt', 'r')
except:
    fh = open('Profiles.txt', "w+")
    print('creating profile database...')

try:
    fh = open('IP.txt', 'r')
except:
    fh = open('IP.txt',"w+")
    print('creating IP database...')

if __name__ == '__main__':
    a = Starter()
    get_ip_addresses_func()
    b = Send()
    c = Recieve()
    d = Check2()
    a.start()

    while connected == False:
        time.sleep(.1)

    if connected == True:
        print("Send started")
        started = True
        b.start()
        d.start()