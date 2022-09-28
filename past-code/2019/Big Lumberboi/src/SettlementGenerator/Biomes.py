biomes = {
    "plains": [1, 129],
    "forest": [4, 18, 132],
    "birchForest": [27, 28, 155, 156],
    "darkForest": [29, 157],
    "swamp": [6, 134],
    "jungle": [21, 22, 23, 149, 151],
    "riverBeach": [7, 11, 16, 25],
    "taiga": [5, 19, 133, 30, 31, 158, 32, 33, 160, 161],
    "snowyIcy": [12, 140, 26],
    "mountains": [3, 13, 34, 131, 162, 20],
    "mushroom": [14, 15],
    "desert": [2, 17, 130],
    "savanna": [35, 36, 163, 164],
    "badlands": [37, 38, 39, 165, 166, 167],
    "aquatic": [0, 10, 24, 44, 45, 46, 47, 48, 49, 50]
}

def getBiomeDict():
    biomeDict = {}
    for key, value in biomes.items():
        for i in value:
            biomeDict[i] = key
    
    return biomeDict
