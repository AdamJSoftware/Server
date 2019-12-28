from threading import Thread
import time
import uuid
import os
import socket
import selectors
import types
import datetime
import threading
import sys
import gc
import json
from Scripts import File_Sender
from Scripts import Get
from Scripts import BackupEngine
from Scripts import Compare_Engine


sel = selectors.DefaultSelector()


def error_log(error):
    with open(os.path.join('Resources', 'ErrorLog.txt'), 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")

# Any error is written to the error log

def config_read():
    with open(os.path.join('Resources', 'config.json'), 'r') as f:
        return json.load(f)

def error_print(error_message, error):
    print("SYSTEM ERROR - " + error_message + ": " + str(error))

# Any error is displayed to the user


class pc_list():
    instances = []

    def __init__(self, update, name, hostname, ip, sock, mac, port, receiver, checker):
        self.client_update = update
        self.client_number = ''
        self.client_name = name
        self.client_hostname = hostname
        self.client_ip = ip
        self.client_sock = sock
        self.client_port = port
        self.client_receiver = receiver
        self.client_checker = checker
        self.client_mac = mac
        self.client_receiver_port = 0
        self.client_checker_port = 0
        self.client_file_sender_port = 0

        for index, val in enumerate(pc_list.instances):
            if val == '--REPLACE--':
                pc_list.instances[index] = self
                return
        pc_list.instances.append(self)

    def add_port(self):
        for index, val in enumerate(pc_list.instances):
            if val == '--REPLACE--':
                self.client_port = index*3
                return
        self.client_port =  int(self.client_number)*3
        self.client_receiver_port = self.client_port - 2
        self.client_checker_port = self.client_port - 1
        self.client_file_sender_port = self.client_port

    def add_number(self):
        for index, val in enumerate(pc_list.instances):
            if val == '--REPLACE--':
                self.client_number = index
                return
        self.client_number = int(len(pc_list.instances))

    # def find(self, given_item, given_list, looking_list):
    #     for key, val in self.items():
    #         if str(val) == given_item:

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


def find(given_item):
    for index, instance in enumerate(pc_list.instances):
        for (key, value) in instance.values():
            if str(value) == str(given_item):
                return instance


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
    pc_list.instances[client_number - 1] = '--REPLACE--'
    # for val in vars(pc_list).items():
    #     if not str(val[0]).__contains__('__'):
    #         print(val)
    #         val[1][client_number] = '--REPLACE--'


def service_connection(key, mask):
    try:
        global accepted
        temporary_sock = key.fileobj
        if temporary_sock not in vars(pc_list).items():
            if accepted is True:
                random = str(uuid.uuid4())
                random = random[:4]
                random = 'temporary' + str(random)
                # The three lines above are creating a temporary name for the client
                print('TEMPORARY: {}'.format(temporary_sock))
                new_client = pc_list('JUST JOINED', str(random), '', get_ip_from_sock(
                    temporary_sock), temporary_sock, '', '', '', '')
                # pc_list["clientName"] = append_to_pc_list(pc_list["clientName"], str(random))
                # pc_list["clientSocket"] = append_to_pc_list(pc_list["clientSocket"], sock)
                # pc_list["clientIP"] = append_to_pc_list(pc_list["clientIP"], get_ip_from_sock(temporary_sock))
                new_client.add_number()
                new_client.add_port()
                # Most of the client details are appended to the pc_list
                print("Please wait for system to configure new computer...")
                # FIX THIS WAITING THING FOR MORE SECURE CONNECITION
                time.sleep(1)
                client_number = new_client.client_number

                print(client_number)
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
                            _, client_hostname, client_MAC, client_name = str(
                                recv_data).split("||")
                    except:
                        pass
                print(f'''
                    Hostname: {client_hostname}
                    MAC: {client_MAC}
                    Name: {client_name}''')
                # temporary_sock.sendall(pc_list["clientPort"][clientNumber].encode("utf-8"))

                # Waiting to receive the rest of the details about the client
                new_client.client_name = client_name

                print(f"NEW CLIENT NAME: {new_client.client_name}")

                print('Finished switching name')
                # Replacing the temporary name with the actual name
                new_client.client_hostname = client_hostname
                print('Finished adding hostname')
                new_client.client_mac = client_MAC
                print('Finished adding MAC')
                port = new_client.client_port
                print(port)
                main_port = int(port) - 2
                new_client.client_receiver = client_name
                new_client.client_checker = client_name
                print(f'Client Number: {new_client.client_number}')
                # pc_list["clientStarter"][clientNumber] = DedicatedStarter(main_port, clientNumber, temporary_sock)
                # print('Starting dedicated starter')
                # pc_list["clientStarter"][clientNumber].start()

                dedicated_starter(new_client, temporary_sock)

                sel.unregister(temporary_sock)
                temporary_sock.close()
                print('CLOSED CONNECTION WITH TEMPORARY SOCK')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))


