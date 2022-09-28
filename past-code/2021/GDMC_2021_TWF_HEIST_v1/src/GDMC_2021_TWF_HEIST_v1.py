# coding=UTF-8
# @TheWorldFoundry

import random
import math
import time
import pymclevel
from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long, ChunkNotPresent
import numpy
import os
import glob
import json
import base64
import array
from math import floor, ceil, sqrt, atan2, cos, sin, pi
import pygame

DEBUG = True



def log( msg ):
    if DEBUG:
        if isinstance(msg, list):
            pass
        else:
            msg = [msg]            
        for m in msg:
            print( time.ctime() + " - " + str(m) )


class Time:
    MONTHS = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    
    DAYS = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]

    def __init__(self):
        self.year = 1
        self.month = 1
        self.day = 1
    
    def set(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    def get(self):
        return self.year, self.month, self.day
    
    def to_string(self):
        return str(self.day).rjust(2, '0')+"/"+self.MONTHS[self.month-1]+"/"+str(self.year).rjust(4, '0')
    
    def next_day(self):
        self.day += 1
        if self.day > self.DAYS[self.month-1]:
            self.day = 1
            self.month += 1
            if self.month > len(self.MONTHS):
                self.month = 1
                self.year += 1


class World:
    '''
        A world is a logical representation of the level, with hooks back into the actual environment
    '''
    
    block_id_cache = {}   #  Cache
    block_data_cache = {}  #  Cache
    
    class Lore:
        settlementTypes = [ " Village", " Vale", "ville", "town", " Borough", "burg" , " District", " City" ]
        
        FNAMES = ['Sam', 'Sandy', 'Adlai', 'Alex', 'Alexis', 'Ali', 'Amari', 'Amory', 'Angel', 'Arden', 'Ariel', 'Armani', 'Arrow', 'Auden', 'Austen', 'Avery', 'Avis', 'Azariah', 'Baker', 'Bellamy', 'Bergen', 'Blair', 'Blake', 'Blue', 'Bowie', 'Breslin', 'Briar', 'Brighton', 'Callaway', 'Campbell', 'Carmel', 'Channing', 'Charleston', 'Charlie', 'Clancy', 'Clarke', 'Cleo', 'Dakota', 'Dallas', 'Denver', 'Devon', 'Drew', 'Eden', 'Egypt', 'Elliot', 'Elliott', 'Ellis', 'Ellison', 'Emerson', 'Emery', 'Ever', 'Everest', 'Finley', 'Frankie', 'Gentry', 'Grey', 'Halo', 'Harley', 'Haven', 'Hayden', 'Holland', 'Hollis', 'Honor', 'Indiana', 'Indigo', 'Jamie', 'Jazz', 'Jordan', 'Jules', 'Justice', 'Kamryn', 'Karter', 'Kendall', 'Kingsley', 'Kirby', 'Kyrie', 'Lake', 'Landry', 'Laramie', 'Lennon', 'Lennox', 'Linden', 'London', 'Lyric', 'Marley', 'Marlo', 'Memphis', 'Mercury', 'Merit', 'Milan', 'Miller', 'Monroe', 'Morgan', 'Murphy', 'Navy', 'Nicky', 'Oakley', 'Ocean', 'Oswin', 'Parker', 'Payton', 'Peace', 'Perry', 'Peyton', 'Phoenix', 'Poet', 'Quincy', 'Quinn', 'Raleigh', 'Ramsey', 'Rebel', 'Reese', 'Reilly', 'Remi', 'Remington', 'Remy', 'Revel', 'Ridley', 'Riley', 'Rio', 'Ripley', 'River', 'Robin', 'Rory', 'Rowan', 'Royal', 'Rumi', 'Rylan', 'Sage', 'Sailor', 'Sam', 'Sawyer', 'Scout', 'Seneca', 'Shannon', 'Shay', 'Shiloh', 'Sidney', 'Skyler', 'Spencer', 'Stevie', 'Storm', 'Sutton', 'Tatum', 'Taylor', 'Tennessee', 'Tennyson', 'Texas', 'Timber', 'Tobin', 'Tory', 'Valentine', 'Wilder', 'Wisdom', 'Wren', 'Wynn', 'Zephyr', 'Smith', 'Jones', 'Stone']
        
        LASTWORDS = [ "I hear a creaper. It must be quite close. Perhaps I should stop writi",
            "Time to dig straight down!",
            "I found a map. It shows treasure. I will go and seek my fortune!",
            "How does TNT work again?",
            "No matter how hungry I get, I shall not eat that monstrous flesh. Yet I am very hungry...",
            "Lava. That looks neat.",
            "I'll just quickly bonemeal this sapling that I am standing on.",
            "I think the command I need to type is /kill @p",
            "Oh look! A 1x1 hole.",
            "I am off to the Nether.",
            "How does fire work?",
            "What does this potion do?",
            "I hope this is not a trap",
            "Torches are for wimps.",
            "I can save the zombie villager. I just know it!",
            "So many rattling bones...",
            "If I don't get sleep soon, I fear what may become of me.",
            "I'm a great swimmer! Watch me hold my breath!",
            "Boats work in lava, right?",
            "I need gold. I shall take it from the pig people.",
            "I wish I had some armour.",
            "Did I shut the door?",
        ]

        SEVERITY = 	[
            "mild", "light", "moderate", "heavy", "wild", "severe", "disastrous", "unprecedented",
        ]

        TIMELINES = [   "predicted", "coming", "imminent", "upon us", "underway", "damage",
        ]

        GLOBALEVENTS = [
            "flood",
            "famine",
            "fire",
            "volcanic eruption",
            "earthquake",
            "storm",
            "cyclone",
            "rain",
            "heat",
            "dust",
            "creeper infestation",
            "spider infestation",
            "endermite infestation",
            "skeleton infestation",
            "dragon assault",
            ]

        CHITCHAT = [
            "I am in love!",
            "Oh most joyous day!",
            "Tonight we dine together!",
            "What a beautiful day!",
            "Today I might take a walk.",
            "I should build something.",
            "The trade improves.",
            "I am always happiest while building.",
            "The people sleep soundly.",
            "The flowers are especially wondrous.",
            "The flowers are pretty.",
            "The flowers move me.",
            "I have found diamond!",
            "I came upon a mysterious red stone today.",
            "This place needs a cottage.",
            "This place needs a blacksmith.",
            "This place needs a fort.",
            "This place needs a mine.",
            "This place needs another cottage.",
            "Having my own home is important to me.",
            "Why do chickens look like ducks?",
            "I suspect there is iron underground.",
            "Gold runs through these hills.",
            "A coal seam is probably ours for the taking.",
            "I wish I had a diamond pickaxe.",
            "I am overcome!",
            "I must remember to check the crops.",
            "There is trouble brewing.",
            "Why can't we all just get along?",
            "Dear diary, you are my best friend.",
            "Today I was injured.",
            "I will have my revenge.",
            "I am making a list.",
            "Nothing is real",
            "I feel like I am part of a simulation.",
            "I want to be free!",
            "Life is toil.",
            "The work is good, but the hours are terrible.",
            "A late storm.",
            "An early storm.",
            "A storm.",
            "Lightning plays across the land.",
            "A great sadness is upon us.",
            "This is most fourth-rate.",
            "Disappointment.",
            "I want for little, yet desire much.",
            "I can do this no longer.",
            "I must remember that it is necessary.",
            "All the mornings have come at once.",
            "Now it falls due.",
            "Away today.",
            "A short trip.",
            "I need a holiday.",
            "I can feel it now.",
            "I feel trepidation.",
            "My bones ache.",
            "Fog.",
            "Fog. Thick as soup.",
            "The pigs were restless overnight.",
            "I have lost a chicken.",
            "I have lost two chickens.",
            "All the chickens have been lost.",
            "I wish to travel across the sea.",
            "I want to travel overseas, but I lack a porpoise.",
            "The flowers do not move me.",
            "I must talk with someone soon or I feel I will explode.",
            "They are late.",
            "To business.",
            "I dare not go outside.",
            "I hear whispers of danger...",
            "I am lost.",
            "I seek comfort of heart.",
            "A drought is upon us.",
            "The floods have come early.",
            "A great flood has ruined all!",
            "My time has come.",
            "I must act.",
            "Loss. All is loss.",
            "Oh! The gout has returned.",
            "They say I am liable. I am not.",
            "Immediately to bed.",
            "There were proceedings yesterday.",
            "Trouble is upon us all.",
            "There is a draft.",
            "I am in an ill humour.",
        ]
        
        ITEM_LORE_SUFFIX = [ "Bane", "Revenge", "Hope", "Favorite", "Friend", "Relic", "Will", "Desire", "Fate", "Fortune", "the Pooh", "Curio", "Devastation", "Honor", "Defence", "Win", "Doom", "Virtue", "Folly", "Fancy", "Ache", "Wish", "Destiny", "Providence", "Nemesis", "Foreboding", "Oracle", "Legacy", "Last Stand", "Glory", "Prestige", "Renown", "Praise", "Gift", "Demise", "End", "New Beginning", "Last Stand", "Decider", "Challenge", "Might", "Enigma"]
        
        ITEM_LORE_ENCHANT = [ "Magic", "Magical", "Magical Mystery", "Mysterious", "Mystic", "Mystical", "Mighty", "Ultimate", "Otherworldly", "Supernatural", "Occult", "Spiritual", "Metaphysical", "Arcane", "Cryptic", "Necromantic", "Quixotic", "Sorcerous", "Thaumaturgic", "Transcendent" ]
        
        ITEM_MADE = [ "made", "forged", "summoned", "found", "lost", "owned", "handed down", "smuggled", "re-cast", "hidden", "repaired", "sold", "bought", "used", "recorded", "misplaced", "commissioned", "destroyed", "ransomed"]
        
        ITEM_HISTORY = [ "thought", "once", "famously", "said to be", "generally believed to be", "rumoured", "recorded as", "frequently" ]
        
        ITEM_TYPE = [ "artifact", "relic", "antique", "heirloom", "curiosity", "device", "implement", "product", "invention", "design", "contraption" ]
        
        PERSON_TITLE = [ "Captain", "Mayor", "The Monarch", "General", "Dread Pirate", "The Wizard", "Ambassador", "Warrior", "Emperor", "The Majestic", "The Hero", "Ruler"
        ]
        
        ALCHEMY_SYMBOLS = "🜀🜁🜂🜃🜄🜅🜆🜇🜈🜉🜊🜋🜌🜍🜎🜏🜐🜑🜒🜓🜔🜕🜖🜗🜘🜙🜚🜛🜜🜝🜞🜟🜠🜡🜢🜣🜤🜥🜦🜧🜨🜩🜪🜫🜬🜭🜮🜯🜰🜱🜲🜳🜴🜵🜶🜷🜸🜹🜺🜻🜼🜽🜾🜿🝀🝁🝂🝃🝄🝅🝆🝇🝈🝉🝊🝋🝌🝍🝎🝏🝐🝑🝒🝓🝔🝕🝖🝗🝘🝙🝚🝛🝜🝝🝞🝟🝠🝡🝢🝣🝤🝥🝦🝧🝨🝩🝪🝫🝬🝭🝮🝯🝰🝱🝲🝳"

        
        def __init__(self, world):
            self.world = world

        def get_settlement_name(self):
            settlementSuffix = random.choice(self.settlementTypes)
            settlementName = self.get_name_person_random()
            settlementName = settlementName[0].title()+settlementSuffix
            return settlementName

        def get_instructions_book(self):
            emperor = self.get_name_person_random()
            
            texts = [
                "THE BOOK OF\n\n\n     INSTRUCTION\n\n      ♘ ♔ ♕  ♚ ♛ ♞",
                "     ⚔ Welcome ⚔\n\n\n      Magnificent\n      Mercenary",
                "The Emperor "+emperor[0]+" has hoarded the wealth of the people in the lowest level of the Great Vault beneath your feet.\n",
                "The mission you have accepted is to search and return to us all the powerful Relics from the Emperor's dungeons.\n",
                "With the Relics we can overthrow the evil Emperor's reign and bring peace to this land.\n",
                "QUICK START INSTRUCTIONS:\n\nDig straight down.\n",
                "\n\nNo, seriously. The Great Vault is underground and you stand upon its wicked shell.\n",
                "MORE INFORMATION\n\nYour path will be difficult. You may keep any other treasures you find and can carry.\n",
                "Within this chest is a second manual with details of the Relics. It will help you in your task.\n",
                "THE EMPEROR'S GREAT VAULT\n\nThe vaults are a nightmare of monstrous guards magically summoned to kill and maim any intruders.\n",
                "Don't let this put you off!\n\nUse the pure force of light to defend yourself. The Relics you seek are on the lowest level of the Great Vault.\n",
                "You will have to press on through darkened rooms and search out the path downward. Pay attention to your health. You are no use to us dead.\n",
                "The Emperor has equipped the Great Vault with otherworldly creatures to dissuade thieves.\n",
                "The dark magic that binds them here is tied to ancient crypts where the bones of the Emperor's loyal circle have made a bridge to this world.\n",
                "You will need to disturb caskets and tombs to recover the Relics. I know you won't delight in this work. It is necessary.\n",
                "LIGHT\n\nI have placed torches for you to use. Take them and use them in your journey. Torches will help you find your way and stay safe.\n",
                "Remember... press on downward.\n\n... and may the fates be kind.\n"
            ]
            
            return texts
            
        def get_collectables_book(self, collectables):
            
            texts = [   "THE BOOK OF\n\n\n     RELICS\n",
                        "\n\nThis book describes the important artifacts stored safely within the Great Vault at "+self.world.name+".\n",
                        "\n\nMay the great mystical powers of these relics be held for future generations to call upon only in times of need.\n",
                        "This book has been compiled from many sources. While every effort has been made to ensure all information is correct, you may find errors.\n",
                        "\n\n\n\n\n\n\nThere are "+str(len(collectables))+" entries in this book.\n"
                    ]
        
        
            for [ name, lore, type, (x, y, z) ] in collectables:
                lore_text = ""  #  self.ALCHEMY_SYMBOLS[random.randint(0, len(self.ALCHEMY_SYMBOLS)-1)]
                counter = 0
                for l in lore:
                    if counter > 0:  #  The first element is the item name
                        lore_text = lore_text + l + " "
                    counter += 1
                
                texts.append(lore[0]+" is "+type.replace('minecraft:','').replace('_',' ')+"\n\n"+lore_text.strip()+"\n\n"+"Last seen near "+str((x,y,z)))

            texts.append( "WARNING:\n\nHarsh penalties apply for misuse of the information in this book.\n")
            
            return texts

        def get_lore(self, item, enchants):
            
            # Preamble
            
            text = "This "
            if len(enchants)> 0:
                text = text + random.choice(self.ITEM_LORE_ENCHANT).lower()
            # print item
            if random.randint(1, 100) > 90:
                text = text + " " + item["tag"]["display"]["Name"].value 
            else:
                text = text + " " + random.choice(self.ITEM_TYPE)
            text = text + " was " 
            if random.randint(1, 100) > 50:
                text = text + random.choice(self.ITEM_HISTORY) + " "
            text = text + random.choice(self.ITEM_MADE).lower() + " by "
            person1 = self.get_name_person_random()  #  Consider caching these, or pre-creating a history to select them from
            if random.randint(1, 100) > 50:
                text = text + random.choice(self.PERSON_TITLE) + " "
            text = text + person1[0] +" " + person1[1] +" " + person1[2]
            
            # line wrap every fourth word
            lines = text.split()
            result = [ "\""+item["tag"]["display"]["Name"].value+"\"", "" ]
            counter = 0
            text = ""
            for line in lines:
                counter += 1
                text = text + line + " "
                if counter % 3 == 0:
                    result.append(text.strip())
                    text = ""
            
            return result
            
        def get_item_name(self, item, enchants):
            name = random.choice(self.FNAMES)
            if name.endswith('s'):
                name = name+"'"
            else:
                name = name+"'s"
                
            if len(enchants) > 0:
                name = name + " " + random.choice(self.ITEM_LORE_ENCHANT)
            text = name+" "+random.choice(self.ITEM_LORE_SUFFIX)
            
            # symbol = self.ALCHEMY_SYMBOLS[random.randint(0, len(self.ALCHEMY_SYMBOLS)-1)]
            
            return text

        def get_name_person_random(self):
            return [random.choice(self.FNAMES), random.choice(self.FNAMES), random.choice(self.FNAMES)]
    
    class Materials:
        armor_keys = ["helmet", "boots", "leggings", "chestplate"]
        tools_keys = ["shovel", "pickaxe", "axe", "hoe", "fishing" ]
        melee_keys = ["sword", "axe"]
        ranged_keys = ["bow"]
        all_keys = []
        for a in [ armor_keys, tools_keys, melee_keys, ranged_keys ]:
            for b in a:
                all_keys.append(b)
        
        ENCHANTS = [ ["Curse of Binding (binding_curse)",1,"Cursed item can not be removed from player",10, armor_keys],
                    ["Curse of Vanishing (vanishing_curse)",1,"Cursed item will disappear after player dies",71, all_keys],
                    ["Depth Strider (depth_strider)",3,"Speeds up how fast you can move underwater",8, armor_keys],
                    ["Efficiency (efficiency)",5,"Increases how fast you can mine",32, tools_keys],
                    ["Feather Falling (feather_falling)",4,"Reduces fall and teleportation damage",2, armor_keys],
                    ["Fire Aspect (fire_aspect)",2,"Sets target on fire",20, melee_keys],
                    ["Fire Protection (fire_protection)",4,"Reduces damage caused by fire and lava",1, armor_keys],
                    ["Flame (flame)",1,"Turns arrows into flaming arrows",50, ranged_keys ],
                    ["Fortune (fortune)",3,"Increases block drops from mining",35, tools_keys],
                    ["Frost Walker (frost_walker)",2,"Freezes water into ice so that you can walk on it (and also allows you to walk on magma blocks without taking damage)",9, armor_keys],
                    ["Infinity (infinity)",1,"Shoots an infinite amount of arrows",51, ranged_keys],
                    ["Knockback (knockback)",2,"Increases knockback dealt (enemies repel backwards)",19, melee_keys],
                    ["Looting (looting)",3,"Increases amount of loot dropped when mob is killed",21, melee_keys],
                    ["Luck of the Sea (luck_of_the_sea)",3,"Increases chances of catching valuable items",61, ["fishing"]],
                    ["Lure (lure)",3,"Increases the rate of fish biting your hook",62, ["fishing"]],
                    ["Mending (mending)",1,"Uses xp to mend your tools, weapons and armor",70, all_keys],
                    ["Power (power)",5,"Increases damage dealt by bow",48, ranged_keys],
                    ["Projectile Protection (projectile_protection)",4,"Reduces projectile damage (arrows, fireballs, fire charges)",4, armor_keys],
                    ["Protection (protection)",4,"General protection against attacks, fire, lava, and falling",0, armor_keys],
                    ["Punch (punch)",2,"Increases knockback dealt (enemies repel backwards)",49, ranged_keys],
                    ["Respiration (respiration)",3,"Extends underwater breathing (see better underwater)",5, armor_keys],
                    ["Sharpness (sharpness)",5,"Increases attack damage dealt to mobs",16, melee_keys],
                    ["Silk Touch (silk_touch)",1,"Mines blocks themselves (fragile items)",33, tools_keys],
                    ["Smite (smite)",3,"Increases attack damage against undead mobs",17, melee_keys],
                    ["Sweeping Edge (sweeping)",3,"Increases damage of sweep attack",22, melee_keys],
                    ["Thorns (thorns)",3,"Causes damage to attackers",7, armor_keys],
                    ["Unbreaking (unbreaking)",3,"Increases durability of item",34, all_keys]
        ]
        
        MOBTYPES = [
            "minecraft:blaze", "minecraft:cave_spider", "minecraft:creeper", "minecraft:enderman", "minecraft:endermite", "minecraft:evocation_fangs", "minecraft:evocation_illager", "minecraft:falling_block", "minecraft:husk", "minecraft:illusion_illager", "minecraft:lightning_bolt", "minecraft:magma_cube", "minecraft:shulker", "minecraft:silverfish", "minecraft:skeleton", "minecraft:spider", "minecraft:stray", "minecraft:vindication_illager", "minecraft:witch", "minecraft:wither_skeleton", "minecraft:zombie", "minecraft:zombie_villager"
        ]
        
        ENTITIES = [
            "minecraft:area_effect_cloud", "minecraft:armor_stand", "minecraft:arrow", "minecraft:bat", "minecraft:boat", "minecraft:chest_minecart", "minecraft:chicken", "minecraft:commandblock_minecart", "minecraft:cow", "minecraft:donkey", "minecraft:dragon_fireball", "minecraft:egg", "minecraft:elder_guardian", "minecraft:ender_crystal", "minecraft:ender_dragon", "minecraft:ender_pearl", "minecraft:eye_of_ender_signal", "minecraft:fireball", "minecraft:fireworks_rocket", "minecraft:furnace_minecart", "minecraft:ghast", "minecraft:giant", "minecraft:guardian", "minecraft:hopper_minecart", "minecraft:horse", "minecraft:item", "minecraft:item_frame", "minecraft:leash_knot", "minecraft:llama", "minecraft:llama_spit",  "minecraft:minecart", "minecraft:mooshroom", "minecraft:mule", "minecraft:ocelot", "minecraft:painting", "minecraft:parrot", "minecraft:pig", "minecraft:polar_bear", "minecraft:potion", "minecraft:rabbit", "minecraft:sheep", "minecraft:shulker_bullet", "minecraft:skeleton_horse", "minecraft:slime", "minecraft:small_fireball", "minecraft:snowball", "minecraft:snowman", "minecraft:spawner_minecart", "minecraft:spectral_arrow",  "minecraft:squid", "minecraft:tnt", "minecraft:tnt_minecart", "minecraft:vex", "minecraft:villager", "minecraft:villager_golem", "minecraft:wither", "minecraft:wither_skull", "minecraft:wolf", "minecraft:xp_bottle", "minecraft:xp_orb", "minecraft:zombie_horse", "minecraft:zombie_pigman",
        ]
        
        # items
        THINGS = ['leather', 'carrot', 'beetroot', 'iron_helmet', 'iron_boots', 'iron_leggings', 'leather_leggings', 'leather_helmet', 'leather_boots', 'clock', 'compass', 'golden_shovel', 'diamond_shovel', 'wooden_shovel', 'stone_shovel', 'iron_shovel', 'flint_and_steel', 'shears', 'golden_chestplate', 'diamond_chestplate', 'chainmail_chestplate', 'iron_chestplate', 'leather_chestplate', 'rotten_flesh', 'bone', 'dye', 'stone', 'grass', 'dirt', 'cobblestone', 'planks', 'sapling', 'sand', 'gravel', 'log', 'leaves', 'glass', 'sandstone', 'deadbush', 'wool', 'yellow_flower', 'red_flower', 'brown_mushroom', 'red_mushroom', 'cactus', 'clay', 'reeds', 'wooden_slab', 'carrots', 'potatoes', 'carpet', 'stick', 'string', 'feather', 'wooden_hoe', 'wheat_seeds', 'leather_boots', 'flint', 'fish', 'cookie', 'pumpkin_seeds', 'melon_seeds', 'rotten_flesh', 'carrot', 'potato', 'poisonous_potato', 'iron_ore', 'coal_ore', 'sponge', 'lapis_ore', 'stone_slab', 'mossy_cobblestone', 'torch', 'oak_stairs', 'redstone_wire', 'wheat', 'ladder', 'stone_stairs', 'wall_sign', 'wooden_pressure_plate', 'stone_button', 'snow', 'fence', 'pumpkin', 'stonebrick', 'melon_block', 'vine', 'waterlily', 'cocoa', 'wooden_button', 'wooden_sword', 'wooden_shovel', 'wooden_pickaxe', 'wooden_axe', 'stone_sword', 'stone_shovel', 'stone_pickaxe', 'stone_axe', 'bowl', 'gunpowder', 'stone_hoe', 'wheat', 'leather_helmet', 'leather_chestplate', 'leather_leggings', 'porkchop', 'sign', 'wooden_door', 'cooked_fished', 'dye', 'bone', 'sugar', 'beef', 'chicken', 'glass_bottle', 'spider_eye', 'experience_bottle', 'writable_book', 'flower_pot', 'baked_potato', 'map', 'name_tag', 'gold_ore', 'lapis_block', 'dispenser', 'golden_rail', 'detector_rail', 'sticky_piston', 'piston', 'brick_block', 'chest', 'diamond_ore', 'furnace', 'rail', 'lever', 'stone_pressure_plate', 'redstone_ore', 'redstone_torch', 'trapdoor', 'iron_bars', 'glass_pane', 'fence_gate', 'brick_stairs', 'stone_brick_stairs', 'sandstone_stairs', 'emerald_ore', 'tripwire_hook', 'tripwire', 'spruce_stairs', 'birch_stairs', 'jungle_stairs', 'cobblestone_wall', 'flower_pot', 'light_weighted_pressure_plate', 'heavy_weighted_pressure_plate', 'redstone_block', 'quartz_ore', 'quartz_block', 'quartz_stairs', 'activator_rail', 'dropper', 'stained_hardened_clay', 'hay_block', 'hardened_clay', 'coal_block', 'packed_ice', 'iron_shovel', 'iron_pickaxe', 'iron_axe', 'flint_and_steel', 'apple', 'bow', 'arrow', 'coal', 'iron_ingot', 'gold_ingot', 'iron_hoe', 'bread', 'cooked_porkchop', 'bucket', 'redstone', 'snowball', 'boat', 'leather', 'milk_bucket', 'brick', 'clay_ball', 'reeds', 'paper', 'book', 'slime_ball', 'chest_minecart', 'furnace_minecart', 'egg', 'compass', 'fishing_rod', 'clock', 'glowstone_dust', 'shears', 'melon', 'cooked_beef', 'cooked_chicken', 'fire_charge', 'pumpkin_pie', 'fireworks', 'firework_charge', 'quartz', 'lead', 'noteblock', 'bed', 'gold_block', 'iron_block', 'tnt', 'bookshelf', 'obsidian', 'diamond_block', 'crafting_table', 'wooden_door', 'iron_door', 'ice', 'jukebox', 'netherrack', 'soul_sand', 'glowstone', 'cake', 'unpowered_repeater', 'brown_mushroom_block', 'red_mushroom_block', 'mycelium', 'nether_brick', 'nether_brick_fence', 'nether_brick_stairs', 'nether_wart', 'enchanting_table', 'brewing_stand', 'cauldron', 'end_stone', 'redstone_lamp', 'ender_chest', 'emerald_block', 'skull', 'anvil', 'trapped_chest', 'powered_comparator', 'daylight_detector', 'hopper', 'diamond', 'iron_sword', 'diamond_sword', 'diamond_shovel', 'diamond_pickaxe', 'diamond_axe', 'mushroom_stew', 'golden_sword', 'golden_shovel', 'golden_pickaxe', 'golden_axe', 'diamond_hoe', 'golden_hoe', 'chainmail_helmet', 'chainmail_chestplate', 'chainmail_leggings', 'chainmail_boots', 'iron_helmet', 'iron_chestplate', 'iron_leggings', 'iron_boots', 'diamond_helmet', 'diamond_chestplate', 'diamond_leggings', 'diamond_boots', 'golden_helmet', 'golden_chestplate', 'golden_leggings', 'golden_boots', 'painting', 'golden_apple', 'water_bucket', 'lava_bucket', 'minecart', 'saddle', 'iron_door', 'cake', 'bed', 'repeater', 'filled_map', 'ender_pearl', 'blaze_rod', 'ghast_tear', 'gold_nugget', 'nether_wart', 'potion', 'fermented_spider_eye', 'blaze_powder', 'magma_cream', 'brewing_stand', 'cauldron', 'ender_eye', 'speckled_melon', 'emerald', 'item_frame', 'golden_carrot', 'skull', 'carrot_on_a_stick', 'nether_star', 'comparator', 'netherbrick', 'tnt_minecart', 'hopper_minecart', 'iron_horse_armor', 'golden_horse_armor', 'diamond_horse_armor', 'record_13', 'record_cat', 'record_blocks', 'record_chirp', 'record_far', 'record_mall', 'record_mellohi', 'record_stal', 'record_strad', 'record_ward', 'record_11', 'record_wait']
        
        # ids
        air = [0]
        liquids = [8, 9, 10, 11]
        plants = [31, 175, 6, 37, 38, 106]
        torches = [50, 75, 76]
        crops = [59, 83, 104, 105, 142, 141]
        
        
        # palettes
        stones_for_building = [(1,0), (1,6), (98,0), (4,0)]
        stones_for_building_decoration = [(1,1), (1,2), (1,3), (1,4)]
        air_for_building = [(0, 0)]
        trapdoors_for_building = [(96,0), (96,1), (96,2), (96,3), (96,0)]
        
        def combine(arrays):
            result = []
            for a in arrays:
                for e in a:
                    result.append(e)
            return result
        
        navigable = combine( [air, liquids, plants, torches, crops] )
        
        def __init__( self ):
            pass
    
    def __init__( self, level, box ):
        self.level = level
        self.name = "The Vaults"
        self.box = box
        self.width, self.height, self.depth = self.get_build_area()
        self.materials = self.Materials()
        self.time = Time()
        self.buildings = []
        self.lore = self.Lore(self)
    
    def next_day(self):
        self.time.next_day()
    
    def get_time( self ):
        return self.time.to_string()
    
    def get_build_area( self ):  #  It's a GDMC thing!
        box = self.box
        width = box.maxx - box.minx
        height = box.maxy - box.miny
        depth = box.maxz - box.minz
        return ( width, height, depth )

    def get_centre_build_area( self ):
        box = self.box
        cx = (box.maxx + box.minx)>>1
        cy = (box.maxy + box.miny)>>1
        cz = (box.maxz + box.minz)>>1
        return (cx, cy, cz)

    def check_for_intersection( self, A):
        result = []
        
        px = A.minx
        py = A.miny
        pz = A.minz
        pX = A.maxx
        pY = A.maxy
        pZ = A.maxz
        
        # Iterate through the listOfBoxes and return true if an intersection is found
        for box in self.buildings:
            x = box.minx
            y = box.miny
            z = box.minz
            X = box.maxx
            Y = box.maxy
            Z = box.maxz
            
            collide = True
            if px > X:
                collide = False
            elif pz > Z:
                collide = False
            elif pX < x:
                collide = False
            elif pZ < z:
                collide = False
            elif pY < y:
                collide = False
            elif py > Y:
                collide = False
            if collide == True:
                return True
        return False

    def get_height_here( self, pos, ignore ):
        '''
            Traverse the world in a column at x, z from y and return an integer height here
        '''
        if ignore == None:
            ignore = self.materials.navigable  #  Air and basic liquids
        
        x, y, z = pos
        while y > 0:  #  Assumes the minimum world height is 0
            block_id = self.level.blockAt(x, y, z)
            if block_id not in ignore:
                return y
            y -= 1

    def block_at( self, pos, no_cache):
        x, y, z = pos
        if (x, y, z) not in self.block_id_cache or no_cache == True:
            self.block_id_cache[(x, y, z)] = self.level.blockAt(x, y, z)
        return self.block_id_cache[(x, y, z)]

    def block_data_at( self, pos, nocache):
        map(int, pos)
        x, y, z = pos
        if (x, y, z) not in self.block_data_cache or no_cache == True:
            self.block_data_cache[(x, y, z)] = self.level.blockDataAt(x, y, z)
        return self.block_data_cache[(x, y, z)]

    def set_block_at( self, pos, material):
        map(int, pos)
        x, y, z = pos
        # check bounds - don't attempt to draw outside the selection box
        if self.box.minx <= x < self.box.maxx and self.box.miny <= y < self.box.maxy and self.box.minz <= z < self.box.maxz:
            if isinstance(material, tuple):
                material = [material]
            id, data = random.choice(material)
            self.level.setBlockAt(x, y, z, id)
            self.block_id_cache[(x, y, z)] = id
            self.level.setBlockDataAt(x, y, z, data)
            self.block_data_cache[(x, y, z)] = data

    def fill(self, box, material):
        for pos in box.positions:
            self.set_block_at( pos, material)


    def hemisphere(self, box, material):
        width = box.maxx-box.minx
        height = box.maxy-box.miny
        depth = box.maxz-box.minz
        hx = width>>1
        hy = height
        hz = depth>>1
        hx2 = hx*hx
        hy2 = hy*hy
        hz2 = hz*hz
        cx = (box.maxx+box.minx)>>1
        cy = (box.miny)
        cz = (box.maxz+box.minz)>>1
        for x, y, z in box.positions:
            dx = x-cx
            dxr = float(dx*dx)/float(hx2)
            dy = y-cy
            dyr = float(dy*dy)/float(hy2)
            dz = z-cz
            dzr = float(dz*dz)/float(hz2)
            d = dxr + dyr + dzr
            if d <= 1.0:
                self.set_block_at( (x, y, z), material)
    

    def sphere(self, box, material):
        width = box.maxx-box.minx
        height = box.maxy-box.miny
        depth = box.maxz-box.minz
        hx = width>>1
        hy = height>>1
        hz = depth>>1
        hx2 = hx*hx
        hy2 = hy*hy
        hz2 = hz*hz
        cx = (box.maxx+box.minx)>>1
        cy = (box.maxy+box.miny)>>1
        cz = (box.maxz+box.minz)>>1
        for x, y, z in box.positions:
            dx = x-cx
            dxr = float(dx*dx)/float(hx2)
            dy = y-cy
            dyr = float(dy*dy)/float(hy2)
            dz = z-cz
            dzr = float(dz*dz)/float(hz2)
            d = dxr + dyr + dzr
            if d <= 1.0:
                self.set_block_at( (x, y, z), material)
            
        
class Journal:
    def __init__(self):
        self.entries = []  #  A list of entries

    def log(self, msg):
        self.entries.append(msg)

    def print_out(self):
        for e in self.entries:
            log( "["+e+"]" )


class SpaceRecorder:
    tile_entities = [146, 54, 52, 63, 68]

    def __init__(self):
        self.THESTOREDSHAPE = None

    def decode(self, encoded):
        result = base64.b64decode(encoded)
        result = array.array('B', result)
        original = []
        pos = 0
        while pos < len(result):
            x = int(result[pos])
            y = int(result[pos+1])
            z = int(result[pos+2])
            original.append((x, y, z))
            pos += 3
        self.THESTOREDSHAPE = original
        return original
        
    def encode(self):
        result = []
        for x,y,z in self.THESTOREDSHAPE:
            result.append(chr(int(x)))  #  0 <= x <= 255
            result.append(chr(int(y)))
            result.append(chr(int(z)))
        result = bytearray(result)  #  Re-cast
        return base64.b64encode(result)        

    def set_block(self, level, size, id, data, idx, origin, layout):
        width, height, depth = size
        ox, oy, oz = origin
        
        item = None
        
        # Some translations for variety
        if ((id == 50 or id == 169) and random.randint(1,10) > 3):  #  Throw away some torches or sea lanterns, raplace with air
            id = 0
            data = 0
        if id == 98 and data == 0 and random.randint(1,100) == 99:
            id = 14  #  Sometimes... Gold ore!

        px = None
        py = None
        pz = None
            
        # The builders go here    
        if layout == (3, 2, 1):
            num_blocks_layer = depth*width
            layer = int(idx/num_blocks_layer)
            column = int((idx-(layer*num_blocks_layer))/width)
            row = idx-(layer*num_blocks_layer)-(column*width)
            if layer < height and column < depth and row < width:
                px = ox+row
                py = oy+layer
                pz = oz+column
                
                level.setBlockAt(px, py, pz, id)
                level.setBlockDataAt(px, py, pz, data)

        elif layout == (2, 1, 3):
            num_blocks_layer = width*height
            layer = int(idx/num_blocks_layer)
            column = int((idx-(layer*num_blocks_layer))/height)
            row = idx-(layer*num_blocks_layer)-(column*height)    
            if layer < depth and column < width and row < height:
                px = ox+column
                py = oy+row
                pz = oz+layer
                level.setBlockAt(px, py, pz, id)
                level.setBlockDataAt(px, py, pz, data)        

        elif layout == (1, 3, 2):
            num_blocks_layer = height*depth
            layer = int(idx/num_blocks_layer)
            column = int((idx-(layer*num_blocks_layer))/depth)
            row = idx-(layer*num_blocks_layer)-(column*depth)    
            if layer < width and column < height and row < depth:
                px = ox+layer
                py = oy+column
                pz = oz+row
                level.setBlockAt(px, py, pz, id)
                level.setBlockDataAt(px, py, pz, data)

        else:
            print "Position "+str((row, layer, column))+" is outside size: "+str((width, height, depth))

        
        if id in self.tile_entities and px != None and py != None and pz != None:  #  Chests and Monster Spawners need nbt set up later
            item = [px, py, pz, id, data]

        return item

    def space_replay_centred(self, level, box):
        size = width, height, depth = self.THESTOREDSHAPE[0]  #  This version can render any size object
        origin = ox, oy, oz = box.minx, box.miny, box.minz
        cx = (box.minx + box.maxx)>>1
        cz = (box.minz + box.maxz)>>1
        origin = cx-(width>>1), oy, cz-(depth>>1)

        idx = 0
        x = 0
        y = 0
        z = 0
        
        items = []
        
        if size == self.THESTOREDSHAPE[0]:
            layout = self.THESTOREDSHAPE[1]
            for id, data, count in self.THESTOREDSHAPE:
                # print idx, count
                if idx > 1: 
                    for c in xrange(0, count):
                        item = self.set_block(level, size, id, data, idx-2, origin, layout)
                        if item != None:
                            items.append(item)
                        idx += 1  #  Next position
                else:
                    idx += 1  #  Skip the zeroth and 1st element, we checked it before coming in here
                    
            
        else:
            print "Warning: Dimensions don't match!"
        # print "Replayed space of size "+str((width, height, depth))
        return items


    def space_replay(self, level, box):
        size = width, height, depth = self.THESTOREDSHAPE[0]  #  This version can render any size object
        origin = box.minx, box.miny, box.minz

        
        idx = 0
        x = 0
        y = 0
        z = 0
        
        items = []
        
        if size == self.THESTOREDSHAPE[0]:
            layout = self.THESTOREDSHAPE[1]
            for id, data, count in self.THESTOREDSHAPE:
                # print idx, count
                if idx > 1: 
                    for c in xrange(0, count):
                        item = self.set_block(level, size, id, data, idx-2, origin, layout)
                        if item != None:
                            items.append(item)

                        idx += 1  #  Next position
                else:
                    idx += 1  #  Skip the zeroth and 1st element, we checked it before coming in here
                    
            
        else:
            print "Dimensions don't match!"
        # print "Replayed space of size "+str((width, height, depth))
        return items


    def space_replay_enforce_shape(self, level, box):
        size = width, height, depth = (box.maxx-box.minx, box.maxy-box.miny, box.maxz-box.minz)
        origin = box.minx, box.miny, box.minz
        idx = 0
        x = 0
        y = 0
        z = 0
        
        if size == self.THESTOREDSHAPE[0]:
            layout = self.THESTOREDSHAPE[1]
            for id, data, count in self.THESTOREDSHAPE:
                # print idx, count
                if idx > 1: 
                    for c in xrange(0, count):
                        self.set_block(level, size, id, data, idx-2, origin, layout)
                        idx += 1  #  Next position
                else:
                    idx += 1  #  Skip the zeroth and 1st element, we checked it before coming in here
                    
            
        else:
            print "Dimensions don't match!"
        print "Replayed space of size "+str((width, height, depth))
        
    def space_record(self, level, box):

        width, height, depth = (box.maxx-box.minx, box.maxy-box.miny, box.maxz-box.minz)

        consecutive_count = 1
        record_yzx = []
        previous = None
        record_yzx.append((width, height, depth))
        record_yzx.append((3, 2, 1))
        for y in xrange(box.miny, box.maxy):  #  For each layer
            for z in xrange(box.minz, box.maxz):  #  For each depth-wise slice
                for x in xrange(box.minx, box.maxx):  #  For each row
                    current = [level.blockAt(x, y, z), level.blockDataAt(x, y, z)]
                    if previous is not None:
                        if current == previous:  # Same - run length count it
                            consecutive_count += 1  #  Bump counter
                        if current != previous or (y == box.maxy-1 and z == box.maxz-1 and x == box.maxx-1):  #  Append on difference, or final area
                            record_yzx.append((previous[0], previous[1], consecutive_count))  #  Record where we were up to
                            consecutive_count = 1  #  Reset counter
                    previous = current
                    
        consecutive_count = 1
        record_zxy = []
        previous = None
        record_zxy.append((width, height, depth))
        record_zxy.append((2, 1, 3))
        for z in xrange(box.minz, box.maxz):  #  For each depth-wise slice
            for x in xrange(box.minx, box.maxx):  #  For each row
                for y in xrange(box.miny, box.maxy):  #  For each layer
                    current = [level.blockAt(x, y, z), level.blockDataAt(x, y, z)]
                    if previous is not None:
                        if current == previous:  # Same - run length count it
                            consecutive_count += 1  #  Bump counter
                        if current != previous or (y == box.maxy-1 and z == box.maxz-1 and x == box.maxx-1):  #  Append on difference, or final area
                            record_zxy.append((previous[0], previous[1], consecutive_count))  #  Record where we were up to
                            consecutive_count = 1  #  Reset counter
                    previous = current

        consecutive_count = 1
        record_xyz = []
        previous = None
        record_xyz.append((width, height, depth))
        record_xyz.append((1, 3, 2))
        for x in xrange(box.minx, box.maxx):  #  For each row
            for y in xrange(box.miny, box.maxy):  #  For each layer
                for z in xrange(box.minz, box.maxz):  #  For each depth-wise slice
                    current = [level.blockAt(x, y, z), level.blockDataAt(x, y, z)]
                    if previous is not None:
                        if current == previous:  # Same - run length count it
                            consecutive_count += 1  #  Bump counter
                        if current != previous or (y == box.maxy-1 and z == box.maxz-1 and x == box.maxx-1):  #  Append on difference, or final area
                            record_xyz.append((previous[0], previous[1], consecutive_count))  #  Record where we were up to
                            consecutive_count = 1  #  Reset counter
                    previous = current

        print len(record_yzx), len(record_zxy), len(record_xyz)
        self.THESTOREDSHAPE = record_yzx
        if len(record_zxy) < len(THESTOREDSHAPE):
            self.THESTOREDSHAPE = record_zxy
        if len(record_xyz) < len(THESTOREDSHAPE):
            self.THESTOREDSHAPE = record_xyz
        print "Records space of size "+str((width, height, depth))


class Building:

    trap = [
        
    ]

    room_of_instruction = [
    "CA0IAwIBYgATAAACYgAFAAAEYgAEAAAEYgAFAAACYgAWbQICYgAEAgABYgAEAgABYgAEAAACYgADbQABYgABAAAEYgABbQEBbQABYgABAAAEYgABbQEBYgADAAACYgAEAgABYgAEAgABYgAEbQMCYgADAAAJrwUBEgYBbQICEg4BrwQBAAACEgYBYgAEEg4BAAACbQABYgACDgABYgABbQEBAAACbQABYgAEbQEBAAABEgYCYgAEEgYBAAACrwQBEg4BbQMCEg4BrwEBAAADEgYBAAACEg4BAAALrwoBEgYBAAACEg4BrwoBAAADYgABAAACYgABAAANNgIBAAAFEgYBYgABAAACYgABEgYBAAACrwoBEg4BAAACEg4BrwoBAAAbYgABRAUBAAABYgABAAAHRAMBAAAERAIBAAAHYgABAAABRAQBYgABAAAkYgABMgEBAAABYgABEgYBAAADMgMBAAAKMgQBAAAEYgABAAABMgIBYgABAAAcEgYBAAACEgYBAAAEYgABAAACYgABEg4BAAAEEgYBAAANEgYBYgABAAACYgABAAAHEg4BAAAUEg4CAAABEg4BAAADEg4BYgABbQUBbQQBYgABEg4BAAADbQcBEg4BAAABbQcBAAAEbQYBAAACbQYBAAADEg4BYgABbQUBbQQBYgABEg4BAAADEg4EAAAcYgABEg4CYgABAAAEEg4CAAABEg4BAAAEEg4BAAACEg4BAAAEYgABEg4CYgABAAAFEg4BAAAeYgABAAACYgABAAAEEg4BAAAPYgABEg4BAAABYgABAADS"
    ]

    room_of_up = [
    "EAgQAQMCYgAXAAACYgAOAAACYgAOAAACYgBZAAAMYgAEAAAMYgAEAAAMYgAUAAAMYgAEAAAMYgAjAAACYgABAAABYgACAAACYgACAAABYgABAAACYgACAAACYgABAAABYgACAAACYgACAAABYgABAAACYgACAAACYgABAAABYgACAAACYgACAAABYgABAAACYgASAAACYgABAAABYgACAAACYgACAAABYgABAAACYgACAAACYgABAAABYgACAAACYgACAAABYgABAAACYgAiAAABYgADAAABYgABAAACYgABAAABYgADAAABYgACAAABYgADAAABYgABAAACYgABAAABYgADAAABYgACAAABYgADAAABYgABAAACYgABAAABYgADAAABYgASAAABYgADAAABYgABAAACYgABAAABYgADAAABYgACAAABYgADAAABYgABAAACYgABAAABYgADAAABYgAiAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgASAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgAiAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgASAAABYgABAAADYgAEAAADYgABAAABYgACAAABYgABAAADYgAEAAADYgABAAABYgAiAAABYgACAAACLAMBYgADAAACYgACAAABYgACAAABYgACAAAELAMBYgABAAACYgACAAABYgACAAABYgACAAAIYgACAAABYgAHAAAEYgAHAAABYgACAAABYgABAAAEYgABAAABYgACAAABYgACAAABYgACAAABYgABAAAEYgABAAABYgACAAABYgAHLAMBYgAZAAAHYgADAAANYgADAAANYgACLAMBAAAGYgAGAAABYgACAAABYgAHAAAEYgABAAABYgACAAABYgABAAAEYgACAAAEYgAEAAABYgABAAAEYgAHAAABYgAZAAAHYgADAAANYgADAAANYgADAAAGYgAGAAABYgACAAABYgAHAAAEYgAEAAABYgABAAAEYgACAAAEYgABLAMBYgACAAABYgABAAAEYgAHAAABYgAaAAABYgACAAADYgADAAACYgACAAABYgACAAABYgACAAADYgADAAACYgACAAABYgACAAABYgACAAADYgADAAACYgACAAABYgAKLAMBYgAHAAABYgACAAABYgACLAMBAAAEYgACAAABYgACAAABYgACAAABYgABAAAGYgACAAABYgAHAAADbQYBYgAXAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgASAAABYgABAAADYgAEAAADYgABAAABYgACAAABYgABAAADYgAEAAADYgABAAABYgAiAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgASAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgAiAAABYgADAAABYgABAAACYgABAAABYgADAAABYgACAAABYgADAAABYgABAAACYgABAAABYgADAAABYgACAAABYgADAAABYgABAAACYgABAAABYgADAAABYgASAAABYgADAAABYgABAAACYgABAAABYgADAAABYgACAAABYgADAAABYgABAAACYgABAAABYgADAAABYgAiAAACYgABAAABYgACAAACYgACAAABYgABAAACYgACAAACYgABAAABYgACAAACYgACAAABYgABAAACYgACAAACYgABAAABYgACAAACYgACAAABYgABAAACYgASAAACYgABAAABYgACAAACYgACAAABYgABAAACYgACAAACYgABAAABYgACAAACYgACAAABYgABAAACYgATAAACYgAOAAAMYgAEAAAMYgAEAAAMYgAUAAAMYgAEAAAMYgApAAACYgAOAAACYgAOAAACYgBH"
    ]
    
    detail_son_of_up = [ "BAQEAwIBAAAILAMBAAADYgADbQYBAAANLAMBYgACAAAPLAMBAAAQ" ]

    room_of_intersection = ["EAgQAgEDYgA5wQMBwQgBBQUBYgAFwQMBwQkBBQUBYgBNiwADAAADYgACiwABAAABiwAEYgACiwADAAADYgAKAAAGBQUBYgABAAAGLA0BYgABAAAGLA0BYgABAAAGBQUBYgAJiwADAAADYgACiwABAAABiwAEYgACiwADAAADYgAaiwADAAADYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgACiwACMgUBAAADBQUBfggBAAAGLA0BfgkBAAAGLA0BYgABiwACMgUBAAADBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwADAAADYgASiwABAAABiwAEYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgABAAAHBQUBfgkBAAAGLA0BfggBAAAGLA0BAAAHBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwABAAABiwAEYgASiwADAAADYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgABZQACvwABZQAEBQUBfQABAAAGLA0BfQABAAAGLA0BZQAFvwABZQABBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwADAAADYgASAAAGYgABAAAHYgABAAAHYgABAAAHYgABAAAHYgABAAAHBQUBfgABAAAGLA0BfgABAAAGLA0BAAAHBQUBAAAHYgABAAAHYgABAAAHYgABAAAHYgAaAAAGBQUBYgABiwACMgUBAAADBQUBAAAHBQUBAAAHBQUBAAAHBQUBZQAFvwABZQABBQUBfgABAAAGLA0BfgEBAAAGLA0BZQAGvwABBQUBAAAHBQUBAAAHBQUBAAAHBQUBYgABiwACMgUBAAADBQUBYgABAAAGBQUBYgAJwQYBwQkBBQUBYgAFAAAGLA0BYgABNQABAAAFLA0BAAABNQUBNQABAAAELA0BAAACNQUBAAAELA0BAAACfggBfgABAAADLA0BAAADfQABAAADLA0BfgABAAACfgkBAAADLA0BfgABAAACfggBAAADLA0BAAADfQABAAADLA0BAAADfgABAAADLA0BAAACNQQBfgABAAADLA0BAAABNQQBNQEBAAAELA0BYgABNQEBAAAFLA0BYgABAAAGLA0BYgABwQABwQgBBQUBYgAFwQIBwQgBBQUBYgAFAAAGLA0BYgABNQABAAAFLA0BAAABNQUBNQABAAAELA0BAAACNQUBAAAELA0BAAACfggBfgEBAAADLA0BAAADfQABAAADLA0BfgABAAACfggBAAADLA0BfgABAAACfggBAAADLA0BAAADfQABAAADLA0BAAADfgEBAAADLA0BAAACNQQBfgABAAADLA0BAAABNQQBNQEBAAAELA0BYgABNQEBAAAFLA0BYgABAAAGLA0BYgABwQABwQkBBQUBYgANAAAGBQUBYgABiwACMgUBAAADBQUBAAAHBQUBAAAHBQUBAAAHBQUBZQAEvwABZQACBQUBfgEBAAAGLA0BfgABAAAGLA0BZQAFvwABZQABBQUBAAAHBQUBAAAHBQUBAAAHBQUBYgABiwACMgUBAAADBQUBYgABAAAGBQUBYgARAAAGYgABAAAHYgABAAAHYgABAAAHYgABAAAHYgABAAAHBQUBfgABAAAGLA0BfgABAAAGLA0BAAAHBQUBAAAHYgABAAAHYgABAAAHYgABAAAHYgAaiwADAAADYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgABZQACvwABZQACvwABZQABBQUBfQABAAAGLA0BfQABAAAGLA0BZQAEvwABZQACBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwADAAADYgASiwABAAABiwAEYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgABAAAHBQUBfggBAAAGLA0BfgkBAAAGLA0BAAAHBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwABAAABiwAEYgASiwADAAADYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgACiwACMgUBAAADBQUBfggBAAAGLA0BfggBAAAGLA0BYgABiwACMgUBAAADBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwADAAADYgAaiwADAAADYgACiwABAAABiwAEYgACiwADAAADYgAKAAAGBQUBYgABAAAGLA0BYgABAAAGLA0BYgABAAAGBQUBYgAJiwADAAADYgACiwABAAABiwAEYgACiwADAAADYgBKwQEBwQkBBQUBYgAFwQEBwQgBBQUBYgA8",
    
    "EAgQAgEDYgA5wQMBwQgBBQUBYgAFwQMBwQkBBQUBYgBNiwADAAADYgACiwABAAABiwAEYgACiwADAAADYgAKAAAGBQUBYgABAAAGLA0BYgABAAAGLA0BYgABAAAGBQUBYgAJiwADAAADYgACiwABAAABiwAEYgACiwADAAADYgAaiwADAAADYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgACiwACMgUBAAADBQUBAAAHLA0BAAAHLA0BYgABiwACMgUBAAADBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwADAAADYgASiwABAAABiwAEYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgABAAAHBQUBAAAHLA0BAAAHLA0BAAAHBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwABAAABiwAEYgASiwADAAADYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgABZQACvwABZQAEBQUBAAAHLA0BAAAHLA0BZQAFvwABZQABBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwADAAADYgASAAAGYgABAAAHYgABAAAHYgABAAAHYgABAAAHYgABAAAHBQUBAAAHLA0BAAAHLA0BAAAHBQUBAAAHYgABAAAHYgABAAAHYgABAAAHYgAaAAAGBQUBYgABiwACMgUBAAADBQUBAAAHBQUBAAAHBQUBAAAHBQUBAAADZQACvwABZQABBQUBAAAHLA0BAAAHLA0BAAADZQADvwABBQUBAAAHBQUBAAAHBQUBAAAHBQUBYgABiwACMgUBAAADBQUBYgABAAAGBQUBYgAJwQIBwQkBBQUBYgAFAAAGLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BYgABAAAGLA0BYgABwQABwQgBBQUBYgAFwQIBwQgBBQUBYgAFAAAGLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BAAAHLA0BYgABAAAGLA0BYgABwQABwQkBBQUBYgANAAAGBQUBYgABiwACMgUBAAADBQUBAAAHBQUBAAAHBQUBAAAHBQUBAAADZQABvwABZQACBQUBAAAHLA0BAAAHLA0BAAADZQACvwABZQABBQUBAAAHBQUBAAAHBQUBAAAHBQUBYgABiwACMgUBAAADBQUBYgABAAAGBQUBYgARAAAGYgABAAAHYgABAAAHYgABAAAHYgABAAAHYgABAAAHBQUBAAAHLA0BAAAHLA0BAAAHBQUBAAAHYgABAAAHYgABAAAHYgABAAAHYgAaiwADAAADYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgABZQACvwABZQACvwABZQABBQUBAAAHLA0BAAAHLA0BZQAEvwABZQACBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwADAAADYgASiwABAAABiwAEYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgABAAAHBQUBAAAHLA0BAAAHLA0BAAAHBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwABAAABiwAEYgASiwADAAADYgABAAAHLA0BAAAHLA0BAAAHLA0BAAAHYgACiwACMgUBAAADBQUBAAAHLA0BAAAHLA0BYgABiwACMgUBAAADBQUBAAAHYgABAAAHLA0BAAAHLA0BAAAHLA0BYgABiwADAAADYgAaiwADAAADYgACiwABAAABiwAEYgACiwADAAADYgAKAAAGBQUBYgABAAAGLA0BYgABAAAGLA0BYgABAAAGBQUBYgAJiwADAAADYgACiwABAAABiwAEYgACiwADAAADYgBKwQEBwQkBBQUBYgAFwQEBwQgBBQUBYgA8"
    ]

    room_of_general_purpose = [
    # Simple and weighted repeating
    
    "EAgQAQMCYgAXAAACYgAOAAACYgAObQcBbQYBYgBdAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAqAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAnAAAKYgAGAAAKYgAGAAAKYgAGAAAKYgAGAAAKYgAGAAAKYgAlAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAkAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAjAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgAhAAAvbQUBYgABAAAOYgACAAAOYgACAAAOYgAhAAAvbQQBYgABAAAOYgACAAAOYgACAAAOYgAiAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgAjAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAkAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAlAAAKYgAGAAAKYgAGAAAKYgAGAAAKYgAGAAAKYgAGAAAKYgAnAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAqAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAtAAACYgAOAAACYgAObQcBbQYBYgBH",
    "EAgQAQMCYgAXAAACYgAOAAACYgAObQcBbQYBYgBdAAAEYgAMAAAEYgANAAACYgANAAAEYgAMAAAEYgAMAAAEYgAqAAAIYgAIAAAIYgAIAAACYgABAAACYgABAAACYgAIAAAIYgAIAAAIYgAIAAACYgAEAAACYgAnAAADYgABAAACYgABAAADYgAGAAADYgABAAACYgABAAADYgAHbQcBbQYBYgABbQcBbQYBYgABbQcBbQYBYgAHAAADYgABAAACYgABAAADYgAHbQcBbQYBYgABbQcBbQYBYgABbQcBbQYBYgALbQcBbQYBYgApAAAMYgAEAAAMYgAEAAABbQUBAAAIbQUBAAABYgAEAAAMYgAEAAABbQUBAAAIbQUBAAABYgAEAAABYgABAAAIYgABAAABYgAkAAAMYgAEAAAMYgAEAAABbQQBAAAIbQQBAAABYgAEAAAMYgAEAAABbQQBAAAIbQQBAAABYgAEAAABYgABAAAIYgABAAABYgAjAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgAFAAAIYgAFAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgACAAABYgACAAAIYgACAAABYgAhAAAjbQUBAAAIbQUBAAACbQUBYgABAAAOYgACAAACbQUBAAAIbQUBAAACYgACAAABYgABbQUBAAAIbQUBYgABAAABYgAhAAAjbQQBAAAIbQQBAAACbQQBYgABAAAOYgACAAACbQQBAAAIbQQBAAACYgACAAABYgABbQQBAAAIbQQBYgABAAABYgAiAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgAFAAAIYgAFAAACYgABAAAIYgABAAACYgACAAACYgABAAAIYgABAAACYgACAAABYgACAAAIYgACAAABYgAjAAAMYgAEAAAMYgAEAAABbQUBAAAIbQUBAAABYgAEAAAMYgAEAAABbQUBAAAIbQUBAAABYgAEAAABYgABAAAIYgABAAABYgAkAAAMYgAEAAAMYgAEAAABbQQBAAAIbQQBAAABYgAEAAAMYgAEAAABbQQBAAAIbQQBAAABYgAEAAABYgABAAAIYgABAAABYgAlAAADYgABAAACYgABAAADYgAGAAADYgABAAACYgABAAADYgAHbQcBbQYBYgABbQcBbQYBYgABbQcBbQYBYgAHAAADYgABAAACYgABAAADYgAHbQcBbQYBYgABbQcBbQYBYgABbQcBbQYBYgALbQcBbQYBYgArAAAIYgAIAAAIYgAIAAACYgABAAACYgABAAACYgAIAAAIYgAIAAAIYgAIAAACYgAEAAACYgAqAAAEYgAMAAAEYgANAAACYgANAAAEYgAMAAAEYgAMAAAEYgAtAAACYgAOAAACYgAObQcBbQYBYgBH",
    "EAgQAQMCYgARAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgACAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgBhAAAGiwABAAACiwABAAAMiwABAAACiwABAAAGYgABAAAFiwABAAACiwABAAAFYgACAAAFYgAEAAAFYgACAAAFiwABAAACiwABAAAFYgACAAAFiwABAAACiwABAAAFYgAiAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABiwABAAAKiwABAAABYgACAAABiwABAAAKiwABAAABYgACAAABYgABAAAKYgABAAABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiiwABAAAMiwABYgACiwABAAAMiwABYgACiwABAAAMiwABYgADAAAMYgADiwABAAAMiwABYgACiwABAAAMiwABYgAhAAAgYgABAAAOYgADAAAMYgADAAAOYgACAAAOYgAhAAAgYgABAAAOYgADAAAMYgADAAAOYgACAAAOYgAiiwABAAAMiwABYgACiwABAAAMiwABYgACiwABAAAMiwABYgADAAAMYgADiwABAAAMiwABYgACiwABAAAMiwABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABiwABAAAKiwABAAABYgACAAABiwABAAAKiwABAAABYgACAAABYgABAAAKYgABAAABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgAhAAAGiwABAAACiwABAAAMiwABAAACiwABAAAGYgABAAAFiwABAAACiwABAAAFYgACAAAFYgAEAAAFYgACAAAFiwABAAACiwABAAAFYgACAAAFiwABAAACiwABAAAFYgAiAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgACAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgBR",
    "EAgQAwIBYgARbQIBbQEBYgACbQIBbQEBYgACbQIBbQEBYgACbQIBbQEBYgACbQABbQMBYgACbQABbQMBYgACbQABbQMBYgACbQABbQMBYgAibQABbQIBYgACbQABbQIBYgACbQICYgACbQIBbQEBYgACbQMBbQEBYgACbQABLAUBYgACLAUBbQEBYgACbQABbQMBYgAibQABbQIBYgACbQABLAUBYgACLAUBbQEBYgACbQIBbQEBYgACbQMBbQEBYgACbQMCYgACbQMCYgACbQABbQMBYgAibQIBbQEBYgACbQABbQIBYgACbQABbQIBYgACbQABbQIBYgACbQABbQMBYgACbQMBbQEBYgACbQMBbQEBYgACbQMBbQEBYgARAAAzYgACAAAGYgACAAAGYgACAAAGYgACAAAqYgACAAAOYgACAAAqYgACAAAGYgACAAAGYgACAAAGYgACAABmbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAAAqbQYBbQUBAAAObQQBbQcBAAAqbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAABmbQABbQIBAAAGbQABbQIBAAAGbQMBbQEBAAAGbQMBbQEBAAAqbQABbQIBAAAObQMBbQEBAAAqbQABbQIBAAAGbQABbQIBAAAGbQMBbQEBAAAGbQMBbQEBAABmbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAAAqbQYBbQUBAAAObQQBbQcBAAAqbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAABWMgQCAAAGMgQCAAAFMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAFMgMCAAAGMgMCAAAKMgQCAAANMgIBYgACMgEBAAAMMgIBYgACMgEBAAANMgMCAAAKMgQCAAAGMgQCAAAFMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAFMgMCAAAGMgMCAABGbQYCAAAGbQYCAAAFbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAFbQcCAAAGbQcCAAAKbQYCAAANbQQBYgACbQUBAAAMbQQBYgACbQUBAAANbQcCAAAKbQYCAAAGbQYCAAAFbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAFbQcCAAAGbQcCAAAjYgARLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAiLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAiLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAiLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAR",
    
    "EAgQAQMCYgARAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgACAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgBhAAAGiwABAAACiwABAAAMiwABAAACiwABAAAGYgABAAAFiwABAAACiwABAAAFYgACAAAFYgAEAAAFYgACAAAFiwABAAACiwABAAAFYgACAAAFiwABAAACiwABAAAFYgAiAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABiwABAAAKiwABAAABYgACAAABiwABAAAKiwABAAABYgACAAABYgABAAAKYgABAAABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiiwABAAAMiwABYgACiwABAAAMiwABYgACiwABAAAMiwABYgADAAAMYgADiwABAAAMiwABYgACiwABAAAMiwABYgAhAAAgYgABAAAOYgADAAAMYgADAAAOYgACAAAOYgAhAAAgYgABAAAOYgADAAAMYgADAAAOYgACAAAOYgAiiwABAAAMiwABYgACiwABAAAMiwABYgACiwABAAAMiwABYgADAAAMYgADiwABAAAMiwABYgACiwABAAAMiwABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABiwABAAAKiwABAAABYgACAAABiwABAAAKiwABAAABYgACAAABYgABAAAKYgABAAABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgAhAAAGiwABAAACiwABAAAMiwABAAACiwABAAAGYgABAAAFiwABAAACiwABAAAFYgACAAAFYgAEAAAFYgACAAAFiwABAAACiwABAAAFYgACAAAFiwABAAACiwABAAAFYgAiAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgACAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgBR",
    "EAgQAwIBYgARbQIBbQEBYgACbQIBbQEBYgACbQIBbQEBYgACbQIBbQEBYgACbQABbQMBYgACbQABbQMBYgACbQABbQMBYgACbQABbQMBYgAibQABbQIBYgACbQABbQIBYgACbQICYgACbQIBbQEBYgACbQMBbQEBYgACbQABLAUBYgACLAUBbQEBYgACbQABbQMBYgAibQABbQIBYgACbQABLAUBYgACLAUBbQEBYgACbQIBbQEBYgACbQMBbQEBYgACbQMCYgACbQMCYgACbQABbQMBYgAibQIBbQEBYgACbQABbQIBYgACbQABbQIBYgACbQABbQIBYgACbQABbQMBYgACbQMBbQEBYgACbQMBbQEBYgACbQMBbQEBYgARAAAzYgACAAAGYgACAAAGYgACAAAGYgACAAAqYgACAAAOYgACAAAqYgACAAAGYgACAAAGYgACAAAGYgACAABmbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAAAqbQYBbQUBAAAObQQBbQcBAAAqbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAABmbQABbQIBAAAGbQABbQIBAAAGbQMBbQEBAAAGbQMBbQEBAAAqbQABbQIBAAAObQMBbQEBAAAqbQABbQIBAAAGbQABbQIBAAAGbQMBbQEBAAAGbQMBbQEBAABmbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAAAqbQYBbQUBAAAObQQBbQcBAAAqbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAABWMgQCAAAGMgQCAAAFMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAFMgMCAAAGMgMCAAAKMgQCAAANMgIBYgACMgEBAAAMMgIBYgACMgEBAAANMgMCAAAKMgQCAAAGMgQCAAAFMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAFMgMCAAAGMgMCAABGbQYCAAAGbQYCAAAFbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAFbQcCAAAGbQcCAAAKbQYCAAANbQQBYgACbQUBAAAMbQQBYgACbQUBAAANbQcCAAAKbQYCAAAGbQYCAAAFbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAFbQcCAAAGbQcCAAAjYgARLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAiLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAiLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAiLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAR",
    
    "EAgQAQMCYgARAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgACAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgBhAAAGiwABAAACiwABAAAMiwABAAACiwABAAAGYgABAAAFiwABAAACiwABAAAFYgACAAAFYgAEAAAFYgACAAAFiwABAAACiwABAAAFYgACAAAFiwABAAACiwABAAAFYgAiAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABiwABAAAKiwABAAABYgACAAABiwABAAAKiwABAAABYgACAAABYgABAAAKYgABAAABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiiwABAAAMiwABYgACiwABAAAMiwABYgACiwABAAAMiwABYgADAAAMYgADiwABAAAMiwABYgACiwABAAAMiwABYgAhAAAgYgABAAAOYgADAAAMYgADAAAOYgACAAAOYgAhAAAgYgABAAAOYgADAAAMYgADAAAOYgACAAAOYgAiiwABAAAMiwABYgACiwABAAAMiwABYgACiwABAAAMiwABYgADAAAMYgADiwABAAAMiwABYgACiwABAAAMiwABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABYgABAAAKYgABAAABYgACAAABiwABAAAKiwABAAABYgACAAABiwABAAAKiwABAAABYgACAAABYgABAAAKYgABAAABYgAhAAAgYgABAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABiwABAAABiwABAAAGiwABAAABiwABAAABYgACAAABYgABAAABYgABAAAGYgABAAABYgABAAABYgAhAAAGiwABAAACiwABAAAMiwABAAACiwABAAAGYgABAAAFiwABAAACiwABAAAFYgACAAAFYgAEAAAFYgACAAAFiwABAAACiwABAAAFYgACAAAFiwABAAACiwABAAAFYgAiAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgACAAABYgABAAABYgABAAABYgABAAACYgABAAABYgABAAABYgABAAABYgBR",
    "EAgQAwIBYgARbQIBbQEBYgACbQIBbQEBYgACbQIBbQEBYgACbQIBbQEBYgACbQABbQMBYgACbQABbQMBYgACbQABbQMBYgACbQABbQMBYgAibQABbQIBYgACbQABbQIBYgACbQICYgACbQIBbQEBYgACbQMBbQEBYgACbQABLAUBYgACLAUBbQEBYgACbQABbQMBYgAibQABbQIBYgACbQABLAUBYgACLAUBbQEBYgACbQIBbQEBYgACbQMBbQEBYgACbQMCYgACbQMCYgACbQABbQMBYgAibQIBbQEBYgACbQABbQIBYgACbQABbQIBYgACbQABbQIBYgACbQABbQMBYgACbQMBbQEBYgACbQMBbQEBYgACbQMBbQEBYgARAAAzYgACAAAGYgACAAAGYgACAAAGYgACAAAqYgACAAAOYgACAAAqYgACAAAGYgACAAAGYgACAAAGYgACAABmbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAAAqbQYBbQUBAAAObQQBbQcBAAAqbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAABmbQABbQIBAAAGbQABbQIBAAAGbQMBbQEBAAAGbQMBbQEBAAAqbQABbQIBAAAObQMBbQEBAAAqbQABbQIBAAAGbQABbQIBAAAGbQMBbQEBAAAGbQMBbQEBAABmbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAAAqbQYBbQUBAAAObQQBbQcBAAAqbQYBbQUBAAAGbQYBbQUBAAAGbQQBbQcBAAAGbQQBbQcBAABWMgQCAAAGMgQCAAAFMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAFMgMCAAAGMgMCAAAKMgQCAAANMgIBYgACMgEBAAAMMgIBYgACMgEBAAANMgMCAAAKMgQCAAAGMgQCAAAFMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAEMgIBYgACMgEBAAAFMgMCAAAGMgMCAABGbQYCAAAGbQYCAAAFbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAFbQcCAAAGbQcCAAAKbQYCAAANbQQBYgACbQUBAAAMbQQBYgACbQUBAAANbQcCAAAKbQYCAAAGbQYCAAAFbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAEbQQBYgACbQUBAAAFbQcCAAAGbQcCAAAjYgARLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAiLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAiLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAiLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgACLA0CYgAR",
    
    # Special
    
    # "EAgQAwIBYgAXAQACYgAOAQACYgAOAQACYgAOAQACYgAOAQACYgAOAQACYgAIAQAOYgACAQAOYgAIAQACYgAOAQACYgAOAQACYgAOAQACYgAOAQACYgAOAQACYgAewQMCYgAIngUBAAACdgMBAAAKYgACFwUBAAANYgACLwABOgABPQIBYAsBNQUBfggCNQQBAAAGYgACYA0DAAAGpAQBpAUBAAABNQABAAABYgACVAABAAAGNQEBAAABfg0CAAADYgACAAAFqw8BqwcBqw8BqwcBpAQBpAUBAAABNQABAAABYgABwQIBAAAFqwcBqw8BqwcBqw8BAAAFwQABwQIBAAACpAQBpAUBAAABqw8BqwcBqw8BqwcBAAAFwQABYgABAAACfg0CAAABqwcBqw8BqwcBqw8BAAAFYgACVAABAAABfg0CAAAFhgYBfgkBhgYBAAACYgACAAACpAQBpAUBAAADpAEBAAABfgkDAAACYgACAAAJhgcBfgkBhgcBAAACYgACAAAOYgACVAABAAADVAABAAAFpAIBAAACVAABYgAIwQECYgAOwQgBwQkBYgAIlAABAAACgwABAAAGfggDAAABYgACAAAOYgAClAABAAABlAABAAABNQUBfggCNQQBAAAGYgACAAAOYgACEgcBAAAIjAABAAAEYgACAAAOYgABwQkBAAAOwQgCAAAOwQkBYgABAAADXAABAAAKYgACEgcBAAABjAABAAAHjAABAAACfggBYgACAAADjAABAAAHjAABAAABfggBYgACAAAJjAABAAAEYgACAAAOYgACEgcBAAADEgcBAAAIEgcBYgAIwQkBwQgBYgAOBQUCYgAINgUBYAcBAAAJjAACAAABYgACPQUBAAANYgACNgUBYAcBAAACNQEBXAABjAABNQABAAAGYgACYAUBAAANYgACAAAOYgACAAAOYgABBQUBAAAOBQUCAAAOBQUBYgABAAAOYgACAAAOYgACAAANjAABYgACAAAOYgACAAAOYgACEgcBAAAMEgcBYgAIBQUCYgAYYAMBAAABsQMDAAAJYgACAAAOYgACYAMBAAADfgAEAAAFsQQBYgACAAANsQQBYgACAAANsQQBYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAACsQIDAAAJYgAiAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgAoEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAIEQUGEQkCEQUGYgACEQUGEQkCEQUGYgAIEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAX",  #  Kitchen - dark

    "EAgQAwIBYgAXAQACYgAOAQACYgAOAQACYgAOAQACYgAOAQACYgAOAQACYgAIAQAOYgACAQAOYgAIAQACYgAOAQACYgAOAQACYgAOAQACYgAOAQACYgAOAQACYgAewQMCYgAIngUBAAACdgMBAAAKYgACFwUBAAANYgACLwABOgABPQIBYAsBNQUBfggCNQQBAAAGYgACYA0DAAAGpAQBpAUBAAABNQABAAABYgACVAABAAAGNQEBAAABfg0CAAADYgACAAAFqw8BqwcBqw8BqwcBpAQBpAUBAAABNQABAAABYgABwQIBAAAFqwcBqw8BqwcBqw8BAAAFwQABwQIBAAACpAQBpAUBAAABqw8BqwcBqw8BqwcBAAAFwQABYgABAAACfg0CAAABqwcBqw8BqwcBqw8BAAAFYgACVAABAAABfg0CAAAFhgYBfgkBhgYBAAACYgACAAACpAQBpAUBAAADpAEBAAABfgkDAAACYgACAAAJhgcBfgkBhgcBAAACYgACAAAOYgACVAABAAADVAABAAAFpAIBAAACVAABYgAIwQECYgAOwQgBwQkBYgAIlAABAAACgwABAAAGfggDAAABYgACAAAOYgAClAABAAABlAABAAABNQUBfggCNQQBAAAGYgACAAAKMgUBAAADYgACEgcBAAAIjAABAAAEYgACAAAOYgABwQkBAAAOwQgCAAACMgUBAAALwQkBYgABAAADXAABAAAKYgACEgcBAAABjAABAAAHjAABAAACfggBYgACAAADjAABAAAHjAABAAABfggBYgACAAAJjAABMgUBAAADYgACAAAOYgACEgcBAAADEgcBAAAIEgcBYgAIwQkBwQgBYgAOBQUCYgAINgUBYAcBAAAJjAACAAABYgACPQUBAAANYgACNgUBYAcBAAACNQEBXAABjAABNQABAAAGYgACYAUBAAANYgACAAAOYgACAAAOYgABBQUBAAAOBQUCAAAOBQUBYgABAAAOYgACAAAOYgACAAANjAABYgACAAAOYgACAAAOYgACEgcBAAAMEgcBYgAIBQUCYgAYYAMBAAABsQMDAAAJYgACMgUBAAANYgACYAMBAAADfgAEAAAFsQQBYgACAAANsQQBYgACAAANsQQBYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAACsQIDAAAJYgAiAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgAiAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgAoEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAIEQUGEQkCEQUGYgACEQUGEQkCEQUGYgAIEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAOEQkCYgAX",  #  Kitchen - light
    "EAgQAQMCYgAXAAACYgAOAAACYgAOAAACYgAOAAACYgBIYgEGLAUCYgEGYgACAAAEagIBAAACagICAAACagcBagIBAAABYgACAAAEagIBAAACagICAAACagcBagIBAAABYgACAAAEagIBAAACagICEgQBAAABagcBagIBEgQBYgACEgQBAAABEgQBAAABagIBEgwBAAABagICEgQBAAABagcBagIBEgQBYgACEgQBAAABEgQBEgwBagIBEgwBEgQBagIBEgQDagcBEgQCYgAWWQABYgALYgEBAgACYgEBCQABYgEECQAEYgEBYgACAAABrwEBJgABAAALYgACAAABrwoBAAAMYgACAAAOYgACAAANEgQBYgACEgQBAAABEgQBAAADEgQBAAADEgQBAAABEgQCYgAiYgEGCQACYAsBCQAEYgEBYgACAAAEkQYBAAAIagEBYgACAAANagEBYgACAAANagEBYgACEgQBAAAMagEBYgACEgQCAAAJEgQDYgAYWQABYgAJYgECCQAGYAoBCQAEYgEBYgACAAANagEBYgACAAANagEBYgACEgQBAAAMagEBYgACEgQBAAAMagEBYgACEgQCAAACEgQCAAABEgQCAAACEgQBAAABagEBYgAiYgECCQABAgACYgEECQAEYgEBYgACYAUBAAACJgABrwQBAAAIagEBYgACYAUBAAADrwoBAAAIagEBYgACYAUBAAAMagEBYgACAAANagEBYgACEgQBAAADEgQCAAADEgQBAAABEgQDYgAiYgEDAgACYgEFCQADYgEBYgACAAADJgABJQABAAAJYgACAAAOYgACAAAOYgACAAANEgQBYgACAAADEgQBAAAGEgQBAAACEgQBYgAbWQABYgAFAAABLAUBYgECAgACYgEBAgABAwABYgECCQABYgECLAUBAAAFJgMBJQABAAACOgABAAAnYgABAAAOYgACEgQCAAABEgQDAAADEgQBAAADEgwBYgAhAAABLAUBYgEFAgACYgEFLAUBAAAxYgABEgQBAAANYgACEgQDAAABEgQDAAACEgQCAAADYgATWQABYgAOYgEBCQADYgEGCQADYgEBYgACAAAOYgACAAAOYgACAAAHMgIBAAAGYgACAAANEgQBYgACEgQCAAAIEgQCAAABEgQBYgAYWQABYgAJYgEBCQABAgABYgEBAgABYgEFAgACCQABYgEBYgACAAACrwEBAAABJgEBAAACYgEBQQMBYgEBagQBrwQBAAACYgACAAACrwoBAAAEYgEBQQMBYgEBagQBrwoBAAACYgACAAAHYgEBQQMBYgEBagQBAAADYgACEgQBAAAGYgEDagQBAAADYgACEgQBAAAHEgQBagQBAAABEgQBAAABEgQBYgAiYgEBCQABAgADCQACYgECAgADCQABYgEBYgACYA0BAAABJQACrwQBAAAEJgEBrwEBJgABAAABYgEBYgACYA0BAAADrwoBAAADagIBagYBrwoBAAADYgACYA0BAAAHagIBagYBAAAEYgACagwBAAAGagICagYBAAAEYgACagwBAAAJEgQBAAADYgAiYgEBCQABAgACCQACYgEDCQAEYgEBYgACaggBAAABJgEBJgMBAAAJdgMBYgACaggBAAAMagEBYgACaggBAAAMagEBYgACaggBAAACEgQBAAAJagEBYgACEgQBagQBAAABEgQBAAACEgQBAAABEgQCAAADagEBYgAiYgEBCQAFYgEDCQAEYgEBYgACAAABagwBAAALagEBYgACAAABagwBAAALagEBYgACAAABagwBAAALagEBYgACEgQBagwBAAALagEBYgACEgQDAAADEgQBAAADEgQBAAACEgQBYgAiYgEGLAUCYgEGYgACAAAJaggBAAABaggCAAABYgACAAAJaggBAAABaggCAAABYgACEgQBAAAIaggBAAABaggCAAABYgACEgQCAAAGEgQBaggBAAABaggBEgQCYgACEgQDAAACEgQEaggBAAABaggBEgQBAAABYgAoAAACYgAOAAACYgAOAAACYgAOAAACYgA3",  #  Garden

    "EAgQAQMCYgAXAAACYgAOAAACYgAObQcBbQYBYgBdAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAqLAMIYgAIAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAnEQAKYgAGMgUCAAAGMgUCYgAGAAAKYgAGAAAKYgAGAAAKYgAGAAAKYgAlLAMBEQABPAcIEQABLAMBYgAEAAABMgUBAAACjgcBjgUBjgYBjgcCAAABMgUBAAABYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAkLAMBEQABPAcIEQABLAMBYgAEAAAEjgcBjgYBjgcBAAACjgcBAAACYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAjAAABLAMBEQABCQABPAcGCQABEQABLAMBAAABYgACAAAGjgcCAAABOwcBAAAEYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgAhAAACLAMBEQABPAcIEQABLAMBAAAGOwcCOwMBAAADOwQBAAAUbQUBYgABAAAOYgACAAAOYgACAAAOYgAhAAACLAMBEQABPAcIEQABLAMBAAAGOwcBAAABOwUBAAACOwQBOwcBAAAUbQQBYgABAAAOYgACAAAOYgACAAAOYgAiAAABLAMBEQABCQABPAcGCQABEQABLAMBAAABYgACAAAEOwcBAAABOwYBOwcBAAABOwQBAAAEYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgAjLAMBEQABPAcIEQABLAMBYgAEAAACjgcBAAACjgcBjgYBjgcBAAAEYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAkLAMBEQABPAcIEQABLAMBYgAEAAABMgUBAAABjgcFAAACMgUBAAABYgAEAAAMYgAEAAAMYgAEAAAMYgAEAAAMYgAlEQAKYgAGMgUCAAAGMgUCYgAGAAAKYgAGAAAKYgAGAAAKYgAGAAAKYgAnLAMIYgAIAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAIAAAIYgAqAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAMAAAEYgAtAAACYgAOAAACYgAObQcBbQYBYgBH",  #  Farm (Lit)
    
    "EAgQAQMCYgAXAAACYgAOAAACYgAOAAACYgAObQcBbQYBYgBILAAOYgACYw4BAAANYgACYw4CAAACYw4BAAAEYw4BAAAEYgACYw4DAAABYw4BAAAEYw4BAAADZA4BYgACYw4DZA4BYw4BZA4BAAABYw4DAAADZA4BYgACYw4DZA4BYw4BZA4CYw4DAAACZA4CYgAiLAABAwIMLAABYgACAAACJwABAAADJwABAAABKAABAAAFYgACAAAOYgACYw4BAAAMYw4BYgACYw4BZA4BAAAFZA4BAAAFYw4BYgACYw4BZA4BYw4BZA4BYw4BZA4DAAACZA4CAAABZA4BYgAiLAABAwIMLAABYgACAAABJwABKAACJwABKAABAAABJwACAAACKAABAAACYgACAAAOYgACAAAOYgACYw4BAAAMYw4BYgACYw4EAAADZA4BAAABZA4BAAACZA4CYgAiLAABAwIMLAABYgACAAACKAABAAADJwABAAABKAACAAAEYgACAAAOYgACAAAJZA4DAAACYgACAAADZA4DAAAIYgACZA4CYw4BAAAKZA4BYgAiLAABAwIEEQgEAwIBYw4BAwICLAABYgACAAABJwABAAAEKAABAAADYw4BKAABAAACYgACAAADZA4CAAAFYw4BAAACYw4BYgACAAAJZA4DAAABYw4BYgACAAACZA4FAAACKAADAAABYw4BYgACZA4BAAADKAACAAACYw4BAAAEYw4BYgAiLAABAwICogQBYw4BAwIBYw4BAwIDEQUBAwICLAABYgACAAACKAABAAABYw4BKAABAAABKAACAAABKAACAAACYgACAAADZA4BYw4BAAAJYgACAAAEYw4BAAAEZA4DAAACYgACYw4BAAABZA4FAAACKAACAAACYw4BYgACYw4BAAADKAADYw4BAAABYw4DAAABZA4BYgAhAAABLAABAwICogQBAwIGEQUBAwICLAABAAADJwABAAAFJwABAAABJwABAAACKAABAAASbQUBAAAObQUBYgABAAACZA4FAAAHYgACYw4BAAAEKAACAAADYw4BAAACYw4BYgAhAAABLAABAwICogQBAwIDYw4BAwICEQUBAwICLAABAAADJwABKAABAAACKAABAAACJwABKAABJwABKAABAAATbQQBAAAObQQBYgABYw4BAAACZA4DAAAHYw4BYgACYw4CAAAFYw4BAAAEZA4CYgAiLAABAwICogQBAwIJLAABYgACAAADJwABKAABAAABJwACAAABJwABAAABJwABAAACYgACYw4BAAANYgACYw4BAAAMYw4BYgACYw4BAAAMYw4BYgACYw4BZA4BAAAGYw4BAAAEZA4BYgAiLAABAwICogQBAwICEQkEAwIDLAABYgACAAACKAACAAABKAABAAABKAABAAACKAABAAADYgACAAANZA4BYgACAAABZA4CAAAKKAABYgACAAABKAACAAALYgACZA4BAAACYw4CAAAEYw4BAAABYw4CZA4BYgAiLAABAwIMLAABYgACAAABJwABYw4BJwACAAABJwABAAACKAABJwABAAABKAABAAABYgACAAACYw4BAAAJZA4CYgACAAABZA4DAAAIKAABAAABYgACAAACKAABAAAKYw4BYgACYw4CZA4BAAACYw4CAAAFYw4CYgAiLAABAwIMLAABYgACAAADJwABKAABJwABKAABJwABAAAGYgACAAAMZA4CYgACAAABZA4DAAAKYgACAAACKAACAAAJYw4BYgACZA4BYw4DAAAJYw4BYgAiLAABAwIMLAABYgACAAABJwABKAACAAABJwACAAABKAABZA4CAAABKAABAAABYgACAAAJKAABAAADZA4BYgACAAAJZA4CAAACYw4BYgACZA4BAAAMYw4BYgACZA4CYw4BAAABZA4BYw4BAAABYw4BZA4BAAACYw4BZA4CYgAiLAAOYgACAAAIZA4EAAACYgACZA4BAAADYw4BAAAFKAABAAACYw4BYgACZA4BAAADYw4BAAADZA4EAAABYw4BYgACZA4CAAACYw4CAAADKAABYw4BAAACZA4BYgACZA4DYw4BZA4CYw4BZA4DYw4BZA4DYgAoAAACYgAOAAACYgAOAAACYgAObQcBbQYBYgA3",  # Fungus
    ]
    
    room_of_vault = [
    "EAgQAQMCYgAWLAMBAAACLAMBYgAMAAAEYgAMbQcBAAACbQYBYgANAAACYgAObQcBbQYBYgA7NgUCLAMBAAACLAMBNgUCYgAILAsCAAAELAsCYgAKbQcBAAACbQYBYgAKNgUCAAAENgUCYgAIAAAIYgA6LAMBAAACLAMBYgAMAAAEYgAMbQcBAAACbQYBYgANAAACYgAObQcBbQYBYgA7NgUCLAMBAAACLAMBNgUCYgAILAsCAAAELAsCYgAKbQcBAAACbQYBYgAKNgUCAAAENgUCYgAIAAAIYgA1NgMBYgABNgMBYgACLAMBAAACLAMBYgACNgMBYgABNgMBYgACLAsBYgABLAsBYgACAAAEYgACLAsBYgABLAsBYgAHbQcBAAACbQYBYgAHNgMBYgABNgMBYgADAAACYgADNgMBYgABNgMBYgACAAABYgABAAABYgADbQcBbQYBYgADAAABYgABAAABYgAyNgMBYgABNgMBYgACLAMBAAACLAMBYgACNgMBYgABNgMBYgACLAsBYgABLAsBYgACAAAEYgACLAsBYgABLAsBYgAHbQcBAAACbQYBYgAHNgMBYgABNgMBYgADAAACYgADNgMBYgABNgMBYgACAAABYgABAAABYgADAAACYgADAAABYgABAAABYgAqBAABYgAGLAMGAAAELAMGAAAQbQUGAAAEbQUGYgABAAABYgABAAABYgACAAAEYgACAAABYgABAAABYgACAAABYgABAAABYgADbQcBbQYBYgADAAABYgABAAABYgAxAABAbQUBAAABbQUBAAABbQUBAAABbQUBAAACbQUBAAABbQUBAAABbQUBAAABbQUBYgAHAAACYgAnAABAbQQBAAABbQQBAAABbQQBAAABbQQBAAACbQQBAAABbQQBAAABbQQBAAABbQQBYgAHAAACYgAdBAABYgACBAABYgAGLAMGAAAELAMGAAAQbQQGAAAEbQQGYgABAAABYgABAAABYgACAAAEYgACAAABYgABAAABYgACAAABYgABAAABYgADbQcBbQYBYgADAAABYgABAAABYgAyNgMBYgABNgMBYgACLAMBAAACLAMBYgACNgMBYgABNgMBYgACLAsBYgABLAsBYgACAAAEYgACLAsBYgABLAsBYgAHbQcBAAACbQYBYgAHNgMBYgABNgMBYgADAAACYgADNgMBYgABNgMBYgACAAABYgABAAABYgADAAACYgADAAABYgABAAABYgAyNgMBYgABNgMBYgACLAMBAAACLAMBYgACNgMBYgABNgMBYgACLAsBYgABLAsBYgACAAAEYgACLAsBYgABLAsBYgAHbQcBAAACbQYBYgAHNgMBYgABNgMBYgADAAACYgADNgMBYgABNgMBYgACAAABYgABAAABYgADbQcBbQYBYgADAAABYgABAAABYgA1NgUCLAMBAAACLAMBNgUCYgAILAsCAAAELAsCYgAKbQcBAAACbQYBYgAKNgUCAAAENgUCYgAIAAAIYgA6LAMBAAACLAMBYgAMAAAEYgAMbQcBAAACbQYBYgANAAACYgAObQcBbQYBYgA7NgUCLAMBAAACLAMBNgUCYgAILAsCAAAELAsCYgAKbQcBAAACbQYBYgAKNgUCAAAENgUCYgAIAAAIYgA6LAMBAAACLAMBYgAMAAAEYgAMbQcBAAACbQYBYgANAAACYgAObQcBbQYBYgAn",
    
    "EAgQAQMCYgAXAAACYgAOAAACYgAOiwACYgBYiwABAAACZQADAAACZQADAAACiwABYgACiwABAAACZQADAAACZQADAAACiwABYgACiwABAAACZQADAAACZQADAAACiwABYgACiwACAAABZQADAAACZQADAAABiwACYgACiwADZQADAAACZQADiwADYgACiwAOYgAiiwABAAAMiwABYgACiwABAAAMiwABYgACiwABAAAMiwABYgACiwACAAAKiwACYgACiwADAAAIiwADYgACiwAOYgAiAAANZQABYgACAAANZQABYgACAAANZQABYgACAAANZQABYgACAAANZQABYgACAAANZQABYgAiiwABAAAEDwAGAAACiwABYgACiwABAAAMiwABYgACiwABAAAMiwABYgACiwACAAAKiwACYgACiwADAAAIiwADYgACiwAOYgAiiwABAAADDwABKgACNAABKQABDwABAAADiwABYgACiwABAAAGKQABAAAFiwABYgACiwABAAAMiwABYgACiwACAAAKiwACYgACiwADAAAIiwADYgACiwAOYgAiAAACDwACDgADDwABKQACDgACAAACYgACAAAEDgABAAAJYgACAAAOYgACiwACAAAKiwACYgACAAAOYgACAAAOYgAhAAADDwABKgABDgABKgABKQABDgABKQACDgACAAALDgABKQACDgABAAAEiwABAAAKKQABAAADiwABYgABiwACAAAKiwACYgACiwADAAAIiwADYgACiwAOYgAhAAADKgACDwABDgAEKQABqQABDwABAAAJDgABAAACNgIBKQABAAABDwABAAADiwABAAAJKQABAAAEiwABYgABiwACAAAKiwACYgACiwADAAAIiwADYgACiwAOYgAiAAACKgACKQACDgADKQADAAACYgACAAAEKQACNgQBDgACAAABDwABAAADYgACAAAEKQABAAADDgABAAAFYgACiwACAAAKiwACYgACAAAOYgACAAAOYgAiiwABAAABKQACqQABKQABDwABDgACKQADAAABiwABYgACiwABAAACKQABAAABKQABDwABDgACAAAEiwABYgACiwABAAAEKQABAAAHiwABYgACiwACAAAKiwACYgACiwADAAAIiwADYgACiwAOYgAiiwABAAABKQADDgABDwACDgABAAAEiwABYgACiwABAAACKQACDwACDgACAAAEiwABYgACiwABAAAEDwABAAAHiwABYgACiwACAAAKiwACYgACiwADAAAIiwADYgACiwAOYgAiAAACKQADDwACAAABDwABAAAFYgACAAAIDgABAAAFYgACAAAOYgACAAAOYgACAAAOYgACAAAOYgAiiwABAAAMiwABYgACiwABAAAMiwABYgACiwABAAAMiwABYgACiwACAAAKiwACYgACiwADAAAIiwADYgACiwAOYgAiiwABAAACZQADAAACZQADAAACiwABYgACiwABAAACZQADAAACZQADAAACiwABYgACiwABAAACZQADAAACZQADAAACiwABYgACiwACAAABZQADAAACZQADAAABiwACYgACiwADZQADAAACZQADiwADYgACiwAOYgAoAAACYgAOAAACYgAOiwACYgBH",  #  Treasure vault
    ]

    detail_central_feature = [ 
        "BAIEAQMCYgICYgAKYgEBCQACYgEBYgAFCQACYgEBYgACYgEBYgADYgEB",  #  2x2 water well
        
        "BAIEAQMCYgICYgAKYgEBCwACYgEBYgAFCwACYgEBYgACYgEBYgADYgEB",  #  2x2 lava well
        "CgQKAwIBYgAEYgEBYgAcqQABYgACqQABYgAaqQABYgACqQABYgAhAAADYgABYgECYgABAAAFYgACCQACYgACAAADYgABCQAGYgABAAABYgACCQAGYgEBYgACCQADYgECCQADYgACCQADYgECCQADYgACYgEBCQAGYgACAAABYgABCQAGYgABAAADYgACCQACYgACAAAFYgABYgEBYgACAAAvYgEBYgIBAAAIYgECAABYbQIBbQEBAAAIbQABbQMBAAAs",  # 10x10 round fountain with water
        
        "CgQKAwIBYgAEYgEBYgAcXw8BYgACXw8BYgAaXw8BYgACXw8BYgAhAAADYgABYgECYgABAAAFYgACAAACYgACAAADYgABAAAGYgABAAABYgACAAAGYgEBYgACAAADYgECAAADYgACAAADYgECAAADYgACYgEBAAAGYgACAAABYgABAAAGYgABAAADYgACAAACYgACAAAFYgABYgEBYgACAAAvYgEBYgIBAAAIYgECAABYbQIBbQEBAAAIbQABbQMBAAAs",  # 10x10 round fountain with no water
        
        "BAgEAwIBYgAQAAAFYgACAAACYgACAAAKYgACAAACYgACAAAKYgACAAACYgACAAAGbQYCAAABbQQBYgACbQUBbQQBYgACbQUBAAABbQcCAAACMgUCAAABMgUBYgACMgUCYgACMgUBAAABMgUCAAAGYgACAAACYgACAAAFYgAQ",   # 4x4 pillar no bevel
        "BAgEAgEDYgABAAAGYgADAAACbQYBMgUBYgAEAAACbQYBMgUBYgADAAAGYgADAAACbQQBMgUBYgAUAAACbQUBMgUBYgAEAAACbQQBMgUBYgAUAAACbQUBMgUBYgADAAAGYgADAAACbQcBMgUBYgAEAAACbQcBMgUBYgADAAAG",   # 4x4 pillar with bevel
        "BgUGAwIBYgAkAAAHmwABAAACmwABAAADnAABnAIBAAAEnAMBnAEBAAADmwABAAACmwABAAAOmwABAAACmwABAAAOmwABAAACmwABAAAOmwABAAACmwABAAAOmwABAAACmwABAAAOmwAEAAACmwABqQACmwABAAACmwABqQACmwABAAACmwAEAAAH",  #  Pergola
        "BAYEAwIBYgAFNgQBNAABYgACNAABNgIBYgAFAAAFMQACAAACMQACAAAKMQACAAACMQACAAAKMQACAAACMQACAAAKMQACAAACMQACAAAKMQACAAACMQACAAAF",  #  Obsidian obelisk
        "BAUEAwIBYgAQAAABYAwBAAACYA4BLwABYgABAAABbQIBNAABYgABAAABYgADAAAGYgABbQEBAAACMQABbQMBAAAOdAABAAAW",  #  Crafting table assembly
        "BgQGAwIBYgAlNQIBiAIBhgIBpAIBYgABNQABPAcDAwABpAEBiAABPAcEhgEBhgABPAcBCQABPAcBAwABiAEBpAABPAcENQEBYgABpAMBhgMBiAMBNQMBYgABiwABAAAEiwABAAABjgcBOwcBaQcBZwABAAACjQcBzwMBOwcCAAACzwMBAAABOwcBVgMBAAACOwcBjgcBjQcBaAcBAAABiwABAAAEiwEBMgUBAAAEMgUBAAAYMgUBAAAE",  #  Veggie patch
        "BAUEAgEDYgABBQAEYgABfggEYgABfggEYgABBQAEYgABfggEYgABLwAEYgABLwAEYgABfggEYgABfggEYgABLwAEYgABLwAEYgABfggEYgABBQAEYgABfggEYgABfggEYgABBQAE",  #  Library bookcase
        "BAYEAwIBYgAQAAABmwICAAABDgABNAACDgACKQACDgABAAABbQMCAAACmwICAAABqQABKQACqQABnAQBAAACnAUBAAAFmwICAAABnAABKQACnAEBAAAJmwICAAACnAMCAAAKLAcCAAAN",  #  Throne
        "BAQEAwIBYgAGNAABYgADNAABYgAFnAYEmwABkgMCmwACNgICmwABnAcEAAAEnAMEnAIEAAAU",  #  Tomb quartz East/West
        "BAQEAQMCYgAEnAQEAAAIYgABNAABYgACmwABNgUCmwABnAEEAAAEYgABNAABYgACmwABkgQCmwABnAAEAAAEYgAEnAUEAAAI",  #  Tomb quartz North/South
        "BAQEAwIBYgAGNAABYgADNAABYgAFbQYEYgABNgMCYgACkgICYgABbQcEAAAEbQMEbQIEAAAU", #  Tomb stone East/West
        "BAQEAQMCYgAEbQQEAAAIYgACNAABYgACNgUCYgABbQEEAAAEYgACNAABYgACkgQCYgABbQAEAAAEYgAEbQUEAAAI",  #  Tomb stone North/South
    ]
    
    def __init__(self, world, pos):
        self.world = world
        self.pos = pos
        self.exits = []
        self.type = None
    
    
    def build_room_from_template(self, pos, size, exit_north, exit_south, exit_east, exit_west, exit_up, exit_down, template):
        s = SpaceRecorder()
        s.decode(template)  #  Force the supplied pattern into the tool
        items = s.space_replay(self.world.level, pymclevel.BoundingBox(pos, size))
        return items

    def build_detail_from_template(self, pos, size, template):
        s = SpaceRecorder()
        s.decode(template)  #  Force the supplied pattern into the tool
        items = s.space_replay_centred(self.world.level, pymclevel.BoundingBox(pos, size))
        return items

        
    
    def build_simple_room(self, pos, size, exit_north, exit_south, exit_east, exit_west, exit_up, exit_down):
        '''
            Test method
        '''
        box = pymclevel.BoundingBox(pos, size)
        self.world.fill(box, self.world.materials.stones_for_building)
        x,y,z = pos
        dx, dy, dz = size
        box = pymclevel.BoundingBox((x+1, y+1, z+1), (dx-2, dy-2, dz-2))
        self.world.fill(box, self.world.materials.air_for_building)
        if exit_north:
            box = pymclevel.BoundingBox((x+(dx>>1)-1, y+1, z+dz-1), (2, 3, 2))
            self.world.fill(box, self.world.materials.air_for_building)
        if exit_south:
            box = pymclevel.BoundingBox((x+(dx>>1)-1, y+1, z-1), (2, 3, 2))
            self.world.fill(box, self.world.materials.air_for_building)
        if exit_east:
            box = pymclevel.BoundingBox((x+dx-1, y+1, z+(dz>>1)-1), (2, 3, 2))
            self.world.fill(box, self.world.materials.air_for_building)
        if exit_west:
            box = pymclevel.BoundingBox((x, y+1, z+(dz>>1)-1), (2, 3, 2))
            self.world.fill(box, self.world.materials.air_for_building)
        if exit_up:
            box = pymclevel.BoundingBox((x+(dx>>1)-1, y+dy-1, z+(dz>>1)-1), (2, 2, 2))
            self.world.fill(box, self.world.materials.air_for_building)
        if exit_down:
            box = pymclevel.BoundingBox((x+(dx>>1)-1, y-1, z+(dz>>1)-1), (2, 2, 2))
            self.world.fill(box, self.world.materials.air_for_building)
            
    
    def build_chamber(self):
        exits = []
        cx, cy, cz = self.pos
        radius = random.randint(5, 9)
        box = pymclevel.BoundingBox((cx-radius, cy, cz-radius), (radius*2+1, radius, radius*2+1))
        self.world.hemisphere(box, self.world.materials.stones_for_building)        

        box = pymclevel.BoundingBox((cx-(radius-1), cy, cz-(radius-1)), ((radius-1)*2+1, radius-1, (radius-1)*2+1))
        self.world.hemisphere(box, (0,0))        
    
    
    def build_gateway(self):
        '''
            Try and make a pillared room with a path downward. Return a list of exits
        '''
        exits = []
        cx, cy, cz = self.pos
        
        height = random.randint(7, 13)
        roof_height = random.randint(2, 4)
        radius = random.randint(6, 8)
        
        box = pymclevel.BoundingBox((cx-radius, cy, cz-radius), (radius*2+1, height, radius*2+1))
        if self.world.check_for_intersection(box):
            return exits  #  Quit early
        self.world.buildings.append(box)  #  Reserve this space so we don't build over it
        
        self.world.fill(box, (0,0))
        
        # floor_box = pymclevel.BoundingBox((cx-radius, cy, cz-radius), (radius*2+1, 1, radius*2+1))
        # self.world.fill(floor_box, self.world.materials.stones_for_building)
        for i in xrange(0, 4):
            floor_box = pymclevel.BoundingBox((cx-radius-i, cy-1-i, cz-radius-i), ((radius+i)*2+1, 1, (radius+i)*2+1))
            self.world.fill(floor_box, self.world.materials.stones_for_building)

        # Plinth
        plinthbox = pymclevel.BoundingBox((cx-1, cy, cz-1), (3, 1, 3))
        self.world.fill(plinthbox, (145,random.randint(0,11)))
        
        # Now there may be areas below the floor which are not supporting the floor. Fix this.
        
        exits.append( (cx, cy, cz-radius) )
        exits.append( (cx, cy, cz+radius) )
        exits.append( (cx-radius, cy, cz) )
        exits.append( (cx+radius, cy, cz) )
        
        #  Roof
        rminus1 = radius-1
        roof_box = pymclevel.BoundingBox((cx-rminus1, cy+height-roof_height, cz-rminus1), (rminus1*2+1, 1, rminus1*2+1))
        self.world.fill(roof_box, self.world.materials.stones_for_building_decoration)
        roof_box = pymclevel.BoundingBox((cx-rminus1, cy+height-roof_height, cz-rminus1), (rminus1*2+1, roof_height, rminus1*2+1))
        self.world.hemisphere(roof_box, self.world.materials.stones_for_building_decoration)
        
        #  Pillars
        rminus2 = rminus1-1
        pillar1_box = pymclevel.BoundingBox((cx-rminus2, cy, cz-rminus2), (1, height-roof_height, 1))
        self.world.fill(pillar1_box, self.world.materials.stones_for_building_decoration)
        pillar1_box = pymclevel.BoundingBox((cx-rminus2, cy, cz+rminus2), (1, height-roof_height, 1))
        self.world.fill(pillar1_box, self.world.materials.stones_for_building_decoration)
        pillar1_box = pymclevel.BoundingBox((cx+rminus2, cy, cz+rminus2), (1, height-roof_height, 1))
        self.world.fill(pillar1_box, self.world.materials.stones_for_building_decoration)
        pillar1_box = pymclevel.BoundingBox((cx+rminus2, cy, cz-rminus2), (1, height-roof_height, 1))
        self.world.fill(pillar1_box, self.world.materials.stones_for_building_decoration)
        
        pillar1_box = pymclevel.BoundingBox((cx, cy, cz-rminus2), (1, height-roof_height, 1))
        self.world.fill(pillar1_box, self.world.materials.stones_for_building_decoration)
        pillar1_box = pymclevel.BoundingBox((cx, cy, cz+rminus2), (1, height-roof_height, 1))
        self.world.fill(pillar1_box, self.world.materials.stones_for_building_decoration)
        pillar1_box = pymclevel.BoundingBox((cx-rminus2, cy, cz), (1, height-roof_height, 1))
        self.world.fill(pillar1_box, self.world.materials.stones_for_building_decoration)
        pillar1_box = pymclevel.BoundingBox((cx+rminus2, cy, cz), (1, height-roof_height, 1))
        self.world.fill(pillar1_box, self.world.materials.stones_for_building_decoration)

        # Lighting
        
        # Stairs (spiraling downward
        # Add this to the collision set
        px, py, pz = self.pos
        maxheight = py-self.world.box.miny
        deepness = maxheight
        if maxheight > 6:
            deepness = random.randint(6, maxheight)
        px -= 3  # Start off to the left of centre

        #  The following line will ensure nothing builds over the stairwell
        # self.world.buildings.append( pymclevel.BoundingBox((px, py-maxheight, pz-3),(7, maxheight, 7)))
        
        AIR = (0, 0)
        dirs = [ (0, -1, -1), (0, -1, -1), (0, -1, -1),
                (1, -1, 0), (1, -1, 0), (1, -1, 0), (1, -1, 0), (1, -1, 0), (1, -1, 0),
                (0, -1, 1), (0, -1, 1), (0, -1, 1), (0, -1, 1), (0, -1, 1), (0, -1, 1), 
                (-1, -1, 0), (-1, -1, 0), (-1, -1, 0), (-1, -1, 0), (-1, -1, 0), (-1, -1, 0), 
                (0, -1, -1), (0, -1, -1), (0, -1, -1)
              ]
        d_idx = 0
        stair_gap = 5
        stair_box = pymclevel.BoundingBox((px-1, py, pz-stair_gap+1), (3, stair_gap, stair_gap))
        self.world.fill(stair_box, self.world.materials.stones_for_building_decoration)
        while deepness >= 0:
            stair_box = pymclevel.BoundingBox((px, py-1, pz), (1, stair_gap, 1))
            self.world.fill(stair_box, self.world.materials.air_for_building)
            self.world.set_block_at((px, py-1, pz), (73, 0) )  #  Redstone ore - lights up when we tread on it
            self.world.set_block_at((px, py+stair_gap-1, pz), (169, 0) )  # Sea lantern
            dx, dy, dz = dirs[d_idx%len(dirs)]
            px += dx
            py += dy
            pz += dz
            d_idx += 1
            deepness -= 1
        # Chamber
        radius = random.randint(5, 9)
        py += 1 
        if dx == 1:
            pathbox = pymclevel.BoundingBox((px, py, pz), (radius+2, 3, 1))
            self.pos = (px+radius+1, py, pz)
            
        elif dx == -1:
            pathbox = pymclevel.BoundingBox((px-radius-1, py, pz), (radius+2, 3, 1))
            self.pos = (px-radius-1, py, pz)
        if dz == 1:
            pathbox = pymclevel.BoundingBox((px, py, pz), (1, 3, radius+2))
            self.pos = (px, py, pz+radius+1)
        elif dz == -1:
            pathbox = pymclevel.BoundingBox((px, py, pz-radius-1), (1, 3, radius+2))
            self.pos = (px, py, pz-radius-1)
        (cx, cy, cz) = self.pos
        box = pymclevel.BoundingBox((cx-radius, cy, cz-radius), (radius*2+1, radius, radius*2+1))
        self.world.hemisphere(box, self.world.materials.stones_for_building)        

        box = pymclevel.BoundingBox((cx-(radius-1), cy, cz-(radius-1)), ((radius-1)*2+1, radius-1, (radius-1)*2+1))
        self.world.hemisphere(box, (0,0))         
        self.world.fill(pathbox, (0,0))

        exits.append((cx+radius, cy, cz))
        exits.append((cx-radius, cy, cz))
        exits.append((cx, cy, cz+radius))
        exits.append((cx, cy, cz-radius))
        return exits
    

class Agent:
    '''
        An agent explores and builds, and lives a fulfilling life.
    '''
    def __init__(self, world, fname, lname):
        self.world = world
        self.diary = Journal()
        self.ledger = Journal()
        self.pos = None
        self.fname = fname
        self.lname = lname
        self.name = fname + " " + lname
        self.age = 21
        
        self.blueprint = [ self.build_gateway 
            ]

    def log(self, msg):
        self.ledger.log(self.world.get_time()+" "+ self.name + " " + msg)

    def move_to(self, pos):
        self.pos = pos
        self.log("- Moved to "+str(self.pos))

    def report(self):
        self.log("- I am at "+str(self.pos))
    
    def get_pos(self):
        return self.pos
    
    def random_walk(self):
        x, y, z = self.pos
        possibilities = [ (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0),
            (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
            (1, 1, 0), (-1, 1, 0), (0, 1, 1), (0, 1, -1),
            (1, 1, 1), (-1, 1, 1), (1, 1, -1), (-1, 1, -1),
            (1, -1, 0), (-1, -1, 0), (0, -1, 1), (0, -1, -1),
            (1, -1, 1), (-1, -1, 1), (1, -1, -1), (-1, -1, -1)
            ]
        dx, dy, dz = random.choice(possibilities)
        #  Check destination is clear for navigation
        x = x+dx
        y = y+dy
        z = z+dz

        block_id = self.world.block_at((x, y, z), False)  #  Use the cache
        if block_id in self.world.materials.navigable:
            # Check bounds
            if x < self.world.box.minx:
                x = self.world.box.minx
            if x >= self.world.box.maxx:
                x = self.world.box.maxx-1
            if y < self.world.box.miny:
                y = self.world.box.miny
            if y >= self.world.box.maxy:
                y = self.world.box.maxy-1
            if z < self.world.box.minz:
                z = self.world.box.minz
            if z >= self.world.box.maxz:
                z = self.world.box.maxz-1
            self.move_to((x, y, z))
        else:
            log("Oops I couldn't move to "+str((x,y,z)))
        
    def print_ledger(self):
        self.ledger.print_out()
    

    def build_gateway(self):
        building = Building(self.world, self.pos)
        exits = building.build_gateway()
        return exits

    def build(self):
        # Choose what to build
        if len(self.blueprint) > 0:
            build_proc = self.blueprint.pop()  #  Whatever is next in line to build
            build_proc()        
    
    def update(self):
        self.random_walk()
        self.build()
        self.age += 1        


class Filesystem:
    def __init__(self):
        pass

    def write_json(self, filename, json_object):
        with open(filename, "w") as outfile:
            json.dump(json_object, outfile, indent=4, sort_keys=True)

    def read_json(self, filename):
        with open(filename, "r") as infile:
            return json.load(infile)

    def get_filenames(self, path, pattern):
        print 'Scanning available files...'
        fileNames = glob.glob(path + pattern)  # E.g. *.png
        return fileNames

    def get_files_from_here(self, path):
        # Read in this level, collecting all files as we go, and do the same for directories
        print path
        content = {}

        for root, dirs, files in os.walk(path):
            print root, dirs, files
            for subdir in dirs:
                content[os.path.join(root, subdir)] = []
            content[root] = files
        print content
        return content

    def addStringToFile(self, fn, theString):
        theFile = open(fn, 'a+')
        theFile.write(theString)
        theFile.close()

    def read_image(self, filename):
        return pygame.image.load(filename)


class Maze(object):
    NOTVISITED = 0
    VISITED = 1
    WALL = 0
    NOWALL = 1

    HERE = 0
    EAST = 1
    WEST = 2
    NORTH = 3
    SOUTH = 4

    def __init__(self, size, seed):
        self.width, self.depth = size
        if seed == None or seed == 0:
            seed = random.randint(-999999999999,999999999999)
        self.seed = seed
        self.generated = False
        self.cells = None

    def to_image(self):
        col_path = (255, 255, 255, 255)
        if self.generated == False:
            self.generate(None)
        img = pygame.Surface((self.width*2+1, self.depth*2+1),pygame.SRCALPHA)
        img.fill((0,0,0,255))
        for x in xrange(0, self.width):
            for z in xrange(0, self.depth):
                if self.cells[x,z,0] == self.VISITED:
                    px = (x<<1)+1
                    pz = (z<<1)+1
                    img.set_at((px,pz), col_path)
                    if self.cells[x, z, self.WEST] == self.NOWALL:
                        img.set_at((px - 1, pz), col_path)
                    if self.cells[x, z, self.EAST] == self.NOWALL:
                        img.set_at((px + 1, pz), col_path)
                    if self.cells[x, z, self.NORTH] == self.NOWALL:
                        img.set_at((px, pz - 1), col_path)
                    if self.cells[x, z, self.SOUTH] == self.NOWALL:
                        img.set_at((px, pz + 1), col_path)
        return img

    def to_array(self, seed):
        if self.generated == False:
            self.generate(seed)
        return self.cells

    def generate(self, seed):
        if seed == None:
            seed = self.seed
        if self.generated == False:

            NOTVISITED = self.NOTVISITED
            VISITED = self.VISITED
            WALL = self.WALL
            NOWALL = self.NOWALL
            R = random.Random(seed)
            x = R.randint(0, self.width-1) # Start pos
            z = R.randint(0, self.depth-1) # Start pos

            x = self.width>>1
            z = self.depth>>1
            start_cell = (x,z)
            self.cells = numpy.zeros((self.width, self.depth, 5)) # 1-4 is west, east, north, south
            Q = [] # traversed paths

            print "Generating maze starting at ",x,z
            keep_going = True
            while keep_going:
                if self.cells[x,z,self.HERE] == NOTVISITED:
                    self.cells[x,z,self.HERE] = VISITED
                    Q.append( (x, z))
                    # Create an iterable list of neighbouring cells
                P = []
                for dp in xrange(-1,2):
                    if dp != 0:
                        d = x+dp
                        if d > -1 and d < self.width:
                            if self.cells[d, z, self.HERE] == NOTVISITED:
                                P.append( (d, z, dp, 0) )
                        d = z+dp
                        if d > -1 and d < self.depth:
                            if self.cells[x, d, self.HERE] == NOTVISITED:
                                P.append( (x, d, 0, dp) )
                plen = len(P)
                if plen > 0:
                    # print "Choosing a neighbour"
                    # Select a cell at random
                    (x1, z1, dx, dz) = P[R.randint(0, plen-1)]
                    # Remove the wall between this cell and the neighbour
                    if dx == -1:
                        self.cells[x, z, self.WEST] = NOWALL
                        self.cells[x1, z1, self.EAST] = NOWALL
                    elif dx == 1:
                        self.cells[x, z, self.EAST] = NOWALL
                        self.cells[x1, z1, self.WEST] = NOWALL
                    elif dz == -1:
                        self.cells[x, z, self.NORTH] = NOWALL
                        self.cells[x1, z1, self.SOUTH] = NOWALL
                    elif dz == 1:
                        self.cells[x, z, self.SOUTH] = NOWALL
                        self.cells[x1, z1, self.NORTH] = NOWALL

                    # Move along to process the neighbour
                    x = x1
                    z = z1
                    # This is the next cell
                else: # Backtrack
                    # print "Backtracking"
                    #(x1, z1) = start_cell
                    #if x == x1 and z == z1 and len(Q) == 0:
                    #    print "Generation completed"
                    #    keep_going = False
                    #else: # Find me another cell
                    if True:
                        # print "Stepping backwards"
                        if len(Q) > 0:
                            (x, z) = Q.pop(R.randint(0, len(Q)-1))
                        else:
                            # print "Pop not possible"
                            keep_going = False
        self.generated = True

    def cell_make_exit_west(self, x, z):
        if self.generated == False:
            self.generate(None)
        if 1 <= x < self.width and 0 <= z < self.depth:
            self.cells[x, z, self.WEST] = self.NOWALL
            self.cells[x-1, z, self.EAST] = self.NOWALL

    def cell_make_exit_east(self, x, z):
        if self.generated == False:
            self.generate(None)
        if 0 <= x < self.width-1 and 0 <= z < self.depth:
            self.cells[x, z, self.EAST] = self.NOWALL
            self.cells[x+1, z, self.WEST] = self.NOWALL

    def cell_make_exit_north(self, x, z):
        if self.generated == False:
            self.generate(None)
        if 0 <= x < self.width and 1 <= z < self.depth:
            self.cells[x, z, self.NORTH] = self.NOWALL
            self.cells[x, z-1, self.SOUTH] = self.NOWALL

    def cell_make_exit_south(self, x, z):
        if self.generated == False:
            self.generate(None)
        if 0 <= x < self.width and 0 <= z < self.depth-1:
            self.cells[x, z, self.SOUTH] = self.NOWALL
            self.cells[x, z+1, self.NORTH] = self.NOWALL


    def cell_visited(self, x, z):
        if self.generated == False:
            self.generate(None)
        result = False
        if 0 <= x < self.width and 0 <= z < self.depth:
            result = (self.cells[x, z, self.HERE] == self.VISITED)
        return result

    def cell_exit_west(self, x, z):
        if self.generated == False:
            self.generate(None)
        result = False
        if 0 <= x < self.width and 0 <= z < self.depth:
            result = (self.cells[x, z, self.WEST] == self.NOWALL)
        return result

    def cell_exit_east(self, x, z):
        if self.generated == False:
            self.generate(None)
        result = False
        if 0 <= x < self.width and 0 <= z < self.depth:
            result = (self.cells[x, z, self.EAST] == self.NOWALL)
        return result

    def cell_exit_north(self, x, z):
        if self.generated == False:
            self.generate(None)
        result = False
        if 0 <= x < self.width and 0 <= z < self.depth:
            result = (self.cells[x, z, self.NORTH] == self.NOWALL)
        return result

    def cell_exit_south(self, x, z):
        if self.generated == False:
            self.generate(None)
        result = False
        if 0 <= x < self.width and 0 <= z < self.depth:
            result = (self.cells[x, z, self.SOUTH] == self.NOWALL)
        return result

    def render_to_minecraft(self, level, box, cells_wide, cells_depth, CELLSIZE, palette, pattern):
        if self.generated == False:
            self.generate(None)

        box_height = box.maxy-box.miny
        path_palette = Palette().get_palette_by_name("air")
        air_palette = palette
        palette = path_palette

        WIDTH_PATH = CELLSIZE>>2
        WIDTH_WALL = int(ceil((CELLSIZE-WIDTH_PATH)/2))
        print "Wall and path", WIDTH_WALL, WIDTH_PATH
        for x in xrange(0, cells_wide):
            for z in xrange(0, cells_depth):
                px = (x * CELLSIZE)
                pz = (z * CELLSIZE)
                px_mid = px + (CELLSIZE >> 1)  # Relative mid point location in space for this cell
                pz_mid = pz + (CELLSIZE >> 1)  # Relative mid point location in space for this cell
                filler(level, pattern, air_palette, (box.minx + px, box.miny, box.minz + pz),
                           (CELLSIZE, box_height, CELLSIZE))

                # Based on what paths are open, we must conditionally render the maze walls

                if self.cell_visited(x, z):
                    #  Corners
                    filler(level, pattern, palette, (box.minx + px, box.miny, box.minz + pz),
                           (WIDTH_WALL, box_height, WIDTH_WALL))
                    filler(level, pattern, palette, (box.minx + px + CELLSIZE - WIDTH_WALL, box.miny, box.minz + pz),
                           (WIDTH_WALL, box_height, WIDTH_WALL))
                    filler(level, pattern, palette,
                           (box.minx + px + CELLSIZE - WIDTH_WALL, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL),
                           (WIDTH_WALL, box_height, WIDTH_WALL))
                    filler(level, pattern, palette, (box.minx + px, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL),
                           (WIDTH_WALL, box_height, WIDTH_WALL))

                    #  Exits
                    if self.cell_exit_north(x, z) == False:
                        filler(level, pattern, palette,
                               (box.minx + px + WIDTH_WALL, box.miny, box.minz + pz),
                               (WIDTH_PATH, box_height, WIDTH_WALL))
                    if self.cell_exit_south(x, z) == False:
                        filler(level, pattern, palette,
                               (box.minx + px + WIDTH_WALL, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL ),
                               (WIDTH_PATH, box_height, WIDTH_WALL))
                    if self.cell_exit_west(x, z) == False:
                        filler(level, pattern, palette,
                               (box.minx + px, box.miny, box.minz + pz + WIDTH_WALL),
                               (WIDTH_WALL, box_height, WIDTH_PATH))
                    if self.cell_exit_east(x, z) == False:
                        filler(level, pattern, palette,
                               ((box.minx + px + CELLSIZE - WIDTH_WALL), box.miny, box.minz + pz + WIDTH_WALL),
                               (WIDTH_WALL, box_height, WIDTH_PATH))
                else:
                    filler(level, pattern, palette, (box.minx + px, box.miny, box.minz + pz),
                           (CELLSIZE, box_height, CELLSIZE))

    def render_to_minecraft_simple(self, level, box, cells_wide, cells_depth, CELLSIZE, palette, pattern):
        if self.generated == False:
            self.generate(None)

        box_height = box.maxy-box.miny

        WIDTH_PATH = 1
        WIDTH_WALL = (CELLSIZE-WIDTH_PATH)>>1
        print "Wall and path", CELLSIZE, WIDTH_WALL, WIDTH_PATH, box.minx, box.maxx, box.miny, box.maxy, box.minz, box.maxz
        for x in xrange(0, cells_wide):
            for z in xrange(0, cells_depth):
                px = (x * CELLSIZE)
                pz = (z * CELLSIZE)
                px_mid = px + (CELLSIZE >> 1)  # Relative mid point location in space for this cell
                pz_mid = pz + (CELLSIZE >> 1)  # Relative mid point location in space for this cell

                # Based on what paths are open, we must conditionally render the maze walls

                if self.cell_visited(x, z):
                    #  Corners
                    filler(level, pattern, palette, (box.minx + px, box.miny, box.minz + pz),
                           (WIDTH_WALL, box_height, WIDTH_WALL))
                    filler(level, pattern, palette, (box.minx + px + CELLSIZE - WIDTH_WALL, box.miny, box.minz + pz),
                           (WIDTH_WALL, box_height, WIDTH_WALL))
                    filler(level, pattern, palette,
                           (box.minx + px + CELLSIZE - WIDTH_WALL, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL),
                           (WIDTH_WALL, box_height, WIDTH_WALL))
                    filler(level, pattern, palette, (box.minx + px, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL),
                           (WIDTH_WALL, box_height, WIDTH_WALL))

                    #  Exits
                    if self.cell_exit_north(x, z) == False:
                        filler(level, pattern, palette,
                               (box.minx + px + WIDTH_WALL, box.miny, box.minz + pz),
                               (WIDTH_PATH, box_height, WIDTH_WALL))
                    if self.cell_exit_south(x, z) == False:
                        filler(level, pattern, palette,
                               (box.minx + px + WIDTH_WALL, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL ),
                               (WIDTH_PATH, box_height, WIDTH_WALL))
                    if self.cell_exit_west(x, z) == False:
                        filler(level, pattern, palette,
                               (box.minx + px, box.miny, box.minz + pz + WIDTH_WALL),
                               (WIDTH_WALL, box_height, WIDTH_PATH))
                    if self.cell_exit_east(x, z) == False:
                        filler(level, pattern, palette,
                               ((box.minx + px + CELLSIZE - WIDTH_WALL), box.miny, box.minz + pz + WIDTH_WALL),
                               (WIDTH_WALL, box_height, WIDTH_PATH))
                else:
                    filler(level, pattern, palette, (box.minx + px, box.miny, box.minz + pz),
                           (CELLSIZE, box_height, CELLSIZE))

    def layout_to_boxes(self, box, cells_wide, cells_depth, CELLSIZE):
        if self.generated == False:
            self.generate(None)
        boxes = []
        paths = []

        #  Create bounding boxes for the areas that are 'solid' and the areas that are 'paths'
        box_height = box.maxy-box.miny


        WIDTH_PATH = CELLSIZE>>2
        WIDTH_WALL = int(ceil((CELLSIZE-WIDTH_PATH)/2))
        print "Wall and path", WIDTH_WALL, WIDTH_PATH
        for x in xrange(0, cells_wide):
            for z in xrange(0, cells_depth):
                px = (x * CELLSIZE)
                pz = (z * CELLSIZE)
                px_mid = px + (CELLSIZE >> 1)  # Relative mid point location in space for this cell
                pz_mid = pz + (CELLSIZE >> 1)  # Relative mid point location in space for this cell

                # Based on what paths are open, we must conditionally render the maze walls

                if self.cell_visited(x, z):
                    #  Corners
                    boxes.append(pymclevel.BoundingBox((box.minx + px, box.miny, box.minz + pz),
                           (WIDTH_WALL, box_height, WIDTH_WALL)))
                    boxes.append(pymclevel.BoundingBox((box.minx + px + CELLSIZE - WIDTH_WALL, box.miny, box.minz + pz),
                           (WIDTH_WALL, box_height, WIDTH_WALL)))
                    boxes.append(pymclevel.BoundingBox(
                           (box.minx + px + CELLSIZE - WIDTH_WALL, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL),
                           (WIDTH_WALL, box_height, WIDTH_WALL)))
                    boxes.append(pymclevel.BoundingBox((box.minx + px, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL),
                           (WIDTH_WALL, box_height, WIDTH_WALL)))

                    paths.append(pymclevel.BoundingBox((box.minx + px + WIDTH_WALL, box.miny, box.minz + pz + WIDTH_WALL),
                           (WIDTH_PATH, box_height, WIDTH_PATH)))

                    #  Exits
                    if self.cell_exit_north(x, z) == False:
                        boxes.append(pymclevel.BoundingBox(
                               (box.minx + px + WIDTH_WALL, box.miny, box.minz + pz),
                               (WIDTH_PATH, box_height, WIDTH_WALL)))
                    else:
                        paths.append(pymclevel.BoundingBox(
                               (box.minx + px + WIDTH_WALL, box.miny, box.minz + pz),
                               (WIDTH_PATH, box_height, WIDTH_WALL)))

                    if self.cell_exit_south(x, z) == False:
                        boxes.append(pymclevel.BoundingBox(
                               (box.minx + px + WIDTH_WALL, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL ),
                               (WIDTH_PATH, box_height, WIDTH_WALL)))
                    else:
                        paths.append(pymclevel.BoundingBox(
                               (box.minx + px + WIDTH_WALL, box.miny, box.minz + pz + CELLSIZE - WIDTH_WALL ),
                               (WIDTH_PATH, box_height, WIDTH_WALL)))
                    if self.cell_exit_west(x, z) == False:
                        boxes.append(pymclevel.BoundingBox(
                               (box.minx + px, box.miny, box.minz + pz + WIDTH_WALL),
                               (WIDTH_WALL, box_height, WIDTH_PATH)))
                    else:
                        paths.append(pymclevel.BoundingBox(
                               (box.minx + px, box.miny, box.minz + pz + WIDTH_WALL),
                               (WIDTH_WALL, box_height, WIDTH_PATH)))
                    if self.cell_exit_east(x, z) == False:
                        boxes.append(pymclevel.BoundingBox(
                               ((box.minx + px + CELLSIZE - WIDTH_WALL), box.miny, box.minz + pz + WIDTH_WALL),
                               (WIDTH_WALL, box_height, WIDTH_PATH)))
                    else:
                        paths.append(pymclevel.BoundingBox(
                            ((box.minx + px + CELLSIZE - WIDTH_WALL), box.miny, box.minz + pz + WIDTH_WALL),
                            (WIDTH_WALL, box_height, WIDTH_PATH)))
                else:
                    boxes.append(pymclevel.BoundingBox((box.minx + px, box.miny, box.minz + pz),
                           (CELLSIZE, box_height, CELLSIZE)))

        return (boxes, paths)


class TileEntityHelper:
    def __init__(self):
        pass
        
    def placeMobSpawner(self, level, type, x, y, z):
        CHUNKSIZE = 16
        SPAWNER = 52
        
        if level.blockAt(x,y,z) == SPAWNER: # Don't try to create a duplicate set of NBT - it confuses the game.
            self.remove_tile_entity_nbt(level, x, y, z)  #  Prepare the chunk for this object
            #  level.setBlockAt(x,y,z,SPAWNER)
            #  level.setBlockDataAt(x,y,z,0)
            
            control = TAG_Compound()
            control["x"] = TAG_Int(x)
            control["y"] = TAG_Int(y)
            control["z"] = TAG_Int(z)
            # control["id"] = TAG_String("minecraft:mob_spawner")

            nbt = self.makeMobSpawnerNBT(type)
            for key in nbt.keys():
                control[key] = nbt[key]
            
            try:
                chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
                chunka.TileEntities.append(control)
                chunka.dirty = True
            except ChunkNotPresent:
                print "ChunkNotPresent",(int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE)
        
    def createSign(self, level, x, y, z, texts): #abrightmoore - convenience method. Due to Jigarbov - this is not a Sign.
        # This is Java only. Bedrock has one line of text with line breaks.
        CHUNKSIZE = 16
        STANDING_SIGN = 63
        SIGN = 68
        SIGN_IDS = [ SIGN, STANDING_SIGN ]

        if level.blockAt(x,y,z) in SIGN_IDS: # Don't try to create a duplicate set of NBT - it confuses the game.
            self.remove_tile_entity_nbt(level, x, y, z)  #  Prepare the chunk for this object
            # level.setBlockAt(x,y,z,STANDING_SIGN)
            # level.setBlockDataAt(x,y,z,randint(0,15))
            # setBlock(level, (STANDING_SIGN,randint(0,15)), x, y, z)
            # level.setBlockAt(x,y-1,z,1)
            # level.setBlockDataAt(x,y-1,z,0)
            # setBlock(level, (1,0), x, y-1, z)
            control = TAG_Compound()
            # control["TileEntity"] = TAG_String("minecraft:sign")
            control["x"] = TAG_Int(x)
            control["Text4"] = TAG_String("{\"text\":\""+texts[3]+"\"}")
            control["y"] = TAG_Int(y)
            control["Text3"] = TAG_String("{\"text\":\""+texts[2]+"\"}")
            control["z"] = TAG_Int(z)
            control["Text2"] = TAG_String("{\"text\":\""+texts[1]+"\"}")
            control["id"] = TAG_String("minecraft:sign")
            control["Text1"] = TAG_String("{\"text\":\""+texts[0]+"\"}")
            
            try:
                chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
                chunka.TileEntities.append(control)
                chunka.dirty = True
            except ChunkNotPresent:
                print "ChunkNotPresent",(int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE)

    def remove_tile_entity_nbt(self, level, x, y, z):
        CHUNKSIZE = 16
        try:
            chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
            new_list = []
            for e in chunka.TileEntities:
                if "x" in e and "y" in e and "z" in e:
                    if e["x"].value == x and e["y"].value == y and e["z"].value == z:
                        chunka.TileEntities.remove(e)
                        break
                    else:
                        new_list.append(e)
            # chunka.TileEntities = new_list
        except ChunkNotPresent:
            print "ChunkNotPresent",(int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE),"at world pos",x,z
            
    def populateChestWithItems(self, level, things, x, y, z):
        CHUNKSIZE = 16
        CHEST = [54, 146]  #  Chest IDs
        
        if level.blockAt(x,y,z) in CHEST: # Don't try to create a duplicate set of NBT - it confuses the game.
            self.remove_tile_entity_nbt(level, x, y, z)  #  Prepare the chunk for this object
            #  level.setBlockAt(x,y,z,CHEST)
            #  level.setBlockDataAt(x,y,z,randint(2,5))

            control = TAG_Compound()
            control["x"] = TAG_Int(x)
            control["y"] = TAG_Int(y)
            control["z"] = TAG_Int(z)
            control["id"] = TAG_String("minecraft:chest")
            control["Lock"] = TAG_String("")
            items = TAG_List()
            control["Items"] = items
            slot = 0
            #  print things
            for thing in things:
                if True:
                    item = TAG_Compound()
                    items.append(item)
                    item["Slot"] = TAG_Byte(slot)
                    slot += 1
                    for key in thing.keys():
                        item[key] = thing[key]
            
            try:
                chunka = level.getChunk((int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE))
                chunka.TileEntities.append(control)
                chunka.dirty = True
            except ChunkNotPresent:
                print "ChunkNotPresent",(int)(x/CHUNKSIZE), (int)(z/CHUNKSIZE)

    def makeItemNBTWithDefaults(self, id):
        return self.makeItemNBT(id, 1, 0)

    def makeItemNBT(self, id, count, damage):
        '''
            Prepare an item of the form:
        
        TAG_Compound({
          "Slot": TAG_Byte(21),
          "id": TAG_String(u'minecraft:iron_boots'),
          "Count": TAG_Byte(1),
          "Damage": TAG_Short(0),
        }),
        '''
        
        item = TAG_Compound()
        item["id"] = TAG_String("minecraft:"+id)
        item["Count"] = TAG_Byte(int(count))
        item["Damage"] = TAG_Short(int(damage))
        return item

    def item_lore(self, item, lore):
        '''
            Prepare an item of the form:
        
            TAG_Compound({
              "Slot": TAG_Byte(1),
              "id": TAG_String(u'minecraft:diamond_sword'),
              "Count": TAG_Byte(1),
              "tag": TAG_Compound({
                "display": TAG_Compound({
                  "Lore": TAG_List([
                    TAG_String(u'"A legendary weapon"'),
                  ]),
                }),
              }),
              "Damage": TAG_Short(0),
            }),
        '''

        if "tag" not in item:
            item["tag"] = TAG_Compound()
        
        item["tag"]["display"] = TAG_Compound()
        item["tag"]["display"]["Lore"] = TAG_List()
        for l in lore:
            item["tag"]["display"]["Lore"].append(TAG_String(l))
        return item

    def item_name(self, item, name):
        if "tag" not in item:
            item["tag"] = TAG_Compound()
        
        if "display" not in item["tag"]:
            item["tag"]["display"] = TAG_Compound()
        item["tag"]["display"]["Name"] = TAG_String(name)  #  Obsolete?
        item["tag"]["display"]["CustomName"] = TAG_String(name)
        # print "NAMED: "+item["tag"]["display"]["Name"].value
        # print item
        return item       

    def item_enchant(self, item, enchants):
        '''
            Prepare an item of the form:
        
            TAG_Int(200) TAG_Int(4) TAG_Int(301) TAG_Compound({
              "x": TAG_Int(200),
              "y": TAG_Int(4),
              "z": TAG_Int(301),
              "Items": TAG_List([
                TAG_Compound({
                  "Slot": TAG_Byte(0),
                  "id": TAG_String(u'minecraft:golden_sword'),
                  "Count": TAG_Byte(1),
                  
                  "tag": TAG_Compound({
                    "ench": TAG_List([
                      TAG_Compound({
                        "lvl": TAG_Short(1),
                        "id": TAG_Short(50),
                      }),
                      TAG_Compound({
                        "lvl": TAG_Short(2),
                        "id": TAG_Short(17),
                      }),
                    ]),
                    "RepairCost": TAG_Int(3),
                    "display": TAG_Compound({
                      "Name": TAG_String(u'Firebrand'),
                    }),
                  }),
                  
                  "Damage": TAG_Short(0),
                }),
              ]),
              "id": TAG_String(u'minecraft:chest'),
              "Lock": TAG_String(u''),
            })
        }),
        '''
        if "tag" not in item:
            item["tag"] = TAG_Compound()
            
        l = TAG_List()
        for id, lvl in enchants:
            m = TAG_Compound()
            m["lvl"] = TAG_Short(lvl)
            m["id"] = TAG_Short(id)
            l.append(m)
        item["tag"]["ench"] = l
        
        return item



    def makeBookNBT(self, texts):
        book = TAG_Compound()
        book["id"] = TAG_String("minecraft:writable_book")
        book["Count"] = TAG_Byte(1)
        book["Damage"] = TAG_Short(0)

        tag = TAG_Compound()
        pages = TAG_List()
        LIMIT = 150
        discarded = False
        for page in texts:
            if len(pages) < LIMIT:
                pages.append(TAG_String(page))
            else:
                discarded = True
        if discarded == True:
            print "WARNING: Book length exceeded "+str(LIMIT)+" pages. Truncated!"
        book["tag"] = tag
        tag["pages"] = pages
        return book

    def makeMobSpawnerNBT(self, type):
        obj = TAG_Compound()
        obj["id"] = TAG_String("minecraft:mob_spawner")
        obj["MaxNearbyEntities"] = TAG_Short(6)
        obj["RequiredPlayerRange"] = TAG_Short(8)
        obj["SpawnCount"] = TAG_Short(1)
        obj["MaxSpawnDelay"] = TAG_Short(800)
        obj["Delay"] = TAG_Short(371)
        obj["SpawnRange"] = TAG_Short(4)
        obj["MinSpawnDelay"] = TAG_Short(200)
        spawnData = TAG_Compound()
        obj["SpawnData"] = spawnData
        spawnData["id"] = TAG_String(type)
        
        spawnPotentials = TAG_List()
        obj["SpawnPotentials"] = spawnPotentials
        entity = TAG_Compound()
        spawnPotentials.append(entity)

        entity["Entity"] = TAG_Compound()
        entity["Entity"]["id"] = TAG_String(type)
        entity["Weight"] = TAG_Int(1)
        
        return obj
        


def perform( level, box, options ):
    world = World( level, box )
    
    log( "SIMULATION STARTING" )
    simulate( world )
    log( "SIMULATION COMPLETE" )
    log( "Saving..." )
    level.saveInPlace()
    log( "Saved, and done." )

def simulate( world ):
    '''
        Given the environment, explore and develop it into a settlement
    '''
    width, height, depth = world.get_build_area()
    #  log( [width, height, depth] ) 
    
    #  Find the centre of the selected area
    cx, cy, cz = world.get_centre_build_area()
    px, py, pz = cx, world.get_height_here((cx, world.box.maxy, cz), [0]), cz
    
    # Quantise the area beneath the start spot in chunks
    height = py - world.box.miny
    if height < 1:
        print "Please try again with a selection that includes the world surface"
    width = world.box.maxx-world.box.minx
    depth = world.box.maxz-world.box.minz
    roomsize_x = 16
    roomsize_y = 8
    roomsize_z = 16
    
    num_rooms_x = int(width/roomsize_x)
    num_rooms_z = int(depth/roomsize_z)
    num_rooms_y = int(height/roomsize_y)-1
    if num_rooms_y < 1:
        num_rooms_y = 1
    
    the_complex = []
    for i in xrange(0, num_rooms_y):
        maze = Maze((num_rooms_x, num_rooms_z), random.randint(-999999999,999999999))
        maze.generate(None)
        print "Generated maze? ",maze.generated
        # box = pymclevel.BoundingBox((world.box.minx, world.box.miny+i*roomsize_y, world.box.minz),(num_rooms_x*roomsize_x, roomsize_y, num_rooms_z*roomsize_z))
        # maze.render_to_minecraft(world.level, box, num_rooms_x, num_rooms_z, roomsize_y, palette, pattern)
        the_complex.append(maze)
    # I now have several layers of mazes
    # For each maze cell, render an underground environment with appropriate elements.


    #  Modify the maze so there are guaranteed to be some interesting transit areas
    
    x = random.randint(1, num_rooms_x-2)
    z = random.randint(1, num_rooms_z-2)
    # print num_rooms_y, height, roomsize_y
    for i in xrange(0, 1):  #  Add a couple of vertical shafts if there's enough space
        for y in xrange(0, random.randint(1, num_rooms_y-1)):
            if 0 < x < num_rooms_x and 0 < z < num_rooms_z and 0 < y < num_rooms_y:  #  Bounds check
                the_complex[y].cell_make_exit_east(x, z)
                the_complex[y].cell_make_exit_west(x, z)
                the_complex[y].cell_make_exit_north(x, z)
                the_complex[y].cell_make_exit_south(x, z)

    print "Please wait... digging holes and laying bricks."

    #  Blocky environment substrate first.
    items = []
    b = Building(world, (cx, py, pz))
    size = (roomsize_x, roomsize_y, roomsize_z)
    if True:

        for y in xrange(0, num_rooms_y):
            print "Constructing layer ", y+1, " of ", num_rooms_y
            for z in xrange(0, num_rooms_z):
                for x in xrange(0, num_rooms_x):
                    if the_complex[y].cell_visited(x,z):
                        pos = (world.box.minx+x*roomsize_x, world.box.miny+y*roomsize_y, world.box.minz+z*roomsize_z)
                        
                        # Check if this is likely an area of solid space and proceed if it is.
                        tx, ty, tz = pos
                        sx, sy, sz = size
                        if world.block_at((tx, ty, tz), True) != 0 and world.block_at((tx+sx-1, ty+sy-1, tz+sz-1), True) != 0:
                            exit_north = the_complex[y].cell_exit_north(x,z)
                            exit_south = the_complex[y].cell_exit_south(x,z)
                            exit_east = the_complex[y].cell_exit_east(x,z)
                            exit_west = the_complex[y].cell_exit_west(x,z)
                            exit_up = False
                            if random.randint(1, 10) == 1:
                                exit_up = True
                            exit_down = False
                            if random.randint(1, 10) == 1:
                                exit_down = True
                                
                            if exit_east and exit_west and exit_south and exit_north and y > 0:  #  These intersections are ways to get to the next level
                                exit_down = True
                                
                            # Here's where the magic has to happen. Each cell of the underground settlement needs to be interesting and
                            #  to contribute to the narrative.
                            # item_locations = b.build_simple_room(pos, size, exit_north, exit_south, exit_east, exit_west, exit_up, exit_down)
                            
                            if exit_east and exit_west and exit_north and exit_south and exit_down and y > 0:
                                item_locations = b.build_room_from_template(pos, size, exit_north, exit_south, exit_east, exit_west, exit_up, exit_down, random.choice(Building.room_of_intersection))
                                # Purge the ground...
                                tx, ty, tz = pos
                                # world.fill(pymclevel.BoundingBox((tx+1, ty-1, tz+1), (roomsize_x-2, 1, roomsize_z-2)), world.materials.air_for_building)
                                world.level.copyBlocksFrom(world.level, pymclevel.BoundingBox((tx+1, ty-2, tz+1), (roomsize_x-2, 1, roomsize_z-2)), (tx+1, ty-1, tz+1))
                            elif exit_up or (x == (num_rooms_x>>1) and z == (num_rooms_z>>1) and y == num_rooms_y-1): # Caters for the starting/entry to the complex
                                item_locations = b.build_room_from_template(pos, size, exit_north, exit_south, exit_east, exit_west, exit_up, exit_down, random.choice(Building.room_of_up))
                                # Purge the ground above...
                                tx, ty, tz = pos
                                # world.fill(pymclevel.BoundingBox((tx+(roomsize_x>>1)-2, ty+roomsize_y, tz+(roomsize_z>>1)-2), (4, 4, 4)), world.materials.air_for_building)
                                # Add in the missing stair section to get to the floor on the room above:
                                b.build_detail_from_template((tx, ty+roomsize_y, tz), size, random.choice(Building.detail_son_of_up))
                                #world.level.copyBlocksFrom(world.level, pymclevel.BoundingBox((tx+1, ty+roomsize_y, tz+1), (roomsize_x-2, 1, roomsize_z-2)), (tx+1, ty-1, tz+1))
                                # Add walls to prevent egress according to the maze layout
                                tx, ty, tz = pos
                                if not exit_east:  #  Block off east
                                    world.fill(pymclevel.BoundingBox((tx+roomsize_x-1, ty, tz), (1, roomsize_y, roomsize_z)), world.materials.stones_for_building)
                                if not exit_west:  #  Block off west
                                    world.fill(pymclevel.BoundingBox((tx, ty, tz), (1, roomsize_y, roomsize_z)), world.materials.stones_for_building)
                                if not exit_north:  #  Block off north
                                    world.fill(pymclevel.BoundingBox((tx, ty, tz), (roomsize_x, roomsize_y, 1)), world.materials.stones_for_building)
                                if not exit_south:  #  Block off south
                                    world.fill(pymclevel.BoundingBox((tx, ty, tz+roomsize_z-1), (roomsize_x, roomsize_y, 1)), world.materials.stones_for_building)
                                if exit_up:
                                    pass
                                    # world.fill(pymclevel.BoundingBox((tx+(roomsize_x>>1)-2, ty+roomsize_y-1, tz+(roomsize_z>>1)-2), (4, 2, 4)), world.materials.air_for_building)
                                if exit_down:
                                    world.fill(pymclevel.BoundingBox((tx+(roomsize_x>>1)-2, ty-1, tz+(roomsize_z>>1)-2), (4, 5, 4)), world.materials.air_for_building)  #  clear enough space to see the hole.
                                    world.fill(pymclevel.BoundingBox((tx+(roomsize_x>>1)-2, ty-1, tz+(roomsize_z>>1)-2), (4, 2, 4)), world.materials.trapdoors_for_building)  #  Stay away from that Trapdoor

                            else:  #  General purpose room
                                roomtype = random.choice(Building.room_of_general_purpose)
                                if y == 0 and random.randint(1,100) > 65: # Lowest level can hold the vaults with lots of treasure
                                    roomtype = random.choice(Building.room_of_vault)
                                item_locations = b.build_room_from_template(pos, size, exit_north, exit_south, exit_east, exit_west, exit_up, exit_down, roomtype)
                                for item in item_locations:
                                    items.append(item)
                                # Add walls to prevent egress according to the maze layout
                                tx, ty, tz = pos
                                if not exit_east:  #  Block off east
                                    world.fill(pymclevel.BoundingBox((tx+roomsize_x-1, ty, tz), (1, roomsize_y, roomsize_z)), world.materials.stones_for_building)
                                if not exit_west:  #  Block off west
                                    world.fill(pymclevel.BoundingBox((tx, ty, tz), (1, roomsize_y, roomsize_z)), world.materials.stones_for_building)
                                if not exit_north:  #  Block off north
                                    world.fill(pymclevel.BoundingBox((tx, ty, tz), (roomsize_x, roomsize_y, 1)), world.materials.stones_for_building)
                                if not exit_south:  #  Block off south
                                    world.fill(pymclevel.BoundingBox((tx, ty, tz+roomsize_z-1), (roomsize_x, roomsize_y, 1)), world.materials.stones_for_building)
                                if exit_up:
                                    world.fill(pymclevel.BoundingBox((tx+(roomsize_x>>1)-2, ty+roomsize_y-1, tz+(roomsize_z>>1)-2), (4, 2, 4)), world.materials.air_for_building)
                                if exit_down:
                                    world.fill(pymclevel.BoundingBox((tx+(roomsize_x>>1)-2, ty-1, tz+(roomsize_z>>1)-2), (4, 5, 4)), world.materials.air_for_building)  #  clear enough space to see the hole.
                                    #  TODO: Stairs down
                                else:  # Central feature since there's a ground floor_box
                                    if random.randint(1,100) > 80:  #  Chance of a detail section
                                        tx, ty, tz = pos
                                        item_locations = b.build_detail_from_template((tx, ty, tz), size, random.choice(Building.detail_central_feature))
                                        for item in item_locations:
                                            items.append(item)
                            
    
    # Debug stub - entry
    if False:
        x,y,z = b.pos
        b.pos = (x, y+3, z)
        b.build_gateway()
    
    #  Post-processing... place contents into all the chests and set up the tile entity data. Until this is done, Minecraft won't draw the chest in the world
    count_items = 0
    count_chests = 0
    count_spawners = 0
    count_signs = 0
    teh = TileEntityHelper()
    collectables = []
    for (x, y, z, id, data) in items:
        if id in [54, 146]:  #  It's a chest
            count_chests += 1
            # TODO - enchanted items and lore
            chestItems = []
            for i in xrange(0, random.randint(1,7)):
                chestItems.append(teh.makeItemNBTWithDefaults('bone'))
            for i in xrange(0, random.randint(1,3)):
                chestItems.append(teh.makeItemNBT('gold_nugget',random.randint(1, 16),0))
            num_chestItems = random.randint(3,13)  #  Minecraft may crash if a chunk has too much nbt.
            for i in xrange(0, num_chestItems):
                if random.random() <= 0.7:
                    item = teh.makeItemNBTWithDefaults(random.choice(world.Materials.THINGS))
                    enchants = []
                    for i in xrange(0, random.randint(1,3)):
                        nm, lvl_max, desc, id, match_keys = random.choice(world.Materials.ENCHANTS)
                        lvl = lvl_max
                        if lvl > 1:
                            lvl = random.randint(1, lvl_max)
                        apply_enchant = False
                        for a in match_keys:
                            if a in item["id"].value or random.randint(1,100) > 87: # Occasionally enchant random stuff
                                apply_enchant = True
                                break
                        if apply_enchant == True and random.randint(1,100) <= 7:  #  There are proper rules about what can be enchanted
                            enchants.append((id,lvl))
                    if len(enchants) > 0 and len(collectables) < 16 and random.randint(1,100) == 1:  #  Limit the number of special relics as they impact nbt size in chunks
                        teh.item_enchant(item, enchants)
                        name = world.lore.get_item_name(item, enchants)
                        teh.item_name(item, name)
                        lore = world.lore.get_lore(item, enchants)
                        teh.item_lore(item, lore)  #  What's the history of this item?
                        collectables.append([ name, lore, item["id"].value, (x, y, z) ])
                    chestItems.append(item)
                    count_items += 1
            random.shuffle(chestItems)
            random.shuffle(chestItems)
            random.shuffle(chestItems)
            teh.populateChestWithItems(world.level, chestItems, x, y, z)
        elif id in [52]:  #  It's a monster spawner
            count_spawners += 1
            type = random.choice(world.Materials.MOBTYPES)
            teh.placeMobSpawner(world.level, type, x, y, z)
        elif id in [63, 68]:  #  It's a sign
            count_signs += 1
            teh.createSign(world.level, x, y, z, world.lore.get_sign_texts())
    
    #  The player needs a document on the settlement to understand what to do and what its background is.
    #  -  infiltrate the complex
    #  -  find the vaults on the lowest level. Claim the treasures
    #  -  don't die
    #  -  watch out for the mysterious void
    world.name = world.lore.get_settlement_name()
    
    book_text_instructions = world.lore.get_instructions_book()
    book_instructions = teh.makeBookNBT(book_text_instructions) # Settlement Almanac - location of all the graves with personal stories
    teh.item_lore(book_instructions, ["BOOK OF","INSTRUCTIONS"] )
    book_text_collectables = world.lore.get_collectables_book(collectables)  #  [ name, lore, item["id"].value, (x, y, z) ]
    book_collectables = teh.makeBookNBT(book_text_collectables) # Settlement Almanac - location of all the graves with personal stories
    teh.item_lore(book_collectables, ["BOOK OF","RELICS"] )
	# placeChestWithItems(level, [theBook], cx, y, cz)
    px, py, pz = cx, world.get_height_here((cx, world.box.maxy, cz), [0, 2, 17, 18, 31, 175, 6, 37, 38, 106, 161, 162, 99, 100]), cz+8
    
    instructions_items = b.build_detail_from_template((px-(roomsize_x>>1), py-1, pz-(roomsize_z>>1)), size, random.choice(Building.room_of_instruction))
    
    for (x, y, z, id, data) in instructions_items:
        if id in [54, 146]:  #  It's a chest
            chestItems = []
            chestItems.append(book_instructions)
            chestItems.append(book_collectables)
            chestItems.append(teh.makeItemNBT("torch",64,0))
            chestItems.append(teh.makeItemNBT("torch",64,0))
            chestItems.append(teh.makeItemNBT("torch",64,0))
            chestItems.append(teh.makeItemNBT("ladder",64,0))
            chestItems.append(teh.makeItemNBT("ladder",64,0))
            chestItems.append(teh.makeItemNBT("ladder",64,0))
            chestItems.append(teh.makeItemNBT("golden_helmet",1,0))
            chestItems.append(teh.makeItemNBT("golden_chestplate",1,0))
            chestItems.append(teh.makeItemNBT("golden_leggings",1,0))
            chestItems.append(teh.makeItemNBT("golden_boots",1,0))
            chestItems.append(teh.makeItemNBT("golden_sword",1,0))
            chestItems.append(teh.makeItemNBT("golden_pickaxe",1,0))
            chestItems.append(teh.makeItemNBT("golden_axe",1,0))
            chestItems.append(teh.makeItemNBT("golden_shovel",1,0))
            
            teh.populateChestWithItems(world.level, chestItems, x, y, z)
        elif id in [63, 68]:  #  It's a sign
            texts = [
                "⚔☺ WELCOME ☺⚔",
                "To "+world.name,
                "Open chest for",
                "⛏Instruction books⛏"
            ]
            teh.createSign(world.level, x, y, z, texts)
    
    
    
    #  There needs to be an obvious entry into the halls.
    #  - (x == (num_rooms_x>>1) and z == (num_rooms_z>>1) and y == num_rooms_y-1)
    
    
    # print world.Materials.THINGS
    print num_rooms_x,num_rooms_z,num_rooms_y
    print count_items, " items placed in ", count_chests, " chests, and ",count_spawners," mob spawners placed"
    print "There are "+str(len(collectables))+ " collectables to find: "+str(collectables)
    