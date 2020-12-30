# Colonization-SAV-files
SAV file reader, editor, and tools

The goal of this project is to describe as much of the format of the save game files for Colonization 3.0 as possible and to build
a Python module that can read, modify, and rebuild valid SAV files.

Included are some helper files. The scripts are written for Python 3.6 and should be cross platform

## ALLTERRA.MP
A map file built with the map editor that features all the different terrain types as islands in the north of the map. The south
of the map contains 1 large continent. The east coast has all the base terrain types laid out in 3x3 patterns meant to easily build
coastal and inland colonies. The colony should be located 1 tile north of the moutains. This gives 1 mountain square for ore, 1 sea
square for fishing and sea port, and 6 forested squares. The north and west sides of the colony have a river for faster piece
movement. The next 3x3 grid inland features the same base terrain type but only has 1 forested square in the E. The SE ocean tile
allows for fishing over farming.

Further west along the north shore is larger 5x5 terrain sections, with 1 cental mountain and a river running N/S on the west edge.

## hex_compare.py
A helper script to compare the hex differences between two files with the address ranges programmed in. If a different number of
units, colonies, or villages exists, it will attempt to drop that section and compare the remainder. The way to use the script is
to edit the path variable at the top and plug in the save file numbers that you want to compare.

Generally you want to make as few changes as possible between comparisons. If you're going to have a unit perform an action, try to
have the next unit in the move order list have no orders so the game will wait for you to do something. Use a similar unit pause
concept for other actions too.

Example: You want to see how "load food" is stored in a trade route:
1. Create a trade route that has load food at the first stop.
2. Wait for the game to pause on a unit waiting for orders (they're blinking).
3. Save the game in the first slot (for file 00).
4. Edit the trade route to change the load food to load muskets.
5. You should be back on the blinking unit waiting for orders
6. Save the game in the second slot (for file 01).
7. Run hex_compare.py on files 01 and 02.
8. Note their absolute bytes and offset within the address range.
9. Look at the data in a hex editor like https://hexed.it/

Example: You want to see how a pioneer stores the remaining tools she has:
1. Go to Europe and buy a hardy pioneer.
2. Immediately get another unit (so they are the very next unit in the move queue).
3. Go to the new world and keep both units outside of a colony (outside the fence is fine).
4. Move the pioneer to a space she can build a road.
5. Save the game in the first slot.
6. Give the order to build the road.
7. If the road did not finish, clear the pioneer's order and go back to step 5 on the next turn.
8. The second unit should be waiting for orders.
9. Save the game in the second slot.
10. Run hex_compare.py on files 01 and 02.
11. Note their absolute bytes and offset within the address range.
12. Look at the data in a hex editor like https://hexed.it/


## colmapplotter.py
A helper script to visualize map data in a SAV file. There are 4 maps in a save game. At the
top of the script, edit the path as appropriate and select the file slot you want. Choose which
maps to display (0-3). Run the script and it will use characters to represent each tile. It may
help to pick a more square font, like 'terminal'.

In the static tables section there are examples of how to edit the maps. For example, once a terrain tile is
identified, it can be switched to dispaly a '-' in it's place, making it easier to see the remaining tiles.
Another good use on the terrain map is to change the Ocean tiles to ' '.

If comparing the maps between different saves, you'll want to set up static tables so that the same hex value
maps to the same letter on each run. The dynamic code assigns them in the order they are first seen, so a
change in the north can completely change the characters used in the south. There is an example commented out in
the code. Run the code the first time with dynamic tables and then copy the table it prints out and paste it in
the code. Sometimes this results in a 'KeyError'. Just add the key to the static table and run it again.


## format.md
This is an outline of the sections in the save file. It does not detail every byte, but describes each section,
where it starts, and the section's length. Important bytes are noted. A more detailed byte map is coming, and
the current version is here: https://docs.google.com/spreadsheets/d/1_IOGjJbMT43z2Tcr-Rhdwkg65iBaAV7Lo3XRl-08hII/edit?usp=sharing

## Future
A python module that fully reads the data and puts it in standard Python structures is partially made, but too sloppy to post yet.
