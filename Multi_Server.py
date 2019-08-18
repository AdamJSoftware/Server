from threading import Thread
import time
import uuid
import os
import socket
import selectors
import types
import datetime
import threading

from Scripts import File_Sender
from Scripts import Get
from Scripts import BackupEngine
from Scripts import Compare_Engine


sel = selectors.DefaultSelector()


def error_log(error):
    with open("Resources/ErrorLog.txt", 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")

# Any error is written to the error log


def error_print(error_message, error):
    print("SYSTEM ERROR - " + error_message + ": " + str(error))

# Any error is displayed to the user


class pc_list:
    client_update = []
    client_number = []
    client_name = []
    client_hostname = []
    client_ip = []
    client_sock = []
    client_mac = []
    client_port = []
    client_receiver = []
    client_checker = []


def replace_socket(index, value):
    pc_list.client_sock[index] = value


def get_ip_from_sock(client_socket):
    client_ip = str(client_socket).rsplit("raddr=('", 1)[1]
    client_ip = str(client_ip).rsplit("',", 1)[0]
    return client_ip


def append_to_pc_list(list_section, value):
    replaced = False
    for index, val in enumerate(list_section):
        if val == '--REPLACE--':
            replaced = True
            list_section[index] = value
    if not replaced:
        list_section.append(value)


def add_client_number():
    replaced = False
    for index, val in enumerate(pc_list.client_number):
        if val == '--REPLACE--':
            replaced = True
            pc_list.client_number[index] = index
    if not replaced:
        pc_list.client_number.append(int(len(pc_list.client_number)))


def replace_in_pc_list(json_section, old_value, new_value):
    for index, val in enumerate(json_section):
        if val == old_value:
            json_section[index] = new_value
    return json_section


def add_port_to_list():
    new_port = (int(len(pc_list.client_port)) + 1) * 3
    replaced = False
    for index, val in enumerate(pc_list.client_port):
        if val == '--REPLACE--':
            replaced = True
            pc_list.client_port[index] = (index + 1) * 3
    if not replaced:
        pc_list.client_port.append(new_port)


class Starter(Thread):

    def __init__(self):

        Thread.__init__(self)
        print("SYSTEM: Starting server")

        host = ''
        port = 8888

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_sock.bind((host, port))
        except Exception as error:
            print("Bind failed. Error : " + str(error))
            time.sleep(1)
            # server_restart()

        server_sock.listen(5)
        print("SYSTEM: Socket created")
        server_sock.setblocking(False)
        sel.register(server_sock, selectors.EVENT_READ, data=None)

    def run(self):
        while True:
            try:
                events = sel.select()
                for key, mask in events:
                    if key.data is None:
                        accept_wrapper(key.fileobj)
                    else:
                        service_connection(key, mask)
            except Exception as error:
                print(error)
                # error_log(error)
                # error_print("Starter thread, tried registering with no computers connected", error)
                # server_restart()


def accept_wrapper(client_socket):
    global conn
    global accepted
    conn, address = client_socket.accept()  # Should be ready to read
    print('Accepted connection from', address)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    accepted = True
    print('finished accepting')


def server_restart():
    print('SYSTEM: Restarting server...')
    time.sleep(1)
    os._exit(1)

def get_index_from_list(json_section, value):
    for index, val in enumerate(json_section):
        if val == value:
            return index


def remove_client_from_list(client_number):
    for val in vars(pc_list).items():
        if not str(val[0]).__contains__('__'):
            val[1][client_number] = '--REPLACE--'


def service_connection(key, mask):
    global accepted
    temporary_sock = key.fileobj
    if temporary_sock not in vars(pc_list).items():
        if accepted is True:
            random = str(uuid.uuid4())
            random = random[:4]
            random = 'temporary' + str(random)
            # The three lines above are creating a temporary name for the client
            print('TEMPORARY: {}'.format(temporary_sock))
            append_to_pc_list(pc_list.client_sock, temporary_sock)
            append_to_pc_list(pc_list.client_name, str(random))
            # pc_list["clientName"] = append_to_pc_list(pc_list["clientName"], str(random))
            # pc_list["clientSocket"] = append_to_pc_list(pc_list["clientSocket"], sock)
            append_to_pc_list(pc_list.client_ip, get_ip_from_sock(temporary_sock))
            append_to_pc_list(pc_list.client_update, 'JUST JOINED')
            # pc_list["clientIP"] = append_to_pc_list(pc_list["clientIP"], get_ip_from_sock(temporary_sock))
            add_port_to_list()
            add_client_number()
            # Most of the client details are appended to the pc_list
            print("Please wait for system to configure new computer...")
            # FIX THIS WAITING THING FOR MORE SECURE CONNECITION
            time.sleep(1)
            client_number = get_index_from_list(pc_list.client_ip, get_ip_from_sock(temporary_sock))

            print(pc_list.client_port[client_number])
            # Note for me, this should be removed in order to avoid another client taking the number
            # Starting the receive thread for the specific client
            client_hostname = ""
            client_name = ""
            client_MAC = ""
            print('Waiting to receive computer info')

            while client_hostname == "":
                try:
                    recv_data = temporary_sock.recv(1024).decode()
                    if str(recv_data).__contains__("--PCNAME--||"):
                        _, client_hostname, client_MAC, client_name = str(recv_data).split("||")
                except:
                    pass
            print('''
                Hostname: {}
                MAC: {}
                Name: {}'''.format(client_hostname, client_MAC, client_name))
            # temporary_sock.sendall(pc_list["clientPort"][clientNumber].encode("utf-8"))

            # Waiting to receive the rest of the details about the client
            replace_in_pc_list(pc_list.client_name, pc_list.client_name[client_number], client_name)

            print("NEW CLIENT NAME: {}".format(pc_list.client_name[client_number]))

            print('Finished switching name')
            # Replacing the temporary name with the actual name
            append_to_pc_list(pc_list.client_hostname, client_hostname)
            print('Finished adding hostname')
            append_to_pc_list(pc_list.client_mac, client_MAC)
            print('Finished adding MAC')
            port = pc_list.client_port[client_number]
            main_port = int(port) - 2
            append_to_pc_list(pc_list.client_receiver, client_name)
            append_to_pc_list(pc_list.client_checker, client_name)
            print('Client Number: {}'.format(client_number))
            # pc_list["clientStarter"][clientNumber] = DedicatedStarter(main_port, clientNumber, temporary_sock)
            # print('Starting dedicated starter')
            # pc_list["clientStarter"][clientNumber].start()

            dedicated_starter(main_port, client_number, temporary_sock)

            sel.unregister(temporary_sock)
            temporary_sock.close()
            print('CLOSED CONNECTION WITH SOCK')


class Receive(Thread):

    def __init__(self, port, sock):
        Thread.__init__(self)
        self.sock = sock
        self.port = port
        self.j = True
        print("Sock: {}".format(self.sock))
        print("SYSTEM: Receive initialized")

    def run(self):
        print('SYSTEM: Receive started')
        while self.j:
            try:
                recv_data = self.sock.recv(1024).decode()
                if str(recv_data) == "--SENDING_FILE--":
                    Get.main(self.port ,get_ip_from_sock(self.sock))
                elif str(recv_data).__contains__("--SENDING_BACKUP_FILES--"):
                    print("GOT BACKUP FILE")
                    message = recv_data.split("--SENDING_BACKUP_FILES--")[1]
                    Get.write_backup_file(message, get_ip_from_sock(self.sock), self.port)
                elif str(recv_data).__contains__("--BACKUP--"):
                    print("BACKING UP")
                    backup_func(self.sock, self.port)
                else:
                    print(recv_data)

            except:
                pass

    def send(self, message):
        self.sock.sendall(message.encode("utf-8"))

    def kill_thread(self):
        print('Killing receiver')
        self.j = False


def backup_func(client_sock, port):
    try:
        s = get_ip_from_sock(client_sock)
        print(s)
        try:
            name = Get.backup(s, port)
        except:
            server_restart()
        BackupEngine.main(name)
        getter, path = Compare_Engine.main(name)
        print("PATH: {}".format(path))
        if getter:
            message_to_send = "--GETFILES--"
            message_to_send = message_to_send.encode("utf-8")
            client_sock.sendall(message_to_send)
            value = File_Sender.get_files(path, port)
            if value is False:
                server_restart()
        else:
            pass
    except Exception as e:
        print(e)


# def check(client_number):
#     port = client_number  # Reserve a port for your service every new transfer wants a new port or you must wait.
#     s = socket.socket()  # Create a socket object
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     host = ""  # Get local machine name
#     try:
#         s.bind((host, port))  # Bind to the port
#     except:
#         return False
#     s.listen(5)  # Now wait for client connection.

#     print('Server listening....')

#     s.accept()

#     af = CheckSendThread(s)
#     af.start()

class Checker(Thread):
    def __init__(self, dedicated_port, client_number, receiver):
        Thread.__init__(self)
        print("PORT: {}".format(dedicated_port))
        self.client_number = client_number
        self.receiver = receiver
        port = int(
            dedicated_port)  # Reserve a port for your service every new transfer wants a new port or you must wait.
        self.s = socket.socket()  # Create a socket object
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = ""  # Get local machine name
        try:
            self.s.bind((host, port))  # Bind to the port
        except:
            pass
        self.s.listen(5)  # Now wait for client connection.

        print('Receiver listening....')

        self.connection, address = self.s.accept()

        print('RECEIVER: ACCEPTED CONNECTION')

        checker2 = Checker2(self.connection, self.client_number, self.receiver)
        checker2.start()

    def run(self):
        while True:
            try:
                time.sleep(1)
                self.connection.send('--TEST--'.encode("utf-8"))
                # print('done')
            except Exception as e:
                print("CHECKER: {}".format(e))
                remove_client_from_list(self.client_number)
                self.receiver.kill_thread()
                return


class Checker2(Thread):
    def __init__(self, connection, client_number, receiver):
        Thread.__init__(self)
        self.connection = connection
        self.receiver = receiver
        # self.connection.settimeout(5.0)
        self.client_number = client_number

    def run(self):
        pc_list.client_update[self.client_number] = datetime.datetime.now()
        while True:
            try:
                time.sleep(1)
                # self.connection.send('--TEST--'.encode("utf-8"))
                data = self.connection.recv(1024).decode()
                pc_list.client_update[self.client_number] = datetime.datetime.now()
                # print(data)
            except Exception as e:
                remove_client_from_list(self.client_number)
                print("CHECKER: {}".format(e))
                self.receiver.kill_thread()
                return


def dedicated_starter(dedicated_port, client_number, temporary_sock):
    print("SYSTEM: Starting dedicated server")
    print("USING PORT: {}".format(dedicated_port))
    host = ''
    port = int(dedicated_port)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_sock.bind((host, port))
    except Exception as error:
        print("Bind failed. Error : " + str(error))
        time.sleep(1)
        # server_restart()

    server_sock.listen(5)
    print("SYSTEM: Socket created")

    temporary_sock.sendall(str("--PORT--{}".format(dedicated_port)).encode("utf-8"))
    print('Finished sending info')
    # server_sock.setblocking(False)

    try:
        connection, address = server_sock.accept()  # Establish connection with client.
        print('SERVER_SOCK: {}'.format(server_sock))

        print('Got connection from', address)
        connection.setblocking(False)
        sock = connection
        replace_socket(client_number, sock)
        print('Finished __init__')
        # data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')
        # events = selectors.EVENT_READ | selectors.EVENT_WRITE
        # self.sock = events[0].fileobj
        # print('replacing socket')
        # pc_list["clientSocket"] = replace_socket(pc_list["clientSocket"], self.client_number, self.sock)
        # print('finished replacing socket')

        print('Initiaiting receiver')
        pc_list.client_receiver[client_number] = Receive(int(dedicated_port) + 2,sock)
        print('starting receiver')
        pc_list.client_receiver[client_number].start()
        print('Initiaiting checker')
        checker_port = int(dedicated_port) + 1
        pc_list.client_checker[client_number] = Checker(str(checker_port), client_number,
                                                        pc_list.client_receiver[client_number])
        print('starting checker')
        pc_list.client_checker[client_number].start()
        print('everything finished succesfully')
        # checker_port2 = int(self.dedicated_port) + 2
        # pc_list["clientChecker2"][self.client_number] = Checker2(str(checker_port2))
        # print('starting checker')
        # pc_list["clientChecker2"][self.client_number].start()
        print('everything finished succesfully')

    except Exception as e:
        print(e)


def send_message():
    send_list = []
    for val in pc_list.client_number:
        if val != '--REPLACE--':
            send_list.append(val)

    if len(send_list) == 1:
        while True:
            user_input = input("Sending to -> {} -> ".format(pc_list.client_name[send_list[0]]))
            if user_input == "/back":
                return
            pc_list.client_receiver[send_list[0]].send(user_input)
    else:
        for val in send_list:
            print(pc_list.client_name[val])
        user_input = input("Please select computer -> ")
        client = get_index_from_list(pc_list.client_name, user_input)
        print("CLIENT NUMBER : {}".format(client))
        while True:
            user_input = input("Sending to -> {} -> ".format(pc_list.client_name[client]))
            if user_input == "/back":
                return
            pc_list.client_receiver[client].send(user_input)


# class FileSenderThread(Thread):
#     def __init__(self, port):
#         Thread.__init__(self)
#         self.port = port

#     def run(self):
#         File_Sender.main(self.port)

def send_file():
    send_list = []
    for val in pc_list.client_number:
        if val != '--REPLACE--':
            send_list.append(val)
    if len(send_list) == 1:
        # pc_list.client_receiver[send_list[0]].send('--SENDING_FILE--')
        print('SOCKET: {}'.format(pc_list.client_sock[send_list[0]]))
        # file_sender_thread = FileSenderThread(pc_list.client_port[send_list[0]])
        # file_sender_thread.start()
        File_Sender.main(pc_list.client_sock[send_list[0]], pc_list.client_port[send_list[0]])
    else:
        for val in send_list:
            print(pc_list.client_name[val])
        user_input = input("Please select computer -> ")
        client = get_index_from_list(pc_list.client_name, user_input)
        print("CLIENT NUMBER : {}".format(client))
        File_Sender.main(pc_list.client_sock[send_list[client]], pc_list.client_port[send_list[client]])


def get_file():
    pass


def main():
    starter_thread = Starter()
    starter_thread.start()
    while True:
        try:
            user_input = input(" -> ")
            if user_input == "/ls -all":
                for val in vars(pc_list).items():
                    if not str(val[0]).__contains__('__'):
                        print(val)
            elif user_input == "/client status":
                update_list = []
                for val in pc_list.client_number:
                    if val != '--REPLACE--':
                        update_list.append(val)
                for val in update_list:
                    print("{}: {} seconds ago".format(pc_list.client_name[val],
                                                      (datetime.datetime.now() - pc_list.client_update[val]).seconds))
            elif user_input == "/m":
                send_message()
            elif user_input == "/send":
                send_file()
            elif user_input == "/threads":
                print(threading.active_count())

            # else:
            #     pc_list["clientReceiver"][0].send(pc_list["clientReceiver"][0], user_input)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()