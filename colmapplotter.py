"""
Written by nwagers, 2020

Intended to be shared by all who are curious.
Released to the public domain and completely
unrestricted, but attribution appreciated.

"""


import string


path = 'C:\\GOG Games\\Colonization\\MPS\\COLONIZE\\COLONY{}.SAV'
slot = '00'
path = path.format(slot)
display = [0, 1, 2, 3]  # maps to print and their order [0, 1, 2, 3]

with open(path, "rb") as binary_file:
        # Read the whole file at once
        data = binary_file.read()

num_colonies = data[0x2e]
num_units = data[0x2c]
num_villages = data[0x2a]
mapsize = (70+2)*(56+2)


maps = []    
for offset in display:
    address = 0xBBD + num_colonies * 202 + num_units * 28
    address += num_villages * 18 + offset * mapsize
    subset = data[address:address+mapsize]
    maps.append((subset, {}))


# Dynamic tables
chars = string.ascii_letters + '0123456789~!@#$%^&*()_`+=:;,<.>/?|[]{}'
for subset, table in maps:
    for tile in subset:
        if tile not in table:
            table[tile] = chars[len(table)]






# Static tables and modifications
# Useful for comparing changes between saves
# Allows for remapping ocean to ' ' or similar
# Copy dynamic table from first run and add in a static map



terrain = {'Tundra': 0, 'Tundra Hills': 32, 'Tundra Mountains': 160,
           'Tundra Minor River': 64, 'Tundra Major River': 192,
           'Tundra Hills Minor River': 96, 'Desert': 1, 'Desert Hills': 33,
           'Desert Mountains': 161, 'Desert Minor River': 65,
           'Desert Major River': 193, 'Desert Hills Minor River': 97,
           'Plains': 2, 'Plains Hills': 34, 'Plains Mountains': 162,
           'Plains Minor River': 66, 'Plains Major River': 194,
           'Plains Hills Minor River': 98, 'Prairie': 3,
           'Prairie Hills': 35, 'Prairie Mountains': 163,
           'Prairie Minor River': 67, 'Prairie Major River': 195,
           'Prairie Hills Minor River': 99, 'Grassland': 4,
           'Grassland Hills': 36, 'Grassland Mountains': 164,
           'Grassland Minor River': 68, 'Grassland Major River': 196,
           'Grassland Hills Minor River': 100, 'Savannah': 5,
           'Savannah Hills': 37, 'Savannah Mountains': 165,
           'Savannah Minor River': 69, 'Savannah Major River': 197,
           'Savannah Hills Minor River': 101, 'Marsh': 6,
           'Marsh Hills': 38, 'Marsh Mountains': 166,
           'Marsh Minor River': 70, 'Marsh Major River': 198,
           'Marsh Hills Minor River': 102, 'Swamp': 7, 'Swamp Hills': 39,
           'Swamp Mountains': 167, 'Swamp Minor River': 71,
           'Swamp Major River': 199, 'Swamp Hills Minor River': 103,
           'Arctic': 24, 'Arctic Hills': 56, 'Arctic Mountains': 184,
           'Arctic Minor River': 88, 'Arctic Major River': 216,
           'Arctic Hills Minor River': 120, 'Boreal Forest': 8,
           'Boreal Forest Minor River': 72,
           'Boreal Forest Major River': 200, 'Scrub Forest': 9,
           'Scrub Forest Minor River': 73, 'Scrub Forest Major River': 201,
           'Mixed Forest': 10, 'Mixed Forest Minor River': 74,
           'Mixed Forest Major River': 202, 'Broadleaf Forest': 11,
           'Broadleaf Forest Minor River': 75,
           'Broadleaf Forest Major River': 203, 'Conifer Forest': 12,
           'Conifer Forest Minor River': 76,
           'Conifer Forest Major River': 204, 'Tropical Forest': 13,
           'Tropical Forest Minor River': 77,
           'Tropical Forest Major River': 205, 'Wetland Forest': 14,
           'Wetland Forest Minor River': 78,
           'Wetland Forest Major River': 206, 'Rain Forest': 15,
           'Rain Forest Minor River': 79,
           'Rain Forest Major River': 207, 'Ocean': 25,
           'Ocean Minor River': 89, 'Ocean Major River': 217,
           'Sea Lane': 26, 'Sea Lane Minor River': 90,
           'Sea Lane Major River': 218}


if 0 in display:
    i = display.index(0)
    
##    # Converts identified terrain to -
##    for key, val in terrain.items(): 
##        if val in maps[i][1] and val != 26:
##            maps[i][1][val] = '-'
            
    # Ocean, Ocean Minor River, and Ocean Major River to <space>
    maps[i][1][25] = ' '
    maps[i][1][89] = ' '
    maps[i][1][217] = ' '


### Example of setting a static table for map 3
##if 3 in display:
##    i = display.index(3)
##    table = {0: 'a', 7: 'b', 10: 'c', 11: 'd', 12: 'e', 15: 'f',
##             14: 'g', 13: 'h', 16: 'i', 2: 'j', 4: 'k', 9: 'l',
##             5: 'm', 3: 'n', 6: 'o', 8: 'p', 23: 'q', 24: 'r',
##             27: 's', 30: 't', 31: 'u', 28: 'v', 25: 'w', 1: 'x',
##             20: 'y', 22: 'z', 64: 'A', 192: 'B', 208: 'C', 128: 'D',
##             80: 'E', 144: 'F', 159: 'G', 158: 'H', 221: 'I',
##             220: 'J', 222: 'K', 223: 'L', 156: 'M', 26: 'N',
##             89: 'O', 90: 'P', 91: 'Q', 92: 'R', 88: 'S', 72: 'T',
##             73: 'U', 154: 'V', 153: 'W', 155: 'X', 157: 'Y',
##             188: 'Z', 176: '0', 29: '1', 191: '2', 189: '3', 48: '4',
##             59: '5', 56: '6', 21: '7', 58: '8', 60: '9', 57: '~',
##             61: '!', 63: '@', 62: '#', 42: '$', 43: '%', 47: '^',
##             32: '&'}
##    maps[i] = ((maps[i][0], table)) 




# Outputs
for subset, table in maps:
    print('0    0    1    1    2    2    3    3    4    4    5    5')
    print('0    5    0    5    0    5    0    5    0    5    0    5')
    for row, start in enumerate(range(0, 4176, 58)):
        line = (''.join([table[x] for x in subset[start:start + 58]]))
        if row % 5 == 0:
            line += f' {row}'
        print(line)
    print('0    0    1    1    2    2    3    3    4    4    5    5')
    print('0    5    0    5    0    5    0    5    0    5    0    5')
    print()
    print(table)
    print()
    print()




