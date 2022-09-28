# plant_blocks = [BlockAPI.block.Sapling, BlockAPI.block.Web, BlockAPI.block.UnusedShrub, BlockAPI.block.TallGrass, BlockAPI.block.Shrub,
#                 BlockAPI.block.DesertShrub2, BlockAPI.block.Flower, BlockAPI.block.Rose, BlockAPI.block.BrownMushroom,
#                 BlockAPI.block.RedMushroom, BlockAPI.block.SugarCane, BlockAPI.block.BrewingStand, BlockAPI.block.TripwireHook,
#                 BlockAPI.block.Tripwire, BlockAPI.block.FlowerPot, BlockAPI.block.TallFlowers, BlockAPI.block.Wood, BlockAPI.block.Leaves]
#
# water_blocks = [BlockAPI.block.Water, BlockAPI.block.WaterActive, BlockAPI.block.Ice]
from itertools import product

from gdmc_http_client_python.interfaceUtils import placeBlockBatched as setBlockDefault, getBlock
from gdmc_http_client_python.worldLoader import WorldSlice
from utils import Point, BoundingBox, Iterable

alterated_pos = set()
def setBlock(point: Point, blockstate: str, buffer_size=50):
    res = setBlockDefault(point.x, point.y, point.z, blockstate, buffer_size)
    alterated_pos.add((point.x, point.z))
    # if res:
    #     for res in filter(lambda _: len(_) > 1, res.split('\n')):
    #         print(res)


def getBlockRelativeAt(world_slice: WorldSlice, x: int, y: int, z: int):
        """
        Get block with coords relative to the building area
        Parameters
        ----------
        world_slice (WorldSlice) the level
        x (int) X coord
        y (int) Y coord
        z (int) Z coord

        Returns
        -------
        Block str at (X, Y, Z)
        """
        x += world_slice.rect[0]
        z += world_slice.rect[1]
        return world_slice.getBlockAt((x, y, z))


