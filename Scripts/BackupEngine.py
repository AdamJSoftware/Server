import os
import sys
import json


def tree_func(absolute_path, current_folder, new_folder, folders):
    try:
        current_folder = os.path.join(current_folder, new_folder)
        folders.append(current_folder)
        # Sets current_folder to the new one (used during recuersiion)
        tree = os.listdir(current_folder)
        # List all the files and folders in in current folder
        for item in tree:
            # for every item in the directory
            if os.path.isdir(os.path.join(current_folder, item)):
                # Check if item is a directory

                # Add this folder in the folder array
                tree_func(absolute_path, current_folder,
                          item, folders)

                # Runs the recursion code adding the files scaned (absolute_path array), the current folder, the item (new folder), what folders to exculde, folders audited and the modification date of a file

            else:
                # absolute_path.append(os.path.join(current_folder, item))
                # Append the file to the absolute path array
                try:
                    absolute_path.append({"name": os.path.join(current_folder, item), "file_date": os.path.getmtime(
                        os.path.join(current_folder, item))})
                    # file_date.append(os.path.getmtime(
                    #     os.path.join(current_folder, item)))
                    # Appending the modification date to the file_date array
                except Exception as e:
                    # Due to privilge issues, this is sometimes not possible so NA is used to keep the position consisten between absolute_path array and file_date array
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print("Error: {} at line {}".format(e, exc_tb.tb_lineno))
                    print('Writing manual')
                    absolute_path.append({"name": os.path.join(
                        current_folder, item), "file_date": 'NA'})
                    # file_date.append('NA')
        return absolute_path, folders
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))


def relative_path(absolute_path, root_directory):
    return absolute_path.split(os.path.join(root_directory, ''))[1]


# absolute_path = []
# The absolute path is the array of every file in the selected directory with it's absolute path (c:\users\...)
# relative_path = []
# The relative path is the array of every file in the selected directory containing the relative path (root=selected folder, documents\...)
# file_date = []
# The file_date is the array containing the last modification time of every file in either the array or absolute path (both of them having the same index)
# exculde = ['itinfluencer']
# Tells the program which folders to exculde


def config_create(backup_config):
    try:
        config = {"absolute_path": [],
                  "folders": [],
                  "relative_path": []}
        with open(backup_config, 'w') as f:
            json.dump(config, f, indent=4)

    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print("Error: {} at line {}".format(e, exc_tb.tb_lineno))


def json_read(backup_directory):
    with open(backup_directory, 'r') as f:
        return json.load(f)


def json_write(data, backup_directory):
    with open(backup_directory, 'w') as f:
        json.dump(data, f, indent=4)


def main(pc_name):
    config_json = json_read(os.path.join('Resources', 'config.json'))
    try:
        if config_json['a_or_r'] == 'r':
            if not os.path.exists(os.path.join('Resources', 'Backups', pc_name)):
                os.mkdir(os.path.join(
                    'Resources', 'Backups', pc_name))
            backup_audit = os.path.join(
                'Resources', 'Backups', pc_name, 'backup_audit.json')
            backup_directory = os.path.join(
                'Resources', 'Backups', pc_name)

        else:
            if not os.path.exists(os.path.join(config_json['backup_directory'], pc_name)):
                os.mkdir(os.path.join(
                    config_json['backup_directory'], pc_name))
            backup_audit = os.path.join(
                config_json['backup_directory'], pc_name, 'backup_audit.json')
            backup_directory = os.path.join(
                config_json['backup_directory'], pc_name)
        config_create(backup_audit)
        # config = config_read()

        current_folder=backup_directory
        absolute_path, folders = tree_func(
            absolute_path=[], current_folder=current_folder, new_folder='', folders=[])
        config = json_read(backup_audit)
        config['absolute_path'] = absolute_path
        for index, item in enumerate(absolute_path):
            relative = relative_path(item['name'], current_folder)
            config['relative_path'].append(
                {"name": relative, "file_date": absolute_path[index]['file_date']})
        for item in folders:
            relative = relative_path(item, current_folder)
            config['folders'].append(relative)
        json_write(config, backup_audit)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))


if __name__ == '__main__':
    try:
        main('DESKTOP-AF6NF3R')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error: {} at line {}".format(e, exc_tb.tb_lineno))
