#!/usr/bin/python
# -*- coding: UTF-8 -*-
import HeightMap as H
import FlatFinder as F
import BorderAreaFinder as S
import GravityFinder as G
import Pioneer as P
from Shrine import *
from pagoda import *
from time import *
from MountainPath import *
from Laying import *
import BuildWFC
import center_position

displayName = "ICE_JIT_ft_WFC"


def get_len(t1, t2):
    return (t1[0] - t2[0])**2 + (t1[1] - t2[1])**2

def get_road_end(start_x, start_z, end_x, end_z, centre_of_map, half):
    min = 10**5
    road_end_list = [(start_x+half, start_z),
                     (start_x+half, end_z),
                     (start_x, start_z+half),
                     (end_x, start_z+half)]
    i = 0
    for one_end in road_end_list:
        m = get_len(one_end, centre_of_map)
        if min < m:
            min = m
            i = road_end_list.index(one_end)
    return road_end_list[i]


def perform(level, box, options):
    begin_time = time()
    """map_R1
    start_x = 140, start_z = 30
    width(x) = 256, depth(z) = 256
    map_R2
    start_x = 3, start_z = -6
    width(x) = 256, depth(z) = 256
    map_R3
    start_x = -346, start_z = -66
    width(x) = 256, depth(z) = 256
    """
    (width, height, depth) = getBoxSize(box)
    start_x = box.minx
    start_z = box.minz
    end_x = box.maxx
    end_z = box.maxz
    # start_x = -200
    # start_z = -500
    # end_x = start_x + 1000
    # end_z = start_z + 1000
    print "========================================================================="
    print 'start_x = %d, start_z = %d' % (start_x, start_z)
    print 'width(x) = %d, depth(z) = %d' % (end_x - start_x, end_z - start_z)
    centre_of_map = (start_x + width/2, start_z + depth/2)

    h = H.HeightMap(level, start_x, start_z, end_x, end_z)                      # Create height map

    if (end_x - start_x) * (end_z - start_z) >= 400*400:
        print('Large map')
        new_centre = center_position.CenterPosition(h.height_map_norm, 400)
        m = MountainPath(level, (start_x, start_z), (h.shape[0]/2, h.shape[1]/2), (0, 0), h, None, 0)
        new_s_x = start_x + new_centre[0] - 200
        new_s_z = start_z + new_centre[1] - 200
        new_e_x = new_s_x + 400
        new_e_z = new_s_z + 400
        road_end = get_road_end(new_s_x, new_s_z, new_e_x, new_e_z, centre_of_map, 200)
        m.end_pos = road_end
        m.scan_path()
        start_x, start_z, end_x, end_z = h.cut_HeightMap_by_filter(new_centre, 400)
        # h.showMap()
        # return
    h.calculate_gradient()
    f = F.FlatFinder(level, h)                                                   # Flat area finding
    candidate_points = f.getCandidatePoints()                                # Flat area's lowest norm points
    area = f.getMergeArea()                                                  # Merge flat area
    border_map = S.BorderAreaFinder(area)                                    # Create border map
    area_with_border = border_map.getAreaMap()
    area_borders_in_order = border_map.getAllAreaBordersInOrder()               # Get borders in measure's order
    show_border = 0
    if show_border == 1:
        # for x in range(area_with_border.shape[0]):
        #     for z in range(area_with_border.shape[1]):
        #         if area_with_border[x, z] == 5:
        #             setBlock(level, x + start_x, h.getHeight(x, z), z + start_z, 41)
        # return
        for group in area_borders_in_order:
            for one_p in group:
                height = h.getHeight(one_p[0], one_p[1])
                setBlock(level, one_p[0] + start_x, height, one_p[1] + start_z, 41)
    small_area = []
    wfc_area = []
    abandon_area = []
    bos = []
    for c_i in range(len(area_borders_in_order)):
        g = G.GravityFinder(area_borders_in_order[c_i])
        gravity_x, gravity_z = g.get_gravity_point2()
        # gravity_px = gravity_x + start_x
        # gravity_pz = gravity_z + start_z
        p = P.Pioneer(level, h, area_with_border, f.mergeArea_meanHeight, start_x, start_z, (gravity_x, gravity_z))
        u = p.getUtilization()
        # print "mean_height:", p.mean_height
        if u >= 0.5 and p.real_measure >= 5000:
            # print "重心 x:", gravity_x, " z:", gravity_z
            print 'creating country'
            print 'w:', p.width, 'h:', p.height
            print 'real_measure:', p.real_measure
            area_with_border = p.give_to_next()
            p.levelling()
            p.define_living_area()
            p.build_bridge()
        elif p.width >= 40 and p.height >= 40:
            area_with_border = p.give_to_next()
            wfc_area.append(p)
        elif p.width >= 17 and p.height >= 17:
            area_with_border = p.give_to_next()
            small_area.append(p)
        # else:
        #     abandon_area.append(p)
    print "small area: ", len(small_area)
    wfc_count = 0
    print "wfc area: ", len(wfc_area)
    for one_wfc_area in sorted(wfc_area, key=lambda one: one.get_mean_height()):
        c_x = one_wfc_area.x1
        c_z = one_wfc_area.z1
        c_px = c_x + start_x
        c_pz = c_z + start_z
        wfc_height = 10
        if one_wfc_area.material_dict["is_desert"]:
            print 'wfc is_desert'
            BuildWFC.dict_4_WFC['minecraft:jungle_log[axis=y,]'] = (17, 2)
            BuildWFC.dict_4_WFC['minecraft:jungle_planks'] = (5, 2)
            BuildWFC.dict_4_WFC['minecraft:oak_planks'] = (0, 0)
            BuildWFC.dict_4_WFC['minecraft:stone_brick_slab[waterlogged=false,type=bottom,]'] = (44, 1)
            # BuildWFC.dict_4_WFC['minecraft:stone_brick_slab[waterlogged=false,type=bottom,]'] = (182, 0)
            # BuildWFC.dict_4_WFC['minecraft:stone_bricks'] = (24, 0)
            BuildWFC.dict_4_WFC['minecraft:stone_bricks'] = (179, 0)
            wfc_height = 20
            Laying(level, h, (start_x, 0, start_z), (c_x, 1, c_z), (c_x + 40, 30, c_z + 40),
                   one_wfc_area.mean_height+1, (12, 0, 12, 0, 0), True)
        else:
            print 'wfc is not desert'
            Laying(level, h, (start_x, 0, start_z), (c_x, 1, c_z), (c_x + 40, 30, c_z + 40),
                   one_wfc_area.mean_height+1, (2, 0, 3, 0, 0), True)

        BuildWFC.build(level, 10, wfc_height, 10, c_px, one_wfc_area.mean_height+2, c_pz)
        wfc_count += 1

    shrine_count = 0
    pagoda_count = 0

    exchange_type_flag = False
    one_near_water = False
    for one_area in sorted(small_area, key=lambda one: one.get_mean_height()):
        c_x = one_area.x1 + one_area.width/2
        c_z = one_area.z1 + one_area.height/2
        c_px = c_x + start_x
        c_pz = c_z + start_z
        if not one_area.secure_area(c_x, c_z, 11, 11):
            abandon_area.append(one_area)
            continue
        if not one_near_water:
            if one_area.find_water(c_x, c_z, 10, 10):
                print "Shrine Builded near water"
                exchange_type_flag = True
                one_near_water = True
                # for one_b_pos in one_area.get_bridge_pos():
                #     b_pos.append(one_b_pos)
        if exchange_type_flag:
            # if one_area.find_water(c_x, c_z, 10, 10):
            #     for one_b_pos in one_area.get_bridge_pos():
            #         b_pos.append(one_b_pos)
            Laying(level, h, (start_x, 0, start_z), (c_x-10, 1, c_z-10), (c_x+11, 26, c_z+11),
                   one_area.mean_height+1, (43, 5, 3, 0, 0), True)
            ss = Shrine_Builder(level, c_px - 8, one_area.mean_height + 2, c_pz - 8, 0,
                                one_area.material_dict["tree_ID"][0],
                                one_area.material_dict["tree_ID"][1], one_area.material_dict["wood_ID"][0],
                                one_area.material_dict["wood_ID"][1],
                                one_area.material_dict["roof_ID"])
            ss.build()
            if one_area.mean_height >= 70:
                m = MountainPath(level, (start_x, start_z), (c_x, c_z), (0, 0), h, one_area.area_with_border, 1)
                res = m.find_goal()
                # print "m.find_goal()", res
                if res != (0, 0):
                    m.scan_path()
            shrine_count += 1
            exchange_type_flag = False
        else:
            # if one_area.find_water(c_x, c_z, 10, 10):
            #     for one_b_pos in one_area.get_bridge_pos():
            #         b_pos.append(one_b_pos)
            Laying(level, h, (start_x, 0, start_z), (c_x - 10, 1, c_z - 10), (c_x + 11, 31, c_z + 11),
                   one_area.mean_height, (43, 5, 3, 0, 0), True)
            # for j in range(57):
            #     setBlock(level, c_px, one_area.mean_height+j, c_pz, 41)
            p = Pagoda_builder(level, c_px - 9, one_area.mean_height + 1, c_pz - 9,
                               one_area.material_dict["tree_ID"][0],
                               one_area.material_dict["tree_ID"][1], one_area.material_dict["wood_ID"][0],
                               one_area.material_dict["wood_ID"][1],
                               one_area.material_dict["roof_ID"])
            p.build()
            if one_area.mean_height >= 70:
                m = MountainPath(level, (start_x, start_z), (c_x, c_z), (0, 0), h, one_area.area_with_border, 0)
                res = m.find_goal()
                # print "m.find_goal()", res
                if res != (0, 0):
                    m.scan_path()
            pagoda_count += 1
            exchange_type_flag = True
    print "abandon area: ", len(abandon_area)
    if pagoda_count == 0 and len(abandon_area) > 0:
        one_area = abandon_area.pop()
        c_x = one_area.x1 + one_area.width / 2
        c_z = one_area.z1 + one_area.height / 2
        c_px = c_x + start_x
        c_pz = c_z + start_z
        Laying(level, h, (start_x, 0, start_z), (c_x - 10, 1, c_z - 10), (c_x + 11, 31, c_z + 11),
               one_area.mean_height, (43, 5, 3, 0, 0), True)
        # for j in range(57):
        #     setBlock(level, c_px, one_area.mean_height+j, c_pz, 41)
        p = Pagoda_builder(level, c_px - 9, one_area.mean_height + 1, c_pz - 9,
                           one_area.material_dict["tree_ID"][0],
                           one_area.material_dict["tree_ID"][1], one_area.material_dict["wood_ID"][0],
                           one_area.material_dict["wood_ID"][1],
                           one_area.material_dict["roof_ID"])
        p.build()
        pagoda_count += 1
    if shrine_count == 0 and len(abandon_area) > 0:
        one_area = abandon_area.pop()
        c_x = one_area.x1 + one_area.width / 2
        c_z = one_area.z1 + one_area.height / 2
        c_px = c_x + start_x
        c_pz = c_z + start_z
        Laying(level, h, (start_x, 0, start_z), (c_x - 10, 1, c_z - 10), (c_x + 11, 26, c_z + 11),
               one_area.mean_height + 1, (43, 5, 3, 0, 0), True)
        ss = Shrine_Builder(level, c_px - 8, one_area.mean_height + 2, c_pz - 8, 0,
                            one_area.material_dict["tree_ID"][0],
                            one_area.material_dict["tree_ID"][1], one_area.material_dict["wood_ID"][0],
                            one_area.material_dict["wood_ID"][1],
                            one_area.material_dict["roof_ID"])
        ss.build()
        shrine_count += 1
    print "shrine:", shrine_count
    print "pagoda:", pagoda_count
    print 'wfc:', wfc_count
    end_time = time()
    run_time = end_time - begin_time
    print "completed"
    print "Filter Runtime: %.2f s" % run_time

