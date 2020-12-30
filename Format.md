# Colonization SAV file structure

## Notes:
Most Strings are stored as 24 byte null terminated ascii, giving up to 23 characters printed. Data between the null terminator and the end of the buffer is ignored. Multi-byte integers are stored in little endian, meaning adding 1 to a register that holds FF 00 would give 00 01. There is at least a 3 byte register for gold, though it’s probably a 4 byte register. So far, no evidence of registers larger than that.

Map data is stored for a (x+2) * (y+2) tile map. A 1 tile buffer is applied on all sides in the game. It’s unclear if these values are represented in the header by bytes 12 (0xC) and 14 (0xE) and possibly as 2 byte values that include 13 (0xD) and 15 (0xF). Some text in files included with the game suggest variable map sizes, but it seems like the map editor does not support that feature. It could be that the game partially supports it, but doesn’t have proper bounds checking and hard-coded map size assumptions. Example: going to/from and being in Europe are represented by map positions (2xx, 2xx). Maps bigger than this size would probably have pathing problems, and no units or colonies could exist at a position with more than one byte. Position data is from the top left corner. The 0 row and 0 column are not displayed along with the highest row and column. Positions are all stored as (column, row) with (1, 1) being the top left visible tile.

Unknown sections or the header probably contains European prices and units, crosses needed for the next unit and/or total crosses, next three units available,, taxes, embargoes, royal forces, independence status, withdrawn status, war status between powers.

## Header
**Length:** 390 (0x186) bytes

**Start byte:** 0 (0x0)

Most important is probably the unit, colony and village counts. Colonies are at byte 46 (0x2E), units at byte 44 (0x2C), and villages at byte 42 (0x2A). These may be 2 byte values since they're all followed by 0x00.

Byte 0x22 may be the current unit (who’s turn).


## Colonies
**Length:** 202 (0xCA) bytes * number of colonies

**Start byte:** 390 (0x186)

All the colonies of the European powers. Each colony keeps track of colonists within it, their specialities and occupations, along with which structures are built and being constructed, and storage of all the goods. This forum post served as the starting point for colony data: https://forums.civfanatics.com/threads/sav-hacking-disband-stockaded-colonies.71229/#post-1418322

## Units
**Length:** 28 (0x1C) bytes * number of units

**Start byte:** 202 (0xCA) bytes * number of colonies +  390 (0x186) bytes

Movable units that are not in colonies. Includes ships, wagon trains, colonists, braves, artillery, and treasure of all powers. Units store position, unit type, which power they belong to, their orders, and what types and how much cargo they are carrying.


## Powers
**Length:** 1264 (0x4F0) bytes

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units +  390 (0x186) bytes

Each power has an even 316 (0x13C) bytes. Data order is English, French, Spanish, Dutch.

Gold is at least 3 bytes at 0x2A (+ 0x13C * power offset). Max money is unknown. Up to 983039 (0x0EFFFF) works. 

Other values in this block are unexplored. Probably the sections with taxes, embargoes, European prices, and Royal Forces.

## Indian Villages
**Length:** 18 (0x12) bytes * number of villages

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 1654 (0x676) bytes

Includes position, tribe, alarm status (per power), missionary status, last goods bought, last goods sold, attack counter (per power), whether they've taught you, and if it's a capital. Does not contain what they will teach you, what they will buy, or what they will sell.


## Unknown B
**Length:** 1351 (0x547) bytes (seems static)

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 1654 (0x676) bytes

The most mysterious section of data. It could be serialized map data if it’s just 1 bit per tile, but that seems unlikely. I suspect one thing it contains is the prime resources. May also contain locations of Lost City Rumors.


## Terrain Map
**Length:** (x+2)*(y+2) bytes = 4176 (0x1050) standard size

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 3005 (0xBBD) bytes

There are 8 base terrain types (Tundra, Prairie, Grassland, Plains, Swamp, Desert, Savannah, Marsh) plus 3 special types (Artic, Ocean, Sea Lane). Each of the base types can have forests, mountains, hills, minor rivers, and major rivers. The arctic functions like a base type except it does not allow forests. Some of these options can be in combination. Forests can be with minor rivers or major rivers, but not both at once. Hills can be with minor rivers. Oceans and sea lanes can have minor or major rivers, but not both at once.


## Unknown Map C
**Length:** (x+2)*(y+2) bytes = 4176 (0x1050) standard size

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + (map width + 2) * (map height + 2) + 3005 (0xBBD) bytes


This map may be some sort of pathing aid. In the ocean it does a line fill from the left hand side until it hits land or column 41. This may be “Pacific Ocean”. At first glance, roads and colonies seem to affect it and it marks some obstructions like native villages and at least some units on the map. Needs more investigation.


## Vis Map
**Length:** (x+2)*(y+2) bytes = 4176 (0x1050) standard size

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 2 * (map width + 2) * (map height + 2) + 3005 (0xBBD) bytes

This is some sort of “last traveled” map, which seems to be among all units. Each power (including tribes) has a code it sets. Land and sea have different values. . The values are overwritten instead of generating a new value that indicates multiple powers have visited the square. This is somehow related to the display mask. It may be a fog of war map. Values are not turn based, as in they don’t decay back to some state. Definitely contains some portion of Lost City Rumors, but doesn't fully describe them.


## Unknown Map D
**Length:** (x+2)*(y+2) bytes = 4176 (0x1050) standard size

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 3 * (map width + 2) * (map height + 2) + 3005 (0xBBD) bytes

Have not explored this map much.

## Unknown E
**Length:** 18 (0x12) * number of ? 

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 4 * (map width + 2) * (map height + 2) + 3005 (0xBBD) bytes

Some sort of repeating structure data like units, colonies and villages. There appears to always be 28 of them. There doesn't seem to be a position on the map associated with them.

## Unknown F
**Length:** 110 (0x6E) bytes

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 4 * (map width + 2) * (map height + 2) + 3509 (0xDB5) bytes

No idea what is here. The data has several 0x1600 and 0x1900 or 0x0016 and 0x0019 sets of bytes.

## Trade Routes
**Length:** 888 (0x378) bytes

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 4 * (map width + 2) * (map height + 2) + 3619 (0xE23) bytes

12 routes. Each route is 74 bytes (0x4A) in length and starts with a 32 (0x20) byte null terminated string. This should cover colonies on the way, load/unloads, and land/sea flags. Haven't broken this down to specific values.
