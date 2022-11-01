# Path Fixing Code - Must Be First
from os import getcwd, environ, chdir, listdir
from os.path import split, join
from random import randint

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

from gdpc.interface import getWorldSlice
from gdpc.vector_util import Rect

save_area = Rect.from_corners(0, 0, 10240, 10240)

# The default step is 512
step = 256

world_path = join('local', 'worlds')
worlds = [join('local', 'worlds', x) for x in listdir(join('local', 'worlds')) if x.endswith('dat')]

if len(worlds) == 0:
    count = randint(1000, 9999)
else:
    count = int(worlds[-1][-8:-4])

world_name = f'TestWorld{count + 1}'
save_world_name = 'New World (2)'

world_slice = getWorldSlice(save_area, save_data=True)
world_slice.to_file(world_name, save_world_name, world_path, step)