class Receive(Thread):

    def __init__(self, client, sock):
        Thread.__init__(self)
        self.sock = sock
        self.port = client.client_receiver_port
        self.client_instance = client
        self.j = True
        print("Sock: {}".format(self.sock))
        print("SYSTEM: Receive initialized")
        print(f'SYSTEM: Receiver running on port: {self.port}')

    def run(self):
        print('SYSTEM: Receive started')
        while self.j:
            time.sleep(0.1)
            try:
                recv_data = self.sock.recv(1024).decode()
                if str(recv_data) == "--SENDING_FILE--":
                    Get.main(self.port, get_ip_from_sock(self.sock))
                elif str(recv_data).__contains__("--SENDING_BACKUP_FILES--"):
                    print("GOT BACKUP FILE")
                    message = recv_data.split("--SENDING_BACKUP_FILES--")[1]
                    config = config_read()
                    if config['a_or_r'] == "a":
                        backup_directory = os.path.join(config['backup_directory'], self.client_instance.client_hostname)
                    else:
                        backup_directory = os.path.join('Resources', 'Backups', self.client_instance.client_hostname)
                    Get.write_backup_file(
                        message, get_ip_from_sock(self.sock), self.port, backup_directory)
                elif str(recv_data).__contains__("--BACKUP--"):
                    print("BACKING UP")
                    backup_func(self.client_instance, self.port)
                else:
                    print(recv_data)

            except:
                pass

    def send(self, message):
        self.sock.sendall(message.encode("utf-8"))

    def kill_thread(self):
        print('Killing receiver')
        self.j = False


def backup_func(client_instance, port):
    try:
        name = client_instance.client_hostname
        Get.backup(str(client_instance.client_ip), client_instance.client_file_sender_port)
        BackupEngine.main(name)
        path = Compare_Engine.main(name)
        File_Sender.files_to_send(client_instance.client_sock, name, client_instance.client_file_sender_port, path)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))


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
    def __init__(self, dedicated_port, client_number, receiver, client_instance):
        Thread.__init__(self)
        print(f"SYSTEM: Checker running on port: {client_instance.client_checker_port}")
        self.client_number = client_number
        self.receiver = receiver
        port = int(client_instance.client_checker_port)  # Reserve a port for your service every new transfer wants a new port or you must wait.
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

        checker2 = Checker2(self.connection, self.client_number,
                            self.receiver, client_instance)
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
    def __init__(self, connection, client_number, receiver, client_instance):
        Thread.__init__(self)
        self.connection = connection
        self.receiver = receiver
        # self.connection.settimeout(5.0)
        self.client_number = client_number
        self.client_instance = client_instance

    def run(self):
        self.client_instance.client_update = datetime.datetime.now()
        while True:
            try:
                time.sleep(1)
                # self.connection.send('--TEST--'.encode("utf-8"))
                data = self.connection.recv(1024).decode()
                self.client_instance.client_update = datetime.datetime.now(
                )
                # print(data)
            except Exception as e:
                remove_client_from_list(self.client_number)
                print("CHECKER: {}".format(e))
                self.receiver.kill_thread()
                return


