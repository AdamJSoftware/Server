import os
import socket
import sys
import time
import types
import uuid
from threading import Thread

import FileDirectory
import pyautogui
from pyautogui import press
import selectors

global rm_first
global rm_message
global rm_sock
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
global sock
global In_Messaging
global enter
global back_message
global back
global message
global go_back
global key

replacing_dict = False
waiting_on_server = False
started = False
back = False
message = False
got = False
show_ls = True
go_back = False
dict = {}
results = []
sock1 = None
connected = False
In_Messaging = False
rm = False
rm_first = "--RM_MESSAGE--"

sel = selectors.DefaultSelector()
pyautogui.FAILSAFE = False

def rm_send():
    pass


def view_func():
    global dict
    Q = input("Would you like to send or get?")
    if Q == "get":
        Q = input('On which computer would you like to view:\n')
        ls_func()
        print('Server')
    elif Q == "send":
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
    print("SYSTEM: Connect to server with these addresses:")
    print("\t" + socket.gethostname())
    while i != num:
        if str(ipList[i]).__contains__("::"):
            ipList.remove(ipList[i])
            num = num - 1
        print("\t" + ipList[i])
        i += 1
    return ipList


def enter_func():
    press('enter')


def PC_and_IP():
    global dict
    i = 1
    for x in dict:
        raddr = str(dict).split("raddr=")[i]
        raddr = raddr.split(">")[0]
        print("\t" + x + " -> IP  -> " + raddr)
        i += 1



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
    global rm_message
    global rm
    global rm_sock
    global In_Messaging
    global back_message
    global back
    back = False
    back_message = ""
    length = len(dict)
    if length == 1:
        try:
            only_client = 'sending message to only connected client'
            if rm is True:
                print(only_client)
                rm_sock.sendall(only_client.encode("utf-9"))
            else:
                print(only_client)
            for x in dict.values():
                if rm is True:
                    message = rm_message
                else:
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
                if rm is True:
                    print("Computer not found. Please reference the computer list:")
                    rm_sock.sendall("Computer not found. Please reference the computer list:")
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
    global rm
    global rm_sock
    global rm_first
    CCC = "Computer currently connected:"
    if rm is True:
        print('RMM')
        print(CCC)
        message = rm_first + CCC
        rm_sock.send(message.encode("utf-8"))
        for x in dict:
            print("\t" + x)
            rm_sock.sendall((rm_first + "\t" + x).encode("utf-8"))
    else:
        print("Computers currently connected:")
        for x in dict:
            print("\t" + x)


def send_func(Q):
    global IP
    global In_Messaging
    global soc
    global rm
    global rm_sock
    length = len(dict)
    if length == 1:
        try:
            message = 'sending file to only connected client'
            if rm is True:
                print(message)
                rm_sock.sendall(message.encode("utf-8"))
            else:
                print(message)
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


def rm_func(sock):
    global rm_sock
    global rm
    rm_sock = sock
    rm = True
    message = ""
    length = len(dict)
    '''
    while message != "/back":
        message = input(" -> ")
        if message.__contains__("/send"):
            send_func(message, rm)
        if message.__contains__("/get"):
            pass
        if message.__contains__("/view"):
            pass
    return
'''

def accept_wrapper(sock):
    global conn
    global accepted
    global rm
    global rm_sock
    conn, addr = sock.accept()  # Should be ready to read
    if rm is True:
        print('Accepted connection from', addr)
        rm_sock.sendall(('Accepted connection from' + str(addr)).encode("utf-8"))
    else:
        print('Accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    accepted = True


def service_connection(key, mask):
    global sock
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
    global done
    global accepted
    sock = key.fileobj
    done = True
    if sock not in dict.values():
        if accepted is True:
            if replacing_dict is False:
                new_client = True
                random = str(uuid.uuid4())
                random = random[:4]
                random = 'temporary' + str(random)
                dict[str(random)] = sock
                with open('Profiles.txt', 'r') as f:
                    print("Please wait for system to configure new computer...")
                    try:
                        got = False
                        waiting_on_server = True
                        print('Waiting to receive computer name')
                        try:
                            c.start()
                        except:
                            pass
                        while done is True:
                            time.sleep(.1)
                        Computer_Name = recv_computername
                        print("Received computer name -> " + Computer_Name)
                        waiting_on_server = False
                        got = True
                    except:
                        Computer_Name = "failed"
                    results = f.read().split(',')
                    length = len(results)
                    length = length - 1
                    i = 0
                    detected = False
                    print("Computer profile list: ")
                    while i != length:
                        Name = results[i]
                        i += 1
                        PC_Name = results[i]
                        i += 1
                        print('\t' + Name + " - " + PC_Name)
                    i = 0
                    while i != length:
                        Name = results[i]
                        i += 1
                        PC_Name = results[i]
                        i += 1
                        try:
                            if Computer_Name == PC_Name:
                                print('Detected -> ' + Name + " -> Hostname -> " + PC_Name)
                                detected = True
                                del dict[random]
                                if Name in dict:
                                    print("Computer with same hostname found. Creating temporary name for client...")
                                    random = str(uuid.uuid4())
                                    random = random[:4]
                                    Name = Name + str(random)
                                dict[Name] = sock
                                print('Computers currently connected:')
                                PC_and_IP()
                                new_client = False
                                if In_Messaging == True:
                                    back_func()
                                else:
                                    enter_func()
                                i = length
                                if started is True:
                                    enter_func()
                        except:
                            print('an unknown error occured')
                        try:
                            if Computer_Name == "failed":
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
                        except:
                            pass

                    if detected == False:
                        try:
                            print('New computer detected. Please wait for system to configure')
                            enter_func()
                            time.sleep(1)
                            one = input("What is the name of this computer: ")
                            del dict[random]
                            dict[one] = sock
                            print(dict)
                            new_client = False
                            print("Adding " + one + " to computer profiles")
                            comma = ","
                            with open("Profiles.txt", 'a', newline='') as resultFile:
                                resultFile.write(one + comma + Computer_Name + comma)
                            if In_Messaging == True:
                                back_func()
                            else:
                                enter_func()
                        except:
                            print("Error adding new computer. Check delete (005)")
        if connected == False:
            connected = True
        done = True
        accepted = False
        got = False



class Starter(Thread):
    global soc
    global data
    global new_data
    global enter
    global key

    def __init__(self):
        global soc
        global new_data
        global enter
        global key
        Thread.__init__(self)
        print("SYSTEM: Starting server")
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
        print("SYSTEM: Socket created")
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)
        self.running = True

    def run(self):
        global enter
        global key
        while self.running:
            events = sel.select()
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)


