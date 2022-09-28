from Lisasfilter import build_traincity_structure, make_empty, build_bridge, build_wall
from pymclevel import BoundingBox, TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Float, TAG_Double, TAG_String, TAG_Long
import Matrix
import random
import math
from Helper import toolbox
import time

# Filter build by


displayName = "Simulation-based village builder"

inputs = (
    #("Type house", ("tower", "tower")),#, "farm", "house", "fountain", "building")),
    ("Max amount of buildings: (0 being no max)", (0, 200)),
    ("Simulation ticks", (30, 1, 50)),
    ("Search area new houses", (20, 16, 30)),
    ("Water", (0.7, 0.0, 1.0)),
    ("Lava", (0.2, 0.0, 1.0)),
    ("Cliffs", (0.1, 0.0, 1.0)),
    ("Scoot", True),
    ("Bridges", False),
    ("City wall", True),
    ("Chronicle", True),
    ("Clear trees", True),
    ("Co-creativity", True),
    #("Stop if 10 mins have passed", False),
)


def perform(level, box, options):
    time_keeping = False #options["Stop if 10 mins have passed"]
    if time_keeping:
        start_time = time.time()
    settlement = Settlement(level, box, options)
    settlement.first_building()
    count = 0
    time_passed = 0
    while count < options["Simulation ticks"] and time_passed < 600:
        count += 1
        settlement.tick()
        if time_keeping:
            time_passed = time.time() - start_time
            print(time_passed)

    if options["Bridges"]:
        settlement.add_bridges_final()
    #if options["Clear trees"]:
        #settlement.remove_trees_final()
    if options["Chronicle"]:
        if count%5 != 0:
            settlement.add_log_chronicle()
        settlement.print_chronicle()
        settlement.place_chronicle()
    if time_keeping and time_passed >= 600:
        print("Simulation cut short to stay within 10 minute time limit")
    pass