def dedicated_starter(client_instance, temporary_sock):
    try:
        print("SYSTEM: Starting dedicated server")
        print(f"USING PORT: {client_instance.client_port}")
        host = ''

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_sock.bind((host, client_instance.client_port))
        except Exception as error:
            print("Bind failed. Error : " + str(error))
            time.sleep(1)
            # server_restart()

        server_sock.listen(5)
        print("SYSTEM: Socket created")

        temporary_sock.sendall((f"--PORT--{client_instance.client_port}".encode('utf-8')))
        print('Finished sending info')
        # server_sock.setblocking(False)

        try:
            # Establish connection with client.
            connection, address = server_sock.accept()
            print('SERVER_SOCK: {}'.format(server_sock))

            print('Got connection from', address)
            connection.setblocking(False)
            sock = connection
            client_instance.client_sock = sock
            print('Finished __init__')
            # data = types.SimpleNamespace(addr=address, inb=b'', outb=b'')
            # events = selectors.EVENT_READ | selectors.EVENT_WRITE
            # self.sock = events[0].fileobj
            # print('replacing socket')
            # pc_list["clientSocket"] = replace_socket(pc_list["clientSocket"], self.client_number, self.sock)
            # print('finished replacing socket')

            print('Initiaiting receiver')
            client_instance.client_receiver = Receive(
                client_instance, sock)
            print('starting receiver')
            client_instance.client_receiver.start()
            print('Initiaiting checker')
            checker_port = int(client_instance.client_port)
            client_instance.client_checker = Checker(str(checker_port), client_instance.client_number,
                                                     client_instance.client_receiver, client_instance)
            print('starting checker')
            client_instance.client_checker.start()
            print('everything finished succesfully')
            # checker_port2 = int(self.dedicated_port) + 2
            # pc_list["clientChecker2"][self.client_number] = Checker2(str(checker_port2))
            # print('starting checker')
            # pc_list["clientChecker2"][self.client_number].start()
            print('everything finished succesfully')

        except Exception as e:
            print(e)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))


def system_message(message):
    print(f'SYSTEM: {message}')


def send_message():
    send_list = []
    for val in pc_list.instances:
        if val.client_name != '--REPLACE--':
            send_list.append(val)

    if len(send_list) == 1:
        while True:
            client_instance = send_list[0]
            user_input = input(
                f"Sending to -> {client_instance.client_name} -> ")
            if user_input == "/back":
                return
            client_instance.client_receiver.send(user_input)
    else:
        for val in send_list:
            print(val.client_name)
        user_input = input("Please select computer -> ")
        client_instance = find(user_input)
        client_number = client_instance.client_number
        print(f"CLIENT NUMBER : {client_number}")
        client_instance = pc_list.instances[client_number]
        while True:
            user_input = input(
                f"Sending to -> {client_instance.client_name} -> ")
            if user_input == "/back":
                return
            client_instance.client_receiver.send(user_input)


# class FileSenderThread(Thread):
#     def __init__(self, port):
#         Thread.__init__(self)
#         self.port = port

#     def run(self):
#         File_Sender.main(self.port)

def send_file():
    send_list = []
    for val in pc_list.instances:
        if val.client_name != '--REPLACE--':
            send_list.append(val)
    if len(send_list) == 1:
        client_instance = send_list[0]
        # pc_list.client_receiver[send_list[0]].send('--SENDING_FILE--')
        print(f'SOCKET: {client_instance.client_sock}')
        # file_sender_thread = FileSenderThread(pc_list.client_port[send_list[0]])
        # file_sender_thread.start()
        File_Sender.main(
            client_instance.client_sock, client_instance.client_port)
    else:
        for val in send_list:
            print(val.client_name)
        user_input = input("Please select computer -> ")
        client_number = find(user_input, 'client_number')
        print(f"CLIENT NUMBER : {client_number}")
        client_instance = pc_list.instances[client_number]
        File_Sender.main(
            client_instance.client_sock, client_instance.client_port)


def get_file():
    pass


def create_config():
    if not os.path.isfile(os.path.join('Resources', 'config.json')):
        config = {
            "server_port": 8888,
            "webGUI_port": 3000,
            "OS": os.name
            }
        with open(os.path.join('Resources', 'config.json'), 'w') as f:
            f.write(json.dumps(config, indent=4))
        system_message('Created config file')


def main():
    create_config()
    starter_thread = Starter()
    starter_thread.start()
    while True:
        try:
            user_input = input(" -> ")
            if user_input == "/ls -all":
                for instance in pc_list.instances:
                    print(f'NAME: {instance.client_name}')
                    for (key, value) in instance.items():
                        print(f'{key} => {value}')
            elif user_input == "/client status":
                update_list = []
                for instance in pc_list.instances:
                    if instance.client_name != '--REPLACE--':
                        update_list.append(instance)
                for instance in update_list:
                    print(
                        f"{instance.client_name}: {(datetime.datetime.now() - instance.client_update).seconds} seconds ago")
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
