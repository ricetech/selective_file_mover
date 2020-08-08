# Selective File Mover
# August 7th, 2020
# Version 1.1.1
# Eric Chen
# @the_ricetech
#
# This script is designed to move a large amount of files and folders from one directory to another.
# See the readme for more details.
#
# Originally written to solve my personal woes when trying to move all of my singleplayer mod files out of the GTA V
# folder so that I could play online without getting banned for singleplayer mods.

import os
import shutil
from time import sleep


def main():
    while True:
        try:
            usage_dir = "D:/0 PF/Steam/steamapps/common/Grand Theft Auto V"
            option = int(input("Select an option:\n"
                               "1: Move files into game directory\n"
                               "2: Move files back into storage directory (overwritten files restored)\n"
                               "3: Quit\n"
                               "Input 1/2/3: "))
            get_files_to_move(usage_dir, retrieve_excluded_files())
            """
            if option == 1:
                all_files = os.listdir(store_dir)
                move_files(all_files, store_dir, usage_dir, error_dir)
            elif option == 2:
                move_files(listOfFiles, usage_dir, store_dir, temp_dir)
                tempFiles = os.listdir("C:/Program Files/Steam/steamapps/common/Grand Theft Auto V/tempW")
                move_files(tempFiles, temp_dir, usage_dir, error_dir)
                if os.listdir(error_dir):
                    print("CAUTION: Something went wrong. Check emergency directory.")
                    input("Press Enter to continue.")
            elif option == 3:
                break
            else:
                print("Invalid input. Try again.")"""
            input()
        except ValueError:
            print("Error: Invalid input")


def crash_with_confirm():
    """
    'Crashes' the program by quitting with exit code 1, but asking the user for any input beforehand to ensure
    those using Terminal/Command Prompt have enough time to read the error before the program exits.
    The error causing this condition must be displayed using a print statement before calling this function.
    """
    input(">> Program cannot continue due to this error. Press Enter to exit.")
    exit(1)


def move_files(items, dir_1, dir_2, overwrite_dir):
    files_overwritten = False
    # overwrite_dir is for files that get overwritten
    # Make sure overwrite_dir is empty
    if len(os.listdir(overwrite_dir)) != 0:
        print("Cannot move files: Overwrite Directory must be empty: " + overwrite_dir)
        crash_with_confirm()

    for item in items:
        source = os.path.join(dir_1, item)
        dest = os.path.join(dir_2, item)
        print("From:", source)
        print("To:", dest)
        if os.path.exists(dest):
            # Move overwritten file to overwrite_dir
            shutil.move(dest, overwrite_dir)
            shutil.move(source, dest)
            files_overwritten = True
        else:
            # If destination file does not exist, move file normally
            shutil.move(source, dest)
    return files_overwritten


def get_files_to_move(usage_dir, excluded_files):
    all_contents = os.listdir(usage_dir)
    unique_contents = [file for file in all_contents if file not in excluded_files]
    return unique_contents


def retrieve_excluded_files():
    with open("files.txt", 'r') as f:
        files = f.read().splitlines()
    return files


if __name__ == '__main__':
    main()
