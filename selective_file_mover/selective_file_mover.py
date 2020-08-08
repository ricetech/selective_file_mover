# Selective File Mover
# August 7th, 2020
# Version 1.1.1
# Eric Chen
# @the_ricetech
#
# This script is designed to move a large amount of files and folders from one directory to another while ignoring
# certain files and folders.
# Throughout this program, 'item' refers to an objects which can be a file OR a folder.
# See the readme for more details.
#
# Originally written to solve my personal woes when trying to move all of my singleplayer mod files out of the GTA V
# folder so that I could play online without getting banned for singleplayer mods.

import os
import shutil
from time import sleep

# Program constants
SETTINGS_FILE_PATH = "selective_file_mover_settings.txt"
EXCLUDED_ITEMS_FILE_PATH = "excluded_items.txt"
OVERWRITE_DIRECTORY_NAME = "0 Overwritten Files (Selective File Mover)"


def main():
    # Get storage/usage paths from file
    usage_dir, store_dir, overwrite_dir, excluded_items = get_paths_and_files()
    # Run program
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


def get_paths_and_files():
    """
    Retrieves the variables required for the program to work: usage_dir, store_dir, overwrite_dir and excluded_items.
    Split into a separate function for readability.
    """
    try:
        dir_paths = get_vars_from_txt(SETTINGS_FILE_PATH)
    except FileNotFoundError:
        print(f">> ERROR: Unable to locate the settings file - {SETTINGS_FILE_PATH}. Make sure it was not renamed.")
        crash_with_confirm()
        return  # Unused return statement to avoid false warnings in code editors
    try:
        excluded_items = get_lines_from_file(EXCLUDED_ITEMS_FILE_PATH)
    except FileNotFoundError:
        print(f">> ERROR: Unable to locate the settings file - {EXCLUDED_ITEMS_FILE_PATH}. "
              f"Make sure it was not renamed.")
        crash_with_confirm()
        return  # Unused return statement to avoid false warnings in code editors
    try:
        usage_dir = dir_paths['usage_dir']
        store_dir = dir_paths['storage_dir']
        overwrite_dir = os.path.join(store_dir, OVERWRITE_DIRECTORY_NAME)
    except KeyError:
        print(">> ERROR: The required variables 'usage_dir' and 'storage_dir' were not present in the settings file: "
              f"{SETTINGS_FILE_PATH}. Please ensure you are using the correct file.")
        crash_with_confirm()
        return  # Unused return statement to avoid false warnings in code editors
    return usage_dir, store_dir, overwrite_dir, excluded_items


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


def move_files(items, source_dir, dest_dir, overwrite_dir):
    overwritten_files = []
    # overwrite_dir is for files that get overwritten

    # Make sure overwrite_dir is empty
    try:
        if len(os.listdir(overwrite_dir)) != 0:
            print(">> ERROR: Cannot move files: Overwrite Directory must be empty: " + overwrite_dir)
            crash_with_confirm()
    except FileNotFoundError:  # Create overwrite_dir if it doesn't exist
        os.makedirs(overwrite_dir)

    for item in items:
        # Ignore overwrite folder
        if item == OVERWRITE_DIRECTORY_NAME:
            continue

        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        # Debugging test - you can uncomment this if you prefer to see it.
        # WARNING: Uncommenting this will result in significantly slower operations.
        # print("From:", source_path)
        # print("To:", dest_path)
        if os.path.exists(dest_path):
            # Move overwritten file to overwrite_dir
            shutil.move(dest_path, overwrite_dir)
            shutil.move(source_path, dest_path)
            overwritten_files.append(dest_path)
        else:
            # If destination file does not exist, move file normally
            shutil.move(source_path, dest_path)
    return overwritten_files


def get_files_to_move(usage_dir, excluded_items):
    dir_contents = os.listdir(usage_dir)
    items_to_move = [item for item in dir_contents if item not in excluded_items]
    return items_to_move


def get_lines_from_file(file):
    with open(file, 'r') as f:
        lines = f.read().splitlines()
    return lines


if __name__ == '__main__':
    main()
