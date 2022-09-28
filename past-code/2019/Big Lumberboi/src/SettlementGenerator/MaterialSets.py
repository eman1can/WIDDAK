from BlockDictionary import blockTypes

default = {
    "stone": blockTypes["cobblestone"],
    "wood": blockTypes["oak_wood"],
    "wood_planks": blockTypes["oak_wood_planks"],
    "fence": blockTypes["oak_wood_fence"],
    "torch": blockTypes["torch"],
    "glass": blockTypes["glass"],
    "glass_pane": blockTypes["glass_pane"],
    "door": blockTypes["oak_wood_door"]
}

oak = {
    "normal": (17, 0),  # Wood block
    "secondary": (5, 0),  # Plank
    "upper slab": (126, 8),
    "lower slab": (126, 0),
    "fence": (85, 0),
    "fence gate": (107 ,0),
    "door": (64, 0)
}

spruce = {
    "normal": (17, 1),  # Wood block
    "secondary": (5, 1),  # Plank
    "upper slab": (126, 9),
    "lower slab": (126, 1),
    "fence": (188, 0),
    "fence gate": (183, 0)
}

birch = {
    "normal": (17, 2),  # Wood block
    "secondary": (5, 2),  # Plank
    "upper slab": (126, 10),
    "lower slab": (126, 2),
    "fence": (189, 0),
    "fence gate": (184, 0)
}

jungle = {
    "normal": (17, 3), # Wood block
    "secondary": (5, 3),  # Plank
    "upper slab": (126, 11),
    "lower slab": (126, 3),
    "fence": (190, 0),
    "fence gate": (185, 0)
}

acacia = {
    "normal": (162, 0), # Wood block
    "secondary": (5, 4),  # Plank
    "upper slab": (126, 12),
    "lower slab": (126, 4),
    "fence": (192, 0),
    "fence gate": (187, 0)
}

darkOak = {
    "normal": (162, 1), # Wood block
    "secondary": (5, 5),  # Plank
    "upper slab": (126, 13),
    "lower slab": (126, 5),
    "fence": (191, 0),
    "fence gate": (186, 0)
}

# Ignore stone for now.
stone = {
    "normal": (4, 0),  # Cobblestone
    "secondary": (1, 0),  # Stone
    "upper slab": (44, 11),
    "lower slab": (44, 3),
    "fence": (139, 0)
}