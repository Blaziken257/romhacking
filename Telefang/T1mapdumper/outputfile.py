import sys
import os
try:
    import png
except ImportError:
    sys.exit("You need to have the PyPNG package installed in order to run this program.\n\
For more information, go to:\n\
http://pypi.python.org/pypi/pypng/0.0.13")

from acres import validacre

def outputfile(o_filename, mode, tilemap, map_tiles, location, grayscale):
    if mode == 1:
        width,height=256,256
    elif mode == 0:
        width,height=1280,1024
    area = width*height
    """Writes the map to the image file."""
    o_filename = os.path.join(os.getcwd(), o_filename)
    outputfile = open(o_filename, "wb")
    print "Generating pixel map."
    if grayscale == 1:
        print "Image will be in grayscale."
        w = png.Writer(width, height, alpha=True, greyscale=True, bitdepth=2, compression=9)
    elif grayscale == 0:
        print "Image will be in color."
        w = png.Writer(width, height, alpha=True, compression=9)
    h_pos = 0
    v_pos = 0
    pixelmap = []
    for v_pos in range(height):
        pixelmap.append([])
        for h_pos in range(width):
            if grayscale == 1:
                #Write color
                if mode == 0:
                    pixel = tilemap[v_pos/128][h_pos/160][(v_pos%128)/16][(h_pos%160)/16][(v_pos%16)/8][(h_pos%16)/8][v_pos%8][h_pos%8]
                else:
                    pixel = tilemap[v_pos/256][h_pos/256][(v_pos%256)/16][(h_pos%256)/16][(v_pos%16)/8][(h_pos%16)/8][v_pos%8][h_pos%8]
                pixelmap[v_pos].append(pixel)
                #Alpha transparency!
                if mode == 0:
                    if map_tiles[v_pos/128][h_pos/160] == 0 and not validacre(location,v_pos/128,h_pos/160):
                        alpha = 1
                    else:
                        alpha = 3
                else:
                    alpha = 3
                pixelmap[v_pos].append(alpha)
                
            else:
                for i in range(3):
                    if mode == 0:
                        pixel = tilemap[v_pos/128][h_pos/160][(v_pos%128)/16][(h_pos%160)/16][(v_pos%16)/8][(h_pos%16)/8][v_pos%8][h_pos%8][i] << 3
                    else:
                        pixel = tilemap[v_pos/256][h_pos/256][(v_pos%256)/16][(h_pos%256)/16][(v_pos%16)/8][(h_pos%16)/8][v_pos%8][h_pos%8][i] << 3
                    pixelmap[v_pos].append(pixel)
                #Alpha transparency!
                if mode == 0:
                    if map_tiles[v_pos/128][h_pos/160] == 0 and not validacre(location,v_pos/128,h_pos/160):
                        alpha = 85
                    else:
                        alpha = 255
                else:
                    alpha = 255
                pixelmap[v_pos].append(alpha)

        #Comment this portion out if you're using IDLE!
        progress = (v_pos + 1)* 100 / height
        if v_pos % 64 == 63 or v_pos == 0:
            sys.stdout.write("Progress: {: >7} of {: >7} pixels ({: >3}%) [{}]\r".format((v_pos+1)*width, area, progress, "-" * (progress / 5) + " " * ((104 - progress) / 5)))
            sys.stdout.flush()
    del pixel, alpha, h_pos, v_pos
    print "\nWriting to file %s..." % o_filename
    w.write(outputfile, pixelmap)
    outputfile.close()
    print "\nFile closed."
