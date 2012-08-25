#DO NOT REMOVE THIS FILE, IT IS CRUCIAL FOR THIS TO WORK!
#Also, it's not meant to be run, either.

hexdump = True #Used for dumping hex files in the Hexdump folder.
  #Useful for debugging the program or for seeing the map in its
  #uncompressed state.
maptiles = True #Used for outputting PNG files of map tiles in the
  #Maptiles folder. This is useful for seeing the tiles that make up the map.
tileset = True #Used for outputting PNG files of tiles in any given map
  #in the Tileset folder.
maplog = True #Used for outputting a log of the map decompression routine;
  #useful for understanding the mechanism behind it, and very useful for
  #debugging.
warnings = True #Used for warnings when something goes wrong when
  #decompressing a map. Sometimes this is due to bugs in the game itself;
  #for example, in Chain Link Chamber, more tiles are generated than
  #what appear on the screen. For that reason, you may want to set this to
  #false.
