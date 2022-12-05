import random
from itertools import product
from os import mkdir
from os.path import exists, join

import sys
import numpy as np
from time import time_ns
from PIL import Image, ImageShow
from sys import platform
import imageio


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

np.set_printoptions(threshold=sys.maxsize)

HEIGHT = 32
WIDTH = 32
SEED = 8

UL    = 0
UP    = 1
UR    = 2
LEFT  = 3
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
EXAMPLE = np.array(
          [[13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13],
           [13,13,13,13,13,13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,13,13,13],
           [13,13,13,13,13,13, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,13,13],
           [13,13,13,13,13, 0, 0, 3, 4, 4, 11,2, 4, 3, 11,1, 3, 4, 1, 1, 0, 0,13],
           [13,13,13,13,13, 0, 3, 2, 4, 11,2, 2, 2, 2, 2, 3, 4, 4, 5, 1, 10,0,13],
           [13,13,13,13, 0, 0, 1, 2, 3, 4, 12,11,11,3, 2, 2, 5, 5, 5, 5, 12,0,13],
           [13,13,13,13, 0, 3, 7, 7, 8, 8, 8, 8, 7, 7, 8, 5, 5, 5, 5, 5, 12,0,13],
           [13,13, 0, 0, 0, 7, 7, 7, 8, 8, 8, 8, 7, 11,11,11,11,1, 1, 1, 1, 0,13],
           [13,13, 0, 9, 9, 4, 4, 8, 8, 8, 8, 8, 11,11,6, 11,11,12,1, 1, 1, 0,13],
           [13, 0, 0, 9, 3, 3, 4, 12,11,11,11,11,3, 2, 6, 2, 12,12,12,1, 0, 0,13],
           [13, 0, 1, 9, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 12,12,12,0, 0,13,13],
           [13, 0, 1, 9, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 12,12,12,0,13,13,13],
           [13, 0, 2, 9, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 12,12,12,0, 0,13,13],
           [13, 0, 2, 9, 4, 2, 2, 2, 2, 3, 3, 3, 3, 11,11,3, 2, 1, 1, 1, 0,13,13],
           [13, 0, 2, 4, 10,4, 2, 3, 2, 3, 2, 9, 2, 2, 11,11,2, 1, 1, 1, 0,13,13],
           [13, 0, 2, 10,4, 2, 12,3, 2, 9, 12,2, 2, 2, 2, 2, 2, 1, 1, 1, 0,13,13],
           [13, 0, 2, 4, 4, 2, 2, 3, 9, 9, 12,2, 0, 1, 1, 1, 1, 0, 0, 0, 0,13,13],
           [13, 0, 2, 2, 1, 0, 12,1, 12,9, 9, 2, 0, 0, 1, 12,12,2, 0, 13,13,13,13],
           [13, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0,13,13,13,13],
           [13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,13, 0, 0, 0, 0, 0,13,13,13,13],
           [13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13]], np.uint8)

def get_image(res):
    image_data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    colors = [
        [0xFF, 0x00, 0x00],  # -2
        [0x00, 0x00, 0x00],  # -1
        [0x97, 0xb4, 0x86],  # 0
        [0xfe, 0xfe, 0xbe],  # 1
        [0xfd, 0xff, 0x69],  # 2
        [0xe4, 0x99, 0x00],  # 3...
        [0xa7, 0x70, 0x00],
        [0xfe, 0x81, 0x7d],
        [0xff, 0x69, 0x48],
        [0xff, 0x69, 0x48],
        [0xa8, 0x27, 0x00],
        [0x81, 0x81, 0x81],
        [0x4f, 0x4f, 0x4f],
        [0xbf, 0xe9, 0xff],
        [0x7d, 0xb6, 0xe1],
        [0x00, 0x00, 0x00]
    ]

    rows, cols = res.shape
    for rix, cix in product(range(rows), range(cols)):
        image_data[rix, cix] = colors[res[rix][cix] + 2]
        #for i in range(10):
        #    for j in range(10):
        #        image_data[rix * 10 + i, cix * 10 + j] = colors[res[rix][cix] + 2]
    return image_data
    #return Image.fromarray(image_data, mode='RGB')

def show_arr(res):
    image = get_image(res)
    ImageShow.show(image, '2D Render')

images = []

def save_arr(res):
    global images
    image = get_image(res)
    images.append(image)

def gen_gif(name):
    global images
    tmp = []
    for img in images:
        image_data = np.zeros((HEIGHT * 10, WIDTH * 10, 3), dtype=np.uint8)
        for h in range(HEIGHT):
            for w in range(WIDTH):
                for i in range(10):
                    for j in range(10):
                        image_data[h * 10 + i][w * 10 + j] = img[h][w]
        tmp.append(Image.fromarray(image_data, mode='RGB'))
    #images = [images[i] for i in range(0, len(images), 100)]
    imageio.mimsave(join('renders', 'wfc', name), tmp + [tmp[-1]] + [tmp[-1]] + [tmp[-1]] + [tmp[-1]] + [tmp[-1]] + [tmp[-1]] + [tmp[-1]] + [tmp[-1]] + [tmp[-1]])

