import os
import settings
import struct

class UndefinedError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def write_log(s, f):
    """Writes string s to file f."""
    if settings.maplog == True:
        f.write(s+"\r\n")
    return

def gbc2rgb(c):
    """Converts a 15-bit RGB GBC format into a 24-bit format."""
    #GBC format: 0bbbbbgggggrrrrr (b-blue, g-green, r-red)
    r = (c % (1 << 5)) << 3
    g = ((c / (1 << 5)) % (1 << 5)) << 3
    b = ((c / (1 << 10)) % (1 << 5)) << 3
    return (r,g,b)

def rgb2gbc(rgb):
    """Takes a 24-bit RGB format (in the form of 3-tuple) and returns a 15-bit GBC format."""
    c = (rgb[0] >> 3) + ((rgb[1] >> 3) << 5) + ((rgb[2] >> 3) << 10)
    return c

def readbyte(f):
    """Reads one byte from a file f."""
    return struct.unpack(">B", f.read(1))[0]

def readshort(f, endian=">"):
    """Reads two bytes from a file f, with an optional parameter for endianness."""
    if endian != '<' and endian != '>':
        raise UndefinedError('Invalid endianness: "{}"'.format(endian))
    return struct.unpack("{}H".format(endian), f.read(2))[0]

def get_rel_ptr(f, bank, base, index, scale=2, offset=0, endian=">"):
    """Get relative pointer."""
    f.seek(base)
    ptr = readshort(f, ">")
    ptr = ram2rom(bank, ptr)
    ptr = ptr + index*scale + offset
    f.seek(ptr)
    ptr = readshort(f, endian)
    ptr = ram2rom(bank, ptr)
    return ptr

def get_abs_ptr(f, bank, base, index, scale=3, offset=0, endian=">"):
    """Get absolute pointer."""
    f.seek(base)
    ptr = readshort(f, ">")
    ptr = ram2rom(bank, ptr)
    ptr = ptr + index*scale + offset
    f.seek(ptr)
    #In DKL2 and DKL3, absolute pointers work in one of two ways:
    #1. Bank, big-endian pointer
    #2. Little-endian pointer, bank
    #Weird, I know.
    if endian == ">":
        ptr_bank, ptr = struct.unpack(">BH", f.read(3))
    else:
        ptr, ptr_bank = struct.unpack("<HB", f.read(3))
    ptr = ram2rom(ptr_bank, ptr)
    return ptr

def ram2rom(bank,ram_offset):
    """Converts a RAM offset to a ROM offset."""
    if bank == 0:
        rom_offset = ram_offset
    else:
        rom_offset = bank * 0x4000 + ram_offset - 0x4000
    return rom_offset

def swap_nib(x):
    """Swaps nibbles. e.g. AF becomes FA."""
    a = (x & 0xF) << 4
    b = (x & 0xF0) >> 4
    c = a + b
    return c

def bit_test(num,bit):
    """Determines if a certain bit is 0 or 1.
Arguments: num is the number being tested.
Bit indicates which bit is being looked at, starting from the right at 0."""
    mask = 1 << bit
    result = num & mask
    result >>= bit
    return result

def decode_tiles(height,width,tiles,order=0):
    """Order = 0: White is first, black is last.
    Order = 1: Black is first, white is last."""
    area=height*width
    pixel_map = []
    for i in range(height):
        pixel_map.append([])

    for i in range(area/0x8):
        v_pos = i / width * 0x8 + i % 0x8
        for j in range(7,-1,-1):
            #Fix this code; it's sloppy
            try:
                if order != 0:
                    color = (bit_test(tiles[i*2],j) + 2 * bit_test(tiles[i*2+1],j))
                else:
                    color = 3 - (bit_test(tiles[i*2],j) + 2 * bit_test(tiles[i*2+1],j))
            except IndexError:
                color = 0
            pixel_map[v_pos].append(color)
    return pixel_map

def open_file(extensions, mode):
    """Opens a file, which takes an array of extensions and a mode."""
    validfile = False
    while validfile == False:
        try:
            filename = raw_input().strip("\"' ")
            validextension = False
            for i in extensions:
                if filename.endswith(i):
                    validfile = True
                    break
            if validfile == True:
                filename = os.path.join(os.getcwd(), filename)
                f = open(filename, mode)
            else:
                s = ""
                if len(extensions) == 1:
                    s = extensions[0]
                elif len(extensions) == 2:
                    s = extensions[0] + " or " + extensions[1]
                elif len(extensions) > 2:
                    for i in extensions[:-1]:
                        s = s + i + ", "
                    s = s + "or " + extensions[-1]
                if filename.endswith(".zip") or filename.endswith(".7z"):
                    print "File name must end in {}. Do not use compressed files. Enter a new file:".format(s)
                else:
                    print "File name must end in {}. Enter a new file:".format(s)
        except IOError:
            print "File does not exist. Enter in a valid file name:"
    return f
