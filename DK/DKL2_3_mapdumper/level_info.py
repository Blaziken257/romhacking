#Internal level order is different from the actual order in the games
level_ptrs = {"DKL2": [0x03, 0x00, 0x04, 0x24, 0x01, 0x27,\
    0x18, 0x09, 0x25, 0x19, 0x0A, 0x1B, 0x26, 0x1C, 0x05, 0x02, 0x28,\
    0x21, 0x15, 0x0F, 0x16, 0x10, 0x1D, 0x22, 0x29,\
    0x0C, 0x17, 0x0D, 0x23, 0x0E, 0x2A,\
    0x06, 0x0B, 0x1E, 0x07, 0x1F, 0x20, 0x2B,\
    0x11, 0x2D,\
    0x12, 0x08, 0x1A, 0x13, 0x14, 0x2C],\
  #In DKL3, this is located at 0xA34F in ROM, but hardcoded in program due to
  #Wrinkly Refuge, Sheepy Shop, and FF bytes making things difficult
    "DKL3": [0x0C, 0x00, 0x0D, 0x03, 0x06, 0x04, 0x24,\
    0x01, 0x0F, 0x0E, 0x09, 0x07, 0x05, 0x25,\
    0x15, 0x12, 0x0A, 0x08, 0x0B, 0x10, 0x26,\
    0x1B, 0x16, 0x02, 0x1E, 0x11, 0x13, 0x27,\
    0x1C, 0x14, 0x17, 0x1F, 0x22, 0x18, 0x28,\
    0x23, 0x20, 0x19, 0x1D, 0x21, 0x1A, 0x29]}

level_names = {"DKL2": ["Pirate Panic", "Mainbrace Mayhem", "Gangplank Galley", "Lockjaw's Locker", "Topsail Trouble", "Krow's Nest",\
"Hothead Hop", "Kannon's Klaim", "Lava Lagoon", "Redhot Ride", "Squawks's Shaft", "Barrel Bayou", "Glimmer's Galleon", "Krockhead Klamber", "Rattle Battle", "Slime Climb", "Kleaver's Kiln",\
"Hornet Hole", "Target Terror", "Bramble Blast", "Rickety Race", "Bramble Scramble", "Mudhole Marsh", "Rambi Rumble", "King Zing Sting",\
"Ghostly Grove", "Krazy Koaster", "Gusty Glade", "Parrot Chute Panic", "Web Woods", "Kreepy Krow",\
"Arctic Abyss", "Windy Well", "Dungeon Danger", "Clapper's Cavern", "Chain Link Chamber", "Toxic Tower", "Stronghold Showdown",\
"Screech's Sprint", "K. Rool Duel",\
"Jungle Jinx", "Black Ice Battle", "Fiery Furnace", "Klobber Karnage", "Animal Antics", "Krocodile Kore"],\
\
    "DKL3": ["Red Wharf", "Seabed Shanty", "Ford Knocks", "Total Rekoil", "Koco Channel", "Liftshaft Lottery", "Barbos Bastion",\
"Coral Quarrel", "Minky Mischief", "Jetty Jitters", "Black Ice Blitz", "Riverbank Riot", "Miller Instinct", "Bleak Magic",\
"Rocketeer Rally", "Vertigo Verge", "Polar Pitfalls", "Surface Tension", "Tundra Blunda", "Redwood Rampage", "Arich Attack",\
"Jungle Jeopardy", "Footloose Falls", "Deep Reef Grief", "Karbine Kaos", "Simian Shimmy", "Rockface Chase", "Krazy KAOS",\
"Tropical Tightropes", "Clifftop Critters", "Rickety Rapids", "Bazuka Bombard", "Ugly Ducting", "Stalagmite Frights", "K. Rool Duel",\
"Whiplash Dash", "Kuchuka Karnage", "Haunted Hollows", "Rainforest Rumble", "Barrel Boulevard", "Ghoulish Grotto", "K. Rool's Last Stand"]}

level_types = {"DKL2": ["Rigging","Ship Deck","Ice","Mine","Forest","Bramble","Jungle","Roller Coaster","Volcano","Marsh","Dungeon","Beehive","Ship Hold"],\
"DKL3": ["Mill","Snow","Stilt","River","Coral","Tree","Cliff","Falls","Cave","Jungle","Machine","Tube"]}
