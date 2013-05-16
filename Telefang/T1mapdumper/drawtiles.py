import struct

def drawtiles(filename):
    """Generates tiles based on an image."""
    image = open(filename, "rb")
    elem = image.read().split()
    header=elem[0]
    #print header
    if header == b"P2":
        return -1
    if header != b"P5":
        return -2
    width=int(elem[1])
    height=int(elem[2])
    white=int(elem[3])
    white += 1
    tilemap=elem[4]
    tiles=[]
    rowtiles=width/8
    columntiles=height/8
    for a in range(columntiles):
        for b in range(rowtiles):
            tiles.append([])
            for c in range(8):
                row = width * (c + a * 8)
                tiles[b+a*rowtiles].append([])
                for d in range(8):
                    pixel = row+d+b*8
                    tiles[b+a*rowtiles][c].append((struct.unpack("<b", tilemap[pixel])[0])*4/white)
    image.close()
    
    return tiles
    
def drawlargetiles(rom,offset,tiles):

    """Assembles 16x16 tiles from 8x8 tiles."""
    rom.seek(offset)
    largetiles = []
    for i in range(0x100):
        largetiles.append([])
        for j in range(2):
            largetiles[i].append([])
            for k in range(2):
                tile=rom.read(1)
                tile = struct.unpack("<B", tile)[0]
                if (tile >= 144):
                    tile = 0
                tile = tiles[tile]
                largetiles[i][j].append(tile)
    return largetiles
