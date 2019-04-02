import os

cd = os.getcwd()


def original_files_func(files):
    original_files = files
    for lines in original_files:
        if lines.__contains__("*"):
            original_files.remove(lines)

    for lines in original_files:
        try:
            newlines = lines.replace("\n", "")
            original_files.remove(lines)
            original_files.append(newlines)
        except Exception as e:
            pass
            print(e)
    return original_files


def backup2(files_and_size, og):
    new_list = []
    for files in files_and_size:
        for remove in og:
            if str(files).__contains__(remove):
                new_file = str(files).replace(remove, str(""))
                first_char = new_file[:1]
                if first_char == '\\':
                    new_file = new_file[1:]
                    new_list.append(new_file)
            else:
                new_list.append(files)
    print("BACKUP2")

    for lines in new_list:
        if lines == "\n":
            new_list.remove(lines)
            print("REMOVED")

    return new_list


def main(name):
    pc = name
    files_to_scan_func(pc)


def get_size(filename):
    try:
        st = os.stat(filename)
        return st.st_size
    except Exception as e:
        print(e)
        return "AN ERROR OCCURRED. FILE NAME MAY BE TOO LONG"


def folder_func(path):
    folder_list = []
    for name in os.listdir(path):
        new_path = os.path.join(path, name)
        folder_list.append(new_path)
    return folder_list


def folder_or_file(file, files_and_size, files):
    path = os.path.normpath(str(file))
    files_and_size.append(file)
    if os.path.isdir(path):
        to_be_appended = folder_func(path)
        files.extend(to_be_appended)
    else:
        size = get_size(file)
        files_and_size.append([size])


def files_to_scan_func(pc):

    f = cd+"\\Resources\\Backups\\" + pc
    og = [f]
    files_and_size = []
    files_to_exclude = []
    files = [f]

    for file in files:
        try:
            file = file.replace("\n", "")
        except Exception as e:
            print("BACKUP ERROR: " + str(e))
        if file.__contains__("*"):
            file = file.split("*")[1]
            files_to_exclude.append(file)
            print("ADDED FILE TO EXCLUDE")
        if len(files_to_exclude) == 0:
            folder_or_file(file, files_and_size, files)
        else:
            for i in files_to_exclude:
                if i in file:
                    pass
                else:
                    folder_or_file(file, files_and_size, files)

    with open("Resources\\Backups\\" + pc + "\\Backup_SEND.txt", "w", encoding="utf-8") as f:
        for file in files_and_size:
            f.write(str(file) + "\n")

    with open("Resources\\Backups\\" + pc + "\\Backup2.txt", "w", encoding="utf-8") as f:
        b2 = backup2(files_and_size, og)
        for file in b2:
            f.write(str(file) + "\n")
