import requests
import os
import subprocess
import time


def main():
    repository_version = requests.get('https://raw.githubusercontent.com/AdamJSoftware/Server/master/Version.txt')
    repository_version = repository_version.content.decode("utf-8")

    updater_version = requests.get("https://raw.githubusercontent.com/AdamJSoftware/Client/Server/UpdateManager.txt")
    updater_version = updater_version.content.decode("utf-8")

    with open("UpdateManager.txt", 'r') as f:
        update_manager_version = f.read()

    if updater_version == update_manager_version:
        print('Update manager up-to-date')
    else:
        print('Please manually update client!')
        time.sleep(10)

    with open('Version.txt', 'r') as f:
        program_version = f.read()

    if repository_version == program_version:
        print('Client up-to-date')
    else:
        print('Updating client')
        client_update()

    subprocess.call(['python.exe', 'Main - UI.py'])


def client_update():
    client_version = requests.get("https://raw.githubusercontent.com/AdamJSoftware/Server/master/Version.txt")
    client_version = client_version.content.decode("utf-8")

    with open("Version.txt", "w") as f:
        f.write(client_version)

    with open("Repository.txt", "r") as f:
        client_repository = f.read()

    remove_files(client_repository.split("\n"))

    client_repository = requests.get("https://raw.githubusercontent.com/AdamJSoftware/Server/master/Repository.txt")
    client_repository = client_repository.content.decode("utf-8")
    with open("Repository.txt", "w") as f:
        f.write(client_repository)
    write_new_files(client_repository.split("\n"))


def remove_files(client_repository):
    for file in client_repository:
        print(file)
        try:
            if os.path.isfile(file):
                os.remove(file)
            else:
                pass
        except Exception as error:
            print(error)


def write_new_files(client_repository):
    for file in client_repository:
        new_file = requests.get("https://raw.githubusercontent.com/AdamJSoftware/Server/master/" + file)
        new_file = new_file.content.decode("utf-8")
        try:
            with open(file, 'w') as f:
                f.write(new_file)
        except Exception as error:
            print(error)


if __name__ == '__main__':
    main()
