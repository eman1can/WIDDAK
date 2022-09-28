import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import* 
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
import Queue
from mcplatform import * 

import utilityFunctions as utilityFunctions


def perform(level, box, options):
    boxes = surfaceBox(level, box)
    init = BoundingBox((box.minx, box.miny, box.minz),(0,0,0))
    house = Shape(init,level)
    house.setBoxData()
    for sub in boxes:
        modifiy = BoundingBox((sub.minx,sub.miny, sub.minz),(sub.width+2, sub.height+2, sub.length+2))
        shape = Shape(modifiy,level)
        shape.setBoxData()
        house = house.Add(shape)
    house.DrawFrame()

    '''
    b1 = BoundingBox((box.minx-1, box.miny-1, box.minz-1), (box.width, box.height, box.length))
    b2 = BoundingBox((box.minx+3, box.miny+3, box.minz+3), (box.width//3, box.height//3, box.length//3))
    b3 = BoundingBox((box.minx+5, box.miny+5, box.minz+5), (5, 5, 5))
    shape1 = Shape(b1, level,(1,0,0))
    shape1.setBoxData()
    shape2 = Shape(b2, level,(1,0,0))
    shape2.setBoxData()
    shape3 = Shape(b3, level, (1,0,0))
    shape3.setBoxData()
    shape1.Add(shape2).Add(shape3).DrawFrame()
    '''
