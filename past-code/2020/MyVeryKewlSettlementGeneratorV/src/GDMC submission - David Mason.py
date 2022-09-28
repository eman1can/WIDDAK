# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 18:59:03 2020

@author: Drogo
"""

from __future__ import division
import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
import utilityFunctions as uf


#def get__bottom(level,min_y):
#    bottom = []
#    #for point in seed.closest_points:
#        
#    for i in range(0,len(seed.closest_points)):
#         
#        point = seed.closest_points[i]
#        
#        for y in range(150, 0, -1):
#            if level.blockAt(point[0],y,point[1]) in [1,2,3,13]:
#                bottom.append(y)
#                seed.closest_points[i].append(y)
#                break

class Seed():
    def __init__(self,x,z,fake):
        self.id = randint(-100000,100000)
        self.seed_pos = [x,z]
        self.x = x
        self.z = z
        self.closest_points = []
        self.closest_points_2d = []
        self.bottom = []
        # self.col = [randint(0,255),randint(0,255),randint(0,255)]
        self.block = (159, randint(0,15))
        #self.y = y
        self.edge_points = []
        
        self.houses = []
        
        self.ratio = 0
        self.fake = fake
        self.mine = False
        self.center_dist = 0


def get_closest_points(map_points, seeds):
    for point in map_points:
        min_dist = 10000000
        min_seed_index = 0
        
        for s in seeds:
            dist = math.sqrt(((s.seed_pos[0]-point[0])**2)+((s.seed_pos[1]-point[1])**2))
            if dist < min_dist:
                min_dist = dist
                min_seed_index = seeds.index(s)

        seeds[min_seed_index].closest_points.append(point)
        seeds[min_seed_index].closest_points_2d.append((point[0], point[1]))

def get_edges(seeds):      
    for seed in seeds:
        #print("cloest",seed.closest_points[0:10])
        #print("cloest 2d",seed.closest_points_2d[0:10])
        for point in seed.closest_points:
            if (point[0]+1,point[1]) not in seed.closest_points_2d:
                seed.edge_points.append(point)
            elif (point[0]-1,point[1]) not in seed.closest_points_2d:
                seed.edge_points.append(point)
            elif (point[0],point[1]+1) not in seed.closest_points_2d:
                seed.edge_points.append(point)
            elif (point[0],point[1]-1) not in seed.closest_points_2d:
                seed.edge_points.append(point)



def get_edges_2d(points):
    edge = []
    
    for point in points:
        if (point[0]+1,point[1]) not in points:
            edge.append(point)
        elif (point[0]-1,point[1]) not in points:
            edge.append(point)
        elif (point[0],point[1]+1) not in points:
            edge.append(point)
        elif (point[0],point[1]-1) not in points:
            edge.append(point)
            
    return edge


def get_edge_3d(points):

    points_dict = {}
    
    for point in points:
        points_dict[(point[0], point[1])] = point[2]
        
    edge = get_edges_2d(points_dict)
    edge_3d = []
    
    for point in edge:
        edge_3d.append((point[0], point[1], points_dict[point]))
        
    return edge_3d


def get_next_edge(current,edge,path,seed,path_2d):


    min_d = 100000
    min_angle_point = ()
    
    #[(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
    #[(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1)]
    
    for (i,j) in [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]+[(0,2),(1,2),(2,2),(2,1),(2,0),(2,-1),(2,-2),(1,-2),(0,-2),(-1,-2),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-1,2)]:
        if (current[0]+i, current[1]+j, current[2]) in edge:
            if (current[0]+i, current[1]+j, current[2]) not in path:
                if (current[0]+i, current[1]+j, current[2]+1) not in path and (current[0]+i, current[1]+j, current[2]+2) not in path:
                    if (current[0]+i, current[1]+j) not in path_2d[len(path_2d)-5:]:
                        
                        return (current[0]+i, current[1]+j, current[2])

  
            
        
def get_next_layer_edge(current, next_layer, path):
#    potential_next_points = []
#    
#    for i in range(-2,3):
#        for j in range(-2,3):
#            if (current[0]+i, current[1]+j, current[2]-1) in next_layer:
#                potential_next_points.append((current[0]+i, current[1]+j, current[2]-1))
#                
#                
#    return min(potential_next_points, key = lambda x: (x[0]**2) + (x[1]**2))
    
    for (i,j) in [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]:
        if (current[0]+i, current[1]+j, current[2]-1) in next_layer:
            if (current[0]+i, current[1]+j, current[2]) not in path:
                if (current[0]+i, current[1]+j, current[2]+1) not in path:
                    return (current[0]+i, current[1]+j, current[2]-1)
            
    for (i,j) in [(0,2),(1,2),(2,2),(2,1),(2,0),(2,-1),(2,-2),(1,-2),(0,-2),(-1,-2),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-1,2)]:
        if (current[0]+i, current[1]+j, current[2]-1) in next_layer:
            if (current[0]+i, current[1]+j, current[2]) not in path: 
                if (current[0]+i, current[1]+j, current[2]+1) not in path:
                    return (current[0]+i, current[1]+j, current[2]-1)

#    for i in range(-2,3):
#        for j in range(-2,3):
#            if (current[0]+i, current[1]+j, current[2]-1) in next_layer:
#                return (current[0]+i, current[1]+j, current[2]-1) 

    
    
#    if (current[0], current[1], current[2]-1) in next_layer:
#        return (current[0], current[1], current[2]-1)
    
#    if (current[0], current[1]+1, current[2]-1) in next_layer:
#        return (current[0], current[1]+1, current[2]-1)
#    
#    elif (current[0]+1, current[1]+1, current[2]-1) in next_layer:
#        return (current[0]+1, current[1]+1, current[2]-1)
#    
#    elif (current[0]+1, current[1], current[2]-1) in next_layer:
#        return (current[0]+1, current[1], current[2]-1)
#    
#    elif (current[0]+1, current[1]-1, current[2]-1) in next_layer:
#        return (current[0]+1, current[1]-1, current[2]-1)
#    
#    elif (current[0], current[1]-1, current[2]-1) in next_layer:
#        return (current[0], current[1]-1, current[2]-1)
#    
#    elif (current[0]-1, current[1]-1, current[2]-1) in next_layer:
#        return (current[0]-1, current[1]-1, current[2]-1)
#    
#    elif (current[0]-1, current[1], current[2]-1) in next_layer:
#        return  (current[0]-1, current[1], current[2]-1)
#    
#    elif (current[0]-1, current[1]+1, current[2]-1) in next_layer:
#        return (current[0]-1, current[1]+1, current[2]-1)
#    

    print("finding next layer")
    
    
#    if (current[0], current[1]+1, current[2]-1) in next_layer:
#        return (current[0], current[1]+1, current[2]-1)
#    
#    elif (current[0]-1, current[1]+1, current[2]-1) in next_layer:
#        return (current[0]+1, current[1]+1, current[2]-1)
#    
#    elif (current[0]-1, current[1], current[2]-1) in next_layer:
#        return (current[0]+1, current[1], current[2]-1)
#    
#    elif (current[0]-1, current[1]-1, current[2]-1) in next_layer:
#        return (current[0]+1, current[1]-1, current[2]-1)
#    
#    elif (current[0], current[1]-1, current[2]-1) in next_layer:
#        return (current[0], current[1]-1, current[2]-1)
#    
#    elif (current[0]+1, current[1]-1, current[2]-1) in next_layer:
#        return (current[0]-1, current[1]-1, current[2]-1)
#    
#    elif (current[0]+1, current[1], current[2]-1) in next_layer:
#        return  (current[0]-1, current[1], current[2]-1)
#    
#    elif (current[0]+1, current[1]+1, current[2]-1) in next_layer:
#        return (current[0]-1, current[1]+1, current[2]-1)
    



        

def get_bottom(level, box, min_y):
    #bottom_matrix = empty([box.maxx-box.minx, box.maxz-box.minz])
    bottom = {}
    print(box.minx, box.maxx,box.minz, box.maxz)
    for x in range(box.minx, box.maxx):
        for z in range(box.minz, box.maxz):
            for y in range(350, box.miny, -1):
                #print(level.blockAt(x,y,z))
                
                if level.blockAt(x,y,z) in [11,10]:
                    uf.setBlock(level,(49,0), x, y, z)############################
                
                if level.blockAt(x,y,z) in [1,2,3,13,9,11,10,8]:
                    bottom[(x,z)] = y
                    break
                    #print((x,z))
                    #bottom.append([x,y,z])
                    

                    
                            
    #print("gotten_botem",bottom)
    return bottom

class Wall():
    def __init__(self,x1,z1,x2,z2,base_y,orientation,shortest,outside_dir,wall_type):
        self.x1 = x1
        self.z1 = z1
        self.x2 = x2
        self.z2 = z2
        self.y = base_y
        self.orientation = orientation
        self.outside_dir = outside_dir
        self.shortest = shortest
        
        self.blocks = {}
        self.wall_type = wall_type
        self.window_space = []
        self.partitioned_window_spaces = []
        self.windows = []
        self.trim = {}
        
        #print("wall",orientation, x1,z1,x2,z2)
        
        offset=0
        
        if outside_dir[0] == "zz": 
            if outside_dir[1] == "+":
                offset = 0
            elif outside_dir[1] == "-":
               offset = -1
               #self.x1 += 1
        elif outside_dir[0] == "xx": 
            if outside_dir[1] == "+":
               offset = -1
               #self.z1 += 1
            elif outside_dir[1] == "-":
                offset = 0
                
                
                
        if wall_type == "base":
            if x1 == x2:
                for z in range(z1,z2):
                    self.blocks[(x1+offset,z,base_y)] = (98,0)
                    self.blocks[(x1+offset,z,base_y+1)] = (98,0)
                    
            elif z1 == z2:
                for x in range(x1,x2):
                    self.blocks[(x,z1+offset,base_y)] = (98,0)
                    self.blocks[(x,z1+offset,base_y+1)] = (98,0)
                    
        elif wall_type == "tudor":
            
#            if 
#            wall_pallette = 
            
            
            
            if x1 == x2:
                for y in range(0,5):
                    for z in range(z1,z2):
                        if y == 0:
                            if orientation == "xx":
                                block = (17,4)
                            elif orientation == "zz":
                                block = (17,8)
                        else:
                            if z == z1 or z == z2-1:
                                block = (17,0)
                            else:
                                block = (121,0)
                                self.window_space.append([x1,z,y])
                        
                        self.blocks[(x1+offset,z,base_y+2+y)] = block
                        #self.blocks[(x1,z,22+y)] = block

                    
            elif z1 == z2:
                for y in range(0,5):
                    for x in range(x1,x2):
                        if y == 0:
                            if orientation == "xx":
                                block = (17,4)
                            elif orientation == "zz":
                                block = (17,8)
                        
                        else:
                            if x == x1 or x == x2-1:
                                block = (17,0)
                            else:
                                block = (121,0)
                                self.window_space.append([x,z1,y])
                        
                        self.blocks[(x,z1+offset,base_y+2+y)] = block
                        #self.blocks[(x,z1,22+y)] = block
                    
        elif wall_type == "corner":
            for y in range(0,6):
                self.blocks[(x1,z1,base_y+y+2)] = (121,0)
                
        elif wall_type == "False":
            if x1 == x2:
                for z in range(z1,z2):
                    self.blocks[(x1+offset,z,base_y-1)] = (98,0)
                    
            elif z1 == z2:
                for x in range(x1,x2):
                    self.blocks[(x,z1+offset,base_y-1)] = (98,0)
                    
            self.y -= 2
                
                    
      
                    
 
        #print("wall_blocks", self.blocks)

def get_plot_and_base_walls(x,z,width,height,corners,base,bottom):
    x1 = x
    z1 = z
    
    x2 = x1 + width
    z2 = z1 + height
    
    base_ys = []
    for x in range(x1,x2):
        for z in range(z1,z2):
            try:
                base_ys.append((x,z,bottom[(x,z)]))
            except:
                pass
            
    #print(base_ys)
    base_y = min(base_ys, key = lambda x:x[2])[2] + 1       
    
    plot = []
    
    if width >= height:
        xx_shortest = False
        zz_shortest = True
    else:
        xx_shortest = True
        zz_shortest = False
        
    #wall_type = "base"
        
    if base:
        wall_type = "base"
    else:
        wall_type = "False"
                
    if corners == "orth":
        top_xx = Wall(x1,z1,x2,z1,base_y,"xx",xx_shortest,["zz","+"],wall_type)
        bum_xx = Wall(x1,z2,x2,z2,base_y,"xx",xx_shortest,["zz","-"],wall_type)
        
        left_zz = Wall(x1,z1,x1,z2,base_y,"zz",zz_shortest,["xx","-"],wall_type)
        right_zz = Wall(x2,z1,x2,z2,base_y,"zz",zz_shortest,["xx","+"],wall_type)
        
        for x in range(x1,x2):
            for z in range(z1,z2):
                plot.append([x,z,base_y])
        
    elif corners == "diag":
        if width >= height:
            top_xx = Wall(x1+1,z1,x2-1,z1,base_y,"xx",xx_shortest,["zz","+"],wall_type)
            bum_xx = Wall(x1+1,z2,x2-1,z2,base_y,"xx",xx_shortest,["zz","-"],wall_type)
            
            left_zz = Wall(x1,z1+1,x1,z2-1,base_y,"zz",zz_shortest,["xx","-"],wall_type)
            right_zz = Wall(x2,z1+1,x2,z2-1,base_y,"zz",zz_shortest,["xx","+"],wall_type)
            
            for x in range(x1,x2):
                for z in range(z1, z2):
                    plot.append([x,z,base_y])
                    
            plot.remove([x1,z1,base_y])
            plot.remove([x2-1,z1,base_y])
            plot.remove([x1,z2-1,base_y])
            plot.remove([x2-1,z2-1,base_y])
        else:
            top_xx = Wall(x1+1,z1,x2-1,z1,base_y,"xx",xx_shortest,["zz","+"],wall_type)
            bum_xx = Wall(x1+1,z2,x2-1,z2,base_y,"xx",xx_shortest,["zz","-"],wall_type)
            
            left_zz = Wall(x1,z1+1,x1,z2-1,base_y,"zz",zz_shortest,["xx","-"],wall_type)
            right_zz = Wall(x2,z1+1,x2,z2-1,base_y,"zz",zz_shortest,["xx","+"],wall_type)
            
            for x in range(x1,x2):
                for z in range(z1, z2):
                    plot.append([x,z,base_y])
                    
            plot.remove([x1,z1,base_y])
            plot.remove([x2-1,z1,base_y])
            plot.remove([x1,z2-1,base_y])
            plot.remove([x2-1,z2-1,base_y])
    
    walls = [top_xx, bum_xx, left_zz, right_zz]
    
    return walls, plot


def get_top_walls(base_walls, flush, corner_type, rect):
    if not flush:
        flush_offset = 1
    else:
        flush_offset = 0
        
    walls = []
     
    for base_wall in base_walls:
        x1 = base_wall.x1
        z1 = base_wall.z1
        x2 = base_wall.x2
        z2 = base_wall.z2
        
        if base_wall.outside_dir[1] == "+":
            dir_mult = -1
        elif base_wall.outside_dir[1] == "-":
            dir_mult = 1
        
        if base_wall.orientation == "xx":
            wall = Wall(x1,z1+flush_offset*dir_mult,x2,z2+flush_offset*dir_mult,base_wall.y,"xx",base_wall.shortest,base_wall.outside_dir,"tudor")
            walls.append(wall)
            
        elif base_wall.orientation == "zz":
            #pass
            #print("hfshdsfkjhdsfjk")
            wall = Wall(x1-flush_offset*dir_mult,z1,x2-flush_offset*dir_mult,z2,base_wall.y,"zz",base_wall.shortest,base_wall.outside_dir,"tudor")
            walls.append(wall)
            #print(wall.blocks)
            
    if not flush and corner_type == "diag":
        x1 = rect[0]
        z1 = rect[1]
        x2 = rect[2]
        z2 = rect[3]
        
        wall_corner_1 = Wall(x1,z1,x1,z1,base_wall.y,None,False,[None,None],"corner")
        wall_corner_2 = Wall(x2,z1,x2,z1,base_wall.y,None,False,[None,None],"corner")
        wall_corner_3 = Wall(x1,z2,x1,z2,base_wall.y,None,False,[None,None],"corner")
        wall_corner_4 = Wall(x2,z2,x2,z2,base_wall.y,None,False,[None,None],"corner")
        
        walls += [wall_corner_1,wall_corner_2,wall_corner_3,wall_corner_4]
        
    return walls
    
def get_rect(plot,bloat):
    min_x = min(plot, key = lambda x: x[0])[0]-bloat
    min_z = min(plot, key = lambda x: x[1])[1]-bloat
    
    max_x = max(plot, key = lambda x: x[0])[0]+bloat
    max_z = max(plot, key = lambda x: x[1])[1]+bloat
    
    return [min_x,min_z,max_x,max_z]

def get_roof(top_walls,width,height,flush,corner_type,droop):
    
    roof = {}
    
    if not flush:
        width += 2
        height += 2
        
        if corner_type == "diag":
            offset = 2
        else:
            offset = 1
        
    elif corner_type == "diag":
        offset = 1
    else:
        offset = 0
        
    droop_offset = 0
        
    if droop:
        droop_offset = 1
        if width > height:
            height += 2
        elif height > width:
            width += 2

    
    for wall in top_walls:
        if not wall.shortest:
            
            y = max(wall.blocks, key = lambda x: x[2])[2] + 1 
            
            if droop:
                y -= 1
            
            if wall.orientation == "xx":
                
                if wall.outside_dir[1] == "+":
                    block1 = (53,2)
                    block2 = (53,3)

                    for x in range(wall.x1-1-offset, wall.x2+1+offset):
                        for z in range(wall.z1, wall.z1+int(height/2)):
                            roof[(x,z-droop_offset,y+z-wall.z1)] = block1
                            roof[(x,(wall.z1+height)-(z-wall.z1)-1-droop_offset,y+z-wall.z1)] = block2
                            
                            if x == wall.x1-1-offset or x == wall.x2+1+offset-1:
                                if z != wall.z1 and z != wall.z1+int(height/2):
                                    roof[(x,z-droop_offset,y+z-wall.z1-1)] = (53,7)
                                    roof[(x,(wall.z1+height)-(z-wall.z1)-1-droop_offset,y+z-wall.z1-1)] = (53,6)                                
                                
                    
                    if height%2 == 1:
                        for x in range(wall.x1-1-offset, wall.x2+1+offset):
                            roof[(x,wall.z1+int(height/2)-droop_offset,y+int(height/2))] = (126,0)
                            roof[(x,wall.z1+int(height/2)-droop_offset,y+int(height/2)-1)] = (5,0)
                              
                    break
                    
                    
            elif wall.orientation == "zz":
                if wall.outside_dir[1] == "-":
                    block1 = (53,0)
                    block2 = (53,1)
                    
                    #print("dsa",wall.x1, wall.z1)

                    for z in range(wall.z1-1-offset, wall.z2+1+offset):
                        for x in range(wall.x1, wall.x1+int(width/2)):
                            roof[(x-droop_offset,z,y+x-wall.x1)] = block1
                            roof[((wall.x1+width)-(x-wall.x1)-1-droop_offset,z,y+x-wall.x1)] = block2
                        
                            if z == wall.z1-1-offset or z == wall.z2+1+offset-1:
                                if x != wall.x1 and x != wall.x1+int(width/2):
                                    roof[(x-droop_offset,z,y+x-wall.x1-1)] = (53,5) 
                                    roof[((wall.x1+width)-(x-wall.x1)-1-droop_offset,z,y+x-wall.x1-1)] = (53,4) 
                            
      
                    if width%2 == 1:
                        for z in range(wall.z1-1-offset, wall.z2+1+offset):
                            roof[(wall.x1+int(width/2)-droop_offset,z,y+int(width/2))] = (126,0)
                            roof[(wall.x1+int(width/2)-droop_offset,z,y+int(width/2)-1)] = (5,0)
                        
                    break    
                       
                pass
                
#                if wall.outside_dir[1] == "+":
#                    block = (53,0)
#                    mult = -1
#                elif wall.outside_dir[1] == "-":
#                    block = (53,1)
#                    mult = 1
#                
#                for z in range(wall.z1,wall.z2):
#                    for x in range(wall.x1, wall.x1+int(width/2)*mult,mult):
#                        roof[(x,z,y+x-wall.x1)] = block
#                        
    return roof
                    
        

def fix_top_walls(top_walls, wall_flush, corner_type, drop):
    for wall in top_walls:
        if wall.shortest:
            #print(wall.blocks)
            wall_y = max(wall.blocks, key = lambda x: x[2])[2] + 1 


            if wall_flush and corner_type == "orth":
                edge_offset = 1
            else:
                edge_offset = 0
                
            if not wall_flush and corner_type == "diag":
                height_adder = 1
            elif wall_flush and corner_type == "orth":
                height_adder = -1
            else:
                height_adder = 0
                

            idk_offset = 0

            if wall.orientation == "xx":
                width = wall.x2 - wall.x1
                
                if wall.outside_dir[1] == "-":
                    idk_offset = 1
                    #idk_offset= 0
                    #print(True)
                
                 
                for x in range(wall.x1+edge_offset, wall.x1 + int(width/2)):
                    if x == wall.x1:
                        block = (17,0)
                    else:
                        block = (121,0)
                    
                    for y in range(wall_y, wall_y+(x-wall.x1)+1+height_adder): 
                        wall.blocks[(x,wall.z2-idk_offset,y)] = block
                        wall.blocks[(wall.x1+width-(x-wall.x1)-1 ,wall.z2-idk_offset,y)] = block
                            
                        
                if width%2 == 1:
                    for y in range(wall_y, wall_y+(wall.x1 + int(width/2)-wall.x1)+1): 
                        wall.blocks[(wall.x1 + int(width/2),wall.z2-idk_offset,y)] = (121,0)
#            
            
            elif wall.orientation == "zz":
                height = wall.z2 - wall.z1
                
                if wall.outside_dir[1] == "+":
                    idk_offset = 1
                    #idk_offset=0
                    #print("Other true")

                    
                for z in range(wall.z1+edge_offset, wall.z1 + int(height/2)):
                    if z == wall.z1:
                        block = (17,0)
                    else:
                        block = (121,0)
                        
                    for y in range(wall_y, wall_y+(z-wall.z1)+1+height_adder):
                        wall.blocks[(wall.x2-idk_offset,z,y)] = block
                        wall.blocks[(wall.x2-idk_offset, (wall.z1+height)-(z-wall.z1)-1, y)] = block
                
                if height%2 == 1:
                    for y in range(wall_y, wall_y+(wall.z1 + int(height/2)-wall.z1)+1):
                        wall.blocks[(wall.x2-idk_offset, wall.z1+int(height/2), y)] = (121,0)
            
def partition_walls(walls):
    for wall in walls:
        
        if not wall.shortest:
            partition_coords = []
        
            y1 = min(wall.blocks, key = lambda x:x[2])[2]
            y2 = max(wall.blocks, key = lambda x:x[2])[2]
            
            if wall.orientation == "xx":
                if wall.outside_dir[1] == "-":
                    idk_offset = 1
                else:
                    idk_offset = 0 
                
                width = wall.x2 - wall.x1
                
                if width > 5:
                    n_partitions = randint(0,int((width-6)/2)+1)
                    coord_options = [(x,wall.z1-idk_offset,y1) for x in range(wall.x1+2,wall.x2-2)]
                    
                    for i in range(n_partitions):
                        new_partition = choice(coord_options)
                        
                        coord_options.remove(new_partition)
                        
                        if (new_partition[0]-1,new_partition[1],new_partition[2]) in coord_options:
                            coord_options.remove((new_partition[0]-1,new_partition[1],new_partition[2]))                        
                        if (new_partition[0]+1,new_partition[1],new_partition[2]) in coord_options:
                            coord_options.remove((new_partition[0]+1,new_partition[1],new_partition[2]))

                        partition_coords.append((new_partition[0],new_partition[1],new_partition[2]))
                        
                        for y in range(1,5):
                            wall.blocks[(new_partition[0],new_partition[1],new_partition[2]+y)] = (17,0)
                    
                partitioned_window_space = []  
                coord_options = [(x,wall.z1-idk_offset,y1) for x in range(wall.x1+2,wall.x2-2)]
                
                for coord in coord_options:
                    if coord in partition_coords:
                        if partitioned_window_space != []:
                            wall.partitioned_window_spaces.append(partitioned_window_space)
                        partitioned_window_space = [] 
                    else:
                        for y in range(1,5):
                            window_space = (coord[0],coord[1],coord[2]+y)
                            partitioned_window_space.append(window_space)
                            
                if partitioned_window_space != []:
                    wall.partitioned_window_spaces.append(partitioned_window_space)
     
                    #remove

            elif wall.orientation == "zz":
                width = wall.z2 - wall.z1
                
                if wall.outside_dir[1] == "+":
                    idk_offset = 1
                else:
                    idk_offset = 0
                
                if width > 5:
                    n_partitions = randint(0,int((width-6)/2)+1)
                    coord_options = [(wall.x1-idk_offset,z,y1) for z in range(wall.z1+2,wall.z2-2)]
                    
                    
                    for i in range(n_partitions):
                        new_partition = choice(coord_options)
                        coord_options.remove(new_partition)
                        
                        if (new_partition[0],new_partition[1]-1,new_partition[2]) in coord_options:
                            coord_options.remove((new_partition[0],new_partition[1]-1,new_partition[2]))                        
                        if (new_partition[0],new_partition[1]+1,new_partition[2]) in coord_options:
                            coord_options.remove((new_partition[0],new_partition[1]+1,new_partition[2]))
                        
                        partition_coords.append((new_partition[0],new_partition[1],new_partition[2]))
                        
                        for y in range(1,5):
                            wall.blocks[(new_partition[0],new_partition[1],new_partition[2]+y)] = (17,0)
                           
                            
                partitioned_window_space = []  
                coord_options = [(wall.x1-idk_offset,z,y1) for z in range(wall.z1+2,wall.z2-2)]
                
                for coord in coord_options:
                    if coord in partition_coords:
                        if partitioned_window_space != []:
                            wall.partitioned_window_spaces.append(partitioned_window_space)
                        partitioned_window_space = [] 
                    else:
                        for y in range(1,5):
                            window_space = (coord[0],coord[1],coord[2]+y)
                            partitioned_window_space.append(window_space)
                            
                if partitioned_window_space != []:
                    wall.partitioned_window_spaces.append(partitioned_window_space)
            
#partitioned_window_spaces
                            
                            
#class Window():
#    def __init__(self, blocks):
#        self.blocks = blocks
#        self.
    
def get_windows(walls):
    for wall in walls:
        #print("partitioned",wall.partitioned_window_spaces)
        if wall.partitioned_window_spaces == []:
            #print("get windows occuring")

            idk_offset = 0
            
            if wall.orientation == "xx":
                if wall.outside_dir[1] == "-":
                    idk_offset = 1
            elif wall.orientation == "zz":
                if wall.outside_dir[1] == "+":
                    idk_offset = 1
            
            y1 = min(wall.blocks, key = lambda x:x[2])[2]
            y2 = max(wall.blocks, key = lambda x:x[2])[2]
            
            window = {}
            
            if wall.orientation == "xx":
                width = wall.x2 - wall.x1
                
                window_type = choice([0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2])
            
                if window_type == 0 and (width == 3 or width == 5 or width == 7):
                    window[(wall.x1+int(width/2),wall.z1-idk_offset,y2-int(width/2))] = (95,0) 
                    
                elif window_type == 1 and (width == 3 or width == 5 or width == 7):
                    for y in range(y1+2,y2-1):
                        window[(wall.x1+int(width/2),wall.z1-idk_offset,y)] = (95,0) 
                        
                elif width%2 == 0:
                    for y in range(y1+2,y2-1):
                        window[(wall.x1+int(width/2),wall.z1-idk_offset,y)] = (95,0) 
                        window[(wall.x1+int(width/2)-1,wall.z1-idk_offset,y)] = (95,0) 
                
                        
            elif wall.orientation == "zz":
                    width = wall.z2 - wall.z1
                
                    window_type = choice([0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2])
                        
                    if window_type == 0 and (width == 3 or width == 5 or width == 7):
                        window[(wall.x1-idk_offset,wall.z1+int(width/2),y2-int(width/2))] = (95,0) 
                        
                    elif window_type == 1 and (width == 3 or width == 5 or width == 7):
                        for y in range(y1+2,y2-1):
                            window[(wall.x1-idk_offset,wall.z1+int(width/2),y)] = (95,0) 
                            
                    elif width%2 == 0:
                        rand_y_off = choice([0,2])
                        for y in range(y1+2+rand_y_off,y2-1):
                            window[(wall.x1-idk_offset,wall.z1+int(width/2),y)] = (95,0) 
                            window[(wall.x1-idk_offset,wall.z1+int(width/2)-1,y)] = (95,0) 
    #                
            wall.windows.append(window)
    
# youre such a loser    
def partitioned_window(walls):
    for wall in walls:
        #print("partitioned window",wall.partitioned_window_spaces)
        if wall.partitioned_window_spaces != []:
            #print("get_partitioned_window occuring")
            for section in wall.partitioned_window_spaces:
                
                y1 = min(section, key = lambda x:x[2])[2]
                y2 = max(section, key = lambda x:x[2])[2]
                
                window = {}
                
                if wall.orientation == "xx":
                    x1 = min(section, key = lambda x:x[0])[0]
                    x2 = max(section, key = lambda x:x[0])[0]
                    
                    width = x2 - x1
                    #print("width1", width,x1,x2)
                    
                    window_type = randint(0,2)
                
                    if window_type == 0 and width%2 == 1:
                        window[(x1+int(width/2),wall.z1,y2-int(width/2))] = (95,0) 
                        
                    elif window_type == 1 and width%2 == 1:
                        for y in range(y1+2,y2-1):
                            window[(x1+int(width/2),wall.z1,y)] = (95,0) 
                            
                    elif width%2 == 0:
                        for y in range(y1+2,y2-1):
                            window[(x1+int(width/2),wall.z1,y)] = (95,0) 
                            window[(x1+int(width/2)-1,wall.z1,y)] = (95,0) 
                    
                            
                elif wall.orientation == "zz":
                        z1 = min(section, key = lambda x:x[1])[1]
                        z2 = max(section, key = lambda x:x[1])[1]
                    
                        width = z2 - z1
                        #print("width2", width,z1,z2)
                    
                        window_type = randint(0,1)
                            
                        if window_type == 0 and width%2 == 1:
                            window[(wall.x1,z1+int(width/2),y2-int(width/2))] = (95,0) 
                            
                        elif window_type == 1 and width%2 == 1:
                            for y in range(y1+2,y2-1):
                                window[(wall.x1,z1+int(width/2),y)] = (95,0) 
                                
                        elif width%2 == 0:
                            rand_y_off = choice([0,2])
                            for y in range(y1+2+rand_y_off,y2-1):
                                window[(wall.x1,z1+int(width/2),y)] = (95,0) 
                                window[(wall.x1,z1+int(width/2)-1,y)] = (95,0) 
                #print("new window", window)
                wall.windows.append(window)
        
def trim_windows(walls,log_choice):
    # N E S W

    if log_choice == "oak": #oak
        stair = 53
        slab = 8
    if log_choice == "jungle": #jungle
        stair = 136
        slab = 11
    if log_choice == "spruce": #spuce
        stair = 134
        slab = 9
    if log_choice == "dark": #dark
        stair = 164
        slab = 13
    if log_choice == "birch": #birch
        stair = 135
        slab = 10
    if log_choice == "acacia": #acacia
        stair = 163
        slab = 12
    
    
    window_trimmings = {
        "bottom_trim": [(126,[slab]),(stair,[7,4,6,5]),(stair,[3,0,2,1]),(96,[9,10,8,11]),(96,[13,14,12,15])]
        # flower box
        #flower
        }
    
    # X Y Z + -
    window_trimmings_pos = {
                           #x y z   +  -
            "bottom_trim": [1,1,-1, 1,-1]
            }
    
    for wall in walls:
        for window in wall.windows:
            if window != {}:
                
                #print(window)
            
                y1 = min(window, key = lambda x:x[2])[2]
                y2 = max(window, key = lambda x:x[2])[2]
                
                trim_name = choice(window_trimmings.keys())
                trim = choice(window_trimmings[trim_name])
                
                if wall.orientation == "xx":
                    x1 = min(window, key = lambda x:x[0])[0]
                    x2 = max(window, key = lambda x:x[0])[0]
                    

                    if len(trim[1]) == 4:
                        if wall.outside_dir[1] == "+":
                            trim = (trim[0],trim[1][2]) 
                            z_offset = -1
                            
                        elif wall.outside_dir[1] == "-":
                            trim = (trim[0],trim[1][0]) 
                            z_offset = 0
                    else:
                        trim = (trim[0],trim[1][0])
                        
                        if wall.outside_dir[1] == "+":
                            z_offset = -1
                        elif wall.outside_dir[1] == "-":
                            z_offset = 0
                    
                    for x in range(x1, x2+1):
                        if trim_name == "bottom_trim":
                            wall.trim[(x,wall.z1+z_offset,y1-1)] = trim
                        
                elif wall.orientation == "zz":
                    z1 = min(window, key = lambda x:x[1])[1]
                    z2 = max(window, key = lambda x:x[1])[1]
                    
                    
                    if len(trim[1]) == 4: 
                        if wall.outside_dir[1] == "+":
                            trim = (trim[0],trim[1][3]) 
                            x_offset = 0
                            
                        elif wall.outside_dir[1] == "-":
                            trim = (trim[0],trim[1][1]) 
                            x_offset = -1
                    else:
                        trim = (trim[0],trim[1][0])
                        
                        if wall.outside_dir[1] == "+":
                            x_offset = 0
                        elif wall.outside_dir[1] == "-":
                            x_offset = -1
                    
                    for z in range(z1, z2+1):
                        if trim_name == "bottom_trim":
                            wall.trim[(wall.x1+x_offset,z,y1-1)] = trim
                    
def place_houses_in_seed(seed,bottom,box,box_2d,log_types,stair_types,slab_types,plank_types):  
    #print(seed.usable_site[:])
    district_points = seed.usable_site[:]
    
    district_points_2d = []
    for point in district_points:
        district_points_2d.append((point[0], point[1]))
    
    #print("diistrict", district_points[0:10])
    #print("distring [pots",len(district_points))
    
    #bottom_rect = get_rect(bottom)
    
    
    if seed.center_dist == 1:
        trial_house_no = 150
    elif seed.center_dist == 2:
        trial_house_no = 20
        
    if len(district_points) > 0:
        used_points = []
        

        for i in range(trial_house_no):  
            new_house_point = choice(district_points)
            new_house = House(new_house_point[0],new_house_point[1],bottom,seed,log_types,stair_types,slab_types,plank_types)
            kill_flag = False
            
            for house_point in new_house.plot:
                
                #if house_point not in district_points or house_point in used_points:
                if (house_point[0],house_point[1]) in used_points:
                    kill_flag = True
                    break
                #print( (house_point[0],house_point[1]) )
                
                #if (house_point[0],house_point[1],house_point[2]-1) not in district_points:
                if (house_point[0],house_point[1]) not in district_points_2d:
                    #print("hpise_point",(house_point[0],house_point[1],house_point[2]))
                    kill_flag = True
                    #print("killed")
                    break
                
#                if house_point[0] < bottom_rect[0] or house_point[0] > bottom_rect[2]:
#                    
#                if house_point[1] < bottom_rect[1] or house_point[1] > bottom_rect[3]:
                
            if kill_flag == False:
                seed.houses.append(new_house)
                #print(True)`
                new_used_points = []
                #print("x",new_house.roof_rect[0],new_house.roof_rect[2])
                #print("z",new_house.roof_rect[1],new_house.roof_rect[3])
                for x in range(new_house.roof_rect[0],new_house.roof_rect[2]):
                    for z in range(new_house.roof_rect[1],new_house.roof_rect[3]):
                        new_used_points.append((x,z))

                        
                #print(len(new_used_points))
                used_points += new_used_points
                
                
            if len(seed.houses) > 5 and seed.center_dist == 2:
                break
                
                
                
            
            #[min_x,min_z,max_x,max_z]
            
            

class House():
    def __init__(self,x,z,bottom,seed,log_types,stair_types,slab_types,plank_types):
        self.seed = seed
        
#        self.log_types = log_types
#        self.stair_types = stair_types
#        self.slab_types = slab_types
#        self.plank_types = plank_types
        
        self.log_types = []
        self.stair_types = []
        self.slab_types = []
        self.plank_types = []
        
        #print("log_types",log_types)
        self.log_choice = choice(log_types)
        
        self.x = x
        self.z = z
        
        self.width = randint(5,9)
        self.height = randint(5,9)
        
        if seed.center_dist == 2:
            self.base = True
        else:
            self.base = choice([True, False])
        
    
        
        self.wall_flush = choice([True, False])
        #self.wall_flush = False
        
        self.corner_type = choice(["orth", "diag"])
        #self.corner_type = "diag"
        
        if self.width != self.height:
            self.roof_droop = choice([True, False])
            #self.roof_droop = True
        else:
            self.roof_droop = False
    
        
        [self.base_walls,self.plot] = get_plot_and_base_walls(x,z,self.width,self.height, self.corner_type,self.base,bottom)
        self.rect = get_rect(self.plot,0)
        self.top_walls = get_top_walls(self.base_walls, self.wall_flush, self.corner_type, self.rect)
        
        if randint(1,3) == 1:
            partition_walls(self.top_walls)####################################
        
        self.roof = get_roof(self.top_walls, self.width, self.height,self.wall_flush, self.corner_type, self.roof_droop)
        fix_top_walls(self.top_walls, self.wall_flush, self.corner_type,self.roof_droop)
        
        self.roof_rect = get_rect(self.roof,3)
        
        get_windows(self.top_walls)
        #partitioned_window(self.top_walls)################################
        
        trim_windows(self.top_walls, self.log_choice)
        
        if randint(1,3) == 1:
            trim_roof(self)
            
        self.door_pos,self.door_blocks,self.door_trim,self.door_trim_pos,self.door_air = get_door(self)
        
        self.inside = {}
        #self.inside_plot = []
        #self.inside_top_plot = []
        get_inside(self)
        
        self.theme = choice(["white","red","cyan"])
        
        
        
        
        
        
        if self.log_choice == "oak": #oak
            self.stair_types.append(53)
            self.slab_types.append((126,0))
            self.plank_types.append((5,0))
        if self.log_choice == "jungle": #jungle
            self.stair_types.append(136)
            self.slab_types.append(126,3)
            self.plank_types.append((5,3))
        if self.log_choice == "spruce": #spuce
            self.stair_types.append(134)
            self.slab_types.append((126,1))
            self.plank_types.append((5,1))
        if self.log_choice == "dark": #dark
            self.stair_types.append(164)
            self.slab_types.append((126,5))
            self.plank_types.append((5,5))
        if self.log_choice == "birch": #birch
            self.stair_types.append(135)
            self.slab_types.append((126,2))
            self.plank_types.append((5,2))
        if self.log_choice == "acacia": #acacia
            self.stair_types.append(163)
            self.slab_types.append((126,4))
            self.plank_types.append((5,4))
            
        
        
        
        
        
        redo_walls(self)
        redo_roof(self)
        
        #self.fence = get_fence(self)
  
def redo_roof(house):
    
    plank = choice(house.plank_types)
    slab = choice(house.slab_types)
    stair = choice(house.stair_types)
    
    for point in house.roof:
        if house.roof[point] == (5,0):
            house.roof[point] = plank
        elif house.roof[point] == (126,0):
            house.roof[point] = slab
        elif house.roof[point][0] == 53:
            new_block = (stair,house.roof[point][1])
            house.roof[point] = new_block
        #elif house.roof[point] == 
            

            
            
            
            
            
          
def redo_walls(house):
    
#            
#        self.log_types = log_types
#        self.stair_types = stair_types
#        self.slab_types = slab_types
#        self.plank_types = plank_types
#    
    if house.theme == "white":
        theme_pal = [(1,3),(251,0),(251,0),(251,0),(251,0),(251,0)]
    elif house.theme == "red":
        theme_pal = [(45,0),(45,0),(45,0),(45,0),(45,0),(159,14)]
    elif house.theme == "cyan":
        theme_pal = [(1,5),(159,9),(159,9),(159,9),(159,9),(159,9)]
    
    
    log_choice = house.log_choice
    
    for wall in house.top_walls:
        for point in wall.blocks:
            #print(point, wall.blocks[point])
            if wall.blocks[point] == (121,0):
                #print("yeoo")
                wall.blocks[point] = choice(theme_pal)
                
     
            if wall.blocks[point][0] == 17:
                if wall.blocks[point][1] == 8:
                    if log_choice == "oak":
                        new_log = (17,8)
                    elif log_choice == "jungle":
                        new_log = (17,11)
                    elif log_choice == "spruce":
                        new_log = (17,9)
                    elif log_choice == "dark":
                        new_log = (162,9)
                    elif log_choice == "birch":
                        new_log = (5,2)
                    elif log_choice == "acacia":
                        new_log = (162,8)
  
                elif wall.blocks[point][1] == 4:
                    if log_choice == "oak":
                        new_log = (17,4)
                    elif log_choice == "jungle":
                        new_log = (17,7)
                    elif log_choice == "spruce":
                        new_log = (17,5)
                    elif log_choice == "dark":
                        new_log = (162,5)
                    elif log_choice == "birch":
                        new_log = (5,2)
                    elif log_choice == "acacia":
                        new_log = (162,4)
                        
                elif wall.blocks[point][1] == 0:
                    if log_choice == "oak":
                        new_log = (17,0)
                    elif log_choice == "jungle":
                        new_log = (17,3)
                    elif log_choice == "spruce":
                        new_log = (17,1)
                    elif log_choice == "dark":
                        new_log = (162,1)
                    elif log_choice == "birch":
                        new_log = (5,2)
                    elif log_choice == "acacia":
                        new_log = (162,0)
                        
                wall.blocks[point] = new_log
        
        
def get_inside(house):
    plot_edge = get_edge_3d(house.plot)
    
    inside_plot = house.plot[:]
    
    #print("edge", plot_edge)
    #print("indside", inside_plot)
    
    for point in plot_edge:
        try: ####################YIKRS TIKES TIKESYIRKESjjksdfkdfjklkljdfskldsfkjlfdskljdfslkfkljdf
            inside_plot.remove([point[0], point[1], point[2]])
        except:
            pass
        
    inside_edge = get_edge_3d(inside_plot)
    
    inside_top = []
    for point in inside_plot:
        inside_top.append((point[0], point[1], point[2]+3))
        
    #house.inside_plot = inside_plot
        
    if house.base:
        for wall in house.base_walls:
            if wall.outside_dir[0] == "xx":
                z = int(wall.z1 + wall.z2)/2
                x = min(wall.blocks, key = lambda x: x[0])[0]
                
                if wall.outside_dir[1] == "+":
                    house.inside[(x-1,z,wall.y+1)] = (50,2)
                    
                elif wall.outside_dir[1] == "-":
                    house.inside[(x+1,z,wall.y+1)] = (50,1)
                    
            
            elif wall.outside_dir[0] == "zz":
                x = int(wall.x1 + wall.x2)/2
                z = min(wall.blocks, key = lambda x: x[1])[1]
                
                if wall.outside_dir[1] == "+":
                    house.inside[(x,z+1,wall.y+1)] = (50,3)
                    
                elif wall.outside_dir[1] == "-":
                    house.inside[(x,z-1,wall.y+1)] = (50,4)
                
    #print(inside_plot)

    valid_edge = []
    stair_spaces = []
    
    #print("insode_edge",inside_edge)
    
    for point in inside_edge:
        #house.inside[(point[0], point[1], point[2])] = (22,0)
        d = sqrt(((house.door_pos[0] - point[0])**2) + ((house.door_pos[1] - point[1])**2))
        
        if d > 3:
            #house.inside[(point[0], point[1], point[2])] = (22,0)
            valid_edge.append(point)
            
            if (point[0]+4, point[1], point[2]) in inside_edge:
                stair_space = []
                for x in range(point[0]+1, point[0]+4):
                    y = x-(point[0]+1)
                    stair_space.append((x,point[1],point[2]+y))
                    
                stair_spaces.append(stair_space)
                    
            elif (point[0], point[1]+4, point[2]) in inside_edge:
                stair_space = []
                for z in range(point[1]+1, point[1]+4):
                    y = z - (point[1]+1)
                    stair_space.append((point[0],z,point[2]+y))
                    
                stair_spaces.append(stair_space)
            
    if house.base:
        if len(stair_spaces) > 0:
            stairs = choice(stair_spaces)
            if stairs[0][0] == stairs[1][0]:
                house.inside[(stairs[0][0],stairs[0][1]-1, inside_edge[0][2]+2)] = (0,0)
                inside_top.remove((stairs[0][0],stairs[0][1]-1, inside_edge[0][2]+3))
                
                valid_edge.remove((stairs[0][0],stairs[0][1]-1, inside_edge[0][2]))
                stair_block = (53,2)
            
            elif stairs[0][1] == stairs[1][1]:
                house.inside[(stairs[0][0]-1,stairs[0][1], inside_edge[0][2]+2)] = (0,0)
                inside_top.remove((stairs[0][0]-1,stairs[0][1], inside_edge[0][2]+3))
                
                valid_edge.remove((stairs[0][0]-1,stairs[0][1], inside_edge[0][2]))
                stair_block = (53,0)
               
            #print("[0]",stairs[0])
            #print("()",(stairs[0][0], stairs[0][1], inside_edge[0][2]))
            #valid_edge.remove((stairs[0][0], stairs[0][1], inside_edge[0][2]))
                
            for point in stairs:
                house.inside[(point[0], point[1], inside_edge[0][2]+2)] = (0,0)
                inside_top.remove((point[0], point[1], inside_edge[0][2]+3))
                house.inside[point] = stair_block
#                try:
#                    valid_edge.remove((point[0], point[1], inside_edge[0][2]))
#                except:
#                    pass
        else:
            ladder_pos = choice(valid_edge)
              
            ladder_block = (65,5)
                    
            house.inside[ladder_pos] = ladder_block
            house.inside[(ladder_pos[0],ladder_pos[1],ladder_pos[2]+1)] = ladder_block
            house.inside[(ladder_pos[0],ladder_pos[1],ladder_pos[2]+2)] = ladder_block
            valid_edge.remove(ladder_pos)
            
            inside_top.remove((ladder_pos[0],ladder_pos[1],ladder_pos[2]+3))  
            
        if inside_top != []:
            chest_point = choice(inside_top)
            house.inside[chest_point] = (54,randint(2,5))
            inside_top.remove(chest_point)
            
                
    table_point = choice(valid_edge)
    house.inside[table_point] = (58,0)
    valid_edge.remove(table_point)
    
    if valid_edge != []:
        furnace_point = choice(valid_edge)
        house.inside[furnace_point] = (61,2)
        
#        if valid_edge != []:
#            chest_point = choice(valid_edge)
#            house.inside[chest_point] = (54,randint(2,5))
            

    
    bed_y = 0
    if house.base:
        inside_comp = inside_top
    else:
        inside_comp = inside_plot
        
        # TOP
    bed_head_pos = choice(inside_comp)

    if (bed_head_pos[0]+1, bed_head_pos[1], bed_head_pos[2]) in inside_comp:
        house.inside[bed_head_pos] = (26,3)
        house.inside[(bed_head_pos[0]+1, bed_head_pos[1], bed_head_pos[2])] = (26,11)
        
    elif (bed_head_pos[0]-1, bed_head_pos[1], bed_head_pos[2]) in inside_comp:
        house.inside[bed_head_pos] = (26,1)
        house.inside[(bed_head_pos[0]-1, bed_head_pos[1], bed_head_pos[2])] = (26,9)
        
    elif (bed_head_pos[0], bed_head_pos[1]+1, bed_head_pos[2]) in inside_comp:
        house.inside[bed_head_pos] = (26,10)
        house.inside[(bed_head_pos[0], bed_head_pos[1]+1, bed_head_pos[2])] = (26,2)
        
    elif (bed_head_pos[0], bed_head_pos[1]-1, bed_head_pos[2]) in inside_comp:
        house.inside[bed_head_pos] = (26,8)
        house.inside[(bed_head_pos[0], bed_head_pos[1]-1, bed_head_pos[2])] = (26,0)
            
        
        
    roof_max = max(house.roof, key = lambda x:x[2])
    
    
    y = roof_max[2]-1
        
    if house.width >= house.height:
        if house.width > 6:
            z = roof_max[1]
            house.inside[(house.x + int(house.width/3),z,y)] = (85,0)
            house.inside[(house.x + int(house.width/3),z,y-1)] = (85,0)
            house.inside[(house.x + int(house.width/3),z,y-2)] = (89,0)
            
            house.inside[(house.x + int(ceil(2*house.width/3)),z,y)] = (85,0)
            house.inside[(house.x + int(ceil(2*house.width/3)),z,y-1)] = (85,0)
            house.inside[(house.x + int(ceil(2*house.width/3)),z,y-2)] = (89,0)
            
            x = house.x + int(house.width/2)
        else:
            x = house.x + int(house.width/2)
            z = roof_max[1]
            
    elif house.width < house.height:
        if house.height > 6:
            x = roof_max[0]
            house.inside[(x,house.z + int(ceil(house.height/3)),y)] = (85,0)
            house.inside[(x,house.z + int(ceil(house.height/3)),y-1)] = (85,0)
            house.inside[(x,house.z + int(ceil(house.height/3)),y-2)] = (89,0)
            
            house.inside[(x,house.z + int(ceil(2*house.height/3)),y)] = (85,0)
            house.inside[(x,house.z + int(ceil(2*house.height/3)),y-1)] = (85,0)
            house.inside[(x,house.z + int(ceil(2*house.height/3)),y-2)] = (89,0)
            
            
            
            z = house.z + int(house.height/2)
        else:
            z = house.z + int(house.height/2)
            x = roof_max[0]
            
    house.inside[(x,z,y)] = (85,0)
    house.inside[(x,z,y-1)] = (85,0)
    house.inside[(x,z,y-2)] = (89,0)
        
            
    
        



        
def get_fence(house):
    grounds_2d = []
    grounds_3d_dict = {}
    plot_2d = []
    
    for point in house.plot:
        plot_2d.append((point[0], point[1]))
    
    for point in house.grounds:
        grounds_2d.append((point[0], point[1]))
        grounds_3d_dict[(point[0], point[1])] = point[2]+1
    
    for i in range(4):
        
        grounds_2d_edge = get_edges_2d(grounds_2d)
        
        for point in grounds_2d_edge:
            grounds_2d.remove(point)
          
    small_grounds = []
    fence_edge = []
            
    for point in grounds_2d:
        if point not in plot_2d:
            small_grounds.append((point[0], point[1], grounds_3d_dict[point]))
        
    for point in grounds_2d_edge:
        if point not in plot_2d:
            fence_edge.append((point[0], point[1], grounds_3d_dict[point]))
        
        
    return small_grounds, fence_edge
        
        
            
def get_door(house):
    plot_2d = []
    for point in house.plot:
        plot_2d.append((point[0], point[1]))
    
    plot_edge = get_edges_2d(plot_2d)
    
    door_air = []
    
    if house.log_choice == "oak": #oak
        door_type = 64
    if house.log_choice == "jungle": #jungle
        door_type = 195
    if house.log_choice == "spruce": #spuce
        door_type = 193
    if house.log_choice == "dark": #dark
        door_type = 197
    if house.log_choice == "birch": #birch
        door_type = 194
    if house.log_choice == "acacia": #acacia
        door_type = 196
    
    if house.base:
        while True:
            door_pos = choice(plot_edge)
            
            if (door_pos[0]+1,door_pos[1]) in plot_edge and (door_pos[0]-1,door_pos[1]) in plot_edge:
                door_blocks = [(door_type,3),(door_type,9)]
                
                door_air.append((door_pos[0],door_pos[1]+1,house.plot[0][2]+1))
                door_air.append((door_pos[0],door_pos[1]+1,house.plot[0][2]+1))
                door_air.append((door_pos[0],door_pos[1]-1,house.plot[0][2]))
                door_air.append((door_pos[0],door_pos[1]-1,house.plot[0][2]))
                
                break
            elif (door_pos[0],door_pos[1]+1) in plot_edge and (door_pos[0],door_pos[1]-1) in plot_edge:
                door_blocks = [(door_type,2),(door_type,9)]
                
                door_air.append((door_pos[0]+1,door_pos[1],house.plot[0][2]+1))
                door_air.append((door_pos[0]+1,door_pos[1],house.plot[0][2]+1))
                door_air.append((door_pos[0]-1,door_pos[1],house.plot[0][2]))
                door_air.append((door_pos[0]-1,door_pos[1],house.plot[0][2]))
                
                break
         
        door_pos = (door_pos[0], door_pos[1], house.plot[0][2]+1)  
        
        
        for wall in house.base_walls:
            if door_pos in wall.blocks:
                
                if wall.outside_dir[0] == "xx":
                    if wall.outside_dir[1] == "+":
                        x_off = 1
                        y_off = 0
                    elif wall.outside_dir[1] == "-":
                        x_off = -1
                        y_off = 0
                elif wall.outside_dir[0] == "zz":
                    if wall.outside_dir[1] == "+":
                        x_off = 0
                        y_off = -1
                    elif wall.outside_dir[1] == "-":
                        x_off = 0
                        y_off = 1
                        
                for point in wall.blocks:
                    door_air.append((point[0]+x_off, point[1]+y_off, point[2]))
                        
                
                break
        #return (door_pos[0], door_pos[1], house.plot[0][2]+1), door_blocks
    else:

        random.shuffle(house.top_walls)
        for wall in house.top_walls:
            
            if wall.outside_dir[0] == "xx" and wall.outside_dir[1] == "+":
                x_off = -1
                y_off = 0
                idk_off = -1
            elif wall.outside_dir[0] == "zz"and wall.outside_dir[1] == "+":
                x_off = 0
                y_off = -1
                idk_off = -1
            else:
                x_off = 0
                y_off = 0
                idk_off = 0
       
            if wall.wall_type == "tudor" and wall.shortest == True:
                if wall.orientation == "xx":
                    z = wall.blocks.keys()[0][1]
                    door_pos = (wall.x1 + 1, z, wall.y+3)
                    door_blocks = [(door_type,3),(door_type,9)]
                    
                    door_air.append((wall.x1 + 1, z+1, wall.y+3))
                    door_air.append((wall.x1 + 1, z+1, wall.y+2))
                    door_air.append((wall.x1 + 1, z-1, wall.y+3))
                    door_air.append((wall.x1 + 1, z-1, wall.y+2))
                    
                    if abs(wall.x2 - wall.x1) in [3,5]:
                        if (wall.x1 + 1, z+1, wall.y+3) in wall.trim.keys():
                            wall.trim[(wall.x1 + 1, z+1, wall.y+3)] = (0,0)
                        elif (wall.x1 + 1, z-1, wall.y+3) in wall.trim.keys():
                            wall.trim[(wall.x1 + 1, z-1, wall.y+3)] = (0,0)
                    
                elif wall.orientation == "zz":
                    x = wall.blocks.keys()[0][0]
                    door_pos = (x, wall.z1 + 1, wall.y+3)
                    door_blocks = [(door_type,2),(door_type,9)]
                    
                    door_air.append((x+1, wall.z1 + 1, wall.y+3))
                    door_air.append((x+1, wall.z1 + 1, wall.y+2))
                    door_air.append((x-1, wall.z1 + 1, wall.y+3))
                    door_air.append((x-1, wall.z1 + 1, wall.y+2))
                    
                    if abs(wall.z2 - wall.z1) in [3,5]:
                        if (x+1, wall.z1 + 1, wall.y+3) in wall.trim.keys():
                            wall.trim[(x+1, wall.z1 + 1, wall.y+3)] = (0,0)
                        elif (x-1, wall.z1 + 1, wall.y+3) in wall.trim.keys():
                            wall.trim[(x-1, wall.z1 + 1, wall.y+3)] = (0,0)
                    
    
#    for wall in house.top_walls:
#        if house.base and house.wall_flush:
#            pass
##            if wall.outside_dir[0] == "xx" and wall.outside_dir[1] == "+":
##                door_trim = (53,0)
##                door_trim_pos = (door_pos[0]+1, door_pos[1], door_pos[2]+1)
##            
##            elif wall.outside_dir[0] == "xx" and wall.outside_dir[1] == "-":
##                door_trim = (53,1)
##                door_trim_pos = (door_pos[0]+1, door_pos[1], door_pos[2]+1)
##            
##            elif wall.outside_dir[0] == "zz" and wall.outside_dir[1] == "+":
##                door_trim = (53,2)
##                door_trim_pos = (door_pos[0], door_pos[1], door_pos[2]-12)
##                        
##            elif wall.outside_dir[0] == "zz" and wall.outside_dir[1] == "-":
##                door_trim = (53,3)
##                door_trim_pos = (door_pos[0], door_pos[1], door_pos[2]-12)
#                
#        else:
#            door_trim = (0,0)
#            door_trim_pos = (0,0,0)
                            
    door_trim = (0,0)
    door_trim_pos = (0,0,0)
    
    
    return door_pos, door_blocks, door_trim, door_trim_pos, door_air
            
        
                    
                
    
        
    
        
        
        
def trim_roof(house):
    #max_y = max(house.roof, key = lambda x:x[2])[2]
    min_y = min(house.roof, key = lambda x:x[2])[2]
    #mid_y = int((max_y+min_y)/2)+1
    
    adder = 0
    
    if house.roof_droop == False:
        adder += 1
        
    #mid_y -= adder
    
    if house.width > house.height:
        if house.width > 4:
            mid_x = house.x + int(house.width/2)
            
            for point in house.roof.keys():
                if point[1] == house.z+adder and house.roof[point][1] in [0,1,2,3]:
                    y = point[2]
                    break
            
            
            house.roof[(mid_x,house.z+adder,y)] = (95,0) 
            house.roof[(mid_x,house.z+adder,y+1)] = (126,0) 
            
            house.roof[(mid_x+1,house.z+adder,y)] = (53,1)
            #house.roof[(mid_x+1,house.z+adder,y)] = (5,0) 
            #house.roof[(mid_x+1,house.z+adder,y+1)] = (126,0) 
            
            if house.width%2 == 0:
                house.roof[(mid_x-1,house.z+adder,y)] = (95,0) 
                house.roof[(mid_x-1,house.z+adder,y+1)] = (126,0) 
                
                house.roof[(mid_x-2,house.z+adder,y)] = (53,0)
                #house.roof[(mid_x-2,house.z+adder,y)] = (5,0)
                #house.roof[(mid_x-2,house.z+adder,y+1)] = (126,0)
                
            else:
                house.roof[(mid_x-1,house.z+adder,y)] = (53,0)
                #house.roof[(mid_x-1,house.z+adder,y)] = (5,0)
                #house.roof[(mid_x-1,house.z+adder,y+1)] = (126,0)
                
        #if house.roof_drop:
            
                
            
            #print((mid_x,house.x+1,mid_y))
        
    elif house.width < house.height:
        if house.height > 4:
            mid_z = house.z + int(house.height/2)
            
            for point in house.roof.keys():
                
                if point[0] == house.x+adder and house.roof[point][1] in [0,1,2,3]:
                    y = point[2]
                    break
            
            house.roof[(house.x+adder,mid_z,y)] = (95,0) 
            house.roof[(house.x+adder,mid_z,y+1)] = (126,0)
            
            house.roof[(house.x+adder,mid_z+1,y)] = (53,3)
#            house.roof[(house.x+adder,mid_z+1,y)] = (5,0)
#            house.roof[(house.x+adder,mid_z+1,y+1)] = (126,0) 
            
            if house.height%2 == 0:
                house.roof[(house.x+adder,mid_z-1,y)] = (95,0) 
                house.roof[(house.x+adder,mid_z-1,y+1)] = (126,0) 
                
                house.roof[(house.x+adder,mid_z-2,y)] = (53,3)
#                house.roof[(house.x+adder,mid_z-2,y)] = (5,0)
#                house.roof[(house.x+adder,mid_z-2,y+1)] = (126,0)
                
            else:
                house.roof[(house.x+adder,mid_z-1,y)] = (53,2)
#                house.roof[(house.x+adder,mid_z-1,y)] = (5,0)
#                house.roof[(house.x+adder,mid_z-1,y+1)] = (126,0)
            
            #print((house.z+1,mid_z,mid_y))
        

def get_district_seeds(box):
    district_seeds = []
    
    center_x = int((box.maxx+box.minx)/2)
    center_z = int((box.maxz+box.minz)/2)
    
    max_r = min([box.maxx-center_x,box.maxz-center_z])
    #min_r = max([(box.maxx-center_x)*0.1,(box.maxz-center_z)*0.1])
    
    median_r = max([int((box.maxx-box.minx)/2), int((box.maxz-box.minz)/2)])
    #r_adder = int(median_r*0.2)
    
    for d in range(0,360,70): #40
        r = randint(0, int(max_r*0.5))
        x = center_x + int(r*sin(radians(d)))
        z = center_z + int(r*cos(radians(d)))
        #print("pos",x,z)
        new_seed = Seed(x,z,False)
        new_seed.center_dist = 1
        district_seeds.append(new_seed)
        
    for d in range(20,380,60): #30
        r = (randint(int(max_r*0.7), int(max_r*0.9)))
        x = center_x + int(r*sin(radians(d)))
        z = center_z + int(r*cos(radians(d)))
        #print("pos",x,z)
        new_seed = Seed(x,z,False)
        new_seed.center_dist = 2
        district_seeds.append(new_seed)
        
    
    #print("district_seeds",len(district_seeds))
        
    for x in range(box.minx,box.maxx,40):
        district_seeds.append(Seed(x,box.minz,True))
        district_seeds.append(Seed(x,box.maxz,True))
        
    for z in range(box.minz,box.maxz,40):    
        district_seeds.append(Seed(box.minx,z,True))
        district_seeds.append(Seed(box.maxx,z,True))
#      
    return district_seeds



def get_house_grounds(seeds):
    for seed in seeds:
        house_temp_seeds = {}
        all_seeds = []
        if len(seed.houses) > 0:
            for house in seed.houses:
                seed_1 = Seed(house.rect[0],house.rect[1],False) #min min
                seed_2 = Seed(house.rect[2],house.rect[3],False) #max max
                
                seed_3 = Seed(house.rect[0],house.rect[3],False) #,min max
                seed_4 = Seed(house.rect[2],house.rect[1],False) #max min
                
                house_temp_seeds[house] = [seed_1,seed_2,seed_3,seed_4]
                all_seeds += [seed_1,seed_2,seed_3,seed_4]
                
            #print("all_seeds", all_seeds)
            get_closest_points(seed.closest_points, all_seeds)
            
            combined_seeds = []            
            
            for house in house_temp_seeds:
                combined_seed = house_temp_seeds[house][0]
                combined_seed.closest_points += (house_temp_seeds[house][1].closest_points+house_temp_seeds[house][2].closest_points+house_temp_seeds[house][3].closest_points)
                
                house_temp_seeds[house] = combined_seed
                combined_seeds.append(combined_seed)
                
            get_edges(combined_seeds)
            
            
            
            #get_edges(all_seeds)
            
            #print("temp",house_temp_seeds)
            
            for house in house_temp_seeds:
                house.grounds = house_temp_seeds[house].closest_points 
                #house.grounds_edges = house_temp_seeds[house].edge_points 
                house.grounds_edges = get_edge_3d(house.grounds)
                
                house.shrinked_grounds, house.fence = get_fence(house)
                


class Branch():
    def __init__(self,x,z,y,d):
        self.x = x
        self.y = y
        self.z = z
        
        self.d = radians(d)
        #print("d", self.d)
        #self.d = d
        
        self.x_cum = 0
        self.y_cum = 0
        self.z_cum = 0
        
        self.l = randint(10,30)
        self.branch = []
        self.skinny_branch = []
        
        self.final_point = ()
        self.branched_off = False
        
        self.pillars = []
        self.pillar_points = []
        
        self.floor = []
        
        self.torch_points = []
        
    def create(self):
        for l in range(0,self.l,3):
            self.x_cum += randint(-1,1) 
            self.y_cum += choice([-1,0,0,0,0,0,1,1,1])
            self.z_cum += randint(-1,1)
              
            x = int(self.x + self.x_cum + (l*sin(self.d)))
            z = int(self.z + self.z_cum + (l*cos(self.d)))
            
            y = self.y + self.y_cum
            
            self.branch.append((x,z,y))
            self.skinny_branch.append((x,z,y))
            
            if l > self.l-4:
                self.final_point = (x,z,y)
            
            
            for i in range(-4,5):
                for j in range(-4,5):
                    
                    self.floor.append((x+i,z+j,y-1))

                    for k in range(0,5):
                        #self.branch.append((x+i,z+j,y+k))
                        
                        if i < -3 or i > 3 or j < -3 or j > 3:
                            if randint(1,3) == 1:
                                self.branch.append((x+i,z+j,y+k))
                        elif k > 4:
                            if randint(1,3) == 1:
                                self.branch.append((x+i,z+j,y+k))
                        else:
                            self.branch.append((x+i,z+j,y+k))
                            
                            
def place_pillars(tunnels,seed):
    all_tunnels = []
    
    for tunnel in tunnels:
        all_tunnels += tunnel.branch
        
    all_tunnels = array(all_tunnels)
    
    for tunnel in tunnels:
        for point in tunnel.skinny_branch:
            if (point[0],point[1]) not in seed.closest_points_2d:            
            
                if randint(1,5) == 1:
                    count = 0
                    
                    new_pillar = []
                    
                    #point = (point[0], point[1], point[2]-1)
                    new_pillar.append((point[0], point[1], point[2]-1))
                    
                    tunnel.torch_points.append((point[0], point[1], point[2]+3))
                    
                    while point in all_tunnels and count < 20:
                        new_pillar.append(point)
                        point = (point[0], point[1], point[2]+1)
                        count += 1
                        
                    tunnel.pillars += new_pillar
                    
#                if count < 30:
#                    self.pillars += new_pillar
#                if len(new_pillar) < 18:
#                    tunnel.pillars += new_pillar
                    
        
    
                            
                    
                            
        
                            
                
                      
                            
                            
                            
                    
                        
                        
        
        
        
            
class Mine():
    def __init__(self,seed, hole, hole_edge, dirt_space, path, tunnels,path_floor):
        self.seed = seed
        self.hole = hole
        self.hole_edge = hole_edge
        self.dirt_space = dirt_space
        self.path = path
        self.tunnels = tunnels
        self.path_floor = path_floor

def make_mine(seeds):
    small_seed = seeds[0]
    
    for seed in seeds:
        if len(seed.closest_points) > len(small_seed.closest_points) and seed.center_dist == 1:
           small_seed = seed
           
           
    small_seed.mine = True
    
    #small_seed = seed
    
    max_y = max(small_seed.closest_points, key = lambda x:x[2])[2]
    min_y = min(small_seed.closest_points, key = lambda x:x[2])[2]
    
    hole = []
    hole_edge = []
    
    layer = small_seed.closest_points_2d[:]
    layer_edge = get_edges_2d(layer)
    
    #print("layer", layer, len(layer))
    #print("edge",len(layer_edge))
    
    
    edge_decrease_count = 1
    
    for y in range(max_y, 20,-1):
        for point in layer:
            hole.append((point[0], point[1], y))
        
        if abs(y-max_y) == int(edge_decrease_count) and len(layer) > 200 and edge_decrease_count < 30:
            for edge_point in layer_edge:
                try:
                    layer.remove(edge_point)
                except:
                    pass
                    #print("ooopse", edge_point)
                
            if edge_decrease_count in [1,2,3]:
                edge_decrease_count += 1
            else:
                edge_decrease_count = edge_decrease_count**1.3
                
            #print(edge_decrease_count)
            
        layer_edge = get_edges_2d(layer)
        #layer_edge = fix_edge(layer_edge)
        
        layer_edge_3d = []
        for point in layer_edge:
            layer_edge_3d.append((point[0], point[1], y))
        
        hole_edge.append(layer_edge_3d)
        
        
    dirt_space = []
    
    for point in small_seed.closest_points:
        for y in range(0,randint(15,25)):
            dirt_space.append((point[0], point[1], point[2]-y))
            

    path,path_floor = get_path(hole_edge, small_seed)
        
    # Tunnel
    
    tunnels = []
    
    for d in range(0,360,60):
        new_branch = Branch(small_seed.x, small_seed.z, 20, d)
        new_branch.create()
        
        tunnels.append(new_branch)
        
    
    for count in range(7):
        new_tunnels = []
        
        for tunnel in tunnels:
            if tunnel.branched_off == False:
                tunnel.branched_off = True
                for d in range(-60,60,choice([60,40,30])):
                    if randint(0,2) == 0:
                        new_tunnel = Branch(tunnel.final_point[0],tunnel.final_point[1],tunnel.final_point[2],degrees(tunnel.d)+d)    
                        new_tunnel.create()
                        new_tunnels.append(new_tunnel)  
                    
        tunnels += new_tunnels
            
    
    place_pillars(tunnels,small_seed)
            

    
    mine = Mine(small_seed, hole, hole_edge, dirt_space, path,tunnels,path_floor)
    
    return mine
    
            


def get_path(hole_edge, seed):
    path = []
    path_2d = []
  
    point = choice(hole_edge[4])
    path.append(point)
    #print(point)
    path_2d.append((point[0],point[1]))
    
    for layer_edge in hole_edge[4:len(hole_edge)-1]:
        for i in range(3):
           point = get_next_edge(point, layer_edge, path,seed,path_2d)
           path.append(point)
           #print(point)
           path_2d.append((point[0],point[1]))
           
          
        point = (point[0],point[1],point[2]-1)
        next_layer_edge = hole_edge[hole_edge.index(layer_edge)+1]
            
        
        min_dist = 100000
        min_point = ()
        
        for edge_point in next_layer_edge:
            dx = point[0]-edge_point[0]
            dz = point[1]-edge_point[1]
            
            dist = sqrt((dx**2)+(dz**2))
            
            if dist < min_dist:
                min_dist = dist
                min_point = edge_point
            
        point = min_point
        path.append(point)
        path_2d.append((point[0],point[1]))
            
    extra_points = []
    path_floor = []
        
    for point in path:
        for i in range(-3,4):
            for j in range(-3,4):
                path_floor.append((point[0]+i, point[1]+j, point[2]-2))
                for k in range(-1,0):
                    new_point = (point[0]+i, point[1]+j, point[2]+k)
                    
                    extra_points.append(new_point)
                    
    path += extra_points
                    
    return path,path_floor







            
    
def get_usable_site(level, seeds, bottom):
    #print("getting usable site")
    # THIS DOESNT WORK IDK WHY 
    for seed in seeds:
        seed.usable_site = seed.closest_points[:]
        
        for point in seed.usable_site:
            
            #print(level.blockAt(point[0], point[1], bottom[(point[0], point[1])]))
            
            
            
            if level.blockAt(point[0], point[1], bottom[(point[0], point[1])]) in [8,9,10,11]:
                seed.usable_site.remove(point)
                
            if level.blockAt(point[0], point[1], bottom[(point[0], point[1])]) in [10,11]:
                uf.setBlock(level,(49,0), point[0], point[2], point[1])
                #print("found lava")
                
            

def perform(level, box, options):
    
    bottom = get_bottom(level, box, 1)
    
    log_types = []
    stair_types = []
    slab_types = []
    plank_types = []
    
    for (chunk, slices, point) in level.getChunkSlices(box):
        #print(point, chunk.root_tag["Level"]["Biomes"].value)
        for val in chunk.root_tag["Level"]["Biomes"].value:    
            if val in [1,3,4,6,8,132]: #oak
                log_types.append("oak")
                #stair_types.append(53)
                #slab_types.append((126,0))
                #plank_types.append((5,0))
            if val in [21,22,23,149,151]: #jungle
                log_types.append("jungle")
                #stair_types.append(136)
                #slab_types.append(126,3)
                #plank_types.append((5,3))
            if val in [5,12,13,19,30,31,32,33,158,160,161,133]: #spuce
                log_types.append("spruce")
                #stair_types.append(134)
                #slab_types.append((126,1))
                #plank_types.append((5,1))
            if val in [6,29,157,134]: #dark
                log_types.append("dark")
                #stair_types.append(164)
                #slab_types.append((126,5))
                #plank_types.append((5,5))
            if val in [2,17,27,28,155,156]: #birch
                log_types.append("birch")
                #stair_types.append(135)
                #slab_types.append((126,2))
                #plank_types.append((5,2))
            if val in [35,36,37,38,39,163,164,165,166,167]: #acacia
                log_types.append("acacia")
                #stair_types.append(163)
                #slab_types.append((126,4))
                #plank_types.append((5,4))
                
    if log_types == []:
        log_types = ["oak"]
            
             
            
        #arr = chunk.root_tag["Level"]["Biomes"].value
          
    #print(bottom)
    
    #print("bottom", len(bottom))
    
    print("finding map bottom")
    
    map_points_3d = []
    map_points_2d = []
    for point in bottom:
        point_3d = (point[0],point[1],bottom[point])
        map_points_3d.append(point_3d)
        map_points_2d.append((point[0],point[1]))
        
    #print("map_points", len(map_points_3d))
    
    print("seeding bottom")
    district_seeds = get_district_seeds(box)
    
    #print(district_seeds)
        
    get_closest_points(map_points_3d, district_seeds)
    get_edges(district_seeds)
    
    for seed in district_seeds:
        if seed.fake:
            district_seeds[district_seeds.index(seed)] = None
            
    for i in range(district_seeds.count(None)):
        district_seeds.remove(None)
    


    get_usable_site(level, district_seeds, bottom)
    
    lamp_post_points = []


    print("drawing major paths")
    
    for seed in district_seeds:
       # uf.setBlock(level,(22,0), seed.x, 30, seed.z)
#        for point in seed.closest_points:
#            uf.setBlock(level,seed.block, point[0], point[2], point[1])
        for point in seed.edge_points:
            #uf.setBlock(level,seed.block, point[0], point[2], point[1])
            
#            if randint(0,15) == 1:
#                
#                dists = []
#                
#                for post in lamp_post_points:
#                    d = sqrt(((post[0]-point[0])**2) + ((post[1]-point[1])**2))
#                    dists.append(d)
#                    
#                if dists != []:
#                    min_d = min(dists)
#                else:
#                    min_d = 11
#                    
#                if min_d > 10:
#                    
#                    x_off = randint(-1,1)
#                    z_off = randint(-1,1)
#                    
#                    lamp_post_points.append((point[0]+x_off, point[1]+z_off))
#                    
#                    uf.setBlock(level,(98,0), point[0]+x_off, point[2]+1, point[1]+z_off)
#                    uf.setBlock(level,(139,0), point[0]+x_off, point[2]+2, point[1]+z_off)
#                    uf.setBlock(level,(98,0), point[0]+x_off, point[2]+3, point[1]+z_off)
#                    uf.setBlock(level,(89,0), point[0]+x_off, point[2]+4, point[1]+z_off)
#                    uf.setBlock(level,(44,5), point[0]+x_off, point[2]+5, point[1]+z_off)
#                    
#                    uf.setBlockIfEmpty(level,(96,15), point[0]+1+x_off, point[2]+4, point[1]+z_off)
#                    uf.setBlockIfEmpty(level,(96,14), point[0]-1+x_off, point[2]+4, point[1]+z_off)
#                    uf.setBlockIfEmpty(level,(96,13), point[0]+x_off, point[2]+4, point[1]+1+z_off)
#                    uf.setBlockIfEmpty(level,(96,12), point[0]+x_off, point[2]+4, point[1]-1+z_off)
            
            for x in range(-1,2):
                for z in range(-1,2):
                        #uf.setBlockToGround(level, (0,0), point[0], point[1], point[2]+2, point[2])
                        for k in range(2):
                            uf.setBlock(level,(0,0), point[0]+x, point[2]+k+1, point[1]+z)
                    #if randint(0,2*(abs(x)+abs(z))) == 0:
                        block = choice([(98,0),(98,0),(98,0),(98,0),(1,5),(4,0),(13,0),(98,1),(98,2)])
                        
                        if level.blockAt(point[0]+x, point[2], point[1]+z) == 9:
                            uf.setBlockIfEmpty(level,(44,5), point[0]+x, point[2]+1, point[1]+z)
                        else:
                            uf.setBlock(level,block, point[0]+x, point[2], point[1]+z)
                            
    

    
 ##############################################################
 
    print("digging hole")
 
    mine = make_mine(district_seeds)
    
    for point in mine.seed.closest_points:
        for k in range(40):
            uf.setBlock(level,(0,0), point[0], point[2]+k, point[1])

    for point in mine.dirt_space:
        dirt_type = choice([(3,0),(3,1)])
        uf.setBlock(level,(3,0), point[0], point[2], point[1])
        
    for tunnel in mine.tunnels:
        for point in tunnel.floor:
            block = choice([(3,0),(3,1),(1,0),(1,5),(1,1),(3,2),(13,0)])
            uf.setBlock(level,block, point[0], point[2], point[1])
    
    for point in mine.hole:
        uf.setBlock(level,(0,0), point[0], point[2], point[1])
    
    
    for tunnel in mine.tunnels:
        for point in tunnel.branch:
            uf.setBlock(level,(0,0), point[0], point[2], point[1])
        
    for tunnel in mine.tunnels:
        for point in tunnel.pillars:
            uf.setBlock(level,(162,1), point[0], point[2], point[1])
            
        for point in tunnel.torch_points:
            uf.setBlock(level,(50,1), point[0]+1, point[2], point[1])
            uf.setBlock(level,(50,2), point[0]-1, point[2], point[1])
            uf.setBlock(level,(50,3), point[0], point[2], point[1]+1)
            uf.setBlock(level,(50,4), point[0], point[2], point[1]-1)
    
    for point in mine.path:
        uf.setBlock(level,(0,0), point[0], point[2], point[1])
        
    torches = []
        
    for point in mine.path_floor:
        
        if randint(1,10) == 1 and level.blockAt(point[0], point[2]-1, point[1]) != 0:
            dists = []
            for torch in torches:
                d = sqrt(((torch[0]-point[0])**2)+((torch[1]-point[1])**2)+((torch[2]-point[2])**2))
                dists.append(d)
                
            if dists == []:
                min_d = 20
            else:
                min_d = min(dists)
                
            if min_d > 5:
               uf.setBlock(level,(50,5), point[0], point[2], point[1])
               torches.append((point[0], point[1],point[2]))
                
                
                
                
####################################################################  
        
        
#        if level.blockAt(point[0], point[2]-1, point[1]) == 0:
#            if level.blockAt(point[0], point[2], point[1]+1) == 1:
#                uf.setBlock(level,(50,4), point[0], point[2], point[1])
#                
#            elif level.blockAt(point[0], point[2], point[1]-1) == 1:
#                 uf.setBlock(level,(50,3), point[0], point[2], point[1])
#                 
#            elif level.blockAt(point[0]+1, point[2], point[1]) == 1:
#                uf.setBlock(level,(50,2), point[0], point[2], point[1])
#                
#            elif level.blockAt(point[0]-1, point[2], point[1]) == 1:
#                uf.setBlock(level,(50,1), point[0], point[2], point[1])
                
#    for point in mine.path_floor:
#        if (point[0]+1, point[2], point[1]) in mine.path_floor:
#            if (point[0]-1, point[2], point[1]-1) in mine.path_floor:
#                uf.setBlock(level,(44,5), point[0], point[2], point[1])
        
        
#        if (point[0]+1, point[2], point[1]) in mine.path:
#            if (point[0]-1, point[2], point[1]) in mine.path:
#                uf.setBlock(level,(44,5), point[0], point[2], point[1])
#                
#                
#        if (point[0], point[2], point[1]+1) in mine.path:
#            if (point[0], point[2], point[1]-1) in mine.path:
#                uf.setBlock(level,(44,5), point[0], point[2], point[1])

        
        
        
        #block = choice([(4,0),(1,0)])
        #uf.setBlock(level,block, point[0], point[2], point[1])
        
        
        
        
        
        
#        #print(level.blockAt(point[0], point[2], point[1]+1))
#        
#        support = randint(1,4)
#        light = randint(1,3) #50,5
#        
#        if level.blockAt(point[0], point[2], point[1]+1) in [1,3,24,12,13]:
#            for i in range(3):
#                block = choice([(4,0),(1,0),(1,0),(1,0),(1,0)])
#                uf.setBlock(level,block, point[0], point[2], point[1]-i)
#                
#                if i < 2 and support == 1:
#                    uf.setBlock(level,(126,8), point[0], point[2]-1, point[1]-i)
#            
#            if light == 1:
#                uf.setBlock(level,(50,5), point[0], point[2]+2, point[1]-3)
#            uf.setBlock(level,(85,0), point[0], point[2]+1, point[1]-3)
#            uf.setBlock(level,(85,0), point[0], point[2], point[1]-3)
#            
#                
#        elif level.blockAt(point[0], point[2], point[1]-1) in [1,3,24,12,13]:
#            for i in range(3):
#                block = choice([(4,0),(1,0),(1,0),(1,0),(1,0)])
#                uf.setBlock(level,block, point[0], point[2], point[1]+i)
#                
#                if i < 2 and support == 1:
#                    uf.setBlock(level,(126,8), point[0], point[2]-1, point[1]+i)
#            
#            if light == 1:
#                uf.setBlock(level,(50,5), point[0], point[2]+2, point[1]+3)
#            uf.setBlock(level,(85,0), point[0], point[2]+1, point[1]+3)
#            uf.setBlock(level,(85,0), point[0], point[2], point[1]+3)
#                  
#        if level.blockAt(point[0]+1, point[2], point[1]) in [1,3,24,12,13]:
#            for i in range(3):
#                block = choice([(4,0),(1,0),(1,0),(1,0),(1,0)])
#                uf.setBlock(level,block, point[0]-i, point[2], point[1])
#                
#                if i < 2 and support == 1:
#                    uf.setBlock(level,(126,8), point[0]-i, point[2]-1, point[1])
#            
##            if light == 1:
##                uf.setBlock(level,(50,5), point[0]-3, point[2]+2, point[1])
##            uf.setBlock(level,(85,0), point[0]-3, point[2]+1, point[1])
##            uf.setBlock(level,(85,0), point[0]-3, point[2], point[1])
#            
#        elif level.blockAt(point[0]-1, point[2], point[1]) in [1,3,24,12,13]:
#            for i in range(3):
#                block = choice([(4,0),(1,0),(1,0),(1,0),(1,0)])
#                uf.setBlock(level,block, point[0]+i, point[2], point[1])
#                
#                if i < 2 and support == 1:
#                    uf.setBlock(level,(126,8), point[0]+i, point[2]-1, point[1])
#            
##            if light == 1:
##                uf.setBlock(level,(50,5), point[0]+3, point[2]+2, point[1])
##            uf.setBlock(level,(85,0), point[0]+3, point[2]+1, point[1])
##            uf.setBlock(level,(85,0), point[0]+3, point[2], point[1])
         
        
        
        
        
        
        
        
        
        
            
    #somethibg about only half of these
        
#            for (i,j) in [(0,1),(1,0),(0,-1),(-1,0)]:
#                if level.blockAt(x+i,y,z+j) in [0]:
#                     uf.setBlock(level,(44,0), point[0]+i, point[2], point[1]-j)
            
            
#            for i in range(-3,4):
#                for j in range(-3,4):
#                    for k in range(0,3):
#                        uf.setBlock(level,(0,0), point[0]+i, point[2]+k, point[1]-j)
                        
                    

                        
                   # uf.setBlock(level,(44,2), point[0]+i, point[2]+j, point[1])
                   

            
    print("creating houses")       
    

    for seed in district_seeds:
        if seed.mine == False:
            place_houses_in_seed(seed, bottom,box,map_points_2d,log_types,stair_types,slab_types,plank_types)
        
    get_house_grounds(district_seeds)


    print("drawing houses")

    for seed in district_seeds:
        #print("seed len",len(seed.houses))
        for house in seed.houses:
            for point in house.grounds_edges:
            #for point in house.grounds:
                #uf.setBlock(level,(35,r), point[0], point[2], point[1])
                
                for x in range(-1,2):
                    for z in range(-1,2):
                        
                        #uf.setBlockToGround(level, (0,0), point[0], point[1], point[2]+2, point[2])

                        if level.blockAt(point[0]+x, point[2], point[1]+z) == 9:
                            uf.setBlockIfEmpty(level,(44,5), point[0]+x, point[2]+1, point[1]+z)
                        else:
                            if randint(0,2*(abs(x)+abs(z))) == 0 and point not in seed.edge_points:
                                
                                for k in range(2):
                                    uf.setBlock(level,(0,0), point[0]+x, point[2]+k+1, point[1]+z)                                
#                                
                                block = choice([(208,0),(3,1),(208,0),(3,1),(208,0),(3,1),(13,0)])
                                
                                uf.setBlock(level,block, point[0]+x, point[2], point[1]+z)


            if seed.center_dist == 2:
                crop_type = choice([(59,7), (142,7), (141,7)])
                for point in house.shrinked_grounds:
                    
                    #uf.setBlockToGround(level, (0,0), point[0], point[1], point[2]+40, point[2])
                    for k in range(40):
                        uf.setBlock(level,(0,0), point[0], point[2]+k, point[1])
                        
                    a = abs(bottom[(point[0], point[1])] - bottom[(point[0]+1, point[1])]) <= 1
                    b = abs(bottom[(point[0], point[1])] - bottom[(point[0]-1, point[1])]) <= 1
                    c = abs(bottom[(point[0], point[1])] - bottom[(point[0], point[1]+1)]) <= 1
                    d = abs(bottom[(point[0], point[1])] - bottom[(point[0], point[1]-1)]) <= 1
                    
                    if a and b and c and d:
                        uf.setBlock(level,(60,7), point[0], point[2]-1, point[1])
                        uf.setBlock(level,(3,0), point[0], point[2]-2, point[1])
                        uf.setBlock(level,crop_type, point[0], point[2], point[1])
                    else:
                        uf.setBlock(level,(2,0), point[0], point[2]-1, point[1])
                        uf.setBlock(level,(3,0), point[0], point[2]-2, point[1])
                        
                
                fence_post_points = []
                
                for point in house.fence:
                    if randint(1,5) == 1:
                        dists = []
                        
                        for post in fence_post_points:
                            d = sqrt(((post[0]-point[0])**2) + ((post[1]-point[1])**2))
                            dists.append(d)
                            
                        if dists == []:
                            min_d = 15
                        else:
                            min_d = min(dists)
                            
                        if min_d > 7:
                            
                            fence_post_points.append((point[0], point[1]))

                            uf.setBlock(level,(98,0), point[0], point[2], point[1])
                            uf.setBlock(level,(89,0), point[0], point[2]+1, point[1])
                            uf.setBlock(level,(44,5), point[0], point[2]+2, point[1])
                            
                            uf.setBlockIfEmpty(level,(96,15), point[0]+1, point[2]+1, point[1])
                            uf.setBlockIfEmpty(level,(96,14), point[0]-1, point[2]+1, point[1])
                            uf.setBlockIfEmpty(level,(96,13), point[0], point[2]+1, point[1]+1)
                            uf.setBlockIfEmpty(level,(96,12), point[0], point[2]+1, point[1]-1)
                        
                    else:
                        block = choice([(139,0),(139,0),(139,0),(139,0),(139,1)])
                        uf.setBlock(level,block, point[0], point[2], point[1])
                        
                    
                    
            for point in house.plot: # CLEAR THE INTERIROR
                max_y = max(house.roof, key = lambda x:x[2])[2]
                for y in range(0,max_y):
                    uf.setBlock(level, (0,0), point[0], point[2]+y, point[1])
            

            

                    
            for wall in house.top_walls:
                for point in wall.blocks:
                    uf.setBlock(level,wall.blocks[point], point[0], point[2], point[1])
                    
                for window in wall.windows:
                    for point in window:
                        uf.setBlock(level,window[point], point[0], point[2], point[1])
                        
            for point in house.door_air:
                uf.setBlock(level,(0,0), point[0], point[2], point[1])
                    
            for wall in house.top_walls:
                for point in wall.trim:
                    uf.setBlock(level,wall.trim[point], point[0], point[2], point[1])
                    
                   
#            for point in house.plot:#########
#                uf.setBlockToGround(level,(22,0), point[0], point[2]+1, point[1], bottom[(point[0],point[1])]-1) 
            
            

            
            
            #floor
            floor_block = choice([(1,6),(4,0),(43,0),(43,5)])
            for point in house.plot:
                #uf.setBlock(level,(126,8), point[0], point[2]+2, point[1])
                if house.base:
                    uf.setBlockIfEmpty(level, (126,8), point[0], point[2]+2, point[1])
                
                uf.setBlock(level, floor_block, point[0], point[2]-1, point[1])
                
                
                
            for wall in house.base_walls:
                for point in wall.blocks:
                    uf.setBlock(level,wall.blocks[point], point[0], point[2], point[1])
                    uf.setBlockToGround(level,wall.blocks[point], point[0], point[2], point[1], bottom[(point[0],point[1])]-1)
                    
#                    if level.blockAt(point[0], point[2]-1, point[1]) in [9,8]:
#                        for k in range(50):
#                            if level.blockAt(point[0], point[2]-k, point[1]) not in [9,8]:
#                                break
#                            else:
#                                uf.setBlock(level,wall.blocks[point], point[0], point[2]-k, point[1])

                 
            #door 
            uf.setBlock(level,house.door_blocks[1], house.door_pos[0], house.door_pos[2], house.door_pos[1])
            uf.setBlock(level,house.door_blocks[0], house.door_pos[0], house.door_pos[2]-1, house.door_pos[1])
            

                #uf.setBlock(level,(0,0), point[0], point[2]-1, point[1])
                
              
            if house.wall_flush == False:
                uf.setBlock(level,(5,0), house.door_pos[0], house.door_pos[2]-2, house.door_pos[1])
                
            uf.setBlock(level,house.door_trim, house.door_trim_pos[0], house.door_trim_pos[2], house.door_trim_pos[1])
                

            for point in house.inside:
                uf.setBlock(level,house.inside[point], point[0], point[2], point[1])
                
            for point in house.roof:
                #print(block)
                uf.setBlock(level,house.roof[point], point[0], point[2], point[1])
            


    for seed in district_seeds:
       # uf.setBlock(level,(22,0), seed.x, 30, seed.z)
#        for point in seed.closest_points:
#            uf.setBlock(level,seed.block, point[0], point[2], point[1])
        for point in seed.edge_points:
            #uf.setBlock(level,seed.block, point[0], point[2], point[1])
            
            if randint(0,15) == 1:
                
                dists = []
                
                for post in lamp_post_points:
                    d = sqrt(((post[0]-point[0])**2) + ((post[1]-point[1])**2))
                    dists.append(d)
                    
                if dists != []:
                    min_d = min(dists)
                else:
                    min_d = 11
                    
                if min_d > 10:
                    
                    x_off = randint(-1,1)
                    z_off = randint(-1,1)
                    
                    lamp_post_points.append((point[0]+x_off, point[1]+z_off))
                    
                    uf.setBlock(level,(98,0), point[0]+x_off, point[2]+1, point[1]+z_off)
                    uf.setBlock(level,(139,0), point[0]+x_off, point[2]+2, point[1]+z_off)
                    uf.setBlock(level,(98,0), point[0]+x_off, point[2]+3, point[1]+z_off)
                    uf.setBlock(level,(89,0), point[0]+x_off, point[2]+4, point[1]+z_off)
                    uf.setBlock(level,(44,5), point[0]+x_off, point[2]+5, point[1]+z_off)
                    
                    uf.setBlockIfEmpty(level,(96,15), point[0]+1+x_off, point[2]+4, point[1]+z_off)
                    uf.setBlockIfEmpty(level,(96,14), point[0]-1+x_off, point[2]+4, point[1]+z_off)
                    uf.setBlockIfEmpty(level,(96,13), point[0]+x_off, point[2]+4, point[1]+1+z_off)
                    uf.setBlockIfEmpty(level,(96,12), point[0]+x_off, point[2]+4, point[1]-1+z_off)
    

            
    print()
                
    





















