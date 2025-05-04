# MP3Cover

A simple desktop application that allows you to add cover art to your MP3 files with just a few clicks.

## Features

- Easy-to-use graphical user interface
- Select multiple MP3 files at once
- Add JPG/PNG images as cover art

## Creating an Executable

You can create a standalone executable using PyInstaller:

1. Install PyInstaller:

    ``` cmd
    pip install pyinstaller
    ```

2. Create the executable:

    ```cmd
    pyinstaller build_config.spec
    ```

The executable will be in the `dist` folder.
