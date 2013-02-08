import os

class UndefinedError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def bit_test(num,bit):
    """Determines if a certain bit is 0 or 1.
Arguments: num is the number being tested.
Bit indicates which bit is being looked at, starting from the right at 0."""
    mask = 1 << bit
    result = num & mask
    result >>= bit
    return result

def gbc2rgb(c):
    """Converts a 15-bit RGB GBC format into a 24-bit format."""
    r = (c % (1 << 5)) << 3
    g = ((c / (1 << 5)) % (1 << 5)) << 3
    b = ((c / (1 << 10)) % (1 << 5)) << 3
    return (r,g,b)

def rgb2gbc(rgb):
    """Takes a 24-bit RGB format (in the form of 3-tuple) and returns a 15-bit GBC format."""
    c = (rgb[0] >> 3) + ((rgb[1] >> 3) << 5) + ((rgb[2] >> 3) << 10)
    return c

def luminance(p):
    """Takes a 3-tuple of a pixel (r,g,b) and returns a floating value indicating the luminance of a color."""
    l = 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]
    return l

def readbyte(f):
    """Reads one byte from a file f."""
    return struct.unpack("<B", f.read(1))[0]

def readshort(f, endian="<"):
    """Reads two bytes from a file f, with an optional parameter for endianness (not needed for Telefang, but useful for 1% of GB games)."""
    if endian != '<' and endian != '>':
        raise UndefinedError('Invalid endianness: "{}"'.format(endian))
    return struct.unpack("{}H".format(endian), f.read(2))[0]

def print_2d_array(x, padding=0, reverse=False):
    s = ""
    y = x[:]
    if reverse == True:
        y.reverse()
    for i in y:
        for j in i:
            temp = str(j)
            if len(temp) < padding:
                temp = temp + " "*(padding-len(temp))
            s = s + temp
        s = s + "\n"
    print s
    return

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
