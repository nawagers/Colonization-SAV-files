"""
Written by nwagers, 2020

Intended to be shared by all who are curious.
Released to the public domain and completely
unrestricted, but attribution appreciated.

"""


path = 'C:\\GOG Games\\Colonization\\MPS\COLONIZE\\COLONY{}.SAV'

path1 = path.format('00')
path2 = path.format('01')



with open(path1, "rb") as binary_file:
        # Read the whole file at once
        data1 = binary_file.read()

with open(path2, "rb") as binary_file:
        # Read the whole file at once
        data2 = binary_file.read()


fields = []
for data in [data1, data2]:
    num_col = data[0x2E]
    num_unit = data[0x2C]
    num_vill = data[0x2A]
    map_width = int.from_bytes(data[0x0C:0x0E], 'little')
    map_height = int.from_bytes(data[0x0E:0x10], 'little')
    
    field = [('Header', 0, 1),
             ('Colonies', 0x186, 202),
             ('Units', 0x186 + 202*num_col, 28),
             ('Powers', 0x186 + 202*num_col + 28*num_unit, 316),
             ('Villages', 0x676 + 202*num_col + 28*num_unit, 18),
             ('Unknown B', 0x676 + 202*num_col + 28*num_unit + 18*num_vill, 1),
             ('Terrain Map', 0xBBD + 202*num_col + 28*num_unit + 18*num_vill, 1),
             ('Unknown Map C', 0xBBD + 202*num_col + 28*num_unit +
              18*num_vill + map_width*map_height, 1),
             ('Vis Map', 0xBBD + 202*num_col + 28*num_unit +
              18*num_vill + 2*map_width*map_height, 1),
             ('Unknown Map D', 0xBBD + 202*num_col + 28*num_unit +
              18*num_vill + 3*map_width*map_height, 1),
             ('Unknown E', 0xBBD + 202*num_col + 28*num_unit +
              18*num_vill + 4*map_width*map_height, 1),
             ('Unknown F', 0xDB5 + 202*num_col + 28*num_unit +
              18*num_vill + 4*map_width*map_height, 1),
             ('Trade Routes', 0xE23 + 202*num_col + 28*num_unit +
              18*num_vill + 4*map_width*map_height, 74)]
    fields.append(field)

print('Start Address')
for name, address, _ in fields[0]:
    print(f'  {name:13} 0x{address:04X}')
print()

# Variable size fields
sizes = [(0x2E, 1, 'colony', 'colonies'),
         (0x2C, 2, 'unit', 'units'),
         (0x2A, 4, 'village', 'villages')]


for address, field, single, plural in sizes:
    
    if data1[address] != data2[address]:
        print(f'***** ERROR: Different {single} count *****')
        print(f'File 1 has {data1[address]} {plural} and ', end = '')
        print(f'file 2 has {data2[address]}')
        print(f'Dropping {plural} from comparison')
        print()
        
        cutsize = fields[0][field + 1][1] - fields[0][field][1]
        removed = fields[1][field + 1][1] - fields[0][field + 1][1]

        # Realign data in data2, blank out section in both
        data1 = (data1[:fields[0][field][1]] + b'\x00' * cutsize +
                 data1[fields[0][field + 1][1]:])
        data2 = (data2[:fields[1][field][1]] + b'\x00' * cutsize +
                 data2[fields[1][field + 1][1]:])

        # Realign addresses for data2
        fields[1] = (fields[1][:field + 1] +
                     [(label, address - removed, group)
                      for label, address, group in fields[1][field + 1:]])


if any(data1[loc] != data2[loc] for loc in [0x0C, 0x0D, 0x0E, 0x0F]):
    print('*** Warning: Different map size ***')
    raise ValueError

if len(data1) != len(data2):
    print('*** Warning: File sizes different ***')
    raise ValueError


for address, vals in enumerate(zip(data1, data2)):
    if vals[0] != vals[1]:
        label = ''
        for field_name, start, length in fields[0]:
            if address >= start:
                label = field_name
                offset = address - start
                group = length

        print(f'Change at 0x{address:04X}: 0x{vals[0]:02X} -> '\
              f'0x{vals[1]:02X}  {label} (0x{offset:04X}', end = '')
        if group > 1:
            print(f', Group {offset // group} Byte {offset % group}', end = '')

        elif 'Map' in label:
            print(f' Position ({offset % map_width}),({offset // map_width})', end = '')
        print(')')
                  
