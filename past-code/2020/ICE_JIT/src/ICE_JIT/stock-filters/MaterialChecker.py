#!/usr/bin/python
# -*- coding: UTF-8 -*-


def Material_Checker(lv, h, s_x, s_z, sx, sz, ex, ez):
    # print sx, sz, ex, ez
    # begin_time = time()
    material_dict = {}
    ID = 0
    data = 0
    m = 0
    tree = [0]*6
    sand_num = 0
    roof_ID = (109, 44, 5, 43, 5)
    material_dict["fence_id"] = (43, 3, 191)
    # material_dict["floor_id"] = [12, 0]
    material_dict["floor_id"] = (1, 6)
    material_dict["is_desert"] = False

    for i in range(sx, ex):
        for k in range(sz, ez):
            height = h.getHeight(i, k)
            for j in range(height, height+10):
                ID = lv.blockAt(i+s_x, j, k+s_z)
                data = lv.blockDataAt(i+s_x, j, k+s_z)
                if ID==17 and data<=3:
                    tree[data]+=1
                elif ID==162 and data<=1:
                    tree[data+3]+=1
                elif ID == 12:
                    sand_num += 1

    for s in range(1, 5):
        if tree[m] < tree[s]:
            m = s

    # print tree
    # end_time = time()
    # run_time = end_time - begin_time
    # print "Material_Checker's runtime: %.2f s" % run_time

    if 0 <= m <= 3:
        material_dict["tree_ID"] = (17, m)
        material_dict["wood_ID"] = (5, m)

    elif m <= 4:
        material_dict["tree_ID"] = (162, m-4)
        material_dict["wood_ID"] = (5, m)
    if float((ex - sx) * (ez - sz)) > 0:
        v = float(sand_num) / float((ex - sx) * (ez - sz))
        if v >= 0.4:
            # print "desert rate above 0.4: ", v
            roof_ID = (180, 182, 0, 179, 0)
            material_dict["fence_id"] = (24, 0, 189)
            material_dict["floor_id"] = (1, 6)
            material_dict["tree_ID"] = (24, 0)
            material_dict["wood_ID"] = (5, 2)
            material_dict["is_desert"] = True
    material_dict["roof_ID"] = roof_ID
    # print material_dict
    return material_dict
