from os.path import exists, expanduser, join
from sys import platform


def get_minecraft_location():
    if platform in ('win32', 'win64'):
        print('On Windows')
        location = expanduser(join('~', 'AppData', 'Roaming', '.minecraft'))
    elif platform == 'darwin':
        print('On Mac')
        location = expanduser(join('~', 'Library', 'Application Support', 'minecraft'))
    else:
        print('On Linux')
        location = expanduser(join('~', '.minecraft'))

    if not exists(location):
        print('Canno\'t find Minecraft location')
        return None
    return location