def intersect_lists(ls0, ls1):
    res = np.full(len(ls0), 0, dtype = np.int32)
    for i in range(len(ls0)):
        if ls0[i] != 0 and ls1[i] != 0:
            res[i] = ls0[i] + ls1[i]
    return res

def get_tile(rules, surr, zeroed):
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
    if res is None or np.sum(res) == 0:
        return -1
    return random.choices(range(len(rules)), weights=np.abs(res) + 1)[0]

def WFC_create_rules(inp):
    h, w = inp.shape

    if h == 0:
        return []

    maxi = np.max(inp)
    rules = np.zeros((maxi + 1, 8, maxi + 1), np.int32)
    for x in range(w):
        for y in range(h):
            ix = inp[y][x]
            for sx in range(8):
                cx, cy = x + DX[sx], y + DY[sx]
                if cx < 0 or cy < 0:
                    continue
                if cx >= w or cy >= h:
                    continue
                rules[ix, sx, inp[cy, cx]] += 1

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
                rules[x][y][z] = rules[x][y][z]**3
    return rules

def get_environment():
    res = np.full((HEIGHT, WIDTH), -1, dtype = np.int32)
    for i in range(WIDTH):
        res[0][i] = 13
        res[HEIGHT - 1][i] = 13
    for i in range(HEIGHT):
        res[i][0] = 13
        res[i][WIDTH - 1] = 13
    return res

def AddToQueue(q, y, x):
    if x < 0 or y < 0:
        return
    if x > WIDTH or y > HEIGHT:
        return
    q.add((y, x))

def WFC_collapse_rules(res, rules, freqs, freqses, resses):
    failures = 50
    curr_freqs = np.full((len(rules)), 0, dtype=float)
    q = set()
    cx = WIDTH // 2
    cy = HEIGHT // 2
    res[cy][cx] = SEED
    curr_freqs[SEED] += (1 / (HEIGHT * WIDTH))

    for sx in range(0, 8):
        AddToQueue(q, cy + DY[sx], cx + DX[sx])

    surr = np.full(8, -1, dtype=np.int32)
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
        res[y][x] = get_tile(rules, surr, np.zeros(rules.shape[0]))
        if res[y][x] == -1:
            failures -= 1
            if (failures == 0 or ((HEIGHT // 2) - 3 < y < (HEIGHT // 2) + 3 and (WIDTH // 2) - 3 < x < (WIDTH // 2) + 3)):
                return False
            for i in range(max(0, y - 1), min(HEIGHT, y + 1)):
                for j in range(max(0, x - 1), min(WIDTH, x + 1)):
                    q.add((i, j))
        else:
            curr_freqs[res[y][x]] += (1 / (HEIGHT * WIDTH))
        save_arr(res)
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

def WFC_Cleanup(output):
    farmland = set()
    q = set()
    for i in range(WIDTH):
        q.add((0, i))
        q.add((HEIGHT - 1, i))
        farmland.add((0, i))
        farmland.add((HEIGHT - 1, i))
    for i in range(HEIGHT):
        q.add((i, 0))
        q.add((i, WIDTH - 1))
        farmland.add((i, 0))
        farmland.add((i, WIDTH - 1))
    while len(q) > 0:
        y, x = q.pop()
        if x < 0 or y < 0 or y >= HEIGHT or x >= WIDTH:
            continue
        for sx in [UP, LEFT, RIGHT, DOWN]:
            if (y + DY[sx], x + DX[sx]) not in farmland and (0 < y + DY[sx] < HEIGHT and 0 < x + DX[sx] < WIDTH and output[y + DY[sx], x + DX[sx]] == 0):
                q.add((y + DY[sx], x + DX[sx]))
                farmland.add((y + DY[sx], x + DX[sx]))
    for iy, y in enumerate(output):
        for ix, x in enumerate(y):
            if x == 0 and ((iy, ix) not in farmland):
                output[iy, ix] = 1  # Change to low residential
    return output

def collapse_this(iter):
    global images
    thing = False
    rules = WFC_create_rules(EXAMPLE)
    freqs = WFC_create_freqs(EXAMPLE, rules)
    freqses = [0.0, 0.0]
    resses = [[], []]
    errs = []
    least = 1.0
    start = time_ns()
    while least > 0.05:
        thing = False
        while (not thing):
            res = get_environment()
            images.clear()
            thing = WFC_collapse_rules(res, rules, freqs, freqses, resses)
        attempt = get_error(freqses[1], freqs)
        if attempt < least:
            least = attempt
            resses[0] = resses[1]
    print((time_ns() - start) / 1000000)
    gen_gif("big_" + str(iter) + ".gif")
    #resses[0] = WFC_Cleanup(resses[0])
    #show_arr(resses[0])

def WFC_print_rules(rules):
    for tile_types in rules:
        for surrounding_tiles in tile_types:
            for weight in surrounding_tiles:
                print(f'{weight:5}', end=' | ')
            print('\b')
        print('-' * (len(surrounding_tiles) * 5 + 3 * len(surrounding_tiles) - 1))

for i in range(30):
    collapse_this(i)