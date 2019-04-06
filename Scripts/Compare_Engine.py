from Scripts import BackupSyncEngine
import time

def error_log(error):
    with open("Resources\\ErrorLog.txt", 'a') as file:
        file.write(time.ctime() + "\n")
        file.write(str(error) + "\n" + "\n")


def error_print(error_message ,error):
    print("SYSTEM ERROR - " + error_message + ": " + str(error))


def main(pc):
    with open("Resources\\Backups\\" + pc + "\\Received_Backup.txt", "r", encoding="utf-8-sig") as received_backup:
        received_backup = received_backup.readlines()
        new_received_backup = []
        for lines in received_backup:
            if lines.__contains__("\n"):
                newline = lines.replace("\n", "")
                new_received_backup.append(newline)
            else:
                new_received_backup.append(lines)

    with open("Resources\\Backups\\" + pc + "\\Backup2.txt", "r", encoding="utf-8-sig") as local_backup:
        local_backup = local_backup.readlines()
        new_local_backup = []
        for line in local_backup:
            if line.__contains__("\n"):
                newline = line.replace("\n", "")
                new_local_backup.append(newline)
            else:
                new_local_backup.append(line)

    missing_files = []
    changed_files = []
    missing_folders = []

    received_backup_files = []
    for index, lines in enumerate(new_received_backup):
        if lines.__contains__("["):
            received_backup_files.append(new_received_backup[index-1])
            received_backup_files.append(lines)

    local_backup_files = []
    for index, line in enumerate(new_local_backup):
        if line.__contains__("["):
            local_backup_files.append(new_local_backup[index-1])
            local_backup_files.append(line)

    for index, lines in enumerate(received_backup_files):
        if not lines.__contains__("["):
            i = False
            j = False
            for index2, line in enumerate(local_backup_files):
                if line == lines:
                    i = True
                    try:
                        if received_backup_files[index + 1] == local_backup_files[index2 + 1]:
                            pass
                        else:
                            j = True
                    except Exception as error:
                        error_log(error)
                        error_print("error while reading received backup files", error)
                else:
                    pass
            if i is False:
                missing_files.append(lines)
            if j is True:
                changed_files.append(lines)
        else:
            pass

    received_backup_folders = []
    for index, lines in enumerate(new_received_backup):
        if str(lines).__contains__("["):
            pass
        else:
            try:
                if new_received_backup[index + 1].__contains__("["):
                    pass
                else:
                    received_backup_folders.append(lines)
            except Exception as e:
                print(e)
                pass

    local_backup_folders = []
    for index, lines in enumerate(new_local_backup):
        if str(lines).__contains__("["):
            pass
        else:
            try:
                if new_local_backup[index + 1].__contains__("["):
                    pass
                else:
                    local_backup_folders.append(lines)
            except Exception as e:
                print(e)
                pass

    for index, lines in enumerate(received_backup_folders):
        i = False
        for index2, line in enumerate(local_backup_folders):
            if line == lines:
                i = True
            else:
                pass
        if i is False:
            missing_folders.append(lines)

    print("MISSING FILES")
    for i in missing_files:
        print("\t"+i)

    print("CHANGED FILES")
    for i in changed_files:
        print("\t"+i)

    print("MISSING FOLDERS")
    for i in missing_folders:
        print("\t"+i)
    BackupSyncEngine.add_folder(missing_folders, pc)

    all_missing_files = missing_files + changed_files
    path = BackupSyncEngine.get_file(all_missing_files, pc)

    if len(all_missing_files) == 0:
        return False, "nothing"
    else:
        return True, path
