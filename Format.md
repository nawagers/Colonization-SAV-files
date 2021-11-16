# Colonization SAV file structure

## Notes:
Most Strings are stored as 24 byte null terminated ascii, giving up to 23 characters printed. Data between the null terminator and the end of the buffer is ignored. Multi-byte integers are stored in little endian, meaning adding 1 to a register that holds FF 00 would give 00 01. There is at least a 3 byte register for gold, though it’s probably a 4 byte register. So far, no evidence of registers larger than that.

Map data is stored for a (x+2) * (y+2) tile map. A 1 tile buffer is applied on all sides in the game. The map size is in bytes 12 (0xC) and 14 (0xE). It’s unclear if these values are 2 byte values that include 13 (0xD) and 15 (0xF). The map editor does not support non-standard map size (58x72). The game partially supports it, but doesn’t have proper bounds checking and has some hard-coded map size assumptions. Example: going to/from and being in Europe are represented by map positions (2xx, 2xx). Maps bigger than this size would probably have pathing problems, and no units or colonies could exist at a position with more than one byte. Position data is from the top left corner. The 0 row and 0 column are not displayed along with the highest row and column. Positions are all stored as (column, row) with (1, 1) being the top left visible tile.

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

Gold is 4 bytes at 0x2A (+ 0x13C * power offset). Using all 4 bytes causes the tax rate to go off screen. 

Market sensitivity data starts at 0x4C (+ 0x13C * power offset). Each supply is first represented by 1 byte, after that block of 16 bytes, each supply has 2 bytes, and then 4 bytes and 4 bytes and 4 bytes to the end of the section. The market data block is (1+2+4+4+4) * 16 = 240 (0xF0) bytes. The first byte increments when prices raise (from buying in Europe) and decrements when prices fall (from selling in Europe). It's not yet clear what happens when it goes below 0 or how custom house sales work. The second group (2 byte array) affects all 4 powers.

Taxes, embargoes, next units, and founding fathers are all found here.

## Indian Villages
**Length:** 18 (0x12) bytes * number of villages

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 1654 (0x676) bytes

Includes position, tribe, alarm status (per power), missionary status, last goods bought, last goods sold, attack counter (per power), whether they've taught you, and if it's a capital. Does not contain what they will teach you, what they will buy, or what they will sell.

## Tribes
**Length:** 78 (0x4E) bytes * number of tribes (8) = 624 (0x270)

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 1654 (0x676) bytes

Includes alarm towards European powers, supply counts, horses/muskets, and more.

## Unknown B
**Length:** 727 (0x2D7) bytes (seems static)

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 2278 (0x8E6) bytes

Not really sure what is in here.


## Terrain Map
**Length:** (x+2)*(y+2) bytes = 4176 (0x1050) standard size

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 3005 (0xBBD) bytes

There are 8 base terrain types (Tundra, Prairie, Grassland, Plains, Swamp, Desert, Savannah, Marsh) plus 3 special types (Arctic, Ocean, Sea Lane). Each of the base types can have forests, mountains, hills, minor rivers, and major rivers. The arctic functions like a base type except it does not allow forests. Some of these options can be in combination. 

The north and south buffers are arctic and it's possible to see an edge of it. The east and west buffers are sea lane tiles.

|Bit(s)|Function|
|---|---|
|1-3|Base|
|4|Forest|
|5|Special|
|6|Hills|
|7|River|
|8|Prominent|

For special types, both the Special and Forest bits are set. The Prominent bit converts Hills to Mountains and Minor River to Major River. The Prominent bit can not be used with both Hills and River or Hills and Forest (no Mountain Rivers or Mountain Forests) except for Arctic Mountains, where both the Special and Forest bits are set along with Hills and Prominent.

|Bits|Base|Forest|
|---|---|---|
|000|Tundra|Boreal Forest|
|001|Prairie|Broadleaf Forest|
|010|Grassland|Conifer Forest|
|011|Plains|Mixed Forest|
|100|Swamp|Rain Forest|
|101|Desert|Scrub Forest|
|110|Savannah|Tropical Forest|
|111|Marsh|Wetland Forest|
|000|Arctic||
|001|Ocean||
|010|Sea Lane||


## Mask Map
**Length:** (x+2)*(y+2) bytes = 4176 (0x1050) standard size

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + (map width + 2) * (map height + 2) + 3005 (0xBBD) bytes

This map contains at least 7 bitwise flags.

|Bit|Function|
|---|---|
|1|Unit|
|2|Colony/Village|
|3|Suppress Prime|
|4|Road|
|5|Purchased Tribal Land|
|6|Pacific Ocean|
|7|Plowed|
|8||

