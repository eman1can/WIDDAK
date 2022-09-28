# Detect Minecraft Installation Location
from os import chdir, getcwd, listdir, symlink, remove
from os.path import exists, expanduser
from sys import platform

save_location = None
if platform in ('win32', 'win64'):
    print('On Windows')
    save_location = expanduser('~/AppData/Roaming/.minecraft/saves')
elif platform == 'darwin':
    print('On Mac')
    save_location = expanduser('~/Library/Application Support/minecraft')
else:
    print('On Linux')
    save_location = expanduser('~/.minecraft')
save_location = save_location.replace('\\', '/')
if not exists(save_location):
    print('Canno\'t find Save Location')
    exit(1)

# Get the List of Projects
years = listdir('past-code')
projects = []
for year in years:
    project_names = listdir(f'past-code/{year}/')
    for project_name in project_names:
        if project_name == '__MACOSX':
            continue
        if project_name == 'maps':  # The Maps For this year
            projects += [(f'Base Maps {year}', f'{getcwd()}/past-code/{year}/{project_name}'.replace('\\', '/'))]
        else:
            projects += [(f'{year} {project_name}', f'{getcwd()}/past-code/{year}/{project_name}/maps'.replace('\\', '/'))]

chdir(save_location)
print(getcwd())
for project_name, project_path in projects:
    if not exists(project_path):
        continue  # This project has no maps
    map_files = [x for x in listdir(project_path) if x != '__MACOSX']
    if len(map_files) == 0:
        continue
    for ix, map_file in enumerate(map_files):
        if exists(f'{project_path}/{map_file}'):
            remove(f'{project_name} Map {ix + 1}')
        symlink(f'{project_path}/{map_file}', f'{project_name} Map {ix + 1}', True)
