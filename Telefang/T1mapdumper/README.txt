*** Telefang Map Dumper v2.1 ***
by Blaziken257

I. About
--------

The Telefang Map Dumper rips maps of your choice using any Telefang ROM. It has support for all maps in the game, and can generate color and grayscale maps. It has some support for hacked ROMs as well. While the program can rip maps, it cannot edit them.

A. Version history
------------------

- v1.0: Released on November 21, 2011
  This is the first release.

- v2.0: Released on August 19, 2012
  The second release. Additions/changes:
  - Program now uses PNG format for images instead of PGM and PPM images. This has the following benefits:
    - This change makes it much easier to be able to view the images in the first place, since PNG is much more widespread than PGM or PPM.
    - These images are now losslessly compressed, resulting in a smaller filesize.
    - Alpha transparency is now used for invalid acres, as opposed to making the pixels darker.

    To accomplish the ability to output PNG images, the PyPNG library is used. It is included with this program, so you don't need to download anything extra, but you can always download it here if you want to use this library in any of your own Python programs: https://pypi.python.org/pypi/pypng/0.0.15

- v2.1: Released on May 15, 2012
  The third release. Additions/changes:
  - Now the entire tileset of each map is output to a file called "outputtiles.png".
  - The user can now choose the hour when overworld maps are chosen. Previously, the palette depended on the hour of the computer's clock.

II. How to use
--------------

A. Getting started
------------------

In order to use this program, you must have Python 2.7.4 installed. This program will NOT run on Python 3. To download Python 2.7.4, visit this link:

http://www.python.org/getit/releases/2.7.4/

(Note: This program may still run on earlier versions of Python 2.7.)

B. Starting the program
-----------------------

Once Python 2.7.4 is installed, you can start the Telefang Map Dumper by double-clicking on mapdump.py. If done correctly, a terminal window should pop up.

C. Using a Telefang ROM
-----------------------

Here, you will be asked to enter the filename of your Telefang ROM (you also may drag the file to the window). It must end in .gbc, meaning it must not be compressed.

D. Map selection
----------------

If it is a valid Telefang ROM, the program will ask you to specify the map that you want to dump. Here is a list of locations:

02 - Overworld - Upper left quadrant         03 - Overworld - Upper right quadrant
04 - Overworld - Lower left quadrant         05 - Overworld - Lower right quadrant
06 - Antenna Trees - Upper left quadrant     07 - Antenna Trees - Upper right quadrant
08 - Antenna Trees - Lower left quadrant     09 - Antenna Trees - Lower right quadrant
10 - Toronko Village Spring                  11 - Marts/Houses
12 - Northeast Cavern - Floor 1              13 - Northeast Cavern - Floor 2
14 - Craft Research Center                   15 - Dementia's Mansion
16 - Tripa Antenna Tree - Floor 1            17 - Tripa Antenna Tree - Floor 2
18 - Tripa Antenna Tree - Floor 3            19 - Tripa Antenna Tree - Floor 4
20 - Tripa Antenna Tree - Floor 5            21 - Pepperi Mountains - Floor 1
22 - Pepperi Mountains - Floor 2             23 - Pepperi Mountains - Floor 3
24 - Pepperi Mountains - Floor 4             25 - Pepperi Mountains - Floor 5
26 - Cactos Ruins - Floor 1                  27 - Cactos Ruins - Floor 2
28 - Cactos Ruins - Floor 3                  29 - Cactos Ruins - Floor 4
30 - Cactos Ruins - Floor 5                  31 - Cactos Ruins - Floor 6
32 - Cactos Ruins - Floor 7                  33 - Cactos Ruins - Floor 8
34 - Burion Ruins - Floor 1                  35 - Burion Ruins - Floor 2
36 - Burion Ruins - Floor 3                  37 - Burion Ruins - Floor 4
38 - Burion Ruins - Floor 5                  39 - Burion Ruins - Floor 6
40 - Burion Ruins - Floor 7                  41 - Burion Ruins - Floor 8
42 - Burion Ruins - Floor 9                  43 - Human World - Main Area
44 - Human World - Antenna Tree              45 - Human World - Unused Buildings
46 - Teletel/Dendel room                     47 - Unused replica of Golaking's room
48 - Second D-Shot room                      49 - Palm Sea Antenna Tree switch room
50 - Sanaeba Research Center - Floor 1       51 - Sanaeba Research Center - Basement 1
52 - Sanaeba Research Center - Basement 2

