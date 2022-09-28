from itertools import product

from numpy import zeros, array

from gdmc_http_client_python.worldLoader import WorldSlice
from utils import BuildArea, Point
from terrain.map import Map


class BiomeMap(Map):

    def __init__(self, level: WorldSlice, area: BuildArea):
        # biomes
        values = zeros((level.chunkRect[2] * 4, level.chunkRect[3] * 4))
        for chunkX, chunkZ in product(range(level.chunkRect[2]), range(level.chunkRect[3])):
            chunkID = chunkX + level.chunkRect[2] * chunkZ
            biomes = level.nbtfile['Chunks'][chunkID]['Level']['Biomes'][:16]
            x0, z0 = chunkX * 4, chunkZ * 4
            values[x0: (x0+4), z0: (z0+4)] = array(biomes).reshape((4, 4), order='F')

        super().__init__(values)
        self.__offset = Point(area.x % 16, area.z % 16)

    def __getitem__(self, item):
        if not isinstance(item, Point):
            return self[Point(item[0], item[1])]
        biomePoint: Point = (item + self.__offset) // 4
        # return Map.__getitem__(self, biomePoint)
        return super(BiomeMap, self).__getitem__(biomePoint)

    _biome_types = {
        ("ocean", 0), ("taiga", 5), ("plains", 1), ("mountains", 3), ("desert", 2), ("forest", 4), ("swamp", 6),
        ("river", 7), ("nether_wastes", 8), ("the_end", 9), ("frozen_ocean", 10), ("frozen_river", 11),
        ("snowy_tundra", 12), ("snowy_mountains", 13), ("mushroom_fields", 14), ("mushroom_field_shore", 15),
        ("beach", 16), ("desert_hills", 17), ("wooded_hills", 18), ("taiga_hills", 19), ("mountain_edge", 20),
        ("jungle", 21), ("jungle_hills", 22), ("jungle_edge", 23), ("deep_ocean", 24), ("stone_shore", 25),
        ("snowy_beach", 26), ("birch_forest", 27), ("birch_forest_hills", 28), ("dark_forest", 29), ("snowy_taiga", 30),
        ("snowy_taiga_hills", 31), ("giant_tree_taiga", 32), ("giant_tree_taiga_hills", 33), ("wooded_mountains", 34),
        ("savanna", 35), ("savanna_plateau", 36), ("badlands", 37), ("wooded_badlands_plateau", 38),
        ("badlands_plateau", 39), ("small_end_islands", 40), ("end_midlands", 41), ("end_highlands", 42),
        ("end_barrens", 43), ("warm_ocean", 44), ("lukewarm_ocean", 45), ("cold_ocean", 46), ("deep_warm_ocean", 47),
        ("deep_lukewarm_ocean", 48), ("deep_cold_ocean", 49), ("deep_frozen_ocean", 50), ("the_void", 127),
        ("sunflower_plains", 129), ("desert_lakes", 130), ("gravelly_mountains", 131), ("flower_forest", 132),
        ("taiga_mountains", 133), ("swamp_hills", 134), ("ice_spikes", 140), ("modified_jungle", 149),
        ("modified_jungle_edge", 151), ("tall_birch_forest", 155), ("tall_birch_hills", 156), ("dark_forest_hills", 157),
        ("snowy_taiga_mountains", 158), ("giant_spruce_taiga", 160), ("giant_spruce_taiga_hills", 161),
        ("modified_gravelly_mountains", 162), ("shattered_savanna", 163), ("shattered_savanna_plateau", 164),
        ("eroded_badlands", 165), ("modified_wooded_badlands_plateau", 166), ("modified_badlands_plateau", 167),
        ("bamboo_jungle", 168), ("bamboo_jungle_hills", 169), ("soul_sand_valley", 170), ("crimson_forest", 171),
        ("warped_forest", 172), ("basalt_deltas", 173)
    }

    # bi map from biome name to biome id
    __biome_to_id = {_[0]: _[1] for _ in _biome_types}
    __id_to_biome = {_[1]: _[0] for _ in _biome_types}

    @staticmethod
    def getBiome(biome_id: int): return BiomeMap.__id_to_biome[biome_id]

    @staticmethod
    def getBiomeId(biome_type: str): return BiomeMap.__biome_to_id[biome_type]


if __name__ == '__main__':
    from terrain import TerrainMaps
    assert BiomeMap.getBiomeId("warm_ocean") == 44
    assert BiomeMap.getBiome(3) == "mountains"
    print({_ for _ in map(lambda _: _[0], BiomeMap._biome_types)})

    terrain = TerrainMaps.request()
    print(terrain.biome[0, 0])

