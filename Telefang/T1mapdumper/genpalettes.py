import struct

def genpalettes(i,rom):
        """Generates palettes based on a RAM pointer. Returns an array of palettes."""
        offset = 0x34000 + (i % 0x4000)
        rom.seek(offset)
        pal=[]
        for a in range(8):
            pal.append([])
            for b in range(4):
                pal[a].insert(0,[])
                color_raw = rom.read(2)
                color_raw = struct.unpack("<H", color_raw)[0]
                #Red
                color = color_raw % 32
                pal[a][0].append(color)
                #Green
                color = (color_raw >> 5) % 32
                pal[a][0].append(color)
                #Blue
                color = (color_raw >> 10) % 32
                pal[a][0].append(color)
        return pal