# The max voxel in grid is (maxx-1, maxy-1, maxz-1)
def getAxis(frontDir):   
    if (frontDir == array([0,0,1])).all():
        xaxis = array([1,0,0])
        yaxis = array([0,1,0])
        zaxis = array([0,0,1])   
    elif (frontDir == array([0,0,-1])).all():
        xaxis = array([-1,0,0])
        yaxis = array([0,1,0])
        zaxis = array([0,0,-1])
    elif (frontDir == array([0,1,0])).all():
        xaxis = array([1,0,0])
        yaxis = array([0,0,-1])
        zaxis = array([0,1,0])
    elif (frontDir == array([0,-1,0])).all():
        xaxis = array([1,0,0])
        yaxis = array([0,0,1])
        zaxis = array([0,-1,0])
    elif (frontDir == array([1,0,0])).all():
        xaxis = array([0,0,-1])
        yaxis = array([0,1,0])
        zaxis = array([1,0,0])
    else:
        xaxis = array([0,0,1])
        yaxis = array([0,1,0])
        zaxis = array([-1,0,0])

    return xaxis, yaxis, zaxis
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
class Shape(object):

    def __init__(self, scope, level, frontDir=(0,0,1) ,shapeType="Box"):
        self.scope = scope
        self.shapeType = shapeType
        self.level = level
        self.dim = array([scope.width, scope.height, scope.length])   
        self.data = full(self.dim,-1,dtype=int)

        self.frontDir = array(frontDir, dtype=int)

        #local coordinate 
        #self.orign = array([scope.minx, scope.miny,scope.minz], dtype=int)

        #self.xaxis, self.yaxis, self.zaxis = getAxis(self.frontDir)
        #self.dim = self.worldTolocal(dim[0],dim[1],dim[2])
    '''
    def setData(self, shapeType):
        scope = self.scope
        for x in range(scope.minx, scope.maxx):
            for y in range(scope.miny, scope.maxy):
                for z in range(scope.minz, scope.maxz):
                    if shapeType.inside(x,y,z):
                        self.data[x][y][z] = -1
                    elif shapeType.boundry(x,y,z):
                        self.data[x][y][z] = 0
                    else:
                        self.data[x][y][z] = 1
    '''
    def setBoxData(self):
        scope = self.scope
        for x in range(0, self.dim[0]):
            for y in range(0, self.dim[1]):
                self.data[x][y][0] = 0
                self.data[x][y][self.dim[2]-1] = 0

        for x in range(0, self.dim[0]):
            for z in range(0, self.dim[2]):
                self.data[x][0][z] = 0
                self.data[x][self.dim[1]-1][z] = 0

        for y in range(0, self.dim[1]):
            for z in range(0, self.dim[2]):
                self.data[0][y][z] = 0
                self.data[self.dim[0]-1][y][z] = 0

    def DrawFrame(self, material=(41,0)):
        for x in range(self.scope.minx, self.scope.maxx):
            for y in range(self.scope.miny, self.scope.maxy):
                for z in range(self.scope.minz, self.scope.maxz):
                    if self.data[x-self.scope.minx][y-self.scope.miny][z-self.scope.minz] == 0:
                    #if self.isOnFace(x,y,z):
                        utilityFunctions.setBlock(self.level, material, x, y, z)
                    elif self.data[x-self.scope.minx][y-self.scope.miny][z-self.scope.minz] == -1:
                        utilityFunctions.setBlock(self.level,(0,0), x, y, z)

    def Add(self, shape):
        s1 = self.scope
        s2 = shape.scope
        minx = min(s1.minx, s2.minx)
        miny = min(s1.miny, s2.miny)
        minz = min(s1.minz, s2.minz)
        maxx = max(s1.maxx, s2.maxx)
        maxy = max(s1.maxy, s2.maxy)
        maxz = max(s1.maxz, s2.maxz)
        w = maxx - minx
        h = maxy - miny
        l = maxz - minz
        newScope = BoundingBox((minx,miny,minz), (w,h,l))
        newShape = Shape(newScope, self.level)
        newdata = full([w,h,l],1,dtype=int)
        for x in range(minx, maxx):
            for y in range(miny,maxy):
                for z in range(minz, maxz):
                    lx = x - minx
                    ly = y - miny
                    lz = z - minz

                    if self.isInside(x,y,z) and shape.isInside(x,y,z):
                        newdata[lx][ly][lz] = -1
                    elif self.isInside(x,y,z) and shape.isOutside(x,y,z):
                        newdata[lx][ly][lz] = -1
                    elif self.isOutside(x,y,z) and shape.isInside(x,y,z):
                        newdata[lx][ly][lz] = -1
                    
                    elif self.isOnFace(x,y,z) and shape.isInside(x,y,z):
                        newdata[lx][ly][lz] = -1
                    elif self.isInside(x,y,z) and shape.isOnFace(x,y,z):
                        newdata[lx][ly][lz] = -1
                    
                    elif self.isOnFace(x,y,z) and shape.isOnFace(x,y,z):
                        newdata[lx][ly][lz] = 0
                    elif self.isOnFace(x,y,z) and shape.isOutside(x,y,z):
                        newdata[lx][ly][lz] = 0
                    elif self.isOutside(x,y,z) and shape.isOnFace(x,y,z):
                        newdata[lx][ly][lz] = 0

        newShape.data = newdata
        return newShape

    #update later by checking data matrix
    def isInside(self,x,y,z):
        s = self.scope
        lx = x - s.minx
        ly = y - s.miny
        lz = z - s.minz
        if 0<=lx<s.width and 0<=ly<s.height and 0<=lz<s.length and self.data[lx][ly][lz] == -1:
            return True
        else:
            return False
        '''
        if self.scope.minx<x and self.scope.maxx-1>x and self.scope.miny<y and self.scope.maxy-1>y and self.scope.minz<z and self.scope.maxz-1>z:
            return True
        return False
        '''

    def isOnFace(self,x,y,z):
        s = self.scope
        lx = x - s.minx
        ly = y - s.miny
        lz = z - s.minz
        if 0<=lx<s.width and 0<=ly<s.height and 0<=lz<s.length and self.data[lx][ly][lz] == 0:
            return True
        else:
            return False
    
    def isOutside(self, x, y,z):
        if not self.isInside(x,y,z) and not self.isOnFace(x,y,z):
            return True
        return False

def isSurface(level, box):
    if box.width<=0 or box.height<=0 or box.length<=0:
        return False
    air = 0
    ground = 0
    for x in range(box.minx, box.maxx):
        for y in range(box.miny, box.maxy):
            for z in range(box.minz, box.maxz):
                tb = level.blockAt((int)(x),(int)(y),(int)(z))  
                if tb == 0:
                    air = air+1
                else: 
                    ground = ground+1
    return  ground > 15

def isEnd(box, w=10, h=10, l=10):
    if box.width<=w and box.height<=h and box.length<=l:
        return True
    return False