class BlockAPI:
    class __BlockList:
        AcaciaDoor = "acacia_door"
        AcaciaFence = "acacia_fence"
        AcaciaFenceGate = "acacia_fence_gate"
        AcaciaLeaves = "acacia_leaves"
        AcaciaLog = "acacia_log"
        AcaciaPlanks = "acacia_planks"
        AcaciaPressurePlate = "acacia_pressure_plate"
        AcaciaSapling = "acacia_sapling"
        AcaciaSign = "acacia_sign"
        AcaciaSlab = "acacia_slab"
        AcaciaStairs = "acacia_stairs"
        AcaciaTrapdoor = "acacia_trapdoor"
        AcaciaWallSign = "acacia_wall_sign"
        AcaciaWood = "acacia_wood"
        Air = "air"
        Allium = "allium"
        AncientDebris = "ancient_debris"
        Andesite = "andesite"
        AndesiteSlab = "andesite_slab"
        AndesiteStairs = "andesite_stairs"
        AndesiteWall = "andesite_wall"
        Anvil = "anvil"
        AzureBluet = "azure_bluet"
        Bamboo = "bamboo"
        BambooSapling = "bamboo_sapling"
        Barrel = "barrel"
        Basalt = "basalt"
        Beacon = "beacon"
        Bedrock = "bedrock"
        BeeNest = "bee_nest"
        Beehive = "beehive"
        Beetroots = "beetroots"
        Bell = "bell"
        BirchDoor = "birch_door"
        BirchFence = "birch_fence"
        BirchFenceGate = "birch_fence_gate"
        BirchLeaves = "birch_leaves"
        BirchLog = "birch_log"
        BirchPlanks = "birch_planks"
        BirchPressurePlate = "birch_pressure_plate"
        BirchSapling = "birch_sapling"
        BirchSign = "birch_sign"
        BirchSlab = "birch_slab"
        BirchStairs = "birch_stairs"
        BirchTrapdoor = "birch_trapdoor"
        BirchWallSign = "birch_wall_sign"
        BirchWood = "birch_wood"
        BlackBanner = "black_banner"
        BlackBed = "black_bed"
        BlackCarpet = "black_carpet"
        BlackConcrete = "black_concrete"
        BlackConcretePowder = "black_concrete_powder"
        BlackGlazedTerracotta = "black_glazed_terracotta"
        BlackShulkerBox = "black_shulker_box"
        BlackStainedGlass = "black_stained_glass"
        BlackStainedGlassPane = "black_stained_glass_pane"
        BlackTerracotta = "black_terracotta"
        BlackWool = "black_wool"
        Blackstone = "blackstone"
        BlackstoneSlab = "blackstone_slab"
        BlackstoneStairs = "blackstone_stairs"
        BlackstoneWall = "blackstone_wall"
        BlastFurnace = "blast_furnace"
        BlueBanner = "blue_banner"
        BlueBed = "blue_bed"
        BlueCarpet = "blue_carpet"
        BlueConcrete = "blue_concrete"
        BlueConcretePowder = "blue_concrete_powder"
        BlueGlazedTerracotta = "blue_glazed_terracotta"
        BlueIce = "blue_ice"
        BlueOrchid = "blue_orchid"
        BlueShulkerBox = "blue_shulker_box"
        BlueStainedGlass = "blue_stained_glass"
        BlueStainedGlassPane = "blue_stained_glass_pane"
        BlueTerracotta = "blue_terracotta"
        BlueWool = "blue_wool"
        BoneBlock = "bone_block"
        Bookshelf = "bookshelf"
        BrainCoral = "brain_coral"
        BrainCoralBlock = "brain_coral_block"
        BrainCoralFan = "brain_coral_fan"
        BrewingStand = "brewing_stand"
        BrickSlab = "brick_slab"
        BrickStairs = "brick_stairs"
        BrickWall = "brick_wall"
        Bricks = "bricks"
        BrownBanner = "brown_banner"
        BrownBed = "brown_bed"
        BrownCarpet = "brown_carpet"
        BrownConcrete = "brown_concrete"
        BrownConcretePowder = "brown_concrete_powder"
        BrownGlazedTerracotta = "brown_glazed_terracotta"
        BrownMushroom = "brown_mushroom"
        BrownMushroomBlock = "brown_mushroom_block"
        BrownShulkerBox = "brown_shulker_box"
        BrownStainedGlass = "brown_stained_glass"
        BrownStainedGlassPane = "brown_stained_glass_pane"
        BrownTerracotta = "brown_terracotta"
        BrownWool = "brown_wool"
        BubbleColumn = "bubble_column"
        BubbleCoral = "bubble_coral"
        BubbleCoralBlock = "bubble_coral_block"
        BubbleCoralFan = "bubble_coral_fan"
        Cactus = "cactus"
        Campfire = "campfire"
        Carrots = "carrots"
        CartographyTable = "cartography_table"
        CarvedPumpkin = "carved_pumpkin"
        Cauldron = "cauldron"
        ChainCommandBlock = "chain_command_block"
        Chest = "chest"
        ChippedAnvil = "chipped_anvil"
        ChiseledNetherBricks = "chiseled_nether_bricks"
        ChiseledQuartzBlock = "chiseled_quartz_block"
        ChiseledRedSandstone = "chiseled_red_sandstone"
        ChiseledSandstone = "chiseled_sandstone"
        ChiseledStoneBricks = "chiseled_stone_bricks"
        ChorusFlower = "chorus_flower"
        ChorusPlant = "chorus_plant"
        Clay = "clay"
        CoalBlock = "coal_block"
        CoalOre = "coal_ore"
        CoarseDirt = "coarse_dirt"
        Cobblestone = "cobblestone"
        CobblestoneSlab = "cobblestone_slab"
        CobblestoneStairs = "cobblestone_stairs"
        CobblestoneWall = "cobblestone_wall"
        Cobweb = "cobweb"
        Cocoa = "cocoa"
        CommandBlock = "command_block"
        Composter = "composter"
        Conduit = "conduit"
        Cornflower = "cornflower"
        CrackedNetherBricks = "cracked_nether_bricks"
        CrackedStoneBricks = "cracked_stone_bricks"
        CraftingTable = "crafting_table"
        CrimsonDoor = "crimson_door"
        CrimsonFence = "crimson_fence"
        CrimsonFenceGate = "crimson_fence_gate"
        CrimsonFungus = "crimson_fungus"
        CrimsonHyphae = "crimson_hyphae"
        CrimsonNylium = "crimson_nylium"
        CrimsonPlanks = "crimson_planks"
        CrimsonPressurePlate = "crimson_pressure_plate"
        CrimsonRoots = "crimson_roots"
        CrimsonSign = "crimson_sign"
        CrimsonSlab = "crimson_slab"
        CrimsonStairs = "crimson_stairs"
        CrimsonStem = "crimson_stem"
        CrimsonTrapdoor = "crimson_trapdoor"
        CrimsonWallSign = "crimson_wall_sign"
        CryingObsidian = "crying_obsidian"
        CutRedSandstone = "cut_red_sandstone"
        CutRedSandstoneSlab = "cut_red_sandstone_slab"
        CutSandstone = "cut_sandstone"
        CutSandstoneSlab = "cut_sandstone_slab"
        CyanBanner = "cyan_banner"
        CyanBed = "cyan_bed"
        CyanCarpet = "cyan_carpet"
        CyanConcrete = "cyan_concrete"
        CyanConcretePowder = "cyan_concrete_powder"
        CyanGlazedTerracotta = "cyan_glazed_terracotta"
        CyanShulkerBox = "cyan_shulker_box"
        CyanStainedGlass = "cyan_stained_glass"
        CyanStainedGlassPane = "cyan_stained_glass_pane"
        CyanTerracotta = "cyan_terracotta"
        CyanWool = "cyan_wool"
        DamagedAnvil = "damaged_anvil"
        Dandelion = "dandelion"
        DarkOakDoor = "dark_oak_door"
        DarkOakFence = "dark_oak_fence"
        DarkOakFenceGate = "dark_oak_fence_gate"
        DarkOakLeaves = "dark_oak_leaves"
        DarkOakLog = "dark_oak_log"
        DarkOakPlanks = "dark_oak_planks"
        DarkOakPressurePlate = "dark_oak_pressure_plate"
        DarkOakSapling = "dark_oak_sapling"
        DarkOakSign = "dark_oak_sign"
        DarkOakSlab = "dark_oak_slab"
        DarkOakStairs = "dark_oak_stairs"
        DarkOakTrapdoor = "dark_oak_trapdoor"
        DarkOakWallSign = "dark_oak_wall_sign"
        DarkOakWood = "dark_oak_wood"
        DarkPrismarine = "dark_prismarine"
        DarkPrismarineSlab = "dark_prismarine_slab"
        DarkPrismarineStairs = "dark_prismarine_stairs"
        DaylightDetector = "daylight_detector"
        DeadBrainCoral = "dead_brain_coral"
        DeadBrainCoralBlock = "dead_brain_coral_block"
        DeadBrainCoralFan = "dead_brain_coral_fan"
        DeadBubbleCoral = "dead_bubble_coral"
        DeadBubbleCoralBlock = "dead_bubble_coral_block"
        DeadBubbleCoralFan = "dead_bubble_coral_fan"
        DeadBush = "dead_bush"
        DeadFireCoral = "dead_fire_coral"
        DeadFireCoralBlock = "dead_fire_coral_block"
        DeadFireCoralFan = "dead_fire_coral_fan"
        DeadHornCoral = "dead_horn_coral"
        DeadHornCoralBlock = "dead_horn_coral_block"
        DeadHornCoralFan = "dead_horn_coral_fan"
        DeadTubeCoral = "dead_tube_coral"
        DeadTubeCoralBlock = "dead_tube_coral_block"
        DeadTubeCoralFan = "dead_tube_coral_fan"
        DiamondBlock = "diamond_block"
        DiamondOre = "diamond_ore"
        Diorite = "diorite"
        DioriteSlab = "diorite_slab"
        DioriteStairs = "diorite_stairs"
        DioriteWall = "diorite_wall"
        Dirt = "dirt"
        Dispenser = "dispenser"
        DragonEgg = "dragon_egg"
        DriedKelpBlock = "dried_kelp_block"
        Dropper = "dropper"
        EmeraldBlock = "emerald_block"
        EmeraldOre = "emerald_ore"
        EnchantingTable = "enchanting_table"
        EndGateway = "end_gateway"
        EndPortal = "end_portal"
        EndPortalFrame = "end_portal_frame"
        EndStone = "end_stone"
        EndStoneBrickSlab = "end_stone_brick_slab"
        EndStoneBrickStairs = "end_stone_brick_stairs"
        EndStoneBrickWall = "end_stone_brick_wall"
        EndStoneBricks = "end_stone_bricks"
        EnderChest = "ender_chest"
        Farmland = "farmland"
        Fern = "fern"
        Fire = "fire"
        FireCoral = "fire_coral"
        FireCoralBlock = "fire_coral_block"
        FireCoralFan = "fire_coral_fan"
        FletchingTable = "fletching_table"
        FrostedIce = "frosted_ice"
        Furnace = "furnace"
        GildedBlackstone = "gilded_blackstone"
        Glowstone = "glowstone"
        GoldBlock = "gold_block"
        GoldOre = "gold_ore"
        Granite = "granite"
        GraniteSlab = "granite_slab"
        GraniteStairs = "granite_stairs"
        GraniteWall = "granite_wall"
        Grass = "grass"
        GrassBlock = "grass_block"
        GrassPath = "grass_path"
        Gravel = "gravel"
        GrayBanner = "gray_banner"
        GrayBed = "gray_bed"
        GrayCarpet = "gray_carpet"
        GrayConcrete = "gray_concrete"
        GrayConcretePowder = "gray_concrete_powder"
        GrayGlazedTerracotta = "gray_glazed_terracotta"
        GrayShulkerBox = "gray_shulker_box"
        GrayStainedGlass = "gray_stained_glass"
        GrayStainedGlassPane = "gray_stained_glass_pane"
        GrayTerracotta = "gray_terracotta"
        GrayWool = "gray_wool"
        GreenBanner = "green_banner"
        GreenBed = "green_bed"
        GreenCarpet = "green_carpet"
        GreenConcrete = "green_concrete"
        GreenConcretePowder = "green_concrete_powder"
        GreenGlazedTerracotta = "green_glazed_terracotta"
        GreenShulkerBox = "green_shulker_box"
        GreenStainedGlass = "green_stained_glass"
        GreenStainedGlassPane = "green_stained_glass_pane"
        GreenTerracotta = "green_terracotta"
        GreenWool = "green_wool"
        Grindstone = "grindstone"
        HayBlock = "hay_block"
        HeavyWeightedPressurePlate = "heavy_weighted_pressure_plate"
        HoneyBlock = "honey_block"
        HoneycombBlock = "honeycomb_block"
        Hopper = "hopper"
        HornCoral = "horn_coral"
        HornCoralBlock = "horn_coral_block"
        HornCoralFan = "horn_coral_fan"
        Ice = "ice"
        InfestedChiseledStoneBricks = "infested_chiseled_stone_bricks"
        InfestedCobblestone = "infested_cobblestone"
        InfestedCrackedStoneBricks = "infested_cracked_stone_bricks"
        InfestedMossyStoneBricks = "infested_mossy_stone_bricks"
        InfestedStone = "infested_stone"
        InfestedStoneBricks = "infested_stone_bricks"
        IronBlock = "iron_block"
        IronDoor = "iron_door"
        IronOre = "iron_ore"
        IronTrapdoor = "iron_trapdoor"
        JackOLantern = "jack_o_lantern"
        Jigsaw = "jigsaw"
        Jukebox = "jukebox"
        JungleDoor = "jungle_door"
        JungleFence = "jungle_fence"
        JungleFenceGate = "jungle_fence_gate"
        JungleLeaves = "jungle_leaves"
        JungleLog = "jungle_log"
        JunglePlanks = "jungle_planks"
        JunglePressurePlate = "jungle_pressure_plate"
        JungleSapling = "jungle_sapling"
        JungleSign = "jungle_sign"
        JungleSlab = "jungle_slab"
        JungleStairs = "jungle_stairs"
        JungleTrapdoor = "jungle_trapdoor"
        JungleWallSign = "jungle_wall_sign"
        JungleWood = "jungle_wood"
        Kelp = "kelp"
        Lantern = "lantern"
        LapisBlock = "lapis_block"
        LapisOre = "lapis_ore"
        LargeFern = "large_fern"
        Lava = "lava"
        Lectern = "lectern"
        LightBlueBanner = "light_blue_banner"
        LightBlueBed = "light_blue_bed"
        LightBlueCarpet = "light_blue_carpet"
        LightBlueConcrete = "light_blue_concrete"
        LightBlueConcretePowder = "light_blue_concrete_powder"
        LightBlueGlazedTerracotta = "light_blue_glazed_terracotta"
        LightBlueShulkerBox = "light_blue_shulker_box"
        LightBlueStainedGlass = "light_blue_stained_glass"
        LightBlueStainedGlassPane = "light_blue_stained_glass_pane"
        LightBlueTerracotta = "light_blue_terracotta"
        LightBlueWool = "light_blue_wool"
        LightGrayBanner = "light_gray_banner"
        LightGrayBed = "light_gray_bed"
        LightGrayCarpet = "light_gray_carpet"
        LightGrayConcrete = "light_gray_concrete"
        LightGrayConcretePowder = "light_gray_concrete_powder"
        LightGrayGlazedTerracotta = "light_gray_glazed_terracotta"
        LightGrayShulkerBox = "light_gray_shulker_box"
        LightGrayStainedGlass = "light_gray_stained_glass"
        LightGrayStainedGlassPane = "light_gray_stained_glass_pane"
        LightGrayTerracotta = "light_gray_terracotta"
        LightGrayWool = "light_gray_wool"
        LightWeightedPressurePlate = "light_weighted_pressure_plate"
        Lilac = "lilac"
        LilyOfTheValley = "lily_of_the_valley"
        LilyPad = "lily_pad"
        LimeBanner = "lime_banner"
        LimeBed = "lime_bed"
        LimeCarpet = "lime_carpet"
        LimeConcrete = "lime_concrete"
        LimeConcretePowder = "lime_concrete_powder"
        LimeGlazedTerracotta = "lime_glazed_terracotta"
        LimeShulkerBox = "lime_shulker_box"
        LimeStainedGlass = "lime_stained_glass"
        LimeStainedGlassPane = "lime_stained_glass_pane"
        LimeTerracotta = "lime_terracotta"
        LimeWool = "lime_wool"
        Lodestone = "lodestone"
        Loom = "loom"
        MagentaTerracotta = "magenta_terracotta"
        MagmaBlock = "magma_block"
        Melon = "melon"
        MelonStem = "melon_stem"
        MossyCobblestone = "mossy_cobblestone"
        MossyCobblestoneSlab = "mossy_cobblestone_slab"
        MossyCobblestoneStairs = "mossy_cobblestone_stairs"
        MossyCobblestoneWall = "mossy_cobblestone_wall"
        MossyStoneBrickSlab = "mossy_stone_brick_slab"
        MossyStoneBrickStairs = "mossy_stone_brick_stairs"
        MossyStoneBrickWall = "mossy_stone_brick_wall"
        MossyStoneBricks = "mossy_stone_bricks"
        MushroomStem = "mushroom_stem"
        Mycelium = "mycelium"
        NetherBrickFence = "nether_brick_fence"
        NetherBrickSlab = "nether_brick_slab"
        NetherBrickStairs = "nether_brick_stairs"
        NetherBrickWall = "nether_brick_wall"
        NetherBricks = "nether_bricks"
        NetherGoldOre = "nether_gold_ore"
        NetherQuartzOre = "nether_quartz_ore"
        NetherSprouts = "nether_sprouts"
        NetherWart = "nether_wart"
        NetherWartBlock = "nether_wart_block"
        NetheriteBlock = "netherite_block"
        Netherrack = "netherrack"
        NoteBlock = "note_block"
        OakDoor = "oak_door"
        OakFence = "oak_fence"
        OakFenceGate = "oak_fence_gate"
        OakLeaves = "oak_leaves"
        OakLog = "oak_log"
        OakPlanks = "oak_planks"
        OakPressurePlate = "oak_pressure_plate"
        OakSapling = "oak_sapling"
        OakSign = "oak_sign"
        OakSlab = "oak_slab"
        OakStairs = "oak_stairs"
        OakTrapdoor = "oak_trapdoor"
        OakWallSign = "oak_wall_sign"
        OakWood = "oak_wood"
        Observer = "observer"
        Obsidian = "obsidian"
        OrangeBanner = "orange_banner"
        OrangeBed = "orange_bed"
        OrangeCarpet = "orange_carpet"
        OrangeConcrete = "orange_concrete"
        OrangeConcretePowder = "orange_concrete_powder"
        OrangeGlazedTerracotta = "orange_glazed_terracotta"
        OrangeShulkerBox = "orange_shulker_box"
        OrangeStainedGlass = "orange_stained_glass"
        OrangeStainedGlassPane = "orange_stained_glass_pane"
        OrangeTerracotta = "orange_terracotta"
        OrangeTulip = "orange_tulip"
        OrangeWool = "orange_wool"
        OxeyeDaisy = "oxeye_daisy"
        PackedIce = "packed_ice"
        Peony = "peony"
        PetrifiedOakSlab = "petrified_oak_slab"
        PinkBanner = "pink_banner"
        PinkBed = "pink_bed"
        PinkCarpet = "pink_carpet"
        PinkConcrete = "pink_concrete"
        PinkConcretePowder = "pink_concrete_powder"
        PinkGlazedTerracotta = "pink_glazed_terracotta"
        PinkShulkerBox = "pink_shulker_box"
        PinkStainedGlass = "pink_stained_glass"
        PinkStainedGlassPane = "pink_stained_glass_pane"
        PinkTerracotta = "pink_terracotta"
        PinkTulip = "pink_tulip"
        PinkWool = "pink_wool"
        Piston = "piston"
        PistonHead = "piston_head"
        Podzol = "podzol"
        PolishedAndesite = "polished_andesite"
        PolishedAndesiteSlab = "polished_andesite_slab"
        PolishedAndesiteStairs = "polished_andesite_stairs"
        PolishedBasalt = "polished_basalt"
        PolishedBlackstone = "polished_blackstone"
        PolishedBlackstoneBrickSlab = "polished_blackstone_brick_slab"
        PolishedBlackstoneBrickStairs = "polished_blackstone_brick_stairs"
        PolishedBlackstoneBrickWall = "polished_blackstone_brick_wall"
        PolishedBlackstoneBricks = "polished_blackstone_bricks"
        PolishedBlackstoneSlab = "polished_blackstone_slab"
        PolishedBlackstoneStairs = "polished_blackstone_stairs"
        PolishedBlackstoneWall = "polished_blackstone_wall"
        PolishedDiorite = "polished_diorite"
        PolishedDioriteSlab = "polished_diorite_slab"
        PolishedDioriteStairs = "polished_diorite_stairs"
        PolishedGranite = "polished_granite"
        PolishedGraniteSlab = "polished_granite_slab"
        PolishedGraniteStairs = "polished_granite_stairs"
        Poppy = "poppy"
        Potatoes = "potatoes"
        PrismarineBrickSlab = "prismarine_brick_slab"
        PrismarineBrickStairs = "prismarine_brick_stairs"
        PrismarineBricks = "prismarine_bricks"
        PrismarineSlab = "prismarine_slab"
        PrismarineStairs = "prismarine_stairs"
        PrismarineWall = "prismarine_wall"
        Pumpkin = "pumpkin"
        PumpkinStem = "pumpkin_stem"
        PurpleBanner = "purple_banner"
        PurpleBed = "purple_bed"
        PurpleCarpet = "purple_carpet"
        PurpleConcrete = "purple_concrete"
        PurpleConcretePowder = "purple_concrete_powder"
        PurpleGlazedTerracotta = "purple_glazed_terracotta"
        PurpleShulkerBox = "purple_shulker_box"
        PurpleStainedGlass = "purple_stained_glass"
        PurpleStainedGlassPane = "purple_stained_glass_pane"
        PurpleTerracotta = "purple_terracotta"
        PurpleWool = "purple_wool"
        QuartzBlock = "quartz_block"
        QuartzBricks = "quartz_bricks"
        QuartzPillar = "quartz_pillar"
        QuartzSlab = "quartz_slab"
        QuartzStairs = "quartz_stairs"
        RedBanner = "red_banner"
        RedBed = "red_bed"
        RedCarpet = "red_carpet"
        RedConcrete = "red_concrete"
        RedConcretePowder = "red_concrete_powder"
        RedGlazedTerracotta = "red_glazed_terracotta"
        RedMushroom = "red_mushroom"
        RedMushroomBlock = "red_mushroom_block"
        RedNetherBrickSlab = "red_nether_brick_slab"
        RedNetherBrickStairs = "red_nether_brick_stairs"
        RedNetherBrickWall = "red_nether_brick_wall"
        RedNetherBricks = "red_nether_bricks"
        RedSand = "red_sand"
        RedSandstone = "red_sandstone"
        RedSandstoneSlab = "red_sandstone_slab"
        RedSandstoneStairs = "red_sandstone_stairs"
        RedSandstoneWall = "red_sandstone_wall"
        RedShulkerBox = "red_shulker_box"
        RedStainedGlass = "red_stained_glass"
        RedStainedGlassPane = "red_stained_glass_pane"
        RedTerracotta = "red_terracotta"
        RedTulip = "red_tulip"
        RedWool = "red_wool"
        RedstoneBlock = "redstone_block"
        RedstoneLamp = "redstone_lamp"
        RedstoneOre = "redstone_ore"
        RedstoneTorch = "redstone_torch"
        Repeater = "repeater"
        RepeatingCommandBlock = "repeating_command_block"
        RespawnAnchor = "respawn_anchor"
        RoseBush = "rose_bush"
        Sand = "sand"
        Sandstone = "sandstone"
        SandstoneSlab = "sandstone_slab"
        SandstoneStairs = "sandstone_stairs"
        SandstoneWall = "sandstone_wall"
        Scaffolding = "scaffolding"
        SeaLantern = "sea_lantern"
        SeaPickle = "sea_pickle"
        Seagrass = "seagrass"
        Shroomlight = "shroomlight"
        ShulkerBox = "shulker_box"
        SlimeBlock = "slime_block"
        SmithingTable = "smithing_table"
        Smoker = "smoker"
        SmoothQuartz = "smooth_quartz"
        SmoothQuartzSlab = "smooth_quartz_slab"
        SmoothQuartzStairs = "smooth_quartz_stairs"
        SmoothRedSandstone = "smooth_red_sandstone"
        SmoothRedSandstoneSlab = "smooth_red_sandstone_slab"
        SmoothRedSandstoneStairs = "smooth_red_sandstone_stairs"
        SmoothSandstone = "smooth_sandstone"
        SmoothSandstoneSlab = "smooth_sandstone_slab"
        SmoothSandstoneStairs = "smooth_sandstone_stairs"
        SmoothStone = "smooth_stone"
        Snow = "snow"
        SnowBlock = "snow_block"
        SoulCampfire = "soul_campfire"
        SoulFire = "soul_fire"
        SoulLantern = "soul_lantern"
        SoulSand = "soul_sand"
        SoulSoil = "soul_soil"
        Spawner = "spawner"
        Sponge = "sponge"
        SpruceDoor = "spruce_door"
        SpruceFence = "spruce_fence"
        SpruceFenceGate = "spruce_fence_gate"
        SpruceLeaves = "spruce_leaves"
        SpruceLog = "spruce_log"
        SprucePlanks = "spruce_planks"
        SprucePressurePlate = "spruce_pressure_plate"
        SpruceSapling = "spruce_sapling"
        SpruceSign = "spruce_sign"
        SpruceSlab = "spruce_slab"
        SpruceStairs = "spruce_stairs"
        SpruceTrapdoor = "spruce_trapdoor"
        SpruceWallSign = "spruce_wall_sign"
        SpruceWood = "spruce_wood"
        StickyPiston = "sticky_piston"
        Stone = "stone"
        StoneBrickSlab = "stone_brick_slab"
        StoneBrickStairs = "stone_brick_stairs"
        StoneBrickWall = "stone_brick_wall"
        StoneBricks = "stone_bricks"
        StoneBrick = "stone_brick"
        StonePressurePlate = "stone_pressure_plate"
        StoneSlab = "stone_slab"
        StoneStairs = "stone_stairs"
        Stonecutter = "stonecutter"
        StrippedAcaciaLog = "stripped_acacia_log"
        StrippedAcaciaWood = "stripped_acacia_wood"
        StrippedBirchLog = "stripped_birch_log"
        StrippedBirchWood = "stripped_birch_wood"
        StrippedCrimsonHyphae = "stripped_crimson_hyphae"
        StrippedCrimsonStem = "stripped_crimson_stem"
        StrippedDarkOakLog = "stripped_dark_oak_log"
        StrippedDarkOakWood = "stripped_dark_oak_wood"
        StrippedJungleLog = "stripped_jungle_log"
        StrippedJungleWood = "stripped_jungle_wood"
        StrippedOakLog = "stripped_oak_log"
        StrippedOakWood = "stripped_oak_wood"
        StrippedSpruceLog = "stripped_spruce_log"
        StrippedSpruceWood = "stripped_spruce_wood"
        StrippedWarpedHyphae = "stripped_warped_hyphae"
        StrippedWarpedStem = "stripped_warped_stem"
        StructureBlock = "structure_block"
        SugarCane = "sugar_cane"
        Sunflower = "sunflower"
        SweetBerryBush = "sweet_berry_bush"
        TallGrass = "tall_grass"
        TallSeagrass = "tall_seagrass"
        Target = "target"
        Terracotta = "terracotta"
        Tnt = "tnt"
        TrappedChest = "trapped_chest"
        TubeCoral = "tube_coral"
        TubeCoralBlock = "tube_coral_block"
        TubeCoralFan = "tube_coral_fan"
        TurtleEgg = "turtle_egg"
        TwistingVines = "twisting_vines"
        Vine = "vine"
        WarpedDoor = "warped_door"
        WarpedFence = "warped_fence"
        WarpedFenceGate = "warped_fence_gate"
        WarpedFungus = "warped_fungus"
        WarpedHyphae = "warped_hyphae"
        WarpedNylium = "warped_nylium"
        WarpedPlanks = "warped_planks"
        WarpedPressurePlate = "warped_pressure_plate"
        WarpedRoots = "warped_roots"
        WarpedSign = "warped_sign"
        WarpedSlab = "warped_slab"
        WarpedStairs = "warped_stairs"
        WarpedStem = "warped_stem"
        WarpedTrapdoor = "warped_trapdoor"
        WarpedWallSign = "warped_wall_sign"
        WarpedWartBlock = "warped_wart_block"
        Water = "water"
        WeepingVines = "weeping_vines"
        WetSponge = "wet_sponge"
        Wheat = "wheat"
        WhiteBanner = "white_banner"
        WhiteBed = "white_bed"
        WhiteCarpet = "white_carpet"
        WhiteConcrete = "white_concrete"
        WhiteConcretePowder = "white_concrete_powder"
        WhiteGlazedTerracotta = "white_glazed_terracotta"
        WhiteShulkerBox = "white_shulker_box"
        WhiteStainedGlass = "white_stained_glass"
        WhiteStainedGlassPane = "white_stained_glass_pane"
        WhiteTerracotta = "white_terracotta"
        WhiteTulip = "white_tulip"
        WhiteWool = "white_wool"
        WitherRose = "wither_rose"
        YellowBanner = "yellow_banner"
        YellowBed = "yellow_bed"
        YellowCarpet = "yellow_carpet"
        YellowConcrete = "yellow_concrete"
        YellowConcretePowder = "yellow_concrete_powder"
        YellowGlazedTerracotta = "yellow_glazed_terracotta"
        YellowShulkerBox = "yellow_shulker_box"
        YellowStainedGlass = "yellow_stained_glass"
        YellowStainedGlassPane = "yellow_stained_glass_pane"
        YellowTerracotta = "yellow_terracotta"
        YellowWool = "yellow_wool"

    class __Materials:
        Andesite = "andesite"

    blocks = __BlockList()

    @staticmethod
    def __buildBlockState(default_values, **kwargs):
        assert all(kw in default_values for kw in kwargs)
        valid_args = filter(lambda kw: kw[1] != default_values[kw[0]], kwargs.items())
        return "[" + ", ".join(f"{kw}={str(val).lower()}" for (kw, val) in valid_args) + "]"

    @staticmethod
    def getStairs(material: str, **kwargs):
        """

        :param material: material or stairs block as str
        :keyword facing: "north"
        :keyword half: "bottom"
        :keyword shape: "straight"
        :keyword waterlogged: "false"
        :return: stair block with properties
        """
        stairs_state_default = {"facing": "north", "half": "bottom", "shape": "straight", "waterlogged": "false"}
        block_str = material if material.endswith("_stairs") else f"{material}_stairs"
        if kwargs:
            block_str += BlockAPI.__buildBlockState(stairs_state_default, **kwargs)
        return block_str

    @staticmethod
    def getDoor(material, **kwargs):
        """
        Parameters
        ----------
        material
        kwargs
            facing: north
            half: lower, upper
            hinge: left
            open: false
            powered: false

        Returns
        -------

        """
        door_state_default = {"facing": "north", "half": "lower", "hinge": "left", "open": "false", "powered": "false"}
        if kwargs:
            return f"{material}_door{BlockAPI.__buildBlockState(door_state_default, **kwargs)}"
        else:
            return f"{material}_door"

    @staticmethod
    def getTorch(**kwargs):
        if not kwargs:
            return "torch"
        else:
            return "wall_torch" + BlockAPI.__buildBlockState({"facing": "north"}, **kwargs)

    @staticmethod
    def getFence(material, **kwargs):
        """
        Parameters
        ----------
        material
            fence/gate material
        kwargs
            facing = {north, east, south, west}

        Returns
        -------

        """
        if not kwargs:
            return f"{material}_fence"
        else:
            return f'{material}_fence_gate' + BlockAPI.__buildBlockState({"facing": "north"}, **kwargs)

    @staticmethod
    def getSlab(material, **kwargs):
        """
        Parameters
        ----------
        material
        kwargs
            type: bottom, top
            waterlogger: true, false
        Returns
        -------

        """
        return f"{material}_slab" + (BlockAPI.__buildBlockState({"type": "bottom", "waterlogged": "false"}, **kwargs))


