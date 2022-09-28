from generation import CropGenerator
from terrain import TerrainMaps

#
# def perform(level, box, options):
#     # type: (MCLevel, BoundingBox, dict) -> None
#     box = TransformBox(box)
#     maps = Maps(level, box)
#     gen = CropGenerator(box)
#     height_map = maps.height_map.box_height(box, False)
#     if options['type'] in Entity.entityList:
#         gen._gen_animal_farm(level, height_map, spruce_house_palette1, options['type'])
#     elif options['type'] == "Harvested":
#         gen._gen_harvested_crop(level, height_map)
#     else:
#

if __name__ == '__main__':
    terrain = TerrainMaps.request()
    gen = CropGenerator(terrain.box)
    height_map = terrain.height_map.box_height(terrain.box, False)
    gen._gen_crop_v1(height_map)
