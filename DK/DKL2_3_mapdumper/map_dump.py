#This is such a mess, I know!!
#I need to clean this later on...

import sys
try:
    import png
except ImportError:
    sys.exit("You need to have the PyPNG package installed in order to run this program.\n\
For more information, go to:\n\
http://pypi.python.org/pypi/pypng/0.0.13")
import os
import struct

import settings
from level_info import level_ptrs, level_names, level_types
import tiles
import rom_utilities
import game_map

if sys.version >= '3':
    sys.exit("Python 3 is not supported at this time due to lack of backwards compatibility. You will have to use Python 2. Sorry!")

print "DKL2/3 Map Dumper v1.0 beta"
print "Enter the filename of your DKL2 or DKL3 ROM or drag it here:"
#Read ROM file
rom = rom_utilities.open_file([".gb",".sgb",".gbc"],"rb")

rom.seek(0x134)
header = rom.read(16)
#Read ROM header to detect correct game
print 'ROM header: "{}"'.format(header.rstrip('\xC0'))
game = None
region = None
version = 0

if header == b"DONKEYKONGLAND95":
    game, region = "DKL", "U"
elif header == b"SUPERDONKEYKONG ":
    game, region = "DKL", "J"
elif header == b"DONKEYKONGLAND 2":
    game, region = "DKL2", "U"
elif header == b"DONKEYKONGLAND\0\0":
    game, region = "DKL2", "J"
elif header == b"DONKEYKONGLAND 3":
    game, region = "DKL3", "U"
    rom.seek(0x14C)
    version = rom_utilities.readbyte(rom) #There are two English versions of DKL3, but I don't know of any difference besides the title screen.
elif header == b"DONKEY KONGAD3J\xC0":
    game, region = "DKL3", "J"
elif header == b"DK COUNTRY\0BDDE\xC0":
    game, region = "DKC", "U"
elif header == b"DKC 2001\0\0\0BDDJ\xC0":
    game, region = "DKC", "J"
else: #Reject non-Donkey Kong ROM
    sys.exit("Invalid ROM. You must use a DKL2 or DKL3 ROM.")

if game == "DKC":
    sys.exit("Donkey Kong Country (GBC) is not supported by this tool. A different tool would have to be used, although it is unlikely that I will ever create one due to lack of interest.")
if game == "DKL":
    sys.exit("Donkey Kong Land is not supported by this tool. A different tool would have to be used!")
elif game == "DKL2":
    if region == "U":
        print "Game: Donkey Kong Land 2 (English)"
    elif region == "J":
        print "Game: Donkey Kong Land 2 (Japanese)"
elif game == "DKL3":
    if region == "U":
        print "Game: Donkey Kong Land III (English, v1.{})".format(version)
    elif region == "J":
        print "Game: Donkey Kong Land III (Japanese)"

#Print list of level names, and number used to choose them
for i in range(len(level_names[game])/3):
    buf = ""
    for j in range(3):
        k = i*3+j
        buf = buf + "{: >2}".format(k) + " - " + "{: <19}".format(level_names[game][k]) + " "
    print buf

#Prompt for the desired level
print "Please enter the level number:"
level = raw_input()
valid_level = False
#Check for proper input
while valid_level == False:
    try:
        level = int(level)        
        if level < 0 or level >= len(level_names[game]):
            print "Invalid level. Try again:"
            level = raw_input()
        else:
            valid_level = True
    except ValueError:
        print "You must enter an integer! Try again:"
        level = raw_input()
del valid_level
level_id = level_ptrs[game][level]
print "Internal level ID: {}".format(level_id)
print "You have selected: {}.".format(level_names[game][level])

#Get level header data, which is used for various things like the right tiles, water level, etc.
level_header = rom_utilities.get_rel_ptr(rom, 0x10, 0x40001, level_id)
print "Level header offset: {:#x}".format(level_header)

#Get level type (Stilt, River, etc.)
rom.seek(level_header+1)

level_type = rom_utilities.readbyte(rom)
print "Level type: {:#x} ({})".format(level_type,level_types[game][level_type])