# adapted from https://minecraft.fandom.com/wiki/Altitude#Natural_resources_and_altitude
b = BlockAPI.blocks
ground_blocks = {
    b.GrassBlock, b.Dirt, b.Gravel, b.Podzol, b.CoarseDirt, b.Farmland,
    b.Stone, b.Andesite, b.Diorite, b.Granite, b.Granite,
    b.Sand, b.Sandstone, b.Clay,
    b.CoalOre, b.IronOre, b.DiamondOre, b.GoldOre, b.RedstoneOre, b.LapisOre, b.EmeraldOre,
    b.Terracotta, b.YellowTerracotta, b.OrangeTerracotta,
    b.Netherrack, b.SoulSand,
    b.Bedrock,
    b.Glowstone
}

water_blocks = {b.Water, b.Ice, b.FrostedIce, b.PackedIce, b.BlueIce}

lava_blocks = {b.Lava}


def connected_component(maps, source_point, connection_condition, early_stopping_condition=None, check_limits=True):
    # type: (Maps, Point, Callable[[Point, Point, Maps], bool], Callable[[Set], bool]) -> (Point, ndarray)
    from numpy import full
    component, points_to_explore = set(), {source_point}

    # firstly, get all connected points in a set
    while points_to_explore:
        if early_stopping_condition and early_stopping_condition(component):
            break
        comp_point = points_to_explore.pop()
        component.add(comp_point)

        # explore direct neighbours for possible connected points
        for dx, dz in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x, z = comp_point.x + dx, comp_point.z + dz
            neighbour = Point(x, z)
            valid_x, valid_z = (0 <= x < maps.width), (0 <= z < maps.length)
            if (not check_limits or (valid_x and valid_z)) and connection_condition(comp_point, neighbour,
                                                                                    maps) and neighbour not in component:
                points_to_explore.add(neighbour)

    # secondly, generate a mask and a masked parcel to hold relevant info
    min_x, max_x = min(_.x for _ in component), max(_.x for _ in component)
    min_z, max_z = min(_.z for _ in component), max(_.z for _ in component)
    origin = Point(min_x, min_z)
    width = max_x - min_x + 1
    length = max_z - min_z + 1
    mask = full((width, length), False)
    for p in component:
        mask[p.x - min_x, p.z - min_z] = True
    return origin, mask


