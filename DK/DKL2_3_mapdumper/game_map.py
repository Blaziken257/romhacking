import rom_utilities
import settings
import os
import struct
import sys

import level_info

class Nibble:
    def __init__(self, rom, logfile, offset, log=True):
        self.nib_pos = 1
        self.offset = offset
        self.rom = rom
        self.logfile = logfile
        self.log = log
    def readnibble(self, count=1):
        self.value = 0
        for i in range(count):
            self.value <<= 4
            if self.nib_pos == 1:
                if self.log == True:
                    self.logfile.write("ROM: {:#x}\r\n".format(self.offset))
                self.byte = rom_utilities.readbyte(self.rom)
                self.nibble = (self.byte & 0xF0) >> 4
                self.nib_pos = 0
            elif self.nib_pos == 0:
                self.nibble = (self.byte & 0xF)
                self.nib_pos = 1
                self.offset += 1
            self.value |= self.nibble
        return self.value

def decompress(f, offset, game, region, level, level_type):
    """Returns a decompressed map.
    f = file
    offset = Self explanatory.
    game = Name of game, used for the filename for logging.
    level = Name of level, used for the filename for logging.
    level_type = Type of level (e.g. Stilt), used for the filename for logging."""
    width = rom_utilities.readbyte(f)
    height = rom_utilities.readbyte(f)
    print "Width: {}; Height: {}".format(width,height)
    offset += 2

    read_map = True
    level_map = []
    for i in range(height):
        level_map.append([])
    x = 0
    y = 0
    buf = []

    #Log to external file for debugging
    if settings.maplog == True:
        if not os.path.exists(os.path.join(os.getcwd(), game)):
            os.makedirs(os.path.join(os.getcwd(), game))
        if not os.path.exists(os.path.join(os.getcwd(), game, 'Logs')):
            os.makedirs(os.path.join(os.getcwd(), game, 'Logs'))

        filename = "{}_{}_Map_{}_log.txt".format(game,region,level_info.level_names[game][level].replace(" ","_"))
        filename = os.path.join(os.getcwd(), game, 'Logs', filename)
        maplog = open(filename, "wb")
        print "Writing log of map decompression to {}.".format(filename)

        rom_utilities.write_log("Width: {}; Height: {}".format(width,height),maplog)
    else:
        maplog = None

    #Decompression starts here, read one nibble (4 bits) at a time
    nib = Nibble(f, maplog, offset, settings.maplog)

    while read_map == True:
        nibble = nib.readnibble()
        rom_utilities.write_log("Nibble read: {:#x}".format(nibble),maplog)
        #Nibbles 0xC, 0xD, 0xE, and 0xF are special cases, as are nibble pairs 0xBE and 0xBF
        #(Note: Figuring this out would have been IMPOSSIBLE without BGB's debugger!!)
        if nibble == 0xB:
            temp = nibble
            nibble = nib.readnibble()
            rom_utilities.write_log("Nibble read: {:#x}".format(nibble),maplog)
            if nibble < 0xE: #Normal byte, this means nibble pair is from 0xB0-0xBD -- this is uncompressed
                buf.append((temp << 4) + nibble)
            elif nibble == 0xE: #0xBE
                #Decompress certain tiles, increasing tile value by 1 each time (useful for long tile structures)
                tile = nib.readnibble(count=2)
                rom_utilities.write_log("Tile: {:#04x}".format(tile),maplog)
                length = nib.readnibble()
                rom_utilities.write_log("Length: {:#x} + 0x3 -> {:#x}".format(length,length+0x3),maplog)
                for i in range(length+3):
                    buf.append(tile)
                    tile += 1
                    
            elif nibble == 0xF: #0xBF
                #Meant for 32x16-tile structures
                tile1 = nib.readnibble(count=2)
                tile2 = nib.readnibble(count=2)

                length = nib.readnibble()

                rom_utilities.write_log("Tile 1: {:#04x}; Tile 2: {:#04x}; Length: {:#x} + 0x2 -> {:#x}".format(tile1, tile2, length, length+0x2),maplog)
                for i in range(length+2):
                    buf.append(tile1)
                    buf.append(tile2)
        elif nibble == 0xC:
            #Repeat previously used tile sequence, allows the same structure over and over
            rew = nib.readnibble(count=2)

            if rew % 2 == 1: #Odd number
                rew = rew / 2 + 1
                rew = rew + (nib.readnibble() << 7)
            else: #Even number
                rew = rew / 2 + 1

            rom_utilities.write_log("Rewind: {:#04x}".format(rew),maplog)
            
            length = nib.readnibble()

            if length == 0xF:
                length = nib.readnibble(count=2)

            rom_utilities.write_log("Length: {:#04x} + 0x04 -> {:#04x}".format(length, length+0x4),maplog)

            for i in range(length+4):
                ptr = y*width+x - rew
                ptr_y = ptr / width
                ptr_x = ptr % width
                tile = level_map[ptr_y][ptr_x]
                rom_utilities.write_log("Pointer: {}; x: {}; y: {}; tile: {:#04x}; RAM: {:#x} -> {:#x}".format(ptr, ptr_x, ptr_y, tile, 0xC600+(height+4)*2+ptr, 0xC600+(height+4)*2+y*width+x),maplog)
                if x >= width:
                    y += 1
                    x = 0
                try:
                    level_map[y].append(tile)
                except IndexError:
                    if settings.warnings == True:
                        #Error handler
                        print "WARNING: Out of range!\n\
There are more bytes than the map can handle.\n\
This is either due to a badly hacked ROM, a bug in the game itself,\n\
or an error in the program's decompression function.\n\
If this results in a buggy map, please report this.\n\
x: {}; y: {}; i: {}; buffer: {}; map width: {}; map height: {}; RAM: {:#x}; ROM: {:#x}\n\
Press Enter to continue or Ctrl+C to quit.".format(x,y,i,buf,len(level_map[0]),len(level_map),0xC600+(height+4)*2+y*width+x,offset)
                    read_map = False
                    byte = 0xEE
                    f.seek(1,1)
                    raw_input()
                    break
                x += 1

        elif nibble == 0xD:
            #Here, tiles only take up four bits -- useful when lots of tiles in a row are next to each other
            high_nibble = nib.readnibble() << 4
            rom_utilities.write_log("High nibble: {:#x}".format(high_nibble),maplog)
            length = nib.readnibble(count=2)
            rom_utilities.write_log("Length: {:#04x} + 0x14 -> {:#x}".format(length,length+0x14),maplog)

            for i in range(length+0x14):
                low_nibble = nib.readnibble()
                tile = high_nibble | low_nibble
                rom_utilities.write_log("Low nibble: {:#x}; Tile: {:#04x}".format(low_nibble, tile),maplog)
                buf.append(tile)
        
        elif nibble == 0xE:
            #Same case as before, but for shorter structures (also takes slightly up less space in ROM)
            high_nibble = nib.readnibble() << 4
            rom_utilities.write_log("High nibble: {:#x}".format(high_nibble),maplog)
            if high_nibble == 0xE0: #We are done!! Stop reading map tiles
                read_map = False
            else:
                length = nib.readnibble()

                rom_utilities.write_log("Length: {:#x} + 0x4 -> {:#x}".format(length,length+0x4),maplog)

                for i in range(length+4):
                    low_nibble = nib.readnibble()
                    tile = high_nibble | low_nibble
                    rom_utilities.write_log("Low nibble: {:#x}; Tile: {:#04x}".format(low_nibble, tile),maplog)
                    buf.append(tile)

        elif nibble == 0xF:
            #Same tile repeated over and over
            tile = nib.readnibble(count=2)
            length = nib.readnibble()

            rom_utilities.write_log("Tile: {:#04x}".format(tile),maplog)

            if length >= 8:
                length = ((length & 0x7) << 4) + nib.readnibble()
                rom_utilities.write_log("Length: {:#04x} + 0x0b -> {:#04x}".format(length,length+0xb),maplog)

                for i in range(length+11):
                    buf.append(tile)
            else:
                rom_utilities.write_log("Length: {:#x} + 0x3 -> {:#x}".format(length,length+0x3),maplog)
                for i in range(length+3):
                    buf.append(tile)
        else: #Normal case!! Uncompressed tile (0x00-0xAF)
            temp = nibble
            nibble = nib.readnibble()
            rom_utilities.write_log("Nibble read: {:#x}".format(nibble),maplog)
            tile = (temp << 4) + nibble
            buf.append(tile)
            rom_utilities.write_log("Uncompressed tile! ({:#04x})".format(tile),maplog)
        if len(buf) > 1:
            rom_utilities.write_log("Buffer: {}; x: {}; y: {}; RAM: {:#x} - {:#x}".format(buf,x,y,0xC600+(height+4)*2+y*width+x,0xC5FF+(height+4)*2+y*width+x+len(buf)),maplog)
        elif len(buf) == 1:
            rom_utilities.write_log("Buffer: {}; x: {}; y: {}; RAM: {:#x}".format(buf,x,y,0xC600+(height+4)*2+y*width+x),maplog)
        else:
            rom_utilities.write_log("x: {}; y: {}; RAM: {:#x}".format(x-1,y,0xC5FF+(height+4)*2+y*width+x),maplog)
        #Write the tiles
        for i in buf:
            if x >= width:
                y += 1
                x = 0
            try:
                level_map[y].append(i)
            except IndexError:
                if settings.warnings == True:
                    #Error handler
                    print "WARNING: Out of range!\n\
There are more bytes than the map can handle.\n\
This is either due to a badly hacked ROM, a bug in the game itself,\n\
or an error in the program's decompression function.\n\
If this results in a buggy map, please report this.\n\
x: {}; y: {}; i: {}; buffer: {}; map width: {}; map height: {}; RAM: {:#x}; ROM: {:#x}\n\
Press Enter to continue or Ctrl+C to quit.".format(x,y,i,buf,len(level_map[0]),len(level_map),0xC600+(height+4)*2+y*width+x,offset)
                read_map = False
                nib.byte = 0xEE
                f.seek(1,1)
                raw_input()
                break
            x += 1
        buf = []

    print "Done decompressing the map tiles."
    if settings.maplog == True:
        print "Done writing to log."
        maplog.close()
    #print level_map

    print "Note: Sprites are not supported yet."

    #Initial code for sprites
    if nib.byte & 0xF0 == 0xE0 and nib.byte != 0xE0 and nib.byte != 0xEE:
        #Not sure if this ever actually occurs, but it imitates the game
        #This function exists because sometimes the EE string ends on a high nibble (e.g. _E E_); sometimes on a low one (e.g. __ EE __)
        f.seek(-1,1)
    #Initially, any tile with a sprite is initialized to 0x80. We must find the sprite table to use the correct graphics (and add sprites when that gets implemented)
    #Sprite pointers take place just after the initial map data, and they are read each time the game finds a tile with value 0x80 or greater
    for i,v in enumerate(level_map):
        for j,w in enumerate(level_map[i]):
            tile_id = w
            if tile_id == 0xFF:
                break
            if rom_utilities.bit_test(tile_id,7) == 1:
                sprite_id = rom_utilities.readbyte(f)
                level_map[i][j] = sprite_id

    sprite_address = rom_utilities.get_abs_ptr(f, 0x10, 0x4000B, level_type)
    sprite_table = []
    #Now the sprite pointers are used to find tuples with the right tile graphics and the sprites (latter is not implemented yet)
    for i,v in enumerate(level_map):
        for j,w in enumerate(level_map[i]):
            sprite_id = w
            if rom_utilities.bit_test(sprite_id,7) == 1:
                sprite_id &= 0x7F
                f.seek(sprite_address + sprite_id*3)
                tile_id = rom_utilities.readbyte(f)
                level_map[i][j] = tile_id
                sprite_id = struct.unpack("<BB",f.read(2))
                sprite_table.append((i,j,sprite_id[0],sprite_id[1]))
                #Used to implement sprites later on!!!
    return width, height, level_map, sprite_table