class Send(Thread):
    global In_Messaging
    global rm_sock
    global rm

    def __init__(self):
        Thread.__init__(self)
        global In_Messaging
        global rm
        global rm_sock
        print("SYSTEM: Send initialized")

    def run(self):
        print("SYSTEM: Send started")
        global In_Messaging
        global rm
        global rm_sock
        rm = False
        while True:
            if rm is True:
                Q = input(' -> test ')
                rm_sock.send(Q.encode("utf-8"))
            else:
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


class Receive(Thread):
    global sock
    global enter
    global back
    global message
    global go_back
    global got
    global recv_computername
    global waiting_on_server
    global key
    global dict
    global done
    global rm

    def __init__(self):
        global rm_sock
        global rm
        global enter
        global waiting_on_server
        global back
        global message
        global sock
        global dict
        global got
        global recv_computername
        global key
        global done
        Thread.__init__(self)
        print("SYSTEM: Receive initialized")

    def run(self):
        global rm
        global rm_sock
        print('SYSTEM: Receive started')
        global recv_computername
        global key
        global enter
        global back
        global message
        global sock
        global got
        global go_back
        global dict
        global waiting_on_server
        global done
        success = False
        while True:
            if got is False:
                try:
                    my_dict = dict
                    for x in my_dict.values():
                        if success is False:
                            try:
                                # print('working')
                                sock = x
                                recv_data = sock.recv(1024).decode()
                                success = True
                                used_sock = sock
                                if rm is True:
                                    if str(recv_data).__contains__("--PCNAME--||"):
                                        if done is True:
                                            recv_computername = str(recv_data).split("||")[1]
                                            done = False
                                    else:
                                        if str(recv_data) == "/send":
                                            ls_func()
                                        elif str(recv_data).__contains__("/send "):
                                            message = recv_data.split("/send ")[1]
                                            send_func(message)

                                else:
                                    if str(recv_data).__contains__("--PCNAME--||"):
                                        if done is True:
                                            recv_computername = str(recv_data).split("||")[1]
                                            done = False
                                    else:
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
                                            print('remote')
                                            dictList = []
                                            [dictList.extend([k, v]) for k, v in my_dict.items()]
                                            Position = dictList.index(x) - 1
                                            print(dictList[
                                                      Position] + ' requested remote connection... Entering remote status')
                                            rm_func(sock)
                                        else:
                                            dictList = []
                                            [dictList.extend([k, v]) for k, v in my_dict.items()]
                                            Position = dictList.index(sock) - 1
                                            message = ('\n' + "Recieved message from -> " + dictList[
                                                Position] + " -> " + recv_data)
                                            print(message)
                                            if rm is True:
                                                rm_sock.sendall(message.encode(1024))
                                            enter_func()
                                            # recv_data = sock.recv(1024).decode()
                                    success = False
                            except:
                                pass
                except:
                    pass


class Check(Thread):
    def __init__(self):
        global done
        global enter
        global back
        global message
        global dict

        global new_client
        global replacing_dict
        Thread.__init__(self)
        print("SYSTEM: Check initialized")

    def run(self):
        global new_client
        global dict
        global done
        global replacing_dict
        print("SYSTEM: Check started")
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
                        # new_client = False
                        print(dict)
                        print('closing connection to ' +
                              str(list(dict.keys())[i]))
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
    fh = open('IP.txt', "w+")
    print('creating IP database...')

if __name__ == '__main__':
    a = Starter()
    # Runs the starting class which creates the class and also connects clients to the server
    get_ip_addresses_func()
    b = Send()
    c = Receive()
    d = Check()
    a.start()

    while connected == False:
        time.sleep(.1)

    if connected == True:
        started = True
        d.start()
        b.start()