def clear_tree_at(terrain, point: Point) -> None:
    terrain.trees.remove_tree_at(point - terrain.area.origin)


def place_torch(x, y, z):
    if getBlock(x, y, z).endswith(":air"):
        torch = BlockAPI.getTorch()
        setBlock(Point(x, z, y), torch)


def fillBlocks(box: BoundingBox, block: str, blocksToReplace: str or Iterable[str] = None):
    """
    Parameters
    ----------
    box
    block
    blocksToReplace
    """
    if blocksToReplace and type(blocksToReplace) == str:
        blocksToReplace = {blocksToReplace}
    for x, y, z, in box.positions:
        p = Point(x, z, y)
        if not blocksToReplace or getBlock(x, y, z)[10:] in blocksToReplace:
            setBlock(p, block)


def symmetric_copy(origin: Point, size: Point, destination: Point, x_sym=False, y_sym=False, z_sym=False):
    if size.x <= 0 or size.y <= 0 or size.z <= 0:
        print("Invalid size for symmetric copy")
        return

    for dx, dy, dz in product(range(size.x), range(size.y), range(size.z)):
        dp = Point(dx, dy, dz)
        destination_x = destination.x + ((size.x - dx) if x_sym else dx)
        destination_y = destination.y + ((size.y - dy) if y_sym else dy)
        destination_z = destination.z + ((size.z - dz) if z_sym else dz)

        block = getBlock(*(origin + dp).coords, True)
        if x_sym:
            block = block.replace("west", "tmp").replace("east", "west").replace("tmp", "east")
        if y_sym:
            block = block.replace("top", "tmp").replace("bottom", "top").replace("tmp", "bottom")
        if z_sym:
            block = block.replace("north", "tmp").replace("south", "north").replace("tmp", "south")

        setBlock(Point(destination_x, destination_z, destination_y), block)
