import random
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from house import *
from little_house import *
from store import *
from field_builder import *


class Cityspace:

    def __init__(self, level, road_width, start_x, start_y, start_z, door, tree_ID, tree_data, wood_ID, wood_data,roof_ID):
        self.level = level
        self.road_width = road_width
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.door = door
        self.tree_ID = tree_ID
        self.tree_data = tree_data
        self.wood_ID = wood_ID
        self.wood_data = wood_data
        self.roof_ID = roof_ID
            

    def build(self):
        lv = self.level
        w = self.road_width
        x = self.start_x
        y = self.start_y
        z = self.start_z
        d = self.door
        t_ID = self.tree_ID
        t_data = self.tree_data
        w_ID = self.wood_ID
        w_data = self.wood_data
        r_ID = self.roof_ID
        sw = 10  #house width
        lw = 5 #little house width
        hw = [0,0] #house width
        fw = [0,0] #field width
        sc = 0 #store counter
        lc = 0 #little house counter
        hc = 0 #house counter
        hlc = 0 
        fc = 0
        ice_f=0
        city = []
        gap = []

        for i in range(w/(sw+3)):
            if 0.5 <= random.random():
                city.append(0)
                sc += 1
                gap.append(0)

        for i in range(len(gap)):
            gap[i]=random.randint(3,5)
        

        for i in range(2):
            #house
            if w >= sc*10+lc*5+sum(fw)+sum(hw)+ice_f+sum(gap) + 17:
                for j in range(int((w-sc*10-lc*5-sum(fw)-sum(hw)-ice_f-sum(gap)-1)/8)):
                    if random.random() < 0.4:
                        hc += 1
                    elif 0.4 <= random.random() and random.random() < 0.5:
                        lc += 1
                        city.append(5)
                        gap.append(random.randint(3,5))
                hw[i] = hc*8+1
            elif w >= sc*10+lc*5+sum(fw)+sum(hw)+ice_f+sum(gap) + 9:
                hw[i] = 9
            if hw[i]>=9:
                city.append(1)
                gap.append(random.randint(3,5))

            #field
            if w> sc*10+lc*5+sum(fw)+sum(hw)+ice_f+sum(gap)+2:
                fw[i] = int(w-sc*10-lc*5-sum(hw)-sum(fw)-ice_f-sum(gap))
                if i==0:
                    if fw[i] >= 3:
                        if fw[i] > 18:
                            fw[i] = 18
                        city.append(2)
                    else:
                        city.append(4)
                    gap.append(random.randint(3,5))
                else:
                    if fw[i] > 18:
                        fw[i] = 18
                    city.append(4)
                    gap.append(random.randint(3,5))


        #print "gap"
        #print gap
        random.shuffle(city)
        city.append(6)

        #print "city"
        #print city

        for i in range(len(city)-1):
            if city[i] == 0:
                store = Store_Builder(lv,x,y,z,d,0,t_ID,t_data,w_ID,w_data,r_ID)
                store.build()
                z += sw+gap[i]
            elif city[i] == 1 and hw[hlc]>0:
                house = House_Builder(lv,x,y,z,d,hw[hlc],0,t_ID,t_data,w_ID,w_data,r_ID)
                house.build()
                z += hw[hlc]+gap[i]
                hlc += 1
            elif city[i] == 2: #and fw[fc]>0:
                f = field(lv,x,y-1,z,9,fw[fc],0,0)
                f.build()
                z += fw[fc]+gap[i]
                fc += 1
            elif city[i] == 4: #and fw[fc]>0:
                f = field(lv,x,y,z,9,fw[fc],4,0)
                f.build()
                z += fw[fc]+gap[i]
                fc += 1
            elif city[i] == 5:
                if d==0:
                    sh = Little_House_Builder(lv,x,y,z,d,0,t_ID,t_data,w_ID,w_data,r_ID)
                    sh.build()
                    f = field(lv,x+5,y,z,4,lw,4,0)
                    f.build()
                else:
                    sh = Little_House_Builder(lv,x+5,y,z,d,0,t_ID,t_data,w_ID,w_data,r_ID)
                    sh.build()
                    f = field(lv,x,y,z,4,lw,4,0)
                    f.build()
                z += lw+gap[i]