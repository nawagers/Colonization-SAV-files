"""
Written by nwagers, 2024

Intended to be shared by all who are curious.
Released to the public domain and completely
unrestricted, but attribution appreciated.

"""

path = 'C:\\GOG Games\\Colonization\\MPS\\COLONIZE\\COLONY{}.SAV'
slot = '00'
path = path.format(slot)
display = [0]  # maps to print and their order [0, 1, 2, 3]

with open(path, "rb") as binary_file:
        # Read the whole file at once
        data = binary_file.read()

num_colonies = data[0x2e]
num_units = data[0x2c]
num_villages = data[0x2a]
map_width = data[0x0C]
map_height = data[0x0E]

offsets = data[0xDB5 + 202*num_colonies + 28*num_units + 18*num_villages + 4*map_width*map_height + 0x6C]
prime_offset = offsets & 0xF
lcr_offset = offsets >> 4 & 0xF
print(f'LCR: {lcr_offset}, Prime: {prime_offset}')


address = 0xBBD + num_colonies * 202 + num_units * 28 + num_villages * 18
subset = data[address:address + map_width*map_height]
address += map_width*map_height
suppress = data[address:address + map_width*map_height]


sea = (26, 90, 218)
water = (25, 26, 89, 90, 217, 218)
    
def prime(row, col, ter):
    if ter in sea:
        return False
    if suppress[row*map_width + col] & 0x4:
        return False
    pattern = {0: [0, 10, 17, 27, 34, 40, 51, 57],
               1: [4, 14, 21, 31, 38, 44, 55, 61],
               2: [2, 8, 19, 25, 32, 42, 49, 59],
               3: [6, 12, 23, 29, 36, 46, 53, 63]}
    col += 4 * prime_offset + (row//4) * 12
    if ter & 0x8 and ter not in water:
        col += 60
    return col % 64 in pattern[row%4]

def lcr(row, col, ter):
    if ter in water:
        return False
    pattern = {1: [36,53,70,87],
               2: [10,27,104,121],
               3: [44,61,78,95],
               0: [2,19,96,113]}
    col += 64 * lcr_offset + 68 * prime_offset + (row//4) * 12
    return col % 128 in pattern[row%4]

def square(row, col, ter):
    if lcr(row,col,ter):
        return 'o'
    if prime(row, col, ter):
        if ter in water:
            return 'f'
        return 'x'
    if ter in water:
        return ' '
    return '-'
    
# Outputs
print(''.join([str(x//10) if x%5 == 0 else ' ' for x in range(map_width)]))
print(''.join([str(x%10) if x%5 == 0 else ' ' for x in range(map_width)]))
for row, start in enumerate(range(0, map_width * map_height, map_width)):
    line = (''.join(square(row, col, x) for col, x in enumerate(subset[start:start + map_width])))
    if row % 5 == 0:
        line += f' {row}'
    print(line)
print(''.join([str(x//10) if x%5 == 0 else ' ' for x in range(map_width)]))
print(''.join([str(x%10) if x%5 == 0 else ' ' for x in range(map_width)]))
print()


