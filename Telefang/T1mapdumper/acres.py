import struct

def acres(rom,g_map,offset):

    acre_tiles = []

    for i in range(8):
        acre_tiles.append([])
        for j in range(8):
            acre_offset = offset + 0x50 * g_map[i][j]
            acre_tiles[i].append([])
            for k in range(8):
                acre_tiles[i][j].append([])
                for l in range(10):
                    rom.seek(acre_offset)
                    tile = rom.read(1)
                    acre_tiles[i][j][k].append(struct.unpack("<B", tile)[0])
                    acre_offset += 1
    return acre_tiles

def tilemap(largetiles,acres=None):
    """Generates 16x16 tiles for the whole map.
    Arguments:

    - largetiles: An array of 16x16 tiles. This is 4-dimensional in grayscale and 5-dimensional in color.
      The dimensions are to accomodate rows, columns, and color channels.
    - acres: A 4-dimensional array of the tile values in each acre, formatted as follows:
        acres[acrerow][acrecolumn][tilerow][tilecolumn]
        If None, then this simply uses an array of each tile from 0 to 255.

    Returns:

    - tilemap: A 4-dimensional array of every pixel."""
    if acres != None:
        mapwidth, mapheight = 8, 8
        acrewidth, acreheight = 10, 8
    else:
        mapwidth, mapheight = 1, 1
        acrewidth, acreheight = 16, 16
    tilemap = []
    for i in range(mapheight):
        tilemap.append([])
        for j in range(mapwidth):
            tilemap[i].append([])
            for k in range(acreheight):
                tilemap[i][j].append([])
                for l in range(acrewidth):
                    if acres != None:
                        tile = acres[i][j][k][l]
                    else:
                        tile = k * 16 + l
                    tilemap[i][j][k].append(largetiles[tile])
    return tilemap

def validacre(loc,row,col):
    """Check if an acre is valid, based on the map, acre row, and acre column.
    Used to make invalid acres appear differently on the map."""
    if loc == 0x02 or loc == 0x06:
        return True
    if loc == 0x05 or loc == 0x09:
        return True
    if loc == 0x10 and row == 3 and col == 2:
        return True
    if loc == 0x1A and row == 0 and col == 6:
        return True
    if loc == 0x22 and row == 2 and col == 3:
        return True
    if loc == 0x28 and row == 0 and col == 3:
        return True
    if loc == 0x32 and row == 1 and col == 4:
        return True
    return False
