import struct
#import time
#import sys
import os
try:
    import png
except ImportError:
    sys.exit("You need to have the PyPNG package installed in order to run this program.\n\
For more information, go to:\n\
http://pypi.python.org/pypi/pypng/0.0.13")
from colorize import colorize
from genpalettes import genpalettes
from drawtiles import drawtiles, drawlargetiles
from gamemap import gamemap
from acres import acres, tilemap
from outputfile import outputfile

print "Telefang Map Dumper v2.1"

print "Enter the filename of your Telefang ROM or drag it here:"
while True:
    try:
        filename = raw_input()
        #Yes, this portion of code was taken from IR-GTS-BW. Sue me.
        if filename.startswith('"') or filename.startswith("'"):
            filename = filename[1:]
        if filename.endswith(" "):
            filename = filename[:-1]
        if filename.endswith('"') or filename.endswith("'"):
            filename = filename[:-1]
        if not filename.endswith(".gbc"):
            if filename.endswith(".zip") or filename.endswith(".7z"):
                print "File name must end in .gbc. Do not use compressed files. Enter a new file:"
            else:
                print "File name must end in .gbc. Enter a new file:"
            continue
	filename = os.path.join(os.getcwd(), filename)
        rom = open(filename, "rb")
        break
    except IOError:
        print "File does not exist. Enter in a valid file name:"

rom.seek(0x134)
header = rom.read(8)
if header != b"TELEFANG":
    print 'Header = "%s"' % header
    sys.exit("Invalid ROM. You must use a Telefang ROM.")

print 'Enter in a location. Enter "L" or "l" to see a list of locations.'

location = 0x100

while (location > 0x34 or location < 0x00):
    while True:
        try:
            location = raw_input()
            
            if location.startswith('l') or location.startswith('L'):
                print "List of locations:"
                print "02 - Overworld - Upper left          03 - Overworld - Upper right"
                print "04 - Overworld - Lower left          05 - Overworld - Lower right"
                print "06 - Antenna Trees - Upper left      07 - Antenna Trees - Upper right"
                print "08 - Antenna Trees - Lower left      09 - Antenna Trees - Lower right"
                print "10 - Toronko Village Spring          11 - Mart/Houses"
                print "12 - Northeast Cavern - F1           13 - Northeast Cavern - F2"
                print "14 - Craft Research Center           15 - Dementia's Mansion"
                print "16 - Tripa Antenna Tree - F1         17 - Tripa Antenna Tree - F2"
                print "18 - Tripa Antenna Tree - F3         19 - Tripa Antenna Tree - F4"
                print "20 - Tripa Antenna Tree - F5         21 - Pepperi Mountains - F1"
                print "22 - Pepperi Mountains - F2          23 - Pepperi Mountains - F3"
                print "24 - Pepperi Mountains - F4          25 - Pepperi Mountains - F5"
                print "26 - Cactos Ruins - F1               27 - Cactos Ruins - F2"
                print "28 - Cactos Ruins - F3               29 - Cactos Ruins - F4"
                print "30 - Cactos Ruins - F5               31 - Cactos Ruins - F6"
                print "32 - Cactos Ruins - F7               33 - Cactos Ruins - F8"
                print "34 - Burion Ruins - F1               35 - Burion Ruins - F2"
                print "36 - Burion Ruins - F3               37 - Burion Ruins - F4"
                print "38 - Burion Ruins - F5               39 - Burion Ruins - F6"
                print "40 - Burion Ruins - F7               41 - Burion Ruins - F8"
                print "42 - Burion Ruins - F9               43 - Human World - Main Area"
                print "44 - Human World - Antenna Tree      45 - Human World - Unused Buildings"
                print "46 - Teletel/Dendel room             47 - Unused replica of Golaking's room"
                print "48 - Second D-Shot                   49 - Palm Sea Antenna Tree switch room"
                print "50 - Sanaeba Research Center - F1    51 - Sanaeba Research Center - B1"
                print "52 - Sanaeba Research Center - B2"
                print "\nNow enter in a location. You may either use decimal or hexadecimal format:"
                location = raw_input()
            
            if location.startswith("0x"):
                location = int(location,16)
            else:
                location = int(location)
            
            if (location > 0x34 or location < 0x00):
                print "Invalid location. Enter a different location:"    
            break
        except ValueError:
            print "Invalid input. Please enter in a number:"

