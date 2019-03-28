import os

cwd = os.getcwd()

def get_file(allMissingFiles, PC):
    path = "Resources\\Backups\\" + PC + "\\GETFILES.txt"
    with open(path, "w", encoding="utf-8") as f:
        for file in allMissingFiles:
            f.write(file + "\n")
    return path


def add_folder(MissingFolders, PC):
    try:
        for folder in MissingFolders:
            os.mkdir(cwd + "\\Resources\\Backups\\" + PC + "\\" + folder)
    except:
        print("an unknown error occured while creating the folder")