def gen_image(f,width,height,no_tiles,pixel_map,level_map,level_id,tile_address,color_address,mode,game,water_shade,water_level):
    """Generates uncompressed image of level.
    f: File to read from.
    width: Width of LEVEL in 32x32-pixel tiles.
    height: Height of LEVEl in 32x32-pixel tiles.
    no_tiles: Number of tiles.
    pixel_map: Pixel map, generated from tile.decompress().
    level_map: Uncompress level map from decompress() function.
    level_id: Internal level id.
    tile_address: Location of tile arrangement (used to arrange 8x8 tiles into 32x32 ones).
    color_address: Location of color tile arrangement.
    mode: "GB", "SGB", or "GBC".
    game: "DKL2" or "DKL3", used for proper water shading in certain levels.
    water_shade: Either 1 or 0. 1 causes water to be shaded (in DKL2, only white pixels are shaded; in DKL3, all pixels except black are shaded).
    water_level: Elevation of water. 0 means the level is filled with water; each time this is increased by 1, the water level drops by 32 pixels. It is then further dropped by a certain constant (3 for DKL2, 11 for DKL3)."""
    map_image = []
    
    imageheight = height*0x20
    imagewidth = width*0x20
    imagearea = imageheight*imagewidth

    for i in range(imageheight):
        map_image.append([])

    for i in range(height):
        for j in range(0x4):
            for k in range(width):
                tile_value = level_map[i][k] & 0x7F
                for l in range(0x4):
                    tile_pos = j*4+l
                    tile_pointer = tile_address + tile_value + 0x100 * tile_pos
                    f.seek(tile_pointer)
                    map_tile = rom_utilities.readbyte(f)
                    pixel_pos = map_tile * 0x8
                    if mode == "GBC":
                        #Color the tiles now
                        color_pointer = color_address + tile_value + 0x100 * tile_pos
                        f.seek(color_pointer)
                        color_tile = rom_utilities.readbyte(f)
                        color_tile &= 0xF
                    else:
                        color_tile = 0
                    for m in range(0x8):
                        for n in range(0x8):
                            if pixel_pos < no_tiles * 8:
                                #Get the right pixel based on the map tiles, the way they are arranged, the level map, and the current pixel coordinates
                                pixel = pixel_map[m][n+pixel_pos]
                            else:
                                pixel = 0
                            pixel = pixel + color_tile*4
                            #Shade the water if necessary
                            if game == "DKL3" and water_shade == 1 and water_level * 0x20 < i * 0x20 + j * 0x8 + m - 11:
                                if mode != "GBC":
                                    if pixel > 0: #Non-black pixels
                                        pixel -= 1
                                else: #Darken one color -- uses weird raster effect in-game
                                    if level_id == 34 and pixel == 1: #Ugly Ducting
                                        pixel = 32
                                    elif level_id == 25 and pixel == 3: #Haunted Hollows
                                        pixel = 32
                            elif game == "DKL2" and water_shade == 1 and water_level * 0x20 < i * 0x20 + j * 0x8 + m - 3:
                                if pixel == 3: #White pixels
                                    pixel = 2 #Turn to light gray
                            map_image[m+0x8*j+0x20*i].append(pixel)
        #Refreshes after every 96 rows of pixels                    
        progress = (i + 1)* 100 / height
        if i % 3 == 2 or i + 1 == height or i == 0:
            sys.stdout.write("Progress: {: >7} of {: >7} pixels ({: >3}%) [{}]\r".format((i+1)*0x20*imagewidth, imagearea, progress, "-" * (progress / 5) + " " * ((104 - progress) / 5)))
            sys.stdout.flush()
            
    return map_image