if (location < 0x02):
    print "NOTE: Map 0x%02X was not finished in the game, and is therefore not fully\nsupported. Unexpected results may occur. Continue? (Y/N)" % location
    response = raw_input()
    if not response.startswith('Y') and not response.startswith('y'):
        sys.exit("Quitting program.")
elif (location > 0x34):
    print "NOTE: Map 0x%02X is an invalid map, and is therefore not fully supported.\nUnexpected results may occur! Continue? (Y/N)" % location
    response = raw_input()
    if not response.startswith('Y') and not response.startswith('y'):
        sys.exit("Quitting program.")

print "Enter 0 for color or 1 for grayscale:"
grayscale = raw_input()
if grayscale != "1":
    grayscale = 0
else:
    grayscale = 1

game_map_pointer = 0x19C000 + location * 3
rom.seek(game_map_pointer)
print "Getting map template of location 0x%02X at offset 0x%02X..." % (location, game_map_pointer)
map_template = rom.read(1)
map_template = struct.unpack("<B", map_template)[0]
print "Map template of location 0x%02X is 0x%02X." % (location, map_template)
print "Finding pointer of map at offsets 0x%02X to 0x%02X..." % (game_map_pointer + 1, game_map_pointer + 2)
game_map = rom.read(2)
game_map = struct.unpack("<H", game_map)[0]
game_map = 0x19C000 + game_map - 0x4000
    
print "Loading map of location 0x%02X from offsets 0x%X to 0x%X..." % (location, game_map, game_map+0x3F)
map_tiles = gamemap(rom,game_map)
print "Map:", map_tiles

del game_map

rom.seek(0x2760+map_template*3)
print "Reading offset 0x%02X to determine the ROM bank that contains the map acres..." % int(0x2760+map_template*3)
game_acres = (struct.unpack("<B",rom.read(1))[0])
print "ROM bank is 0x%02X." % game_acres
game_acres = game_acres % 0x80 * 0x4000

print "Generating acres starting at offset 0x%X..." % game_acres
acres = acres(rom,map_tiles,game_acres)

pal_offsets = [[0x035280, 0x0352A8, 0x0352D0, 0x0352F8, 0x035320, 0x035348, 0x035370, 0x035398, 0x0353C0, 0x0353E8, 0x035410, 0x035438, 0x035460, 0x035488, 0x0354B0, 0x0354D8, 0x035500, 0x035528, 0x035550, 0x035578, 0x0355A0, 0x0355C8, 0x0355F0, 0x035618],
0x034480, 0x0344C0, 0x034500, 0x034540, 0x034580, 0x0345C0, 0x034600, 0x034640, 0x034680, 0x0346C0]

#Overworld
if (location >= 0x02 and location <= 0x09) or location == 0x00:
    #Prompt for hour
    print "You selected an overworld map. Please select\n\
the desired hour of day, in 24-hour format:"
    validhour = False
    while validhour == False:
        hour = raw_input()
        try:
            hour = int(hour)
            if hour == 24: #Set 24 -> 0, since VBA will undoubtedly confuse people
                hour = 0
            elif hour < 0 or hour > 23:
                print "Invalid hour. You must choose in this range: 0-23. Select an hour:"
            else:
                validhour = True
        except ValueError:
            print "Invalid input. You must enter an integer in the range 0-23:"
    del validhour
    print "Current hour: %d" % hour
    pal_offset = pal_offsets[0][hour]
    if location >= 0x06 or location == 0x00:
        tile_file = "antennatrees.pgm"
    else:
        tile_file = "overworld.pgm"
#Toronko Spring etc.
elif location == 0x0A or location == 0x0C or location == 0x0D:
    pal_offset = pal_offsets[1]
    tile_file = "toronkospring.pgm"
#Marts and houses
elif location == 0x0B:
    pal_offset = pal_offsets[6]
    tile_file = "inside.pgm"
#Craft Research Center etc.
elif location == 0x0E or location == 0x0F or location >= 0x32 or location == 0x01:
    pal_offset = pal_offsets[2]
    tile_file = "craft.pgm"
#Tripa Antenna Tree
elif location >= 0x10 and location <= 0x14:
    pal_offset = pal_offsets[3]
    tile_file = "tripa.pgm"
#Pepperi Mountains
elif (location >= 0x15 and location <= 0x19) or (location >= 0x2E and location <= 0x31):
    pal_offset = pal_offsets[4]
    tile_file = "pepperi.pgm"
