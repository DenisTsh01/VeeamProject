import shutil
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def sync(main_folder, backup_folder, log_message):
    datenow = datetime.now()

###############################################################If files don't exist
    if os.path.exists(main_folder) == 0:  # if main folder doesn't exist, we create one
        os.makedirs(main_folder)
        print("Backup folder created successfully")

        main_log_message = os.path.join(main_folder, log_message)
        with open(main_log_message, 'a') as log_file:
            log_file.write(f"{datenow}: {os.path.basename(main_folder)} was successfully created.  \n")

    if os.path.exists(backup_folder) == 0:  # if backup folder doesn't exist, we create one
        os.makedirs(backup_folder)
        print("Backup folder created successfully")
        main_log_message = os.path.join(main_folder, log_message)
        with open(main_log_message, 'a') as log_file:
            log_file.write(f"{datenow}: {os.path.basename(backup_folder)} was successfully created.  \n")

    if os.path.exists(log_message) == 0:
        file = os.path.join(main_folder, log_message)
        with open(file, 'a') as log_file:
            log_file.write(f"{datenow}: {log_file} was successfully created. \n")
        print(f"{datenow}: {os.path.basename(file)} was successfully created.")

    main_log_message = os.path.join(main_folder, log_message)
    with open(main_log_message, 'a') as log_file:
        log_file.write(f"Log: {datenow}: Syncing ...\n")
    print(f"Log: {datenow}: Syncing ...")
############################################################################################################

    all_from = os.listdir(main_folder)  # list of all files from our main folder
    all_to = os.listdir(backup_folder)  # list of existing files of backup folder

    for file in all_from:  # adding a file
        if file not in all_to:
            main_file = os.path.join(main_folder, file)
            backup_file = os.path.join(backup_folder, file)
            shutil.copyfile(main_file, backup_file)
            print(f"{datenow}: File {file} was successfully copied in {os.path.basename(backup_folder)}.")
            main_log_message = os.path.join(main_folder, log_message)
            with open(main_log_message, "a") as log_file:
                log_file.write(
                    f"{datenow}: File {file} was successfully added to {os.path.basename(backup_folder)}.  \n")

    for file in all_to:  # deleting extra files
        if file not in all_from:
            file_path = os.path.join(backup_folder, file)
            os.remove(file_path)
            message2 = f"{datenow}: File {file} was successfully removed from {os.path.basename(backup_folder)}. \n "
            main_log_message = os.path.join(main_folder, log_message)
            with open(main_log_message, "a") as log_file:
                log_file.write(
                    f"{datenow}: File {file} was successfully removed from {os.path.basename(backup_folder)}. \n")
            print(message2)

    for root, dirs, files in os.walk(backup_folder):
        for file in all_from:
            backup_file_path = os.path.join(root, file)
            main_file_path = os.path.join(main_folder, file)

            with open(backup_file_path, 'r') as backup_file:
                backup_content = backup_file.read()

            with open(main_file_path, 'r') as main_file:
                main_content = main_file.read()

            if backup_content != main_content:
                main_log_message = os.path.join(main_folder, log_message)

                backup_log_message = os.path.join(root, os.path.basename(log_message))

                with open(main_log_message, "a") as log_file:
                    log_file.write(
                        f"{datenow}: File {os.path.basename(backup_file_path)} from {os.path.basename(backup_folder)} was successfully updated.\n")
                log_file.close()
                print(backup_log_message)

                shutil.copy(main_file_path, backup_file_path)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    dir_path = input("Main folder dir: ")
    backup_dir = input("Backup folder dir: ")
    log_dir = input("Log dir: ")
    duration = int(input("Backup interval (seconds):"))
    sync(fr"{dir_path}", fr"{backup_dir}", fr"{log_dir}")
    scheduler.add_job(sync, 'interval', args=[dir_path, backup_dir, log_dir], seconds=duration)
    scheduler.start()
