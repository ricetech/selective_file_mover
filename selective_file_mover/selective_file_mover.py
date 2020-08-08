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

# Program constants
SETTINGS_FILE_PATH = "selective_file_mover_settings.txt"
EXCLUDED_FILES_FILE_PATH = "excluded_files.txt"


def main():
    while True:
        try:
            usage_dir = "D:/0 PF/Steam/steamapps/common/Grand Theft Auto V"
            option = int(input("Select an option:\n"
                               "1: Move files into game directory\n"
                               "2: Move files back into storage directory (overwritten files restored)\n"
                               "3: Quit\n"
                               "Input 1/2/3: "))
            get_files_to_move(usage_dir, get_lines_from_file(EXCLUDED_FILES_FILE_PATH))
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


def get_vars_from_txt(file):
    """
    Extracts variables from a text file and places them into a dictionary.
    Required format:
    File type - txt
    Blank lines - only one allowed at the end of the file
    Comments - Use # at the beginning of the line
    Variables - Variable name at the beginning of the line followed by an equals sign followed by the value. Example:
    sample_var = sample val
    :param file: A text file following the guidelines above.
    :return: A dictionary containing all of the variables extracted from the file.
    """
    variables = {}
    with open(file, "r") as settings:
        for line in settings:
            if line[0] == '#':
                continue
            elif len(line.split('=')) == 2:
                var = line.strip().split('=')
                # Add path to dictionary
                variables[var[0].strip()] = var[1].strip()
            else:
                print(">> ERROR: Line format is invalid. Did you add an extra line or delete a '=' by accident?: " +
                      line)
                crash_with_confirm()
        return variables


def move_files(items, dir_1, dir_2, overwrite_dir):
    files_overwritten = False
    # overwrite_dir is for files that get overwritten
    # Make sure overwrite_dir is empty
    if len(os.listdir(overwrite_dir)) != 0:
        print(">> ERROR: Cannot move files: Overwrite Directory must be empty: " + overwrite_dir)
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
    files_to_move = [file for file in all_contents if file not in excluded_files]
    return files_to_move


def get_lines_from_file(file):
    with open(file, 'r') as f:
        lines = f.read().splitlines()
    return lines


if __name__ == '__main__':
    main()
