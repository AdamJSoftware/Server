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


def main(pc):
    try:
        backup_directory = os.path.join('Resources', 'Backups', pc)
        server_backup = config_read(os.path.join(
            backup_directory, 'backup_audit.json'))
        client_backup = config_read(os.path.join(
            backup_directory, 'received_backup.json'))

        missing_files = []
        missing_folders = []
        changed_files = []

        for index, file in enumerate(client_backup['relative_path']):
            if file not in server_backup['relative_path']:
                missing_files.append(file)
            else:
                x = server_backup['relative_path'].index(file)
                if(client_backup['relative_path'][index]['file_date'] == server_backup['relative_path'][x]['file_date']):
                    changed_files.append(file)
        for folder in client_backup['folders']:
            if folder not in server_backup['folders']:
                missing_folders.append(folder)

        # config_create(os.path.join(backup_directory, 'FTS.json'))
        config = {"missing_files": missing_files,
                  "missing_folders": missing_folders, "changed_files": []}
        config_write(config, os.path.join(backup_directory, 'FTS.json'))
        return True, os.path.join(backup_directory, 'FTS.json')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))


if __name__ == "__main__":
    main('DESKTOP-AF6NF3R')
