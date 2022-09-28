from terrain import TerrainMaps
from generation import WindmillGenerator
from utils import TransformBox

if __name__ == '__main__':
    terrain = TerrainMaps.request()
    x, z = terrain.area.x, terrain.area.z
    w, l = terrain.area.width, terrain.area.length
    y = terrain.height_map[0, 0]
    box = TransformBox((x, y, z), (w, 1, l))
    WindmillGenerator(box).generate(terrain, terrain.height_map)
