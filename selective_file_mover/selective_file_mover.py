# Selective File Mover
# August 8th, 2020
# Version 2.0.0
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
    # Get storage/usage paths from files
    usage_dir, store_dir, overwrite_dir, excluded_items = get_paths_and_files()
    # Run program
    while True:
        clear_screen()
        try:
            option = int(input("\nSelect an option:\n" +
                               "1: Move files from usage directory into storage directory\n" +
                               "2: Move files from storage directory into usage directory\n" +
                               "3: Quit\n" +
                               "Input 1/2/3: "))
            if option == 1 or option == 2:  # Usage to Storage
                if option == 1:  # Usage to Storage
                    files_to_move = get_files_to_move(usage_dir, excluded_items)
                    from_dir = usage_dir
                    to_dir = store_dir
                else:  # Storage to Usage
                    # option must == 2 because of the or condition in the parent if statement
                    from_dir = store_dir
                    to_dir = usage_dir
                    files_to_move = os.listdir(store_dir)
                # Move files
                try:
                    overwritten_files = move_files(files_to_move, from_dir, to_dir, overwrite_dir)
                except ValueError as e:
                    print(">> ERROR:", e)
                    crash_with_confirm()
                    return  # Unused return statement to avoid false warnings in code editors
                if not overwritten_files:
                    input("\n>> Operation completed successfully. Press Enter to continue.")
                else:  # Something got overwritten
                    input("\n>> WARNING: Files were overwritten during this operation, which is now complete.\n"
                          "Press Enter to see the list of overwritten files.\n")
                    print("List of overwritten files:")
                    sleep(0.5)
                    for file in overwritten_files:
                        print(file)
                    sleep(0.5)
                    input(f"\n>> The overwritten files (the files that were already in '{to_dir}')\n"
                          f"were moved to '{overwrite_dir}'."
                          f"\nPlease check there and fix the conflicts yourself.\n"
                          f"Remember that you cannot move files using this program without\n"
                          f"emptying that folder, so please remember to do that before using this program again.\n\n"
                          f">> Press Enter to continue. The screen will be cleared.")
            elif option == 3:
                break
            else:
                input(f">> ERROR: Input was not a valid option: {option}. Press Enter to try again.")
        except ValueError:
            input(">> Error: Input was not a number. Press Enter to try again.")


def clear_screen():
    """This function clears the console. It does not work in IDE Terminals."""
    os.system('cls' if os.name == 'nt' else 'clear')


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
    except ValueError as e:
        print(">> ERROR:", e)
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
                raise ValueError("Line format is invalid. Did you add an extra line or delete a '=' by accident?: " +
                                 line)
        return variables


def move_files(items, source_dir, dest_dir, overwrite_dir):
    """
    Moves a files AND folders matching any name in items from source_dir to dest_dir.
    If a file already exists in dest_dir, the version in dest_dir is moved to overwrite_dir and the version from
    source_dir is moved into dest_dir.
    :param items: The list of file and folder names to move. These names should be relative to source_dir and dest_dir,
    and should NOT be full file paths.
    :param source_dir: The directory (full path) to move from.
    :param dest_dir: The directory (full path) to move to.
    :param overwrite_dir: The directory (full path) to send overwritten files to.
    :return: A list of files (full path) in dest_dir that were overwritten. Empty list if no files were overwritten.
    """
    overwritten_files = []
    # overwrite_dir is for files that get overwritten

    # Make sure overwrite_dir is empty
    try:
        if len(os.listdir(overwrite_dir)) != 0:
            raise ValueError("Cannot move files: Overwrite Directory must be empty: " + overwrite_dir)
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
    """
    Produces a list of files/folders in the directory usage_dir that **do not** match a name found in excluded_items.
    :param usage_dir: The directory to scan.
    :param excluded_items: List of file/folder names to ignore. These will not show up in the return, even if found.
    :return: A list of files/folders in usage_dir that do NOT match a name in excluded_items.
    """
    dir_contents = os.listdir(usage_dir)
    items_to_move = [item for item in dir_contents if item not in excluded_items]
    return items_to_move


def get_lines_from_file(file):
    """
    Extracts lines from a text file.
    :param file: The text file to extract lines from.
    :return: A list containing all lines of file.
    """
    with open(file, 'r') as f:
        lines = f.read().splitlines()
    return lines


if __name__ == '__main__':
    main()
