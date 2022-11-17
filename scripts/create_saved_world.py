# Path Fixing Code - Must Be First
from os import getcwd, environ, chdir, listdir, makedirs
from os.path import exists, isdir, islink, split, join
from shutil import copy, copytree

# Start Path Fixing Code
# Ensure that no local imports are before this!
script_path = getcwd()
while not script_path.endswith('WIDDAK'):
    script_path = split(script_path)[0]
    chdir(script_path)
if 'PYTHONPATH' in environ:
    if script_path + ';' not in environ['PYTHONPATH']:
        environ['PYTHONPATH'] += script_path + ';'
else:
    environ['PYTHONPATH'] = script_path
# End Path Fixing Code

from gdpc.common import get_minecraft_location

if not exists(join('local', 'worlds')):
    makedirs(join('local', 'worlds'))

save_location = join(get_minecraft_location(), 'saves')

worlds_to_save = []
for world in listdir(save_location):
    if islink(save_location):
        continue
    worlds_to_save.append(world)

if len(worlds_to_save) == 0:
    print('You have no minecraft worlds! Please make one. :(')
    exit(1)

print('Select a world to save')
for ix, world in enumerate(worlds_to_save):
    print(f'\t{ix:2}. {world}')

chosen_world = input('\t>> ')

if not chosen_world.isdigit() and chosen_world not in worlds_to_save:
    print(f'{chosen_world} is not a valid input!')
    chosen_world = input('\t>> ')

if chosen_world.isdigit():
    chosen_world = worlds_to_save[int(chosen_world)]

print('Enter a name to save as:')
chosen_name = input('\t>> ')

while exists(join('local', 'worlds', chosen_name)):
    print('There is already a world with that name!')
    chosen_name = input('\t>> ')

print(f'Saving {chosen_world} to local/worlds/{chosen_name}')

raw_folder = join('local', 'worlds', chosen_name, 'raw')
edit_folder = join('local', 'worlds', chosen_name, 'edit')

if not exists(raw_folder):
    makedirs(raw_folder)
if not exists(edit_folder):
    makedirs(edit_folder)


def copy_file(src, dst):
    if isdir(src):
        copytree(src, dst)
    else:
        copy(src, dst)


print('Copying Minecraft World...', end='')
for file in listdir(join(save_location, chosen_world)):
    if file == 'session.lock':
        continue
    src = join(save_location, chosen_world, file)
    raw_dst = join(raw_folder, file)
    edit_dst = join(edit_folder, file)
    copy_file(src, raw_dst)
    copy_file(src, edit_dst)
print('Done')
