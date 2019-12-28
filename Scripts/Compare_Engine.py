import json
import os
import sys


def config_read(backup_directory):
    with open(backup_directory, 'r') as f:
        return json.load(f)


def config_write(data, backup_directory):
    with open(backup_directory, 'w') as f:
        json.dump(data, f, indent=4)


def add_folder(missing_folders, pc):
    config = config_read
    for folder in missing_folders:
        try:
            os.mkdir(os.path.join('Resources', 'Backups', pc, folder))
        except Exception as e:
            print("An unknown error occurred while creating the folder")
            print(e)


def add_folders(folders, directory):
    for folder in folders:
        try:
            os.mkdir(os.path.join(directory, folder))
        except:
            pass


def main(pc):
    try:
        config = config_read(os.path.join('Resources', 'config.json'))
        if config['a_or_r'] == 'r':
            backup_directory = os.path.join('Resources', 'Backups', pc)
            server_backup = config_read(os.path.join(
                backup_directory, 'backup_audit.json'))
            client_backup = config_read(os.path.join(
                backup_directory, 'received_backup.json'))
        else:
            backup_directory = os.path.join(config['backup_directory'], pc)
            server_backup = config_read(os.path.join(
                backup_directory, 'backup_audit.json'))
            client_backup = config_read(os.path.join(
                'Resources', 'Backups', pc, 'received_backup.json'))
        missing_files = []
        missing_files_path = []
        missing_files_name = []
        missing_folders = []
        changed_files_path = []
        changed_files_name = []
        changed_files = []

        server_relative_name_array = []
        for item in server_backup['relative_path']:
            server_relative_name_array.append(item["name"])
        for index, file in enumerate(client_backup['relative_path']):
            if file["name"] not in server_relative_name_array:
                print('MISSING FILE')
                missing_files_path.append(client_backup['absolute_path'][index]["name"])
                missing_files_name.append(client_backup['relative_path'][index]["name"])
            else:
                x = server_relative_name_array.index(file["name"])
                if client_backup['relative_path'][index]['file_date'] == server_backup['relative_path'][x]['file_date']:
                    changed_files_path.append(client_backup['absolute_path'][index]['file_date'])
                    changed_files_name.append(client_backup['relative_path'][index]['file_date'])
        for folder in client_backup['folders']:
            if folder not in server_backup['folders']:
                missing_folders.append(folder)

        for index, item in enumerate(missing_files_name):
            missing_files.append({"name": item, "path": missing_files_path[index]})

        for index, item in enumerate(changed_files_name):
            changed_files.append({"name": item, "path": changed_files_path[index]})
        # config_create(os.path.join(backup_directory, 'FTS.json'))
        config = {"missing_files": missing_files,
                  "missing_folders": missing_folders, "changed_files": changed_files}
        config_write(config, os.path.join(backup_directory, 'FTS.json'))

        add_folders(missing_folders, backup_directory)
        return os.path.join(backup_directory, 'FTS.json')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))


if __name__ == "__main__":
    main('DESKTOP-AF6NF3R')
