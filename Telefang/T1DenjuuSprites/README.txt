*** Telefang 1 Denjuu Sprite Exporter/Importer v0.1 ***
by Blaziken257

I. Intro
--------

This tool lets you import or extract sprites from a Telefang 1 ROM. Quite useful for ripping the sprites in the game, or editing them!

II. Installation
----------------

You need Python 2.7.3 for this. Python 3 most likely won't work! Download Python 2.7.3 here:
http://python.org/download/releases/2.7.3/

(If you use Python 3, I've heard of a 2to3 tool that converts this program so that it works properly on Python 3, but you're on your own here. If you're confused, just stick with Python 2.7.3.)

III. Usage
----------

To export sprites, double-click on export.py. To import sprites, double-click on import.py.

  A. Exporting sprites
  --------------------

  When starting export.py, you will first have to open your Telefang ROM. You can drag the file into the command line window for simplicity. It must be a valid ROM -- Telefang 2 will not work here! You will then be asked to enter the number of the Denjuu. For a list, go here:

  http://wikifang.meowcorp.us/wiki/List_of_Denjuu_in_Telefang_1

  You will then be asked for color or grayscale. Enter 1 for grayscale, and anything else for color.

  The program will print the Denjuu name, sprite offset, the color palette offset, the entire color palette (in both RGB and GBC format), and the filename of the exported image. (It will be Denjuu###.png in the same directory as export.py.)

  The resulting Denjuu will face to the left, as it is stored in the ROM.

  After it is done, press Enter to quit the program.

  B. Importing sprites
  --------------------

  Importing sprites is a bit more complicated, so this section will be a bit longer.

  For desired results, the Denjuu should face to the left, as it is stored in the ROM. If it is facing to the right, then the Denjuu will face the wrong direction when playing the game.

  As with exporting sprites, you will be asked to open your Telefang ROM. You will next be asked to enter the number of the Denjuu that you want to import to the ROM. Also, the Denjuu, sprite offset, and color palette offset will be printed.

  Next, you will have to open the image file that you want to import to the ROM. Please note the following:

  - It must be a PNG file.
  - It cannot have more than 4 colors, as this exceeds the GBC hardware limitations.
  - The maximum dimensions must be 64 pixels in width, 56 pixels in height. The sprite importer doesn't accept larger images.
    - While a size of 64x56 is optimal, the importer will accept smaller images. It will then pad it to 64x56 if smaller.

  There are other conditions that, while the importer will accept, it will warn you about them:

  - If the image has less than 4 colors, the importer will warn you about this. It will still accept it, but it will tell you that you can use more colors!
  - If the brightest image is not completely white, the importer will warn you about this too, and will point out that you will see a colored rectangle around the Denjuu when it is seen.
  - If the image is smaller than 64x56, the importer will tell you that is smaller than the maximum limit.

  If the image is accepted by the importer, it will build the color palette, and print it on the screen. After all colors have been found, it will sort them so that the sprite will look normal when Telefang is run in monochrome mode (i.e., on a DMG or SGB). The program will then encode the tiles and write everything to ROM.

  After it is done, press Enter to quit the program.

  C. Issues
  ---------

  If there are issues that you find with either of these two programs, feel free to report them in the thread in Tulunk Village where you found the programs.