#Find address for compressed tiles
tile_offset = rom_utilities.get_abs_ptr(rom, 0x10, 0x40005, level_type)
print "Compressed tiles are located at: {:#x}".format(tile_offset)

raw_tiles, no_tiles = tiles.decompress(rom,tile_offset)

#Output tileset as PNG file
if settings.tileset == True:
    imagearea=(no_tiles+0xF)/0x10*0x400
    imagewidth=0x80
    imageheight=imagearea/imagewidth
    pixel_map = rom_utilities.decode_tiles(imageheight, imagewidth, raw_tiles, 1)

    grayscale = True

    #Could use some cleaning up
    if grayscale == True:
        bitdepth = 2
        palette = None

    #Get right filepath, essentially creates "DKL3/Tileset" or "DKL2/Tileset" folder
    if not os.path.exists(os.path.join(os.getcwd(), game)):
        os.makedirs(os.path.join(os.getcwd(), game))
    if not os.path.exists(os.path.join(os.getcwd(), game, 'Tileset')):
        os.makedirs(os.path.join(os.getcwd(), game, 'Tileset'))

    filename = "{}_{}_Tileset_{}.png".format(game,region,level_types[game][level_type].replace(" ","_"))
    filename = os.path.join(os.getcwd(), game, 'Tileset', filename)
    imagefile = open(filename, "wb")
    print "Writing tiles to {}.".format(filename)
    w=png.Writer(imagewidth, imageheight, palette=palette, compression=9, greyscale=grayscale, bitdepth=bitdepth)
    w.write(imagefile,pixel_map)
    imagefile.close()

imagearea=no_tiles*0x40
imagewidth=no_tiles*8
imageheight=imagearea/imagewidth

pixel_map = rom_utilities.decode_tiles(imageheight, imagewidth, raw_tiles, 1)

#NOW DECOMPRESS MAPS
rom.seek(level_header)
map_id = rom_utilities.readbyte(rom)
#Find offset for map data
map_offset = rom_utilities.get_abs_ptr(rom, 0x10, 0x40003, map_id)
print "Reading map and decompressing it from offset {:#x}.".format(map_offset)

rom.seek(map_offset)
#Get width and height
width, height, level_map = game_map.decompress(rom, map_offset, game, region, level, level_type)[:3]

#Hex dump to external file, useful for debugging
if settings.hexdump == True:        
    if not os.path.exists(os.path.join(os.getcwd(), game)):
        os.makedirs(os.path.join(os.getcwd(), game))
    if not os.path.exists(os.path.join(os.getcwd(), game, 'Hexdumps')):
        os.makedirs(os.path.join(os.getcwd(), game, 'Hexdumps'))
    
    filename = "{}_{}_Map_{}_Hex.bin".format(game,region,level_names[game][level].replace(" ","_"))
    filename = os.path.join(os.getcwd(), game, 'Hexdumps', filename)
    mapfile = open(filename, "wb")
    print "Writing hex dump of map to {}.".format(filename)
    for i in level_map:
        for j in i:
            mapfile.write(chr(j))
    print "Done."
    mapfile.close()

#Arrange 8x8 tiles into 32x32 ones
tile_address = rom_utilities.get_abs_ptr(rom, 0x10, 0x40007, level_type, scale=6, endian="<")
print "Arranging 8x8 tiles into 32x32 ones, starting at ROM offset: {:#x}".format(tile_address)

#Prompt for color/monochrome... DKL3 in Japanese is a special case since it is for GBC and not SGB
if game == "DKL3" and region == "J":
    print "Please enter 0 for GBC color palettes or 1 for monochrome, then press Enter:"
    mode = raw_input()
    if mode != "1":
        mode = "GBC"
    else:
        mode = "GB"
else:
    print "Please enter 0 for SGB color palettes or 1 for monochrome (GB),\n\
then press Enter:"
    mode = raw_input()
    if mode != "1":
        mode = "SGB"
    else:
        mode = "GB"

