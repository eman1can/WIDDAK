# coding=utf-8
"""
Building encyclopedia contains parameters used to compute interest function for each building / scenario
"""


BUILDING_ENCYCLOPEDIA = {

    "Flat_scenario": {

        "Sociability": {
            "house-house": (10, 16, 80),
            "house-crop": (12, 20, 100),
            "house-windmill": (15, 40, 100),
            "house-ghost": (5, 10, 100),
            "crop-crop": (10, 13, 50),
            "crop-house": (12, 25, 50),
            "crop-windmill": (11, 15, 100),
            "crop-ghost": (5, 30, 100),
            "windmill-windmill": (20, 30, 100),
            "windmill-house": (25, 45, 100),
            "windmill-crop": (10, 15, 100),
            "windmill-ghost": (5, 40, 100),
            "ghost-house": (5, 10, 100),
            "ghost-crop": (20, 25, 100),
            "ghost-windmill": (20, 25, 100),

            "house-wood_tower": (16, 24, 40),
            "crop-wood_tower": (8, 16, 30),
            "windmill-wood_tower": (12, 20, 35),
            "wood_tower-house": (30, 40, 50),
            "wood_tower-crop": (12, 18, 25),
            "wood_tower-windmill": (12, 18, 25),
            "wood_tower-ghost": (25, 35, 60),
            "wood_tower-wood_tower": (16, 25, 50),

            "house-stone_tower": (12, 20, 40),
            "crop-stone_tower": (12, 30, 50),
            "windmill-stone_tower": (20, 30, 50),
            "wood_tower-stone_tower": (24, 35, 50),
            "stone_tower-ghost": (0, 10, 60),
            "stone_tower-house": (12, 18, 25),
            "stone_tower-crop": (12, 30, 50),
            "stone_tower-windmill": (12, 30, 50),
            "stone_tower-wood_tower": (24, 35, 50),
            "stone_tower-stone_tower": (24, 35, 50),
        },

        "Accessibility": {
            "house": (8, 11, 30),
            "crop": (8, 20, 40),
            "windmill": (8, 12, 18)
        },

        # represents the distance to the city centre, 0 = center, 1 = map border
        # computed as a balance function
        "Density": {
            "house": (-1, 0, 3),
            "crop": (1, 2, 4),
            "windmill": (1.5, 3, 4),
            "wood_tower": (0, 0.35, 1.2),
            "stone_tower": (-1, 0.2, 1),
        },

        "Altitude": {
            "house": (60, 68, 90),
            "crop": (65, 70, 80),
            "windmill": (65, 75, 95),
            "wood_tower": (62, 75, 90),
            "stone_tower": (68, 80, 95)
        },

        "Steepness": {
            "house": (1, 2),
            "crop": (0.5, 1),
            "windmill": (0, 4),
            "wood_tower": (0, 2.5),
            "stone_tower": (0, 4)
        },

        "RiverDistance": {
            "house": (5, 120),
            "crop": (7, 80),
            "windmill": (12, 150),
            "wood_tower": (12, 150),
            "stone_tower": (12, 150)
        },

        "OceanDistance": {
            "house": (10, 150),
            "crop": (30, 200),
            "windmill": (25, 200),
            "wood_tower": (20, 150),
            "stone_tower": (12, 150)
        },

        "LavaObstacle": {
            "house": (10, 20),
            "crop": (8, 15),
            "windmill": (10, 25),
            "wood_tower": (10, 20),
            "stone_tower": (6, 10)
        },

        # (accessibility, sociability, density, altitude, pure_water, sea_water, lava, steepness)
        "Weighting_factors": {
            "house": (1, 3, 3, 0, 1, 1, 1, 1),
            "crop": (1, 3, 2, 1, 2, 0, 1, 3),
            "windmill": (2, 4, 3, 1, 0, 0, 1, 2),
            "wood_tower": (1, 5, 1, 0, 1.5, 1, 1, 2),
            "stone_tower": (1, 5, 3, 0, 1, 1.5, 1, 2)
        },

        "markov": {
            "house": {"house": 10, "crop": 6},
            "crop": {"crop": 10, "windmill": 3, "house": 6},
            "windmill": {"crop": 1}
        },

        # "markov": {
        #     "house": {"house": 8, "stone_tower": 2, "crop": 6},
        #     "stone_tower": {"house": 1},
        #     "crop": {"crop": 8, "wood_tower": 2, "windmill": 4, "house": 6},
        #     "wood_tower": {"crop": 1},
        #     "windmill": {"crop": 1}
        # },

        "MaxSurface": {
            "crop": 300,
            "ghost": 1,
            "house": 150,
            "stone_tower": 64,
            "wood_tower": 49,
            "windmill": 81
        }
    }
}
