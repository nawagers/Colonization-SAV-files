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
    
    field = [('Header', 0),
             ('Colonies', 0x186),
             ('Units', 0x186 + 202*num_col),
             ('Powers', 0x186 + 202*num_col + 28*num_unit),
             ('Villages', 0x676 + 202*num_col + 28*num_unit),
             ('Unknown B', 0x676 + 202*num_col + 28*num_unit + 18*num_vill),
             ('Terrain Map', 0xBBD + 202*num_col + 28*num_unit + 18*num_vill),
             ('Unknown Map C', 0xBBD + 202*num_col + 28*num_unit +
              18*num_vill + map_width*map_height),
             ('Vis Map', 0xBBD + 202*num_col + 28*num_unit +
              18*num_vill + 2*map_width*map_height),
             ('Unknown Map D', 0xBBD + 202*num_col + 28*num_unit +
              18*num_vill + 3*map_width*map_height),
             ('Unknown E', 0xBBD + 202*num_col + 28*num_unit +
              18*num_vill + 4*map_width*map_height),
             ('Unknown F', 0xDB5 + 202*num_col + 28*num_unit +
              18*num_vill + 4*map_width*map_height),
             ('Trade Routes', 0xE23 + 202*num_col + 28*num_unit +
              18*num_vill + 4*map_width*map_height)]
    fields.append(field)

print('Start Address')
for name, address in fields[0]:
    print(f'  {name:13} 0x{address:04X}')
print()
if data1[0x2E] != data2[0x2E]:
    
    print('***** ERROR: Different colony count *****')
    print(f'File 1 has {data1[0x2E]} colonies and file 2 has {data2[0x2E]}')
    print('Dropping colonies from comparison')
    print()
    cutsize = fields[0][2][1] - fields[0][1][1]
    data1 = data1[:fields[0][1][1]] + b'\x00' * cutsize + data1[fields[0][2][1]:]
    data2 = data2[:fields[1][1][1]] + b'\x00' * cutsize + data2[fields[1][2][1]:]


if data1[0x2C] != data2[0x2C]:
    print('***** ERROR: Different unit count *****')
    print(f'File 1 has {data1[0x2C]} units and file 2 has {data2[0x2C]}')
    print('Dropping units from comparison')
    print()
    cutsize = fields[0][3][1] - fields[0][2][1]
    data1 = data1[:fields[0][2][1]] + b'\x00' * cutsize + data1[fields[0][3][1]:]
    data2 = data2[:fields[1][2][1]] + b'\x00' * cutsize + data2[fields[1][3][1]:]

if data1[0x2A] != data2[0x2A]:
    print('***** ERROR: Different village count *****')
    print(f'File 1 has {data1[0x2A]} villages and file 2 has {data2[0x2A]}')
    print('Dropping villages from comparison')
    print()
    cutsize = fields[0][5][1] - fields[0][4][1]
    data1 = data1[:fields[0][4][1]] + b'\x00' * cutsize + data1[fields[0][5][1]:]
    data2 = data2[:fields[1][4][1]] + b'\x00' * cutsize + data2[fields[1][5][1]:]


if any(data1[loc] != data2[loc] for loc in [0x0C, 0x0D, 0x0E, 0x0F]):
    print('*** Warning: Different map size ***')
    raise ValueError

if len(data1) != len(data2):
    print('*** Warning: File sizes different ***')
    raise ValueError


for address, vals in enumerate(zip(data1, data2)):
    if vals[0] != vals[1]:
        label = ''
        for field_name, start in fields[0]:
            if address >= start:
                label = field_name
                offset = address - start
        print(f'Change at 0x{address:04X}: 0x{vals[0]:02X} -> 0x{vals[1]:02X}  {label} (0x{offset:04X})')