#we air is empty
def surfaceBox(level, box, n=5):
    bfs = Queue.Queue()
    res = []
    
    bfs.put(box)
    while not bfs.empty():
        cur_box = bfs.get()
        flag = isSurface(level, cur_box)
        if isEnd(cur_box) and flag:                  
            res.append(cur_box)
            continue
        elif not isEnd(cur_box) and flag:
            n -= 1
            dim1 = [cur_box.width//2, cur_box.height//2, cur_box.length//2]
            dim2 = [cur_box.width-dim1[0], cur_box.height-dim1[1], cur_box.length-dim1[2]]
            o1 =  [cur_box.minx, cur_box.miny, cur_box.minz]
            d1 =  dim1
            bfs.put(BoundingBox(o1,d1))


            o2 =  (dim1[0]+o1[0],o1[1],o1[2])
            d2 = (dim2[0], dim1[1], dim1[2])

            bfs.put(BoundingBox(o2,d2))

            o3 =  (o1[0]+dim1[0], o1[1], o1[2]+dim1[2])
            d3 = (dim2[0], dim1[1],dim2[2])
            bfs.put(BoundingBox(o3,d3))

            o4 = (o1[0], o1[1], o1[2]+dim1[2])
            d4 = (dim1[0], dim1[1], dim2[2])
            bfs.put(BoundingBox(o4,d4))

            o5 = (o1[0],o1[1]+dim1[2],o1[2])
            d5 = (dim1[0],dim1[1],dim2[2])
            bfs.put(BoundingBox(o5,d5))

            o6 = (o1[0]+dim1[0], o1[1]+dim1[1], o1[2])
            d6 = (dim2[0], dim2[1], dim1[2])
            bfs.put(BoundingBox(o6,d6))

            o7 = (o1[0]+dim1[0], o1[1]+dim1[1], o1[2]+dim1[2])
            d7 = dim2
            bfs.put(BoundingBox(o7,d7))

            o8 = (o1[0], o1[1]+dim1[1], o1[2]+dim1[2])
            d8 = (dim1[0], dim2[1], dim2[2])
            bfs.put(BoundingBox(o8,d8))
    return res











'''
    def worldTolocal(self,point):
        wtol = mat([self.xaxis, self.yaxis, self.zaxis],dtype=int).T
        wpoint =  dot(wtol, mat((point-orign))
        #print "local pos", wpoint
        return wpoint.T 
    
    def localToworld(self,x,y,z):
        ltow = mat([self.xaxis, self.yaxis, self.zaxis],dtype=int).T
        #lpoint = dot(, array(([x-self.orign[0]],[y-self.orign[1]],[z-self.orign[2]])))
        #print mat(ltow).I
        #print "world pos", dot(mat(ltow).I, array(([x],[y],[z])))
        lpoint = dot(mat(ltow).I, array(([x],[y],[z])))
        lpoint = lpoint.T+self.orign
        return lpoint

    def isOnFrontFace(self,x,y,z):
        [lx,ly,lz] = self.worldTolocal(x,y,z)
        if lz == 0:
            return True
        return False

    def isOnBackFace(self,x,y,z):
        [lx,ly,lz] = self.worldTolocal(x,y,z)
        if lz == self.dim[2]:
            return True
        return False

    def isOnLeftFace(self,x,y,z):
        [lx,ly,lz] = self.worldTolocal(x,y,z)
        if lx == 0:
            return True
        return False

    def isOnRightFace(self,x,y,z):
        [lx,ly,lz] = self.worldTolocal(x,y,z)
        if lx == self.dim[0]:
            return True
        return False

    def isOnTopFace(self,x,y,z):
        [lx,ly,lz] = self.worldTolocal(x,y,z)
        if ly == self.dim[1]:
            return True
        return False

    def isOnBottomFace(self,x,y,z):
        [lx,ly,lz] = self.worldTolocal(x,y,z)
        if ly == 0:
            return True
        return False

    def ChangeDir(self,frontD):
        self.xaxis, self.yaxis, self.zaxis = getAxis(self.frontDir)
    
    def Transform(self, angle):
        pass
    
    def Scaling(self, x, y, z):
        pass

    def isOnFacades(self,x,y,z):
        if self.scope.minx==x and self.scope.maxx-1==x and self.scope.miny==y and self.scope.maxy-1==y and self.scope.minz==z and self.scope.maxz-1==z:
            return True
        return False

    def Add(self, shape):
        maxx = max(shape.scope.maxx, self.scope.maxx) 
        minx = min(shape.scope.minx, self.scope.minx)
        newShape = Shape()
        for x in range(minx,maxx):
            if shape.isInside(x,y,z) and self.isInside(x,y,z):
'''



            