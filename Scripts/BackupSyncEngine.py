import os


def get_file(all_missing_files, pc):
    path = "Resources/Backups/" + pc + "/GETFILES.txt"
    with open(path, "w", encoding="utf-8") as f:
        for file in all_missing_files:
            f.write(file + "\n")
    return path


def add_folder(missing_folders, pc):
    for folder in missing_folders:
        try:
            cwd = os.getcwd()
            os.mkdir(cwd + "/Resources/Backups/" + pc + "/" + folder)
        except Exception as e:
            print("An unknown error occurred while creating the folder")
            print(e)
