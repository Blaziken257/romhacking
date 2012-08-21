import struct

def gamemap(rom,offset):
    rom.seek(offset)
    map_tiles = []
    for i in range(8):
        map_tiles.append([])
        for j in range(8):
            acre=rom.read(1)
            map_tiles[i].append(struct.unpack("<B", acre)[0])
    return map_tiles