1. The unit bit is for units of any power, including tribes and ships, and includes units outside the fence of colonies.
2. The colony bit is for all colonies and tribal villages.
3. The prime suppression bit prevents prime resources at a particular square, including fish in the ocean that are more than 2 tiles away from land. * See note below
4. The road bit seems pretty self explanatory.
5. This bit indicates the tile is purchased or seized from the tribe. Normally set at 0, but switching to 1 indicates it is no longer tribal.
6. The Pacific bit notes the Pacific Ocean. The Pacific extends from the west edge of the map to column 41 (inclusive) or until it hits land in a straight line on maps from the generator. Manual editing may improve pathing.
7. The plowed bit is for plowed squares. This bit is *not* set when a forest is cleared. Instead that changes the terrain type.
8. Unknown. This bit may not be used.

Prime resources follow a set pattern as seen here (https://forums.civfanatics.com/threads/prime-resource-positions-demystified.637187/). The pattern is probably different on maps with different widths, because it's likely generated by moving left to right across the rows and wrapping around. There is probably a byte in the header that defines an offset for the starting point. This means that you can't set prime resources for all individual tiles, but you can probably shift them around to benefit *some* individual tiles and knowing the pattern could allow you to design terrain for a specific pattern. The suppression bit is used at the beginning of the game to suppress prime fishing locations that are far off shore. During normal game play it will be set randomly to deplete silver mines (there may be a counter to prevent early depleting, but the final step is random). This bit is not set on general squares that never had a prime resource. It is also not set when clearing a forest with prime timber or fur. The forested tiles have a shifted pattern of prime resources, so when they are cleared and change terrain they no longer have the forested pattern applied. The forested tiles are 4 tiles to the right of unforest tiles. That means if you clear a forest 4 squares to the left of prime fur or timber, you'll find another prime resource.


## Visitor and Pathing Map
**Length:** (x+2)*(y+2) bytes = 4176 (0x1050) standard size

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 2 * (map width + 2) * (map height + 2) + 3005 (0xBBD) bytes

The lower nibble indicates a pathing region. A 0 value is used for the off-screen border tiles. The oceans and continents are labeled from right to left and then top to bottom. Multiple passes are made with threshold sizes, resulting in larger regions generally getting lower numbers. Oceans and continents are numbered independently and have overlapping numbers, so there is both a continent and ocean number 1. If there are more than 15 regions of a type, all remaining regions get a 0xF value.

The upper nibble indicates the last visitor to the tile. A 0xF value means unvisited. For most tiles, when movement occurs from one of the European powers, all 8 squares surrounding the unit are set to that unit's code if the tile was previously unvisited. Notably, this is not true for Lost City Rumors. These tiles are only set when the unit directly occupies it. Once the Lost City Rumor tile has been visited, the Lost City Rumor is removed. The initial location of the LCRs is pattern generated like Prime Resource tiles. Tiles that were previously occupied are only set again when a new unit directly occupies it, instead of all surrounding tiles like when unvisted.

The purpose of the last visitor map is unclear other than removing Lost City Rumors. Land visited by tribes that is contiguous with a village location designates tribal land in part, though this also interacts with some runtime logic. Overall, it may function as a type of fog of war map to show which units are visible.

|Bits|Power|
|---|---|
|0000|English|
|0001|French|
|0010|Spanish|
|0011|Dutch|
|0100|Inca|
|0101|Aztec|
|0110|Arawak|
|0111|Iroquois|
|1000|Cherokee|
|1001|Apache|
|1010|Sioux|
|1011|Tupi|
|1100-1110|(Unused)|
|1111|(Unvisited)|


## Visibility and Score Map
**Length:** (x+2)*(y+2) bytes = 4176 (0x1050) standard size

**Start byte:** 202 (0xCA) bytes * number of colonies + 28 (0x1C) bytes * number of units + 18 (0x12) * number of villages + 3 * (map width + 2) * (map height + 2) + 3005 (0xBBD) bytes

The highest bits of this map are visibility flags for each of the powers. If the bit is 0, then the power can't see that tile. If the bit is 1, then it is visible. The lower nibble, bits 1-4, are the base colony site scores. These are used by the computer players to choose a place to build a colony. Higher scores are better. A 0 score is given to places that can't build (mountains, oceans). Coastal sites usually max out unless there is too much water. Scores are also adjusted at runtime as can be seen from the cheat menu.

|Bit(s)|Function|
|---|---|
|1-4|Colony Score|
|5|English|
|6|French|
|7|Spanish|
|8|Dutch|

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
