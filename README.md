# selective_file_mover

This is a tool to exclude a certain set of files and folders when moving files back and forth between two folders.

While it was originally designed for modding the videogame GTA V, it can work for a variety of other purposes as well.

## Why this was created

The original purpose of this tool was to alleviate frustrations I experienced while experimenting with modifying files in a videogame called GTA V. I would modify the game files to add a custom vehicle in single player, but would need to move my modified single player files out of the game folder before trying to play GTA V Online (Multiplayer) to avoid getting banned for having modified files, even though those modified files did not affect multiplayer.

## What this tool does

- Allows for quick file moving between two folders:
  - A 'usage directory' where the files are actively used, and
  - A 'storage directory' where the files are kept when they are not in use
- When files are being moved from the usage directory to the storage directory, they are checked against the list of excluded items. Files or folders on the list of excluded items are ignored (left in the usage directory) while the rest of the files are moved to the storage directory.
- When files are being moved back from the storage directory to the usage directory, they are all moved since it is assumed that the step above occurred properly.
- This back-and-forth operation can be repeated simply by running the program over and over again.

Here's a visual diagram of the operation:

<img src="README.assets/How it works.png" alt="How it works" style="zoom: 15%;" />

Obviously, the ideal use case involves a significantly greater number of files and folders involved.

## Requirements

- Python 3.6 or newer: https://www.python.org/

## Instructions

Download the latest release here: https://github.com/ricetech/selective_file_mover/releases. 

You can also clone the entire repository if you would like, but the program is not guaranteed to work properly if you go down that route since commits may contain untested features. Therefore, I suggest downloading the latest stable release instead.

After downloading and extracting the program, you will first need to modify `selective_file_mover_settings.txt` and `excluded_items.txt` to suit your needs. If  you don't, the program <u>__will not work__</u>.

### selective_file_mover_settings.txt

There are two very important variables that you will need to change to suit your use case:

- `usage_dir` - This is the 'usage directory' mentioned in [What this tool does](##What this tool does). This is where all of your files should normally be when they're being used.
- `storage_dir` - This is the 'storage directory' mentioned in [What this tool does](##What this tool does). This is where your files **except** excluded files are moved when you ask the program to place your files in storage.
  - This folder should be empty when you first set up the program unless you're reinstalling the program.

You should edit the part after the equal sign to contain the **full path** to the folder.

Here are some important points about this file:

- Do not use relative paths. Use full paths instead (starting with a drive letter if you use Windows).
- The paths can use either forward slashes or backslashes.
- Do NOT edit or remove the equal sign or anything before the equal sign. Doing so will break the program.
- Do NOT add any extra lines.

### excluded_items.txt

In this file, put in all of the files and folders that you want the program to ignore when moving files **from** the usage directory **to** the storage directory. Remember that the program ignores the excluded items when moving from the storage directory back to the usage directory since it assumes that you used the program to move the files there in the first place.

Here are the requirements for this file:

- Each file or folder name should be on its own line.
- A new line at the end of the file is optional.
- There should not be any other blank lines in the file.
- Do not use forward or backslashes.
- At present, it is impossible to exclude a file or folder that is nested inside of another folder.
  - You can exclude an entire folder, but you cannot exclude one specific file inside of this folder and move the rest.
  - This feature can be added if the demand rises.

### Using the program

Once you fill out both files, run `selective_file_mover.py`. The options are explained in the program.

## Feedback/Suggestions/Bugs

If you have a suggestion or have discovered an issue, please open an issue on GitHub: https://github.com/ricetech/selective_file_mover/issues.