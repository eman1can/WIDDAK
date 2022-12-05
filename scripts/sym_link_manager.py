from os import chdir, environ, getcwd, listdir
from os.path import exists, isdir, join, split

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

from scripts.sym_link_base import SymLinkManager

print('Welcome to the sym link manager')

dialog = """Enter a command
\t0. Create Past Code Sym Links
\t1. Remove Past Code Sym Links
\t2. Add World Sym Link
\t3. Remove World Sym Link
\t4. Exit

\t>> """

base = SymLinkManager()


def get_worlds(add):
    world_files = listdir(join('local', 'worlds'))
    worlds = []
    for file in world_files:
        world_path = join('local', 'worlds', file, 'raw')
        if not exists(world_path) or not isdir(world_path):
            continue
        if add and base.is_link(world_path):
            continue
        worlds.append((world_path, file))
    return worlds


def select_world(worlds):
    world_dialog = 'Select a World\n'
    for ix, (world_path, world_name) in enumerate(worlds):
        world_dialog += f'\t{ix}. {world_name}\n'
    world_dialog += '\n\t>> '
    world_command = input(world_dialog)

    try:
        index = int(world_command.strip())
    except ValueError:
        print('Invalid Index')
        return None
    return index


def get_selected_world(add=True):
    index = None
    worlds = get_worlds(add)

    if len(worlds) == 0:
        print('No Worlds to Sym Link\n')
        return None

    while index is None:
        index = select_world(worlds)

    return worlds[index]


while True:
    command = input(dialog)
    try:
        command_index = int(command.strip())
    except ValueError:
        print('Invalid Command\n')
        continue

    if command_index == 4:
        print('Goodbye!')
        break
    elif command_index == 0:
        base.make_past_code_links()
        print('Sym Links Created')
    elif command_index == 1:
        base.remove_past_code_links()
        print('Sym Links Removed')
    elif command_index == 2:
        selected_world = get_selected_world()
        if selected_world is not None:
            base.make_sym_link(*selected_world)
    elif command_index == 3:
        selected_world = get_selected_world(False)
        if selected_world is not None:
            base.delete_sym_link(*selected_world)

base.save_links()