You can also type L or l to list the maps. After you determine the number of the map that you want to dump, you should enter that number; you can use decimal or hex. For example, if you want to dump a map of the first floor of Tripa Antenna Tree, you can enter 16 or 0x10.

Maps 00 and 01 may also be entered, but are not fully supported since they were unfinished in the game, as well as inaccessible. The tiles may not match what the game uses, so the program will warn you about this. 

Some unused maps, such as the unused buildings of the Human World, are supported.

No maps above 52 are supported, as they are just garbage data, and there is no point to dumping them.

E. Color/grayscale 
------------------

Next, the program will ask if you want to dump the map in grayscale or in color. Enter 0 for color or 1 for grayscale. Entering anything else will also produce a color map.

In grayscale, the maps will appear just as they do on the regular Game Boy, which means they will be in four shades of gray. While grayscale maps are less aesthetically pleasing, they have certain advantages:
- The program will not have to color the tiles (described below), resulting in less time to dump the map.
- The grayscale map will be significantly smaller than the color map, since it does not have to store the colors.

If color is chosen, the game read in the color palettes, then later apply them to the tiles once they are read in. When the map is dumped, it will appear just like it does on a Game Boy Color. This process will take a bit more time and will result in a larger file size, but color maps are arguably better looking.

If an overworld map is chosen, then the program will ask you to enter the hour. This will affect the color palette used (e.g. noon will have a bright color palette, night will have a dark palette, etc.). Note that this is changed starting in v2.1; previously, the user could not choose the hour, and instead it was chosen by the current hour of the computer's clock.

F. Map generation
-----------------

Once you entered all the information, the program will start ripping the map from the game. It accomplishes this by:
1. Finding the pointer of the map
2. Generating the 8x8-acre map
3. Finding the bank in which all 64 map acres are located
4. Generating the 10x8-tile acres
5. Reading the tiles from one of the image files, depending on the map
6. If color is chosen, generating the eight color palettes
7. Finding the pointer of the tile table, necessary to construct the 16x16-pixel tiles from the 8x8-pixel tiles
8. If color is chosen, finding the pointer of the tile color palette table, necessary to color all the tiles

At this point, no more reading is necessary, and the program closes the ROM.

Next, the program places each 16x16-pixel tile in each acre. At this point, the entire map is generated.

G. Writing to files 
-------------------

1. Map tilesets
---------------

New to v2.1, the program will first write to "outputtiles.png". This file contains the map's entire tileset, though there will always be corrupted tiles, since none of the maps use 256 tiles. Due to this being in the PNG format, the image will be losslessly compressed. This image will be 256x256 in dimensions. If the grayscale option is chosen, the filesize will be smaller.

2. World maps
-------------

Next, the most important image will be dumped, the map itself. The program will write to "outputmap.png". This will also be in the PNG format, and the same principles from the tileset image apply to this image (except the dimensions here will be 1280x1024).

When the program finds invalid acres (most acres of value 0x00 are invalid, with certain specific exceptions), the game applies alpha transparency to the acres so that the map is easier to read.

Previously, as mentioned before, the program would output to "outputmap.ppm" and "outputmap.pgm" files, and invalid acres would be shaded instead of translucent, but this has now changed.

It is possible that the option for COMPLETE transparency will be supported in a future release. This has the advantage of a smaller file size due to the option to use color indexing.

H. Limitations
--------------

As this program is fairly new, there are various limitations that it has. Many of these limitations can possibly be improved upon in a future release.

