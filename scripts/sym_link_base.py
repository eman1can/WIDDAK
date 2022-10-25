# Detect Minecraft Installation Location
from os import getcwd, listdir, symlink, remove
from os.path import exists, join
from gdpceu.common import get_minecraft_location

save_location = join(get_minecraft_location(), 'saves')

links = {}
if exists('.sym_link_data'):
    with open('.sym_link_data', 'r') as file:
        for x in file:
            v, k = x.strip().split(',')
            links[k] = v
else:
    print('No sym link data found.')

# Verify All Links
dead_links = 0
for link_dst, link_src in links.items():
    if not exists(link_src):
        remove(link_dst)
        dead_links += 1
if dead_links > 0:
    print(f'Removed {dead_links} dead links')


class SymLinkManager:
    def __init__(self):
        self._save_path = save_location
        self._base_path = getcwd()
        self._links = links

    def save_links(self):
        with open('.sym_link_data', 'w') as file:
            for k, v in self._links.items():
                file.write(','.join((v, k)) + '\n')

    def make_sym_link(self, world_path, world_name):
        # Make relative paths absolute
        if not world_path.startswith(self._base_path):
            world_path = join(self._base_path, world_path)
        dst = join(self._save_path, world_name)
        if exists(dst):
            remove(dst)
        symlink(world_path, dst)
        self._links[dst] = world_path
        return world_path, dst

    def delete_sym_link(self, world_path, world_name):
        dst = join(self._save_path, world_name)
        if not exists(dst):
            print(dst)
            print('Sym Link Doesn\'t Exist')
        else:
            remove(dst)
            self._links.pop(dst)

    def is_link(self, link_path):
        absolute_path = join(self._base_path, link_path)
        for link_src, link_dst in self._links:
            if link_src == absolute_path:
                return True
        return False

    def make_past_code_links(self):
        for year in listdir('past-code'):
            for project_name in listdir(join('past-code', year)):
                if project_name == '__MACOSX':
                    continue
                project_path = join(getcwd(), 'past-code', year, project_name)
                if not project_path.endswith('maps'):
                    project_path = join(project_path, 'maps')
                if not exists(project_path):
                    continue
                map_files = [x for x in listdir(project_path) if x != '__MACOSX']
                if len(map_files) == 0:
                    continue
                for ix, map_file in enumerate(map_files):
                    self.make_sym_link(join(project_path, map_file), f'{year} {project_name} Map {ix + 1}')

    def remove_past_code_links(self):
        for year in listdir('past-code'):
            for project_name in listdir(join('past-code', year)):
                if project_name == '__MACOSX':
                    continue
                project_path = join(getcwd(), 'past-code', year, project_name)
                if not project_path.endswith('maps'):
                    project_path = join(project_path, 'maps')
                if not exists(project_path):
                    continue
                map_files = [x for x in listdir(project_path) if x != '__MACOSX']
                if len(map_files) == 0:
                    continue
                for ix in range(len(map_files)):
                    self.delete_sym_link(project_path, f'{year} {project_name} Map {ix + 1}')
