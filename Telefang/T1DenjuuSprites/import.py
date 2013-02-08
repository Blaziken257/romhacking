import rom_utilities
import denjuu_list as dl

import os
import sys
try:
    import png
except ImportError:
    sys.exit("You need to have the PyPNG package installed in order to run this program.\n\
For more information, go to:\n\
http://pypi.python.org/pypi/pypng/0.0.13")
import struct

debug = False
print "Telefang 1 Denjuu Sprite Importer v0.1"

print "Enter the filename of your Telefang ROM or drag it here:"
#Read ROM file
rom = rom_utilities.open_file([".gbc"],"r+b")

rom.seek(0x134)
header = rom.read(16)
#Read ROM header to detect correct game
print 'ROM header: "{}"'.format(header.rstrip('\xC0\x80'))
if not header.startswith(b"TELEFANG"):
    sys.exit("Invalid ROM. You must use a Telefang ROM.")

print "Enter the number of the Denjuu that you want to import.\n\
Go to http://wikifang.meowcorp.us/wiki/List_of_Denjuu_in_Telefang_1 to see a list of Denjuu."

denjuu_no = 0
while denjuu_no < 1 or denjuu_no > 174:
    denjuu_no = raw_input()
    try:
        denjuu_no = int(denjuu_no)
    except ValueError:
        denjuu_no = 0
        print "Error: You did not input an integer."
        continue
    if denjuu_no < 1 or denjuu_no > 174:
        print "Error: You must enter a number between 1 to 174, inclusive."
print "You have selected: {}.".format(dl.denjuu_names[denjuu_no])

offset = 0x1AC000 + ((denjuu_no-1) / 18)*0x4000 + ((denjuu_no-1)%18)*0x380
print "Sprite offset: {:#x}".format(offset)
offset_color = 0x34800 + (denjuu_no-1)*8
print "Color palette offset: {:#x}".format(offset_color)

print "Enter the filename of the Denjuu sprite or drag it here:"
#Read PNG file
imagefile = rom_utilities.open_file([".png"],"rb")

r = png.Reader(imagefile)
try:
    data = r.asRGBA8()
except png.Error:
    print "Program currently doesn't support images with alpha transparency. Please remove this from your image."
    sys.exit()
width = data[0]
height = data[1]
MAX_WIDTH=64
MAX_HEIGHT=56
if width > MAX_WIDTH and height > MAX_HEIGHT:
    print "Error: Width ({}) and height ({}) are too high.\n\
Width should not exceed {} and height should not exceed {}.".format(width,height,MAX_WIDTH,MAX_HEIGHT)
    sys.exit()
elif width > 64:
    print "Error: Width ({}) is too high.\n\
Width should not exceed {}.".format(width,MAX_WIDTH)
    sys.exit()
elif height > 56:
    print "Error: Height ({}) is too high.\n\
Height should not exceed {}.".format(height,MAX_HEIGHT)
    sys.exit()
padleft = 0
padright = 0
padtop = 0
padbottom = 0
if width < MAX_WIDTH:
    padleft = (MAX_WIDTH - width)/2
    padright = (MAX_WIDTH+1 - width)/2
    print "Warning: Width is {0}, which is below {1}. The width of the sprite will be padded to {1} pixels.".format(width,MAX_WIDTH)
if height < MAX_HEIGHT:
    padtop = (MAX_HEIGHT - height)/2
    padbottom = (MAX_HEIGHT+1 - height)/2
    print "Warning: Height is {0}, which is below {1}. The height of the sprite will be padded to {1} pixels.".format(height,MAX_HEIGHT)
grayscale = data[3]['greyscale']
planes = data[3]['planes']
transparency = False
translucency = False
if debug == True:
    print data
d = list(data[2])
palette=[]
for i in range(len(d)):
    for j in range(width):
        rgb = (d[i][j*4],d[i][j*4+1],d[i][j*4+2])
        opacity = d[i][j*4+3]
        if opacity == 0:
            transparency = True
        elif opacity > 0 and opacity < 255:
            translucency = True
        if not rgb in palette and d[i][j*4+3] > 0:
            palette.append(rgb)
            print "Found new color {0} at coordinate ({1}, {2}).".format(rgb,j,i)
if transparency == True:
    print "Transparent pixels found. These pixels will become opaque, and will use the brightest color found in the palette."
if translucency == True:
    print "Translucent pixels found. These pixels will become opaque, but the color will not change."

#Sort by luminance
palette = sorted(palette, key=lambda rgb: rom_utilities.luminance(rgb), reverse=True)
print "Palette:\n"
print "R   G   B\n"
rom_utilities.print_2d_array(palette, padding=4)
if palette[0][0] < 248 or palette[0][1] < 248 or palette[0][2] < 248:
    print "Warning: Brightest color is not white. This will result in a odd-looking sprite where there will be a colored rectangle surrounding the Denjuu at all times."
if len(palette) > 4:
    print "Error: There are {0} colors in this palette. Images cannot exceed 4 colors. Program will close.".format(len(palette))
    sys.exit()
elif len(palette) < 4:
    print "Warning: There are only {0} colors in this palette. This will work fine, but you can still use {1} more color!".format(len(palette),4-len(palette))
rawcolors = [0x7FFF, 0x56B5, 0x294A, 0x0000]
for i in range(len(palette)):
    rawcolors[i]=rom_utilities.rgb2gbc(palette[i])
s = "["
for i in rawcolors:
    s = "{0}0x{1:0>4X}, ".format(s,i)
s = s[:-2] + "]"
print "Raw colors in GBC format: " + s

pixelmap = []
for i,v in enumerate(d):
    pixelmap.append([])
    for j in range(width):
        rgb = tuple(v[j*4:j*4+3])
        #print i, j, rgb, palette.index(rgb)
        if v[j*4+3] > 0:
            pixelmap[i].append(palette.index(rgb))
        else:
            pixelmap[i].append(0)
    for j in range(padleft):
        pixelmap[i].insert(0,0)
    for j in range(padright):
        pixelmap[i].append(0)
for i in range(padtop):
    pixelmap.insert(0,[0]*64)
for i in range(padbottom):
    pixelmap.append([0]*64)
if debug == True:
    print "Denjuu sprite:"
    rom_utilities.print_2d_array(pixelmap)

bytemap = []
if debug == True:
    print "Byte map:"
    for i,v in enumerate(pixelmap):
        print i,v

for i in range(0x1C0):
    v_pos = (i%0x8)+(i/0x40)*0x8
    for j in range(2):
        h_pos = i/0x8*0x8%0x40
        byte = 0
        for k in range(7,-1,-1):
            byte = byte + (((pixelmap[v_pos][h_pos] & (j+1)) >> j) << k)
            h_pos = h_pos + 1
        bytemap.append(byte)
for i in range(0x38):
    s = ""
    for j in range(0x10):
        s = s + "{0:0>2X} ".format(bytemap[i*16+j])
    if debug == True:
        print s

rom.seek(offset)
print "Writing tiles to ROM..."
for i in range(0x380):
    byte = struct.pack("B",bytemap[i])
    rom.write(byte)
print "Writing color palette to ROM..."
rom.seek(offset_color)
for i in range(0x4):
    rgb = struct.pack("<H",rawcolors[i])
    rom.write(rgb)
rom.close()
print "Done! ROM closed.\nPress Enter to close the program."
raw_input()
    
