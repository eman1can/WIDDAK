from os import listdir, mkdir
from os.path import exists, isdir, join
from shutil import copy, copytree

from gdpc_source.gdpc.interface import requestBuildArea
from gdpc_source.gdpc import worldLoader
from gdpc_source.gdpc.toolbox import loop2d
from gdpceu.common import get_minecraft_location

x1, y1, z1, x2, y2, z2 = requestBuildArea()
xw, zw = x2 - x1, x2 - z1
area = xw * zw

# The default step is 512
step = 1280
world_name = 'TestWorld1763'
save_world_name = 'New World (2)'

save_data = True
if exists(join('worlds', f'{world_name}.dat')):
    with open(join('worlds', f'{world_name}.dat'), 'rb') as dat_file:
        fworld_name, fstep, fx1, fz1, fx2, fz2 = dat_file.read().decode('utf-8').split(',')
        fstep, fx1, fz1, fx2, fz2 = int(fstep), int(fx1), int(fz1), int(fx2), int(fz2)

    if fx1 == x1 and fz1 == z1 and fx2 == x2 and fz2 == z2 and fstep == step:
        all_chunks_exist = True
        for x, z in loop2d(x1, z1, x2, z2, step):
            print(x, z, exists(join('worlds', world_name, 'saved', f'{x}_{z}_{step}.chunk')))
            all_chunks_exist &= exists(join('worlds', world_name, 'saved', f'{x}_{z}_{step}.chunk'))
            if not all_chunks_exist:
                x1, z1 = x, z
                break
        if all_chunks_exist:
            print('This World Already Exists')
            exit(0)
        save_data = False
    else:
        # Increment World Name
        while exists(join('worlds', f'{world_name}.dat')):
            world_name = world_name[:-1] + str(int(world_name[-1]) + 1)

# Save Dat File
if save_data:
    print(f'Saving World {x1}, {z1} -> {x2}, {z2}')
    print(f'World Name is: {world_name}')
    with open(join('worlds', f'{world_name}.dat'), 'wb') as dat_file:
        dat_file.write(','.join([world_name, str(step), str(x1), str(z1), str(x2), str(z2)]).encode('utf-8'))
else:
    print(f'Resuming World Save {x1}, {z1} -> {x2}, {z2}')

# Create Folders For World
if not exists(join('worlds', world_name)):
    mkdir(join('worlds', world_name))
if not exists(join('worlds', world_name, 'saved')):
    mkdir(join('worlds', world_name, 'saved'))
if not exists(join('worlds', world_name, 'raw')):
    mkdir(join('worlds', world_name, 'raw'))

# Save Minecraft World
if not exists(join('worlds', world_name, 'raw', 'level.dat')):
    save_location = join(get_minecraft_location(), 'saves')
    for file in listdir(join(save_location, save_world_name)):
        if file == 'session.lock':
            continue
        src = join(save_location, save_world_name, file)
        dst = join('worlds', world_name, 'raw', file)
        if isdir(src):
            copytree(src, dst)
        else:
            copy(src, dst)

# Get Chunks
print('Getting Chunks')
for x, z in loop2d(x1, z1, x2, z2, step):
    if exists(join('worlds', world_name, 'saved', f'{x}_{z}_{step}.chunk')):
        continue
    print(f'{x:5} - {z:5} -> {min(x2, x + step):5} - {min(z2, z + step):5}', end='')
    slice = worldLoader.WorldSlice(x, z, min(x2, x + step), min(z2, z + step))
    slice_name = join('worlds', world_name, 'saved', f'{x}_{z}_{step}.chunk')
    with open(slice_name, 'wb') as data:
        data.write(slice.byte_data)
    print('\b' * 30, end='')
print(f'Done')
# 8192 * 8192 // 512 * 512 = 256
# 67108864 // 262144 = 256
