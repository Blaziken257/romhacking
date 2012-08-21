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

def tilemap(largetiles,acres):
    tilemap = []
    for i in range(8):
        tilemap.append([])
        for j in range(8):
            tilemap[i].append([])
            for k in range(8):
                tilemap[i][j].append([])
                for l in range(10):
                    tilemap[i][j][k].append(largetiles[(acres[i][j][k][l])])
    return tilemap

def validacre(loc,row,col):
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