- The map dumper cannot merge certain maps together:
    - The program can only dump the regular overworld maps, and the antenna tree maps separately. As a result, the antenna trees will have weird looking tiles when dumping overworld maps, and vice versa. This is because they use entirely different tilesets. In the game, when entering or exiting an antenna tree, the game reloads tiles while the screen fades out so that it uses the proper tiles. As of now, the only way to work around this limitation is to dump the maps twice, copy the acres generated from the antenna tree map, and paste them on the regular overworld map. It is possible that in a future release, these maps will be merged together.
    - In the Human World, the main area, the antenna tree, and the unused building maps can only be dumped separately due to the same reason. Again, this may be improved in a future version of the program.
    - The program can only dump overworld maps one quadrant at a time.
- The map dumper dumps maps at a fixed size of 1280x1024, and does not crop off invalid acres. They must be removed manually.

- The program does not dump sprites at all. There are two parts to this problem:
    - There has been very limited research on how the game generates sprites in the first place.
    - Since some sprites disappear at different points in the game, and others move around, it is difficult to determine if they should be displayed, or where they should be positioned on the map.
    
- The program does not label warps. This is unfortunate for people stuck in Dimenza's Mansion, as dumping warp data would be quite useful here. However, the main problem is figuring out to label the warps, as there are many different situations that would need to be covered, and labeling anything in the first place is complicated.

- The program does not label treasure chests. While the data structure for treasure chests is fully understood, figuring out how to place the items on the screen is a different story.

- While the map dumper works to some extent with hacked ROMs, it assumes that the ROM is not hacked in some ways.
    - While the pointers of all maps are read from ROM, the pointer table (0x19C000) is hardcoded into the program. Therefore, if the pointer table is moved for any reason, the program will not work properly.
    - While the bank that contains the map acres is likewise read from ROM, the absolute pointer table (0x2760) is also hardcoded. Again, moving this table will confuse the program.
    - The tile graphics are not read from ROM at all, but rather stored in pgm files (this remains even in v2.1!). If the tiles are hacked, the program will not reflect that unless the pgm files are modified too. This is due to the difficulty of decompressing them. In addition, if the maps are hacked to use different tilesets, the program also won't reflect that (but can be changed easily starting at line 168 in the source code).
    - The color palettes are read from ROM, but the offsets are all hardcoded. While changing the color palettes won't confuse the program (any palette changes correctly will show up in the dumped map), moving them to different offsets /will/ confuse it, and will result in incorrect palettes when the map is dumped.
    - The pointers for the tile table (for constructing 16x16 tiles from 8x8 tiles) and the tile color palette table (for coloring the 8x8 tiles within a 16x16 tile) are read from ROM, but the pointer tables for each (0x178000 and 0x178022) are hardcoded into the program. Changing the pointers in the tables, as well as the data itself, is fine, but moving the pointer tables will confuse the map dumper.
    - The map dumper assumes that there are only 52 maps (counting the unused maps 0x01 and 0x02). If the ROM is extended to allow more than 52 maps, the program won't be able to read maps 53 and beyond.
    - The method to determine which acres are invalid is entirely dependent on the ROM being unhacked. However, this can be changed in the validacre function in the acres.py file.
    - While not tested extensively on Pokémon Diamond, Pokémon Jade, or the Telefang Power English translation, the map dumper SHOULD work just fine on all of these ROMs.

If map hacks of this game start to spring up, this program will provide better support for hacked ROMs.
    
- The way that the program parses PGM files is buggy. This works OK for all the current PGM files as long as they are not modified. However, there are two problems:
    - The only whitespace delimiter that the program currently recognizes is one and only one newline ('\x0A' or '\n'), not anything else. Spaces, tabs, and carriage returns will throw the program off, as well as more than one newline in a row.
    - The program does not recognize comments at all, since it does not recognize "#" as a special character.
        - These problems are largely due to dealing with multiple delimiters. However, this definitely needs to be improved on in a future release.
    - The PGM files may be removed in a future release, anyway, and replaced with a tile decompression algorithm.

- Finally, while the program has been tested on Windows and Ubuntu, it has not been tested on anything else, including Mac. There is no way for me to be able to test this program anywhere else.

- Report bugs in the Tulunk Village forum: http://s15.zetaboards.com/Tulunk_Village/
