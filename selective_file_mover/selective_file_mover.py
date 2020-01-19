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

# SETTINGS
# Live Usage Directory:
usage_dir = "D:/Files/Program Files/Steam/steamapps/common/Grand Theft Auto V"
# Storage area for mod files when not in use
store_dir = "D:/Files/Program Files/0 GTA BACKUP/f_store"
# Directory to put files in if something goes wrong
error_dir = "D:/Files/Program Files/0 GTA BACKUP/z_error_catch_dir"
# List of files to remain in the game directory
gta_files = [
    'Installers',
    'update',
    'x64',
    'bink2w64.dll',
    'commandline.txt',
    'common.rpf',
    'd3dcompiler_46.dll',
    'd3dcsx_46.dll',
    'GFSDK_ShadowLib.win64.dll',
    'GFSDK_TXAA.win64.dll',
    'GFSDK_TXAA_AlphaResolve.win64.dll',
    'GTA5.exe',
    'GTAVLanguageSelect.exe',
    'GTAVLauncher.exe',
    'installscript.vdf',
    'PlayGTAV.exe',
    'steam_api64.dll',
    'x64a.rpf',
    'x64b.rpf',
    'x64c.rpf',
    'x64d.rpf',
    'x64e.rpf',
    'x64f.rpf',
    'x64g.rpf',
    'x64h.rpf',
    'x64i.rpf',
    'x64j.rpf',
    'x64k.rpf',
    'x64l.rpf',
    'x64m.rpf',
    'x64n.rpf',
    'x64o.rpf',
    'x64p.rpf',
    'x64q.rpf',
    'x64r.rpf',
    'x64s.rpf',
    'x64t.rpf',
    'x64u.rpf',
    'x64v.rpf',
    'x64w.rpf'
]


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


def store_mod_files():
    pass


def retrieve_mod_files():
    pass


while True:
    try:
        option = int(input("Select an option:\n"
                           "1: Move files into usage directory (overwritten files go to temp\n"
                           "2: Move files back into storage directory (overwritten files restored)\n"
                           "3: Quit\n"
                           "Input 1/2/3: "))
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
    except ValueError:
        print("Error: Invalid input")
