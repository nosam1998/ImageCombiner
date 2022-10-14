# ImageCombiner

The script can be used to combine all images in the sub-folders of the `in/` folder directory.

The sub-folder names are used in the text file called `READ_ME_FIRST.txt`. This file is automatically created when you successfully run the script.

## Constraints
- All images have to be the same width and height. For example each image has to be `1920x1080`. Just make the background of the image transparent.
- I've only tested the `.PNG` file format. Please use other file formats with caution.
- Currently, tested with `Python 3.8.10`. You might be able to use another version of python 3 but I haven't tested any others yet.


## Run
1. Install `Python 3.8.10`
2. Open up `cmd.exe` or `powershell.exe`
3. Type `python main.py` (It's possible that instead of `python` you might need to use `python3` or even `python38`. This will depend on your PC.)
4. You will be prompted if you want to re-order the images. You need to type `Y` or `N` to proceed.
    1. if you type `Y`. Then you'll want to type the number to the left of the sub-folder and press `enter`. Do this until no more options remain.
    2. if you type `N`. Then the program will continue with the default settings.
5. You should see a folder named `out/`. In that folder you'll find a file named `READ_ME_FIRST.txt`. That file shows how the filename of each image is formatted/built.

#### _DONE!_

The script is dynamic. You can add more sub-folders in the `in/` directory. You can also add more files in each sub-folder.

## Example Input Folder Structure
#### Valid file structure #1:
- `in/`
    - `caps/`
      - `blue.png`
      - `violet.png`
    - `panels/`
      - `dark.png`
      - `light.png`
    - `wood/`
      - `light-blue.png`
      - `light-blue-scribble.png`
      - `orange.png`
    
#### Valid file structure #2:
- `in/`
    - `a`
      - `one.png`
      - `two.png`
    - `b`
      - `three.png`
    - `c`
      - `four.png`
      - `five.png`
      - `six.png`
      - `seven.png`
    - `d`
      - `eight.png`
      - `nine.png`

#### INVALID/NOT Tested file structure #1:
- `in/`
    - `one.png`
    - `two.png`
    - `three.png`