#Get palettes
if mode == "GBC":
    grayscale = False
    bitdepth = 8
    color_pointer = rom_utilities.get_abs_ptr(rom, 0x10, 0x40011, level_type, scale=6, offset=3, endian="<")
    rom.seek(color_pointer)
    palette=[]
    for i in range(8):
        raw_palette = struct.unpack("<HHHH",rom.read(8))
        for j in raw_palette:
            color = rom_utilities.gbc2rgb(j)
            palette.append(color)
    if level_id == 34 or level_id == 25: #Ugly Ducting, Haunted Hollows -- meant for raster shade effect in water
        if level_id == 34:
            #Bytes in color are fragmented!!! (It is generated on the fly, and ASM code separates the two bytes)
            rom.seek(0x14F72)
            color = rom_utilities.readbyte(rom)
            rom.seek(0x14F76)
            color = color + (rom_utilities.readbyte(rom) << 8)
        else:
            rom.seek(0x14F60)
            color = rom_utilities.readbyte(rom)
            rom.seek(0x14F64)
            color = color + (rom_utilities.readbyte(rom) << 8)
        color = rom_utilities.gbc2rgb(color)
        palette.append(color)
    #Print them on screen (I ought to find a better way to do this)
    print "+--------------+-------------+-------------+-------------+-------------+"
    print "|              |   R   G   B |   R   G   B |   R   G   B |   R   G   B |"
    print "+--------------+-------------+-------------+-------------+-------------+"
    for i in range(8):
        buf = "| BG Palette {}".format(i+1)
        for j in range(4):
            buf = buf + " | "
            for k in range(3):
                buf = buf + "{:>3}".format(palette[i*4+j][k])
                if k < 2:
                    buf = buf + " "
        buf = buf + " |"
        print buf
    print "+--------------+-------------+-------------+-------------+-------------+"
    if level_id == 34:
        buf = "| Alt. Pal. 1 "
        for i in [0,32,2,3]:
            buf = buf + " | "
            for j in range(3):
                buf = buf + "{:>3}".format(palette[i][j])
                if j < 2:
                    buf = buf + " "
        buf = buf + " |"
        print buf
        print "+--------------+-------------+-------------+-------------+-------------+"
    elif level_id == 25:
        buf = "| Alt. Pal. 1 "
        for i in [0,1,2,32]:
            buf = buf + " | "
            for j in range(3):
                buf = buf + "{:>3}".format(palette[i][j])
                if j < 2:
                    buf = buf + " "
        buf = buf + " |"
        print buf
        print "+--------------+-------------+-------------+-------------+-------------+"
    #Now we have the color palettes, but we still must give the tiles the right colors
    color_address = rom_utilities.get_abs_ptr(rom, 0x10, 0x40011, level_type, scale=6, endian="<")
    #Get color palettes for SGB games
elif mode == "SGB":
    grayscale = False
    bitdepth = 8
    palette = []
    if game == "DKL2":
        color_pointer = 0x10283 + (level_type+6)*2
    elif game == "DKL3":
        color_pointer = 0x10283 + (level_id+6)*2
    rom.seek(color_pointer)
    color_pointer = rom_utilities.ram2rom(0x4,rom_utilities.readshort(rom)) + 2
    rom.seek(color_pointer)
    print "Loading color palette at ROM offset {:#x}.".format(color_pointer)
    for i in range(4):
        color = rom_utilities.readshort(rom,"<")
        color = rom_utilities.gbc2rgb(color)
        palette.append(color)
    print "+------------+-------------+-------------+-------------+-------------+"
    print "|            |   R   G   B |   R   G   B |   R   G   B |   R   G   B |"
    print "+------------+-------------+-------------+-------------+-------------+"
    buf = "| BG Palette".format(i+1)
    for i in range(4):
        buf = buf + " | "
        for j in range(3):
            buf = buf + "{:>3}".format(palette[i][j])
            if j < 2:
                buf = buf + " "
    buf = buf + " |"
    print buf
    print "+------------+-------------+-------------+-------------+-------------+"
    color_address = 0x0
else:
    grayscale = True
    bitdepth = 2
    palette = None
    color_address = 0x0
    