#Cactos Ruins
elif location >= 0x1A and location <= 0x21:
    pal_offset = pal_offsets[5]
    tile_file = "cactos.pgm"
#Burion Ruins
elif location >= 0x22 and location <= 0x2A:
    pal_offset = pal_offsets[7]
    tile_file = "burion.pgm"
#Human World - Main Area
elif location == 0x2B:
    pal_offset = pal_offsets[8]
    tile_file = "hworldmain.pgm"
#Human World - Antenna Tree
elif location == 0x2C:
    pal_offset = pal_offsets[9]
    tile_file = "hworldtree.pgm"
#Human World - Unused Buildings
elif location == 0x2D:
    pal_offset = pal_offsets[10]
    tile_file = "hworldsecret.pgm"

#Uncomment this out below if you want to make the maps look slightly
#less glitchy than they do in the actual game

##elif location == 0x01:
##    pal_offset = pal_offsets[1]
##    tile_file = "toronkospring.pgm"
##    tile_table = 0x178E91
##    tile_pal_table = 0x178FA1
##elif location == 0x00:
##    hour = int(time.strftime("%H"))
##    print "Current hour: %d" % hour
##    pal_offset = pal_offsets[0][hour]
##    tile_file = "overworld.pgm"
##    tile_table = 0x178066
##    tile_pal_table = 0x1782DE

else:
    pal_offset = 0x34010
    tile_file = "overworld.pgm"

tile_file = os.path.join(os.getcwd(), "images", tile_file)

print "Reading 8x8 tiles from %s..." % tile_file
tiles = drawtiles(tile_file)
if tiles == -1:
    sys.exit("ASCII format not supported at this time.")
elif tiles == -2:
    sys.exit("Invalid file.")

#Generate all eight palettes
if grayscale == 0:
    print "Generating palettes, starting at offset 0x%06X..." % pal_offset
    palettes = genpalettes(pal_offset,rom)
    print "Palettes:", palettes

print "Finding pointer of 16x16 tile table from map template 0x%02X..." % map_template
rom.seek(0x178000+map_template*2)
tile_table = rom.read(2)
tile_table = struct.unpack("<H", tile_table)[0] + 0x178000 - 0x4000
print "Pointer is at 0x%02X to 0x%02X." % (0x178000+map_template*2, 0x178000+map_template*2 + 1)

#Large tiles = 16x16 tiles, formed from four smaller 8x8 tiles
print "Generating 16x16 tiles from the 8x8 tiles, starting at offset 0x%X..." % tile_table
largetiles = drawlargetiles(rom,tile_table,tiles)

#Color all the tiles
if grayscale == 0:
    print "Finding pointer of tile palette table from map template 0x%02X..." % map_template
    rom.seek(0x178022+map_template*2)
    tile_pal_table = rom.read(2)
    tile_pal_table = struct.unpack("<H", tile_pal_table)[0] + 0x178000 - 0x4000
    print "Pointer is at 0x%02X to 0x%02X." % (0x178022+map_template*2, 0x178022+map_template*2 + 1)
    rom.seek(tile_pal_table)
    print "Colorizing 16x16 tiles, starting at offset 0x%X..." % tile_pal_table
    for i,v in enumerate(largetiles):
        for j in range(2):
            for k in range(2):
                l = rom.read(1)
                l = (struct.unpack("<b", l)[0])%8
                largetiles[i][j][k] = colorize(largetiles[i][j][k],palettes[l])

rom.close()
print "ROM closed."

#Generate every tile used in the entire map
print "Generating every tile in the map..."
tile_map = tilemap(largetiles,acres)

print "Generating map's tileset..."
tileset = tilemap(largetiles)

outputfile("outputtiles.png",1,tileset,map_tiles,location,grayscale)
print "Finished outputting the tiles."

#Each map has 8x8 acres
#Each acre has 10x8 large tiles (so 80x64 large tiles)
#Each large tile is broken up into 2x2 small tiles (so 160x128 small tiles)
#Each small tile is 8x8 pixels (so 1280x1024 pixels per map)
#Each pixel has three colors (so 1280x1024x3 = 3,932,160 colors/map)
outputfile("outputmap.png",0,tile_map,map_tiles,location,grayscale)
print "Finished ripping the map."
print "THANK YOU FOR YOUR USING!\nPress Enter to exit the program."

raw_input()
