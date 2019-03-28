from Scripts import BackupSyncEngine


def main(PC):
    with open("Resources/Backups/" + PC + "/Received_Backup.txt", "r", encoding="utf-8-sig") as RB:
        RB = RB.readlines()
        newRB = []
        for lines in RB:
            if lines.__contains__("\n"):
                newline = lines.replace("\n", "")
                newRB.append(newline)
            else:
                newRB.append(lines)

    with open("Resources/Backups/" + PC + "/Backup2.txt", "r", encoding="utf-8-sig") as B:
        B = B.readlines()
        newB = []
        for line in B:
            if line.__contains__("\n"):
                newline = line.replace("\n", "")
                newB.append(newline)
            else:
                newB.append(line)

    MissingFiles = []
    ChangedFiles = []
    MissingFolders = []

    RB_files = []
    for index, lines in enumerate(newRB):
        if lines.__contains__("["):
            RB_files.append(newRB[index-1])
            RB_files.append(lines)

    B_files = []
    for index, line in enumerate(newB):
        if line.__contains__("["):
            B_files.append(newB[index-1])
            B_files.append(line)


    for index, lines in enumerate(RB_files):
        if not lines.__contains__("["):
            i = False
            j = False
            for index2, line in enumerate(B_files):
                if line == lines:
                    i = True
                    if RB_files[index+1] == B_files[index2+1]:
                        pass
                    else:
                        j = True
                else:
                    pass
            if i == False:

                MissingFiles.append(lines)
            if j == True:
                ChangedFiles.append(lines)
        else:
            pass

    RB_folders = []
    for index, lines in enumerate(newRB):
        if str(lines).__contains__("["):
            pass
        else:
            try:
                if newRB[index + 1].__contains__("["):
                    pass
                else:
                    RB_folders.append(lines)
            except:
                pass

    B_folders = []
    for index, lines in enumerate(newB):
        if str(lines).__contains__("["):
            pass
        else:
            try:
                if newB[index + 1].__contains__("["):
                    pass
                else:
                    B_folders.append(lines)
            except:
                pass

    for index, lines in enumerate(RB_folders):
        i = False
        for index2, line in enumerate(B_folders):
            if line == lines:
                i = True
            else:
                pass
        if i == False:
            MissingFolders.append(lines)


    print("MISSING FILES")
    for i in MissingFiles:
        print("\t"+i)

    print("CHANGED FILES")
    for i in ChangedFiles:
        print("\t"+i)

    print("MISSING FOLDERS")
    for i in MissingFolders:
        print("\t"+i)
    BackupSyncEngine.add_folder(MissingFolders, PC)

    allMissingFiles = MissingFiles + ChangedFiles
    pathy = BackupSyncEngine.get_file(allMissingFiles, PC)

    if len(allMissingFiles) == 0:
        return False, "nothing"
    else:
        return True, pathy


if __name__ == '__main__':
    main()
