# Selective File Mover
# January 4th, 2020
# Revision 1.1.0
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


def move_files(items, dir_1, dir_2, overwrite_dir):
    # Dir1 should be where the files are moved to when they need to be used
    # Dir2 is where they should be stored when not in use
    for item in items:
        source = os.path.join(dir_1, item)
        dest = os.path.join(dir_2, item)
        print("From:", source)
        print("To:", dest)
        try:
            if os.path.exists(dest):
                shutil.move(dest, overwrite_dir)
                shutil.move(source, dest)
            else:
                shutil.move(source, dest)
        except FileNotFoundError:
            print("Error: File not Found: " + str(source))


def list_mod_files(game_dir, excluded_files):
    all_contents = os.listdir(game_dir)
    unique_contents = [file for file in all_contents if file not in excluded_files]
    return unique_contents


def retrieve_excluded_files():
    with open("files.txt", 'r') as text:
        files = text.read().splitlines()
        print(files)
    return files


while True:
    try:
        usage_dir = "D:/Files/Program Files/Steam/steamapps/common/Grand Theft Auto V"
        #option = int(input("Select an option:\n"
        #                   "1: Move files into usage directory (overwritten files go to temp\n"
        #                   "2: Move files back into storage directory (overwritten files restored)\n"
        #                   "3: Quit\n"
        #                   "Input 1/2/3: "))
        list_mod_files(usage_dir, retrieve_excluded_files())
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
