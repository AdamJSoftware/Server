import subprocess
import os


def main():
    while True:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        subprocess.call(['python', 'Multi_Server.py'])


if __name__ == '__main__':
    main()
