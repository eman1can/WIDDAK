import MaterialSets
from Biomes import getBiomeDict
from BlockDictionary import blockTypes as block_dictionary
from BiomeChanges import defaultBiomeChanges


def get_biome_materials(biome_id=1):
    biome_dict = getBiomeDict()
    biome_name = biome_dict[biome_id]
    materials = apply_biome_changes_to_material_set(
        MaterialSets.default.copy(), biome_name)

    return materials


def apply_biome_changes_to_material_set(material_set, biome):
    biomeChanges = defaultBiomeChanges[biome]
    return_materials = {}

    for key, value in material_set.items():
        if biomeChanges.get(value['type']):
            value = block_dictionary[biomeChanges[value['type']]]

        return_materials[key] = value

    return return_materials
