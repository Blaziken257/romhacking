import rom_utilities
import denjuu_list as dl

import sys
import os
try:
    import png
except ImportError:
    sys.exit("You need to have the PyPNG package installed in order to run this program.\n\
For more information, go to:\n\
http://pypi.python.org/pypi/pypng/0.0.13")
import struct

debug=False
inverted=False
print "Telefang 1 Denjuu Sprite Exporter v0.1"

print "Enter the filename of your Telefang ROM or drag it here:"
#Read ROM file
rom = rom_utilities.open_file([".gbc"],"rb")

rom.seek(0x134)
header = rom.read(16)
#Read ROM header to detect correct game
print 'ROM header: "{}"'.format(header.rstrip('\xC0\x80'))
if not header.startswith(b"TELEFANG"):
    sys.exit("Invalid ROM. You must use a Telefang ROM.")

print "Enter the number of the Denjuu that you want to export.\n\
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

#Prompt for grayscale
print "Please enter 0 for color or 1 for grayscale, \
then press Enter:"
grayscale = raw_input()
if grayscale != "1":
    grayscale = False
else:
    grayscale = True

offset = 0x1AC000 + ((denjuu_no-1) / 18)*0x4000 + ((denjuu_no-1)%18)*0x380
print "Sprite offset: {:#x}".format(offset)
if grayscale == False:
    offset_color = 0x34800 + (denjuu_no-1)*8
    print "Color palette offset: {:#x}".format(offset_color)

rom.seek(offset)
image=rom.read(0x380)
imageheight = 56
imagewidth = 64
pixelmap = []
for i in range(imageheight):
    pixelmap.append([])
for i in range(0x1C0):
    v_pos = i / 0x40 * 0x8 + i % 0x8
    for j in range(7,-1,-1):
        color = 3 - (rom_utilities.bit_test(ord(image[i*2]),j) + 2 * rom_utilities.bit_test(ord(image[i*2+1]),j))
        if inverted == False:
            pixelmap[v_pos].append(color)
        else:
            pixelmap[v_pos].insert(0,color)
if grayscale == False:
    rom.seek(offset_color)
    rawpalettes=rom.read(8)
    palette=[]
    rawcolors=[]
    s = "["
    for i in range(4):
        color = struct.unpack("<H",rawpalettes[i*2:i*2+2])[0]
        s = "{0}0x{1:0>4X}, ".format(s, color)
        color = rom_utilities.gbc2rgb(color)
        palette.insert(0,color)
    s = s[:-2] + "]"
    print "Palette:\n"
    print "R   G   B\n"
    rom_utilities.print_2d_array(palette, padding=4, reverse=True)
    print "Raw colors in GBC format: " + s
    bitdepth = 8
else:
    bitdepth = 2 #2 is enough for grayscale
    palette = None
rom.close()

filename = os.path.join(os.getcwd(), "Denjuu{:0>3}.png".format(denjuu_no))

imagefile = open(filename, "wb")
print "Writing to {}...".format(filename)
w=png.Writer(imagewidth, imageheight, palette=palette, compression=9, greyscale=grayscale, bitdepth=bitdepth)
w.write(imagefile,pixelmap)
imagefile.close()
print "Done! Image file closed.\nPress Enter to close the program."
raw_input()