class Settlement():
    class Building():
        def __init__(self, type_building, box):  # x, y, z, width, depth, height):
            self.type = type_building
            self.x = box.minx
            self.y = box.miny
            self.z = box.minz
            self.width = box.width
            self.depth = box.length
            self.height = box.height
            self.fanciness = 0
            # self.edge_of_town = True

    def __init__(self, level, box, options, debug=False, time_keeping=False):
        self.level = level
        self.box = box
        self.options = options
        self.smoll_size = 16
        if self.box.length % self.smoll_size != 0 or self.box.width % self.smoll_size != 0 or \
                self.box.length < self.smoll_size*8 or self.box.width < self.smoll_size*8 or self.box.height != 256:
            self.resize_big_box()
            print(self.box.length, self.box.width)
        if self.box.length > 384 or self.box.width > 384:
            self.make_big_box_small()
            print(self.box.length, self.box.width)
        self.buildings = []
        self.build_buildings = []
        self.size_border = options["Search area new houses"]
        self.building_sizes = {"farm": (14, 14, 6), "house": (14, 14, 6), "fountain": (18, 18, 0),
                               "tower": (10, 10, 1), "cleric": (14, 14, 6), "crafter": (14, 14, 6),
                               "smith": (14, 14, 6), "enchanter": (14, 14, 6), "blacksmith": (14, 14, 6),
                               "pasture": (12, 12, 8)}
        self.scooting = options["Scoot"]
        self.clear_trees_bool = options["Clear trees"]
        self.max_buildings = options["Max amount of buildings: (0 being no max)"]
        self.bridges = False
        if self.max_buildings == 0:
            self.max_buildings = 99999
        self.location_weight = 10
        self.needs = {"food": 100, "housing": 100, "jobs": 100, "resources": 100,
                      "social": 100}  # , "social": 0, "protection": 0, "craft": 0, "water": 100}
        self.n_satisfaction = {"food": 0, "housing": 0, "jobs": 0, "resources": 0, "social": 0}
        self.n_multiplier = {"food": 10, "housing": 5, "jobs": 5, "resources": 3, "social": 7}
        self.n_divisor = {"food": 4, "housing": 2, "jobs": 5, "resources": 6, "social": 10}
        self.building_types = {"farm": {"food": 1}, "house": {"housing": 1}, "fountain": {"social": 7},
                               "cleric": {"jobs": 3, "resources": 1}, "crafter": {"jobs": 2, "resources": 5},
                               "smith": {"jobs": 2, "resources": 3}, "enchanter": {"jobs": 1, "resources": 1},
                               "blacksmith": {"jobs": 2, "resources": 2}, "pasture": {"food": 0.5, "resources": 0.5}}
        self.building_bonus = {"farm": {"food": 30}, "house": {"housing": 30}, "fountain": {"social": 50},
                               "cleric": {"jobs": 30, "resources": 10}, "crafter": {"jobs": 20, "resources": 50},
                               "smith": {"jobs": 20, "resources": 30}, "enchanter": {"jobs": 10, "resources": 40},
                               "blacksmith": {"jobs": 20, "resources": 40}, "pasture": {"food": 15, "resources": 15}}
        self.food_production = 0
        self.houses = 0
        self.population = 0
        self.tick_time = 0
        self.occupied = [[False for z in range(self.box.length)] for x in range(self.box.width)]
        self.co_creativity = options["Co-creativity"]
        if options["Co-creativity"]:
            self.check_for_man_made_materials()
        self.score = 0
        self.min_x = 0
        self.max_x = 0
        self.min_z = 0
        self.max_z = 0
        self.old_x_z = []
        self.chached_buildings = []
        self.calculations_done = False
        self.invalid_building_spots = False
        self.debug = debug
        self.time_keeping = time_keeping
        # this can cause problems if we dont update based on where is build
        self.could_not_build_timer = 0
        self.still_build_wall = options["City wall"]
        self.chronicle = options["Chronicle"]
        if self.chronicle:
            self.book = []
            self.book_location = (0, 0, 0)
            self.year = random.randint(450, 550)
            if self.year%10 == 0:
                self.year+=1
        # keep a list of where we can build

    def tick(self):
        self.tick_time += 1
        print("Ticks: " + str(self.tick_time))
        if len(self.buildings) < self.max_buildings:
            self.update_needs()
            if self.debug:
                print("Population: " + str(self.population))
                self.debug_occupied()
            could_build = self.next_building(self.could_not_build_timer)
            if not could_build:
                self.could_not_build_timer += 1
                print(could_build)
            else:
                self.could_not_build_timer = 0
            if self.population > 15 and self.still_build_wall:
                if random.random >0.6:
                    self.still_build_wall = False
                    if self.co_creativity:
                        print("Wall was not build, because co-creativity was enabled")
                    else:
                        self.build_city_wall()
                        if self.chronicle:
                            self.book.append("Because our population was growing, and we were in need for more protection, we build a city wall.")
            if self.chronicle and self.tick_time%5 == 0:
                self.add_log_chronicle()
            print(self.needs)
            return could_build
        else:
            return True

    def add_log_chronicle(self):
        acres = round(float((self.max_x - self.min_x) * (self.max_z - self.min_z)) / 4046, 1)
        self.book.append("In the year " + str(self.year + self.tick_time) + "CE, " + str(self.tick_time) +
                         " years after the village was founded, we have a population of " + str(self.population) +
                         ", " + str(len(self.build_buildings)) + " total buildings, and our village covers " +
                         str(acres) + " acres.")

    def debug_occupied(self):
        for i, line in enumerate(self.occupied):
            for j, element in enumerate(line):
                if element:
                    x = self.box.minx + i
                    z = self.box.minz + j
                    y = toolbox.findSimpleTerrain(self.level, x, z, 1, 255)
                    toolbox.setBlock(self.level, (35, 2), x, y, z)

    def update_needs(self):
        if random.random() < 0.6:
            self.population += 1
        for key in self.needs.keys():
            if self.population < 10:
                if key == "food" or key == "housing":
                    self.needs[key] = max(0, self.needs[key] - (
                            (math.ceil(float(self.population) / self.n_divisor[key]) - self.n_satisfaction[key]) *
                            self.n_multiplier[key]))
            else:
                self.needs[key] = min(101, max(0, self.needs[key] - (
                        (math.ceil(float(self.population) / self.n_divisor[key]) - self.n_satisfaction[key]) *
                        self.n_multiplier[key])))
        pass

    def next_building(self, increment_size_border=0):
        start_time = 0
        calc_time = 0
        valid_time = 0
        need_time = 0
        if self.time_keeping:
            start_time = time.time()
        possible_buildings = self.building_types.keys()  # ["farm", "house"]
        size_border = self.size_border + increment_size_border

        if (not self.calculations_done) or self.invalid_building_spots:
            print("calculating")
            valid_x_z, x_z = self.find_valid_starting_spot(size_border)
            if self.time_keeping:
                valid_time = time.time() - start_time
            best_buildings_and_scores = self.find_best_building_spots(valid_x_z, possible_buildings, x_z[2], x_z[3])
            if self.time_keeping:
                calc_time = time.time() - start_time - valid_time
            # print(best_buildings_and_scores)
            self.chached_buildings = best_buildings_and_scores
        else:
            best_buildings_and_scores = self.chached_buildings
        scores = []
        for i, building in enumerate(best_buildings_and_scores):
            scores.append(self.new_score(possible_buildings[i], building[1]))
        #if self.time_keeping:
            #score_time = time.time() - start_time - calc_time
        if len(scores) == 0:
            return False
        # print(scores)
        max_score_index = scores.index(max(scores))
        if scores[max_score_index] <= 0:
            print("Doing nothing")
            self.calculations_done = True
        else:
            print("Build building")
            print(possible_buildings[max_score_index])
            needs = self.apply_need(possible_buildings[max_score_index])
            self.add_building(possible_buildings[max_score_index],
                                              best_buildings_and_scores[max_score_index][0])
            if self.chronicle:
                reason = " because it was good for "
                if len(needs)==1:
                    reason += needs[0] + "."
                elif len(needs)==2:
                    reason += needs[0] + " and " + needs[1] + "."
                else:
                    reason += needs[0] + ", " + needs[1] + " and " + needs[2] + "."
                self.book.append(str(self.year + self.tick_time) + "CE: We build a " + possible_buildings[max_score_index] + reason)
            #if self.time_keeping:
                #need_time = time.time() - start_time - score_time - calc_time

            self.calculations_done = False
        if self.time_keeping:
            print("Calc time is " + str(calc_time))
            print("Valid time is " + str(valid_time))
        return True


    def find_valid_starting_spot(self, size_border):
        min_building_width = 10
        # size_border = 20
        x_min = max(self.min_x - size_border, self.box.minx)
        z_min = max(self.min_z - size_border, self.box.minz)
        x_max = min(self.max_x + size_border,
                    self.box.maxx - 1) - min_building_width  # To balance where the buildings get placed
        z_max = min(self.max_z + size_border, self.box.maxz - 1) - min_building_width
        #if self.clear_trees_bool:
            #self.clear_trees([x_min, x_max, z_min, z_max])
        valid_x_z = []
        for x in range(x_min, x_max):
            for z in range(z_min, z_max):
                i = x - self.box.minx
                j = z - self.box.minz
                if not self.occupied[i][j]:  # placing[i][j]:
                    if toolbox.findTerrain(self.level, x, z, 1, 255) == -1:
                        self.occupied[i][j] = True
                    else:
                        valid_x_z.append((i, j, x, z))
        return valid_x_z, (x_min, z_min, x_max, z_max)

    def find_best_building_spots(self, valid_x_z, possible_buildings, x_max, z_max, just_pick_a_couple=True,
                                 max_list_buildings=7):
        start_time = 0
        placement_time = 0
        best_buildings_and_scores = []
        if not just_pick_a_couple:
            max_list_buildings = len(valid_x_z)
        invalid_spots = False
        standard_building_placements = None
        standard_building_size = None
        for building in possible_buildings:

            temp_valid_x_z = valid_x_z
            possible_placement_buildings = []
            width, depth = self.determine_building_size(building)
            #print(building)
            if not (building in ["farm", "house", "cleric", "crafter", "smith",
                                 "enchanter" "blacksmith"] and standard_building_placements):
                while len(possible_placement_buildings) < max_list_buildings and len(temp_valid_x_z) > 0:
                    if self.time_keeping:
                        start_time = time.time()
                    i, j, x, z = temp_valid_x_z.pop(random.randint(0, len(temp_valid_x_z) - 1))
                    if x + width < self.box.maxx - 1 and z + depth < self.box.maxz - 1:
                        valid_space = True
                        for m in range(width):  # (min(width+1, len(placing)-i)):
                            for n in range(depth):  # (min(depth+1, len(placing[0])-j)):
                                if self.occupied[i + m][j + n]:
                                    valid_space = False
                                    break
                                elif x + m >= x_max or z + n >= z_max:
                                    if toolbox.findTerrain(self.level, x + m, z + n, 1, 255) == -1:
                                        valid_space = False
                                        self.occupied[i + m][j + n] = True
                                        break
                            else:
                                continue
                            break
                        if valid_space:
                            # add stuff for location score
                            possible_placement_buildings.append(self.determine_costs(x, z, width, depth))
            else:
                #print("Efficiency part 2!")
                possible_placement_buildings = standard_building_placements
                width, depth = standard_building_size
            if self.time_keeping:
                ttime = str(time.time() - start_time)
                #print("Time to find good placement: " + time)
            badness_scores = [building_place[1] for building_place in possible_placement_buildings]
            if len(badness_scores) > 0:
                best_buildings_and_scores.append(
                    possible_placement_buildings[badness_scores.index(min(badness_scores))])
                #print(building)
                if (building in ["farm", "house", "cleric", "crafter", "smith",
                                 "enchanter" "blacksmith"] and not standard_building_placements):
                    #print("Efficiency!")
                    standard_building_placements = possible_placement_buildings
                    standard_building_size = (width, depth)
            else:
                best_buildings_and_scores.append([(0, 0, -1, -1), 100000])
                invalid_spots = True
        self.invalid_building_spots = invalid_spots
        return best_buildings_and_scores


    def build_city_wall(self):
        x_min = self.min_x - 2 - self.box.minx
        x_max = self.max_x + 2 - self.box.minx
        z_min = self.min_z - 2 - self.box.minz
        z_max = self.max_z + 2 - self.box.minz
        mid_point_box = (self.box.minx + int(self.box.width/2), self.box.minz + int(self.box.length/2))
        gate = [(x_min+3+self.box.minx, z_min+self.box.minz), (x_min+3+self.box.minx, z_min+1+self.box.minz), "z"]
        print(gate)
        smallest_distance = (gate[0][0] - mid_point_box[0])**2 + (gate[0][1] - mid_point_box[1])**2
        for x in [x_min, x_max]:
            for z in range(z_min, z_max + 1):
                if 0 < x < self.box.width:
                    if 0 < z < self.box.length:
                        self.occupied[x][z] = True
                    if 0 < z + 1 < self.box.length:
                        self.occupied[x][z] = True
                    if 4 < x < self.box.width-5:
                        if (x+self.box.minx - mid_point_box[0])**2 + (z+self.box.minz - mid_point_box[1])**2 < smallest_distance:
                            smallest_distance = (x - mid_point_box[0])**2 + (z - mid_point_box[1])**2
                            gate = [(x + self.box.minx, z+self.box.minz), (x+self.box.minx, z+1+self.box.minz), "z"]
        for z in [z_min, z_max]:
            for x in range(x_min, x_max + 1):
                if 0 < z < self.box.length:
                    if 0 < x < self.box.width:
                        self.occupied[x][z] = True
                    if 0 < x +1 < self.box.width:
                        self.occupied[x][z] = True
                    if 4 < z < self.box.length-5:
                        if (x+self.box.minx - mid_point_box[0])**2 + (z+self.box.minz - mid_point_box[1])**2 < smallest_distance:
                            smallest_distance = (x - mid_point_box[0])**2 + (z - mid_point_box[1])**2
                            gate = [(x+self.box.minx, z+self.box.minz), (x+self.box.minx+1, z+self.box.minz), "x"]
        print(gate)
        print(self.min_x - 2, self.max_x + 2, self.min_z - 2, self.max_z + 2)
        build_wall(self.min_x - 2, self.max_x + 2, self.min_z - 2, self.max_z + 2, gate, self.level)

    def determine_costs(self, x, z, width, depth):
        height_map = self.get_height_map(x, z, width, depth)
        steepness = self.steepness_score(height_map)
        if steepness < 0:
            print(steepness)
        badness_score = steepness
        return [(x, z, width, depth), badness_score]

    def new_score(self, building_type, effort):
        old_needs = self.needs
        new_needs = self.calculate_new_needs(building_type)
        score = 0
        for need in old_needs.keys():
            score += float(self.a(old_needs[need]) - self.a(new_needs[need]))
        score -= float(effort + 1) / 2000
        return score

    def apply_need(self, building_type):
        old_needs = self.needs
        self.needs = self.calculate_new_needs(building_type)
        changed_needs = []
        for need, value in old_needs.items():
            if self.needs[need] != value:
                changed_needs.append(need)
        return changed_needs


    def calculate_new_needs(self, building_type):
        additions = self.building_bonus[building_type]
        division_factor = 1
        if not building_type in ["farm", "house", "pasture"]:
            division_factor = self.build_buildings.count(building_type) + 1
        old_needs = self.needs.copy()
        for need, bonus in additions.items():
            old_needs[need] = min(100, old_needs[need] + bonus / division_factor)
        return old_needs

    def add_building(self, building_type, (x, z, width, depth)):
        additions = self.building_types[building_type]
        for key, number in additions.items():
            self.n_satisfaction[key] += number
        deep_box = BoundingBox((x, 1, z), (width, 255, depth))
        box = self.find_ground_level(deep_box)
        if self.debug:
            print("House x: " + str(box.minx) + " " + str(box.maxx))
            print("House z: " + str(box.minz) + " " + str(box.maxz))
        self.make_occupied(box)
        if self.clear_trees_bool:
            self.clear_trees((x-20,x+width+20, z-20, z+depth+20))
        self.adjust_minmax_xz(box)
        self.buildings.append(self.Building(building_type, box))
        self.build_buildings.append(building_type)
        build_traincity_structure(self.level, box, building_type)


    def add_bridges_final(self):
        x_raster = []
        z_raster = []
        half_smoll_size = int(self.smoll_size / 2)
        min_bridge_length = 7
        width_brigde = 2
        for x in range(self.box.minx + half_smoll_size, self.box.maxx - half_smoll_size, int(self.smoll_size / 10)):
            z_raster.append(((x, self.box.minz + half_smoll_size), (x, self.box.maxz - half_smoll_size)))
        for z in range(self.box.minz + int(self.smoll_size / 2), self.box.maxz - half_smoll_size,
                       int(self.smoll_size / 10)):
            x_raster.append(((self.box.minx + half_smoll_size, z), (self.box.maxx - half_smoll_size, z)))
        possible_bridges = []
        closeness_counter = 0
        for line in z_raster:
            x = line[0][0]
            if closeness_counter > 0:
                closeness_counter -= 1
            elif self.min_x < x < self.max_x:
                left = line[0][1]
                right = line[1][1]
                largest_brigde = []
                started_bridge = False
                comp_height = -1
                saved_height_left = -1
                saved_height_right = -1
                while left < right:
                    if self.min_z < left < right < self.max_z:
                        height_left = toolbox.findTerrain(self.level, x, left, 0, 200)
                        height_right = toolbox.findTerrain(self.level, x, right, 0, 200)
                        if height_left == height_right and not (
                                height_left == -1 or self.occupied[x - self.box.minx][left - self.box.minz] or
                                self.occupied[x - self.box.minx][right - self.box.minz]) and not started_bridge:
                            started_bridge = True
                            comp_height = height_left
                            largest_brigde = ((x, left), (x, right))
                            saved_height_left = height_left
                            saved_height_right = height_right
                        elif not (started_bridge and not (self.occupied[x - self.box.minx][left - self.box.minz] or
                                                          self.occupied[x - self.box.minx][right - self.box.minz]) and (
                                          height_left == -1 or height_right == -1 or
                                          (saved_height_left - height_left >= min(largest_brigde[0][1] - left, 7) or
                                           saved_height_right - height_right >= min(right - largest_brigde[1][1], 7)))):
                            started_bridge = False
                            comp_height = -1
                            largest_brigde = []
                    left += 1
                    right -= 1
                    #print("z")
                    #print(left, right)
                if len(largest_brigde) > 0 and largest_brigde[1][1] - largest_brigde[0][1] > min_bridge_length:
                    largest_brigde = (largest_brigde[0], largest_brigde[1], comp_height)
                    possible_bridges.append(largest_brigde)
                    closeness_counter = 4
        closeness_counter = 0
        for line in x_raster:
            z = line[0][1]
            if closeness_counter > 0:
                closeness_counter -= 1
            elif self.min_z < z < self.max_z:
                left = line[0][0]
                right = line[1][0]
                largest_brigde = []
                started_bridge = False
                comp_height = -1
                while left < right:
                    if self.min_x < left < right < self.max_x:
                        height_left = toolbox.findTerrain(self.level, left, z, 0, 200)
                        height_right = toolbox.findTerrain(self.level, right, z, 0, 200)
                        if height_left == height_right and not (
                                height_left == -1 or self.occupied[left - self.box.minx][z - self.box.minz] or
                                self.occupied[right - self.box.minx][z - self.box.minz]):
                            started_bridge = True
                            comp_height = height_left
                            largest_brigde = ((left, z), (right, z))
                        elif not (started_bridge and not (self.occupied[left - self.box.minx][z - self.box.minz] or
                                                          self.occupied[right - self.box.minx][z - self.box.minz]) and (
                                          height_left == -1 or height_right == -1 or
                                          (comp_height - height_left >= min(largest_brigde[0][0] - left, 7) or
                                           comp_height - height_right >= min(right - largest_brigde[1][0], 7)))):
                            started_bridge = False
                            comp_height = -1
                            largest_brigde = []
                    left += 1
                    right -= 1
                if len(largest_brigde) > 0 and largest_brigde[1][0] - largest_brigde[0][0] > min_bridge_length:
                    largest_brigde = (largest_brigde[0], largest_brigde[1], comp_height)
                    possible_bridges.append(largest_brigde)
                    closeness_counter = 4
        for possible_bridge in possible_bridges:
            build_bridge(possible_bridge, self.level)


    def adjust_minmax_xz(self, box):
        if box.minx < self.min_x:
            self.min_x = box.minx
        if box.minz < self.min_z:
            self.min_z = box.minz
        if box.maxx > self.max_x:
            self.max_x = box.maxx
        if box.maxz > self.max_z:
            self.max_z = box.maxz

    def first_building(self):
        print("Finding best starting spot")
        deep_box, reasons = self.pick_best_starting_spot()
        print("Found best starting spot")
        if not deep_box:
            print("No house spots found")
            return
        if self.scooting:
            building_box = self.scoot(deep_box, "tower")
        else:
            building_box = self.find_ground_level(deep_box)
        print(building_box.origin)
        #door_position_orientation = self.first_building_door(building_box)
        # print(door_position_orientation)
        self.min_x = building_box.minx
        self.max_x = building_box.maxx
        self.min_z = building_box.minz
        self.max_z = building_box.maxz
        self.old_x_z = [self.min_x, self.max_x, self.min_z, self.max_z]
        make_empty(self.level, building_box)
        build_traincity_structure(self.level, building_box, type="tower")
        self.make_occupied(building_box, building_type="tower")
        #self.buildings.append(self.Building(self.options["Type house"], building_box))
        self.population += 1
        self.houses += 1
        if self.chronicle:
            self.book_location = (building_box.minx+int(building_box.width/2) -1, building_box.miny+1, building_box.minz+int(building_box.length/2))
            self.book.append(str(self.year+self.tick_time) +  "CE: The tower stands at the place our first settler started the city.")
            if len(reasons)==0:
                self.book.append("This spot was chosen, because it was central, and flat compared to the immediate vicinity.")
            else:
                reason = "This spot was chosen because it was close to "
                if len(reasons)==1:
                    reason += reasons[0]+"."
                elif len(reasons)==2:
                    reason += reasons[0] + " and " + reasons[1]+"."
                else:
                    reason += reasons[0] + ", "  + reasons[1]+ " and " + reasons[2] + "."
                self.book.append(reason)
        if self.debug:
            print("First house x: " + str(building_box.minx) + " " + str(building_box.maxx))
            print("First house z: " + str(building_box.minz) + " " + str(building_box.maxz))

    def pick_best_starting_spot(self):
        box = self.box
        level = self.level
        smoll_size = self.smoll_size
        smoll_boxes = []
        possible_placement = []
        for x in range(box.minx, box.maxx, smoll_size):
            for z in range(box.minz, box.maxz, smoll_size):
                smoll_box = BoundingBox((x, box.miny, z), (smoll_size, 255, smoll_size))
                smoll_boxes.append(smoll_box)
                if ((box.minz + 3 * smoll_size) < z < (box.maxz - 3 * smoll_size)) and (
                        (box.minx + 3 * smoll_size) < x < (box.maxx - 3 * smoll_size)):
                    height_map = toolbox.getHeightMap(level, smoll_box)
                    if toolbox.hasValidGroundBlocks(0, smoll_size - 1, 0, smoll_size - 1, height_map):
                        possible_placement.append(True)
                    else:
                        possible_placement.append(False)
                else:
                    possible_placement.append(False)
        places = self.find_water_lava_indexes(smoll_boxes, possible_placement)
        indexes = self.balance_placement_options(places)
        choice = self.choose_middle(possible_placement, indexes)
        reasons = []
        if choice in places[0]:
            reasons.append("water")
        if choice in places[1]:
            reasons.append("lava")
        if choice in places[0]:
            reasons.append("cliffs")
        if choice == -1:
            return None, []
        return smoll_boxes[choice], reasons

    def balance_placement_options(self, places):
        water = self.options["Water"]
        lava = self.options["Lava"]
        cliffs = self.options["Cliffs"]
        sum_locations = water + lava + cliffs
        if sum_locations < 0.01:
            # water = lava = cliffs = 1
            return [item for sublist in places for item in sublist]
        else:
            water = int(self.location_weight * water / sum_locations)
            lava = int(self.location_weight * lava / sum_locations)
            cliffs = int(self.location_weight * cliffs / sum_locations)
            balanced_places = []
            reason_names = []
            for i in range(water):
                balanced_places.append(places[0])
                reason_names.append("water")
            for i in range(lava):
                balanced_places.append(places[1])
                reason_names.append("lava")
            for i in range(cliffs):
                balanced_places.append(places[2])
                reason_names.append("cliffs")
            return [item for sublist in balanced_places for item in sublist]

    def make_occupied(self, box, building_type=None):
        for x in range(box.minx, box.maxx):
            for z in range(box.minz, box.maxz):
                self.occupied[x - self.box.minx][z - self.box.minz] = True

    def choose_middle(self, placement, indexes):
        smoll_size = self.smoll_size
        hat = []
        for i, place in enumerate(placement):
            if place:
                if len(indexes) == 0 or indexes.count(i) > 0:
                    x_score = abs((smoll_size / 2) - i % smoll_size)
                    y_score = abs((smoll_size / 2) - int(i / smoll_size))
                    for j in range((x_score + y_score) + indexes.count(i)): hat.append(i)
        if len(hat) == 0:
            return -1
        return random.choice(hat)

    def find_water_lava_indexes(self, boxes, placement):
        water = 1
        lava = 2
        cliff = 4
        spot_flags = [-1 for z in range(len(boxes))]
        size = 16
        surrounding = [-size - 1, -size, -size + 1, -1, 1, size - 1, size, size + 1]
        valid_water_spots = []
        valid_lava_spots = []
        valid_cliff_spots = []
        for i in range(len(placement)):
            if placement[i]:
                neighbors_water = []
                neighbors_lava = []
                neighbors_cliffs = []
                for sur in surrounding:
                    if spot_flags[i + sur] == -1:
                        spot_flags[i + sur] = 0
                        if self.check_for_water(boxes[i + sur]):
                            spot_flags[i + sur] += water
                        if self.check_for_water(boxes[i + sur], lava=True):
                            spot_flags[i + sur] += lava
                        if self.find_cliff(boxes[i + sur]):
                            spot_flags[i + sur] += cliff
                    temp_flag = spot_flags[i + sur]
                    if temp_flag - cliff >= 0:
                        temp_flag -= cliff
                        neighbors_cliffs.append(True)
                    if temp_flag - lava >= 0:
                        temp_flag -= lava
                        neighbors_lava.append(True)
                    if temp_flag - water >= 0:
                        temp_flag -= water
                        neighbors_water.append(True)
                if neighbors_water.count(True) > 2:
                    valid_water_spots.append(i)
                if neighbors_lava.count(True) > 0:
                    valid_lava_spots.append(i)
                if neighbors_cliffs.count(True) > 0:
                    valid_cliff_spots.append(i)
        return valid_water_spots, valid_lava_spots, valid_cliff_spots

    def find_cliff(self, box, steepness_cutoff=1.5, steepness_range=4, amount=10):
        level = self.level
        height_map = toolbox.getSimpleHeightMap(level, box)
        cliffs = 0
        for i, x in enumerate(range(box.minx, box.maxx - steepness_range)):
            for j, z in enumerate(range(box.minz, box.maxz - steepness_range)):
                x_change = abs(height_map[i][j] - height_map[i + steepness_range][j]) / steepness_range
                y_change = abs(height_map[i][j] - height_map[i][j + steepness_range]) / steepness_range
                if x_change > steepness_cutoff:
                    cliffs += 1
                if y_change > steepness_cutoff:
                    cliffs += 1
                if cliffs > amount:
                    return True
        return False

    def scoot(self, deep_box, type_house):
        new_box = BoundingBox((deep_box.minx - self.smoll_size, deep_box.miny, deep_box.minz - self.smoll_size),
                              (deep_box.width * 3, 255, deep_box.length * 3))
        x = self.building_sizes[type_house][0] + random.randint(0, self.building_sizes[type_house][2])
        z = self.building_sizes[type_house][1] + random.randint(0, self.building_sizes[type_house][2])
        # steepness as low as possible
        height_map = toolbox.getHeightMap(self.level, new_box)
        steepness_score = self.give_steepness_scores(height_map, x, z)
        max = -1000
        max_i = max_j = 0
        for i in range(len(steepness_score)):
            for j in range(len(steepness_score[0])):
                close_to_features_score = self.close_to_feature_score(height_map, i, j, x, z)
                if -1 < steepness_score[i][j]:
                    score = close_to_features_score * 2 - steepness_score[i][j]
                    if score > max:
                        max = score
                        max_i = i
                        max_j = j
        return self.find_ground_level(
            BoundingBox((new_box.minx + max_i, deep_box.miny, new_box.minz + max_j), (x, 255, z)))

    def get_height_map(self, x, z, width, depth):
        box = BoundingBox((x, 1, z,), (width, 255, depth))
        return toolbox.getHeightMap(self.level, box)

    def determine_building_size(self, type_house):
        x = self.building_sizes[type_house][0] + random.randint(0, self.building_sizes[type_house][2])
        z = self.building_sizes[type_house][1] + random.randint(0, self.building_sizes[type_house][2])
        return x, z

    def close_to_feature_score(self, height_map, i, j, x, z):
        score = 0
        if j - 2 > 0 and j + z + 2 < len(height_map[0]):
            for i_x in range(x):

                if height_map[i + i_x][j - 2] == -1:
                    score += 2
                if height_map[i + x - i_x][j + z + 2] == -1:
                    score += 1

        if i - 2 > 0 and i + x + 2 < len(height_map):
            for j_z in range(z):
                if height_map[i - 2][j + j_z] == -1:
                    score += 2
                if height_map[i + x + 2][j + z - j_z] == -1:
                    score += 2
        return score

    def give_steepness_scores(self, height_map, x, z):
        level_changes = [[0 for i in range(len(height_map[0]) - z)] for j in range(len(height_map) - x)]
        for i in range(len(height_map) - x):
            for j in range(len(height_map[0]) - z):
                hm = [height_map[a][j:j + z] for a in range(i, i + x)]  # [arr[i][0:2] for i in range(0,2)]
                level_changes[i][j] = self.steepness_score(hm)
        return level_changes

    def steepness_score(self, hm):
        score = 0
        levels = [item for sublist in hm for item in sublist]
        if levels.count(-1):
            return -1
        else:
            minimum = min(levels)
            for element in levels:
                score += element - minimum
        return score

    def find_ground_level(self, deep_box, median_level=True):
        level = self.level
        min = 256
        max = 0
        all_y = []
        for x in range(deep_box.minx, deep_box.maxx):
            for z in range(deep_box.minz, deep_box.maxz):
                y = toolbox.findTerrain(level, x, z, deep_box.miny, deep_box.maxy)
                if y > 0:
                    all_y.append(y)
                    if y < min:
                        min = y
                if y > max:
                    max = y
        min_y = min
        if median_level:
            max_count = 0
            for i in range(min, max):
                count = all_y.count(i)
                if count > max_count:
                    max_count = count
                    min_y = i
        return BoundingBox((deep_box.minx, min_y + 1, deep_box.minz), (deep_box.width, 255 - min_y, deep_box.length))

    def check_for_water(self, box, min_water_blocks=3, lava=False):
        level = self.level
        air_like = [0, 6, 17, 18, 30, 31, 32, 37, 38, 39, 40, 59, 78, 79, 99, 81, 83, 85, 104, 105, 106, 107, 111, 141,
                    142, 161, 162,
                    175]
        if lava:
            water_like = [10, 11]
        else:
            water_like = [8, 9]
        waters = 0
        for x in range(box.minx, box.maxx):
            for z in range(box.minz, box.maxz):
                for y in xrange(box.maxy - 1, box.miny - 1, -1):
                    if level.blockAt(x, y, z) in air_like:
                        continue
                    elif level.blockAt(x, y, z) in water_like:
                        self.occupied[-box.minx + x][-box.minz + z] = True
                        waters += 1
                        break
                    else:
                        break
                if waters >= min_water_blocks:
                    return True
        return False

    def clear_trees(self, new_x_z):
        air_like = [0, 6, 30, 31, 32, 37, 38, 39, 40, 59, 78, 79, 99, 81, 83, 85, 104, 105, 107, 111, 141,
                    142, 161, 162, 175]
        tree_like = [17, 18, 106]
        for x in range(new_x_z[0], new_x_z[1]):
            for z in range(new_x_z[2], new_x_z[3]):
                if not (x in range(self.old_x_z[0], self.old_x_z[1]) and z in range(self.old_x_z[2], self.old_x_z[3])):
                    for y in range(255, 1, -1):
                        if self.level.blockAt(x, y, z) in air_like:
                            continue
                        elif self.level.blockAt(x, y, z) in tree_like:
                            self.level.setBlockAt(x, y, z, 0)
                            #print("deleting")
                            continue
                        else:
                            break
        if new_x_z[0] < self.old_x_z[0]:
            self.old_x_z[0] = new_x_z[0]
        if new_x_z[1] > self.old_x_z[1]:
            self.old_x_z[1] = new_x_z[1]
        if new_x_z[2] < self.old_x_z[2]:
            self.old_x_z[2] = new_x_z[2]
        if new_x_z[3] > self.old_x_z[3]:
            self.old_x_z[3] = new_x_z[3]

    def remove_trees_final(self):
        air_like = [0, 6, 30, 31, 32, 37, 38, 39, 40, 59, 78, 79, 99, 81, 83, 85, 104, 105, 107, 111, 141,
                    142, 161, 162, 175]
        tree_like = [17, 18, 106]
        for x in range(self.min_x, self.max_x):
            for z in range(self.min_z, self.max_z):
                for y in range(255, 1, -1):
                    if self.level.blockAt(x, y, z) in air_like:
                        continue
                    elif self.level.blockAt(x, y, z) in tree_like:
                        self.level.setBlockAt(x, y, z, 0)
                        #print("deleting")
                        continue
                    else:
                        break

    def a(self, need):
        if need == 0:
            return 100
        return 10 / float(need)

    def resize_big_box(self):
        box_width = self.box.width
        box_length = self.box.length
        while not box_width % self.smoll_size == 0:
            box_width -= 1
        while not box_length % self.smoll_size == 0:
            box_length -= 1
        while box_length < 8 * self.smoll_size:
            box_length += self.smoll_size
        while box_width < 8 * self.smoll_size:
            box_width += self.smoll_size
        self.box = BoundingBox((self.box.minx, 0, self.box.minz), (box_width, 256, box_length))

    def make_big_box_small(self):
        max_size = 384
        box_width = self.box.width
        box_length = self.box.length
        mid_point = (self.box.minx + int(box_width/2), self.box.minz + int(box_length/2))
        if box_length > max_size:
            box_length = max_size
        if box_width > max_size:
            box_width = max_size
        self.box = BoundingBox((mid_point[0]-int(box_width/2), 0, mid_point[1]-int(box_length/2)), (box_width, 256, box_length))

    def print_chronicle(self):
        if not self.chronicle:
            return
        for line in self.book:
            print(line)

    def place_chronicle(self):
        #Code from GEN_Library in the 20XX submission of @TheWorldFoundry
        def placeChestWithItems(level, things, x, y, z):
            CHUNKSIZE = 16
            CHEST = 54

            if level.blockAt(x, y, z) != CHEST:  # Don't try to create a duplicate set of NBT - it confuses the game.
                level.setBlockAt(x, y, z, CHEST)
                level.setBlockDataAt(x, y, z, random.randint(2, 5))

                control = TAG_Compound()
                control["x"] = TAG_Int(x)
                control["y"] = TAG_Int(y)
                control["z"] = TAG_Int(z)
                control["id"] = TAG_String("minecraft:chest")
                control["Lock"] = TAG_String("")
                items = TAG_List()
                control["Items"] = items
                slot = 0
                print things
                for thing in things:
                    # if thing["id"].value != "minecraft:Nothing": # Handle empty slots
                    if True:
                        item = TAG_Compound()
                        items.append(item)
                        item["Slot"] = TAG_Byte(slot)
                        slot += 1
                        for key in thing.keys():
                            item[key] = thing[key]

                try:
                    chunka = level.getChunk((int)(x / CHUNKSIZE), (int)(z / CHUNKSIZE))
                    chunka.TileEntities.append(control)
                    chunka.dirty = True
                except ChunkNotPresent:
                    print "ChunkNotPresent", (int)(x / CHUNKSIZE), (int)(z / CHUNKSIZE)

        def makeBookNBT(texts):
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
                print "WARNING: Book length exceeded " + str(LIMIT) + " pages. Truncated!"
            book["tag"] = tag
            tag["pages"] = pages
            return book

        book_in_world = makeBookNBT(self.book)

        placeChestWithItems(self.level, [book_in_world], self.book_location[0], self.book_location[1], self.book_location[2])

    def check_for_man_made_materials(self):
        man_made = [4, 5, 20, 23, 35, 41, 42, 43, 44, 45, 50, 53, 54, 57, 60, 95, 96, 108, 109, 107, 125, 128, 133, 134,
                    135, 136, 139, 155, 159, 171, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 251]
        air_like = [0, 6, 30, 31, 32, 37, 38, 39, 40, 59, 78, 79, 99, 81, 83, 85, 104, 105, 111, 141,
                    142, 161, 162, 175]
        for x in (self.box.minx, self.box.maxx):
            for z in (self.box.minz, self.box.maxz):
                for y in range(255, 1, -1):
                    if self.level.blockAt(x, y, z) in air_like:
                        continue
                    elif self.level.blockAt(x, y, z) in man_made:
                        self.occupied[x-self.box.minx][z-self.box.minz] = True
                        break
                    else:
                        break

