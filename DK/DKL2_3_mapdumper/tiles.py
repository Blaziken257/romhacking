import rom_utilities

def decompress(f,offset):
    f.seek(offset)

    #Number of tiles
    no_tiles = rom_utilities.readbyte(f)
    print "Number of tiles:", no_tiles
    offset += 1

    #REALLY HARD PART
    #DECOMPRESS TILES
    print "Decompressing the tiles."

    tile_counter = 0
    row_counter = 0
    tile_pointer = 0x00FE
    carry = 0
    raw_tiles = []

    #This code is confusing, but it works perfectly!
    while no_tiles > tile_counter:
        f.seek(offset)
        x = rom_utilities.readbyte(f) #x = register c in ASM code
        offset += 1
        counter = 8
        while counter > 0:
            tile_pointer = (tile_pointer & 0xFF) + 0x3F00
            f.seek(tile_pointer)
            y = rom_utilities.readbyte(f) #y = register a in ASM code
            tile_pointer -= 0x100
            x = (x << 1) + carry
            if x > 0xFF:
                carry = 1
            else:
                carry = 0
                tile_pointer -= 0x100
                y = rom_utilities.swap_nib(y)
            x &= 0xFF
            y = (y << 1) + carry
            if y > 0xFF:
                carry = 1
                f.seek(tile_pointer)
                temp = rom_utilities.readbyte(f)
                tile_pointer = (tile_pointer & 0xFF00) + temp
                counter -= 1
            else:
                carry = 0
                f.seek(tile_pointer)
                tile = rom_utilities.readbyte(f)
                raw_tiles.append(tile)
                row_counter += 1
                tile_pointer = (tile_pointer & 0xFF00) + 0x00FE
                if row_counter == 0x10:
                    row_counter = 0
                    tile_counter += 1
                    if no_tiles <= tile_counter:
                        counter = 0 #This breaks the loop!
                counter -= 1
            y &= 0xFF
    return raw_tiles, no_tiles
