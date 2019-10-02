import os
import sys
global cwd
cwd = os.getcwd()
cwd = cwd.replace('\\', '/')


def main():
    global cw
    global i
    global file
    i = True
    while i == True:
        Q = input(str(cwd)+ " -> ")
        os.system('cls')
        if Q == "/ls":
            ls_func()
        elif Q == "/help":
            help_func()
        elif Q.__contains__("cd"):
            cd_func(Q)
        elif Q.__contains__("/select"):
            selector_func(Q)
        elif Q == "":
            pass
        elif Q == "/back":
            exit()
        else:
            unknown_func()
    return file


def selector_func(Q):
    global cwd
    global i
    global file
    try:
        Q = Q.rsplit("select ", 1)[1]
    except:
        print("Please add space between '/select' and 'file'")
        return
    if Q.isidentifier() or Q.__contains__("."):
        new_file = str(cwd) + '/' + Q
        if os.path.isfile(new_file) or os.path.isdir(new_file):
            file = new_file
            i = False
            return file
        else:
            print("Could not find file")
            return
    else:
        print("Please try again and select a file")


def ls_func():
    global cwd
    List = os.listdir(cwd)
    i = 0
    while i != len(List):
        print(List[i])
        i+=1
    return


def cd_func(Q):
    global cwd
    if Q.__contains__("cd."):
        cwd = cwd.rsplit('/',1)[0]
        return cwd
    else:
        try:
            Q = Q.rsplit("cd ",1)[1]
        except:
            print("Please add space between '/cd' and 'directory'")
            return
        if Q.isidentifier():
            try:
                new_cwd = str(cwd) + '/' + Q
                os.listdir(new_cwd)
                cwd = new_cwd
            except:
                print("could not find directory")
            return
        else:
            print("Please try again and enter a directory")
            return


def help_func():
    print("/select 'file name' --> Selects file and allows to send or grab, \n"
          "/cd. --> Goes to the previous directory, \n"
          "/cd 'directory' --> Goes to the specified directory, \n"
          "/ls --> Shows all files in directory, \n"
          "/back --> Exists selector menu, \n")


def unknown_func():
    print('Unrecognized command. Type "help" for a list of commands')

if __name__ == '__main__':
    main()
