import random
from os.path import exists

import numpy as np
from time import time_ns
from PIL import Image, ImageShow
from sys import platform


class PhotoViewer(ImageShow.Viewer):
    def __init__(self, viewer_exe, format, options=None, **kwargs):
        self._exe = viewer_exe
        self.format = format
        if options is not None:
            self.options = options
        super().__init__(**kwargs)

    def get_command(self, file, **options):
        return f'{self._exe} "{file}" && ping -n 2 127.0.0.1 >NUL && del /f "{file}"'

if platform == 'windows' and exists('C:/IrfanView/i_view64.exe'):
    print('Register IrfanView as Photo Viewer')

viewer = PhotoViewer('C:/IrfanView/i_view64.exe', 'TIFF')
ImageShow.register(viewer, 0)

HEIGHT = 128
WIDTH = 128
SEED = 8

UL = 0
UP = 1
UR = 2
LEFT = 3
RIGHT = 4
DL = 5
DOWN = 6
DR = 7

DX = [-1, 0, 1, -1, 1, -1, 0, 1]
DY = [1, 1, 1, 0, 0, -1, -1, -1]

# EXAMPLE = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
#             [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0],\
#             [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0],\
#             [0, 0, 0, 0, 0, 3, 4, 4, 5, 2, 4, 3, 5, 0],\
#             [0, 0, 0, 0, 3, 2, 4, 5, 2, 2, 2, 2, 2, 0],\
#             [0, 0, 0, 0, 1, 2, 3, 4, 5, 5, 3, 2, 2, 0],\
#             [0, 0, 0, 0, 1, 2, 3, 4, 5, 5, 3, 2, 2, 0],\
#             [0, 0, 0, 3, 6, 6, 7, 7, 7, 7, 6, 6, 6, 0],\
#             [0, 0, 0, 6, 6, 6, 7, 7, 7, 7, 6, 5, 5, 0],\
#             [0, 8, 8, 4, 4, 7, 7, 7, 5, 5, 5, 3, 3, 0],\
#             [0, 8, 3, 3, 3, 5, 5, 5, 5, 5, 5, 2, 2, 0],\
#             [0, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],\
#             [0, 8, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 0],\
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# EXAMPLE = [[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],\
#             [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],\
#             [0, 0, 0, 0, 3, 4, 4, 5, 2, 4, 3, 5],\
#             [0, 0, 0, 3, 2, 4, 5, 2, 2, 2, 2, 2],\
#             [0, 0, 0, 1, 2, 3, 4, 5, 5, 3, 2, 2],\
#             [0, 0, 0, 1, 2, 3, 4, 5, 5, 3, 2, 2],\
#             [0, 0, 3, 6, 6, 7, 7, 7, 7, 6, 6, 6],\
#             [0, 0, 6, 6, 6, 7, 7, 7, 7, 6, 5, 5],\
#             [8, 8, 4, 4, 7, 7, 7, 5, 5, 5, 3, 3],\
#             [8, 3, 3, 3, 5, 5, 5, 5, 5, 5, 2, 2],\
#             [8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],\
#             [8, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]]
EXAMPLE = np.array(
           [[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [ 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
           [ 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 11,2, 4, 3, 11,1, 3, 4, 1, 1, 0, 0, 0, 0],
           [ 0, 0, 0, 0, 0, 0, 3, 2, 4, 11,2, 2, 2, 2, 2, 3, 4, 4, 5, 1, 10,0, 0, 0],
           [ 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 12,11,11,3, 2, 2, 5, 5, 5, 5, 12,0, 0, 0],
           [ 0, 0, 0, 0, 0, 3, 7, 7, 8, 8, 8, 8, 7, 7, 7, 5, 5, 5, 5, 5, 12,0, 0, 0],
           [ 0, 0, 0, 0, 0, 7, 7, 7, 8, 8, 8, 8, 7, 11,11,11,11,1, 1, 1, 1, 0, 0, 0],
           [ 0, 0, 0, 9, 9, 4, 4, 8, 8, 8, 8, 8, 11,11,6, 11,11,12,1, 1, 1, 0, 0, 0],
           [ 0, 0, 0, 9, 3, 3, 4, 12,11,11,11,11,3, 2, 6, 2, 12,12,12,1, 0, 0, 0, 0],
           [ 0, 0, 0, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 12,12,12,1, 0, 0, 0, 0],
           [ 0, 0, 1, 9, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 12,12,12,0, 0, 0, 0, 0],
           [ 0, 0, 1, 9, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 12,12,12,0, 0, 0, 0, 0],
           [ 0, 0, 2, 9, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 12,12,12,0, 0, 0, 0, 0],
           [ 0, 0, 2, 9, 4, 2, 2, 2, 2, 3, 3, 3, 3, 11,11,3, 2, 1, 1, 1, 0, 0, 0, 0],
           [ 0, 0, 2, 4, 10,4, 2, 3, 2, 3, 2, 9, 2, 2, 11,11,2, 1, 1, 1, 0, 0, 0, 0],
           [ 0, 0, 2, 10,4, 2, 12,3, 2, 9, 12,2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0],
           [ 0, 0, 2, 4, 4, 2, 2, 3, 9, 9, 12,2, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
           [ 0, 0, 2, 2, 1, 0, 12,1, 12,9, 9, 2, 0, 0, 1, 12,12,2, 0, 0, 0, 0, 0, 0],
           [ 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
           [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], np.uint8)

def show_arr(res, rules):

    image_data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for rix, row in enumerate(res):
        for cix, p in enumerate(row):
            if p == 0:
                image_data[rix][cix] = 0x97, 0xb4, 0x86
            elif p == 1:
                image_data[rix][cix] = 0xfe, 0xfe, 0xbe
            elif p == 2:
                image_data[rix][cix] = 0xfd, 0xff, 0x69
            elif p == 3:
                image_data[rix][cix] = 0xe4, 0x99, 0x00
            elif p == 4:
                image_data[rix][cix] = 0xa7, 0x70, 0x00
            elif p == 5:
                image_data[rix][cix] = 0xfe, 0x81, 0x7d
            elif p == 6:
                image_data[rix][cix] = 0xff, 0x69, 0x48
            elif p == 7:
                image_data[rix][cix] = 0xff, 0x69, 0x48
            elif p == 8:
                image_data[rix][cix] = 0xa8, 0x27, 0x00
            elif p == 9:
                image_data[rix][cix] = 0x81, 0x81, 0x81
            elif p == 10:
                image_data[rix][cix] = 0x4f, 0x4f, 0x4f
            elif p == 11:
                image_data[rix][cix] = 0xbf, 0xe9, 0xff
            elif p == 12:
                image_data[rix][cix] = 0x7d, 0xb6, 0xe1
            else:
                image_data[rix][cix] = 0, 0, 0
            #percent = p / (max_num - min_num)
            #blue = (1- percent) * 0xFF
            #green = percent * 0xFF
            #image_data[rix][cix] = 0, blue, green

    image = Image.fromarray(image_data, mode='RGB')
    ImageShow.show(image, '2D Render')

def intersect_lists(ls0, ls1):
    res = np.full(len(ls0), 0, dtype=np.int32)
    if ls0[0] == -1:
        return ls1
    for i in range(len(ls0)):
        if ls0[i] == 0 or ls1[i] == 0:
            res[i] = 0
        else:
            res[i] = ls0[i] + ls1[i]
    return res

def _get_tile_new(rules, surr, zeroed):
    res = None
    copied = False
    for tile_type in range(8):
        tile = surr[tile_type]
        if tile == -1:
            continue
        other = rules[tile][DR - tile_type]
        if not copied:
            res = np.array(other, copy=True)
            copied = True
        else:
            res = np.where(np.logical_and(res != 0, other != 0), res + other, zeroed)
    return res

def _get_tile_old(rules, surr):
    res = np.full(len(rules), -1, dtype=np.int32)

    if surr[UL] != -1:
        res = intersect_lists(res, rules[surr[UL]][DR])
    if surr[UP] != -1:
        res = intersect_lists(res, rules[surr[UP]][DOWN])
    if surr[UR] != -1:
        res = intersect_lists(res, rules[surr[UR]][DL])
    if surr[LEFT] != -1:
        res = intersect_lists(res, rules[surr[LEFT]][RIGHT])
    if surr[RIGHT] != -1:
        res = intersect_lists(res, rules[surr[RIGHT]][LEFT])
    if surr[DL] != -1:
        res = intersect_lists(res, rules[surr[DL]][UR])
    if surr[DOWN] != -1:
        res = intersect_lists(res, rules[surr[DOWN]][UP])
    if surr[DR] != -1:
        res = intersect_lists(res, rules[surr[DR]][UL])
    return res

tile_times_old = []
tile_times_new = []

def get_tile(rules, surr, freqs, curr_freqs, zeroed):
    res = _get_tile_new(rules, surr, zeroed)

    return random.choices(range(len(rules)), weights=np.abs(res) + 1)[0]

def WFC_create_rules(inp):
    h = len(inp)
    w = 0
    rules = []
    maxi = 0
    if (h != 0):
        w = len(inp[0])
    else:
        return []
    for i in inp:
        for j in i:
            if j > maxi:
                maxi = j
    rules = np.full((maxi+1, 8, maxi+1), 0, dtype = np.int32)
    for y in range(h):
        for x in range(w):
            if y != h - 1:
                if x != 0:
                    rules[inp[y][x]][UL][inp[y+1][x-1]] += 1
                if x != w - 1:
                    rules[inp[y][x]][UR][inp[y+1][x+1]] += 1
                rules[inp[y][x]][UP][inp[y+1][x]] += 1
            if x != 0:
                rules[inp[y][x]][LEFT][inp[y][x-1]] += 1
            if x != w - 1:
                rules[inp[y][x]][RIGHT][inp[y][x+1]] += 1
            if y != 0:
                if x != 0:
                    rules[inp[y][x]][DL][inp[y-1][x-1]] += 1
                if x != w - 1:
                    rules[inp[y][x]][DR][inp[y-1][x+1]] += 1
                rules[inp[y][x]][DOWN][inp[y-1][x]] += 1
    for rule in rules:
        temp = rule[UP]
        rule[UP] = rule[DOWN]
        rule[DOWN] = temp
        temp = rule[UL]
        rule[UL] = rule[DL]
        rule[DL] = temp
        temp = rule[UR]
        rule[UR] = rule[DR]
        rule[DR] = temp
    for x in range(len(rules)):
        for y in range(len(rules[x])):
            for z in range(len(rules[x][y])):
                rules[x][y][z] = rules[x][y][z] ** 2
            #    total += rules[x][y][z]
            #for z in range(len(rules[x][y])):
            #    rules[x][y][z] /= total
    return rules

def get_environment():
    res = np.full((HEIGHT, WIDTH), -1, dtype=np.int32)
    for i in range(WIDTH):
        res[0][i] = 0
        res[HEIGHT - 1][i] = 0
    for i in range(HEIGHT):
        res[i][0] = 0
        res[i][WIDTH - 1] = 0
    return res

def WFC_collapse_rules(res, rules, freqs, freqses, resses, zeroed):
    failures = 50
    curr_freqs = np.full((len(rules)), 0, dtype=np.dtype(float))
    q = set()
    cx = WIDTH // 2
    cy = HEIGHT // 2
    res[cy][cx] = SEED
    curr_freqs[SEED] += (1 / (HEIGHT * WIDTH))
    q.add((cy + 1, cx - 1))
    q.add((cy + 1, cx))
    q.add((cy + 1, cx + 1))
    q.add((cy, cx - 1))
    q.add((cy, cx + 1))
    q.add((cy - 1, cx - 1))
    q.add((cy - 1, cx))
    q.add((cy - 1, cx + 1))
    while len(q) != 0:
        surr = np.full(8, -1, dtype = np.int32)
        curr = q.pop()
        y = curr[0]
        x = curr[1]
        if y != HEIGHT - 1:
            if x != 0:
                if res[y+1][x-1] == -1:
                    q.add((y+1, x-1))
                elif res[y+1][x-1] >= 0:
                    surr[UL] = res[y+1][x-1]
            if x != WIDTH - 1:
                if res[y+1][x+1] == -1:
                    q.add((y+1, x+1))
                elif res[y+1][x+1] >= 0:
                    surr[UR] = res[y+1][x+1]
            if res[y+1][x] == -1:
                q.add((y+1, x))
            elif res[y+1][x] >= 0:
                surr[UP] = res[y+1][x]
        if x != 0:
            if res[y][x-1] == -1:
                q.add((y, x-1))
            elif res[y][x-1] >= 0:
                surr[LEFT] = res[y][x-1]
        if x != WIDTH - 1:
            if res[y][x+1] == -1:
                q.add((y, x+1))
            elif res[y][x+1] >= 0:
                surr[RIGHT] = res[y][x+1]
        if y != 0:
            if x != 0:
                if res[y-1][x-1] == -1:
                    q.add((y-1, x-1))
                elif res[y-1][x-1] >= 0:
                    surr[DL] = res[y-1][x-1]
            if x != WIDTH - 1:
                if res[y-1][x+1] == -1:
                    q.add((y-1, x+1))
                elif res[y-1][x+1] >= 0:
                    surr[DR] = res[y-1][x+1]
            if res[y-1][x] == -1:
                q.add((y-1, x))
            elif res[y-1][x] >= 0:
                surr[DOWN] = res[y-1][x]
        res[y][x] = get_tile(rules, surr, freqs, curr_freqs, zeroed)
        if res[y][x] == -1:
            failures -= 1
            if (failures == 0 or ((HEIGHT // 2) - 3 < y < (HEIGHT // 2) + 3 and (WIDTH // 2) - 3 < x < (WIDTH // 2) + 3)):
                return False
            for i in range(max(0, y - 1), min(HEIGHT, y + 1)):
                for j in range(max(0, x - 1), min(WIDTH, x + 1)):
                    q.add((i, j))
        else:
            curr_freqs[res[y][x]] += (1 / (HEIGHT * WIDTH))
    #show_arr(res, rules)
    resses[1] = res
    freqses[1] = curr_freqs
    return True

def WFC_create_freqs(inp, rules):
    freqs = np.full((len(rules)), 0, dtype = np.dtype(float))
    for i in inp:
        for j in i:
            freqs[j] += 1
    total = freqs.sum()
    for freq in range(len(freqs)):
        freqs[freq] = freqs[freq] / total
    return freqs

def get_error(ls, freqs):
    err = 0
    for f in range(len(ls)):
        err += (ls[f] - freqs[f]) ** 2
    return err

def collapse_this():
    thing = False
    rules = WFC_create_rules(EXAMPLE)
    zeroed = np.zeros(rules.shape[0])
    freqs = WFC_create_freqs(EXAMPLE, rules)
    freqses = [0.0, 0.0]
    resses = [[], []]
    errs = []
    least = 1.0
    start = time_ns()
    while least > 0.01:
        thing = False
        while(not thing):
            res = get_environment()
            thing = WFC_collapse_rules(res, rules, freqs, freqses, resses, zeroed)
        attempt = get_error(freqses[1], freqs)
        if len(resses[0]) == 0:
            least = attempt
            resses[0] = resses[1]
            print("\nFinished on first try")
        elif (attempt < least):
            least = attempt
            resses[0] = resses[1]
            print("\nCollapsed")
    print((time_ns() - start) / 1000000)
    print(np.sum(tile_times_old) / len(tile_times_old), 'ns old avg')
    print(np.sum(tile_times_new) / len(tile_times_new), 'ns new avg')
    show_arr(resses[0], rules)


while True:
    collapse_this()