import numpy as np
import random
import logging

def l_balcony(matrix, h, x_min, x_max, z_min, orientation, stairs_id, fence_id, structureBloc_id, slab_id, buildingStructureBloc_id):
    if orientation == "N" or orientation == "S":
        z_max = z_min - 1 if orientation == "S" else z_min + 1
        for x in range(x_min, x_max + 1) :
            for z in range(z_min, z_max - 1 if orientation == "S" else z_max + 1, -1 if orientation == "S" else 1) :
                if x == x_min or x == x_max or z == z_max :
                    matrix.setValue(h + 1, x, z, fence_id)
                    if (x == x_min or x == x_max) and not z == z_max :
                        if x == x_min :
                            matrix.setValue(h, x, z, (stairs_id, 4))
                        else :
                            matrix.setValue(h, x, z, (stairs_id, 5))
                    else :
                        if orientation == "S" :
                            matrix.setValue(h, x, z, (stairs_id, 6))
                        else :
                            matrix.setValue(h, x, z, (stairs_id, 7))
                else :
                    matrix.setValue(h, x, z, buildingStructureBloc_id)
                    matrix.setValue(h - 1, x, z, slab_id)
    elif orientation == "W" or orientation == "E" :
        a = True

def t_balcony(matrix, h, x_min, x_max, z_min, orientation, stairs_id, fence_id, structureBloc_id, slab_id, buildingStructureBloc_id):
    if orientation == "N" or orientation == "S":
        a = True

def generateBalcony(matrix, h, x_min, x_max, z_min, z_max, orientation, stairs_id, fence_id, structureBloc_id, slab_id, buildingStructureBloc_id):
    if orientation == "N" or orientation == "S" :
        depth = z_max - z_min
    elif orientation == "W" or orientation == "E" :
        depth = x_max - x_min
    else :
        logging.info("Error orientation {} does not exist".format(orientation))
    functions = [l_balcony]
    if depth > 2 :
        functions.append(t_balcony)
    f = functions[random.randint(0, len(functions) - 1)]
    f(matrix, h, x_min, x_max, z_min, orientation, stairs_id, fence_id, structureBloc_id, slab_id, buildingStructureBloc_id)