#In some levels (e.g. Lava Lagoon, Slime Climb, Clapper's Cavern, Toxic Tower, Ugly Ducting, and Haunted Hollows,
#the water is shaded
rom.seek(level_header+3)
print "Reading bit 6 from from offset {:#x} for water shading.".format(level_header+3)
water_shade = rom_utilities.readbyte(rom)
water_shade = rom_utilities.bit_test(water_shade,6)
if water_shade == 1:
    print "Water is shaded in this level."
    rom.seek(level_header+5)
    water_level = rom_utilities.readbyte(rom)
    print "Reading water level from offset {:#x}.".format(level_header+5)
    print "Water level: {:#x} (from top, in multiples of 0x20 pixels)".format(water_level)
else:
    print "Water is not shaded in this level."
    water_level = 0xFF

#Write map tiles to a PNG file
if settings.maptiles == True:
    map_image = []
    for i in range(0x100):
        map_image.append([])

    for i in range(0x8):
        for j in range(0x4):
            for k in range(0x10):
                tile_value = i*0x10+k
                for l in range(0x4):
                    tile_pos = j*4+l
                    tile_pointer = tile_address + tile_value + 0x100 * tile_pos
                    rom.seek(tile_pointer)
                    map_tile = rom_utilities.readbyte(rom)
                    pixel_pos = map_tile * 0x8
                    if mode == "GBC":
                        color_pointer = color_address + tile_value + 0x100 * tile_pos
                        rom.seek(color_pointer)
                        color_tile = rom_utilities.readbyte(rom)
                        color_tile &= 0x7
                    else:
                        color_tile = 0
                    for m in range(0x8):
                        for n in range(0x8):
                            if pixel_pos < no_tiles * 8:
                                try:
                                    pixel = pixel_map[m][n+pixel_pos]
                                except IndexError:
                                    print "ERROR: Array out of bounds!\n\
i = {}; j = {}; k = {}; l = {}; m = {}; n = {}; width of pixel_map = {}; ({} tiles); height of pixel_map = {} ({} tiles); map_tile = {}; pixel_pos = {}".format(i,j,k,l,m,n,len(pixel_map[0]),len(pixel_map[0])/8,len(pixel_map),len(pixel_map)/8,map_tile,pixel_pos)
                                    print "Please report the bug in the thread where you found it."
                            else:
                                pixel = 0
                            pixel = pixel + color_tile*4
                            map_image[m+0x8*j+0x20*i].append(pixel)

    if not os.path.exists(os.path.join(os.getcwd(), game)):
        os.makedirs(os.path.join(os.getcwd(), game))
    if not os.path.exists(os.path.join(os.getcwd(), game, 'Maptiles')):
        os.makedirs(os.path.join(os.getcwd(), game, 'Maptiles'))

    filename = "{}_{}_Map_Tiles_{}.png".format(game,region,level_types[game][level_type].replace(" ","_"))
    filename = os.path.join(os.path.join(os.getcwd(), game, 'Maptiles'), filename)
    imagefile = open(filename, "wb")
    print "Writing to {}.".format(filename)
    w=png.Writer(0x200, 0x100, palette=palette, compression=9, greyscale=grayscale, bitdepth=bitdepth)
    w.write(imagefile,map_image)
    print "Done."
    imagefile.close()

#Write the actual map to a PNG file!
#Based on the map data, the tile arrangements, and the colors, this part generates the correct pixels
print "Generating the map!"
map_image = []

map_image = game_map.gen_image(rom,width,height,no_tiles,pixel_map,level_map,level_id,tile_address,color_address,mode,game,water_shade,water_level)
imagewidth = width*0x20
imageheight = height*0x20

print ""
if not os.path.exists(os.path.join(os.getcwd(), game)):
    os.makedirs(os.path.join(os.getcwd(), game))
if not os.path.exists(os.path.join(os.getcwd(), game, 'Maps')):
    os.makedirs(os.path.join(os.getcwd(), game, 'Maps'))
    
filename = "{}_{}_Map_{}.png".format(game,region,level_names[game][level].replace(" ","_"))
filename = os.path.join(os.getcwd(), game, 'Maps', filename)
imagefile = open(filename, "wb")
print "Writing to {}.".format(filename)
w=png.Writer(imagewidth, imageheight, palette=palette, compression=9, greyscale=grayscale, bitdepth=bitdepth)
w.write(imagefile,map_image)
print "Done."
imagefile.close()

