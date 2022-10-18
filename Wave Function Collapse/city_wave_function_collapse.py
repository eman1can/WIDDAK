from random import shuffle, choices
from itertools import product
from os import mkdir
from os.path import exists, join

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

HEIGHT = 32
WIDTH = 32
SEED = 8

UL    = 0
UP    = 1
UR    = 2
LEFT  = 3
RIGHT = 4
DL    = 5
DOWN  = 6
DR    = 7

DX = [-1, 0, 1, -1, 1, -1, 0, 1]
DY = [1, 1, 1, 0, 0, -1, -1, -1]

# EXAMPLE = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0],
#             [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 0],
#             [0, 0, 0, 0, 0, 3, 4, 4, 5, 2, 4, 3, 5, 0],
#             [0, 0, 0, 0, 3, 2, 4, 5, 2, 2, 2, 2, 2, 0],
#             [0, 0, 0, 0, 1, 2, 3, 4, 5, 5, 3, 2, 2, 0],
#             [0, 0, 0, 0, 1, 2, 3, 4, 5, 5, 3, 2, 2, 0],
#             [0, 0, 0, 3, 6, 6, 7, 7, 7, 7, 6, 6, 6, 0],
#             [0, 0, 0, 6, 6, 6, 7, 7, 7, 7, 6, 5, 5, 0],
#             [0, 8, 8, 4, 4, 7, 7, 7, 5, 5, 5, 3, 3, 0],
#             [0, 8, 3, 3, 3, 5, 5, 5, 5, 5, 5, 2, 2, 0],
#             [0, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
#             [0, 8, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# EXAMPLE = [[0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
#             [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],
#             [0, 0, 0, 0, 3, 4, 4, 5, 2, 4, 3, 5],
#             [0, 0, 0, 3, 2, 4, 5, 2, 2, 2, 2, 2],
#             [0, 0, 0, 1, 2, 3, 4, 5, 5, 3, 2, 2],
#             [0, 0, 0, 1, 2, 3, 4, 5, 5, 3, 2, 2],
#             [0, 0, 3, 6, 6, 7, 7, 7, 7, 6, 6, 6],
#             [0, 0, 6, 6, 6, 7, 7, 7, 7, 6, 5, 5],
#             [8, 8, 4, 4, 7, 7, 7, 5, 5, 5, 3, 3],
#             [8, 3, 3, 3, 5, 5, 5, 5, 5, 5, 2, 2],
#             [8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
#             [8, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]]
EXAMPLE = np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 11,2, 4, 3, 11,1, 3, 4, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 2, 4, 11,2, 2, 2, 2, 2, 3, 4, 4, 5, 1, 10,0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 12,11,11,3, 2, 2, 5, 5, 5, 5, 12,0, 0, 0],
    [0, 0, 0, 0, 0, 3, 7, 7, 8, 8, 8, 8, 7, 7, 7, 5, 5, 5, 5, 5, 12,0, 0, 0],
    [0, 0, 0, 0, 0, 7, 7, 7, 8, 8, 8, 8, 7, 11,11,11,11,1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 9, 9, 4, 4, 8, 8, 8, 8, 8, 11,11,6, 11,11,12,1, 1, 1, 0, 0, 0],
    [0, 0, 0, 9, 3, 3, 4, 12,11,11,11,11,3, 2, 6, 2, 12,12,12,1, 0, 0, 0, 0],
    [0, 0, 0, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 12,12,12,1, 0, 0, 0, 0],
    [0, 0, 1, 9, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 12,12,12,0, 0, 0, 0, 0],
    [0, 0, 1, 9, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 12,12,12,0, 0, 0, 0, 0],
    [0, 0, 2, 9, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 12,12,12,0, 0, 0, 0, 0],
    [0, 0, 2, 9, 4, 2, 2, 2, 2, 3, 3, 3, 3, 11,11,3, 2, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 2, 4, 10,4, 2, 3, 2, 3, 2, 9, 2, 2, 11,11,2, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 2, 10,4, 2, 12,3, 2, 9, 12,2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 2, 4, 4, 2, 2, 3, 9, 9, 12,2, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 1, 0, 12,1, 12,9, 9, 2, 0, 0, 1, 12,12,2, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], np.uint8)

def get_image(res):
    image_data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    colors = [
        [0xFF, 0x00, 0x00],  # -2
        [0x00, 0x00, 0x00],  # -1
        [0x97, 0xB4, 0x86],  # 0
        [0x97, 0xb4, 0x86],  # ...
        [0xfe, 0xfe, 0xbe],
        [0xfd, 0xff, 0x69],
        [0xe4, 0x99, 0x00],
        [0xa7, 0x70, 0x00],
        [0xfe, 0x81, 0x7d],
        [0xff, 0x69, 0x48],
        [0xff, 0x69, 0x48],
        [0xa8, 0x27, 0x00],
        [0x81, 0x81, 0x81],
        [0x4f, 0x4f, 0x4f],
        [0xbf, 0xe9, 0xff],
        [0x7d, 0xb6, 0xe1]
    ]

    rows, cols = res.shape
    for rix, cix in product(range(rows), range(cols)):
        image_data[rix, cix] = colors[res[rix][cix] + 2]

    return Image.fromarray(image_data, mode='RGB')

def show_arr(res):
    image = get_image(res)
    ImageShow.show(image, '2D Render')

images = []

def save_arr(res):
    global images
    image = get_image(res)
    images.append(image)

def gen_gif():
    global images
    imageio.mimsave(join('renders', 'wfc', 'output.gif'), images)

def intersect_lists(ls0, ls1):
    res = np.full(len(ls0), 0, dtype = np.int32)
    if ls0[0] == -1:
        return ls1
    for i in range(len(ls0)):
        if ls0[i] == 0 or ls1[i] == 0:
            res[i] = 0
        else:
            res[i] = ls0[i] + ls1[i]
    return res

def get_tile(rules, surr, freqs, curr_freqs):
    for tile_type in [UL, UP, UR, LEFT, RIGHT, DL, DOWN, DR]:
        tile = surr[tile_type]
        if tile == -1:
            continue
        other_tile = surr[DR - tile_type]
        if other_tile == -1:
            weights = rules[tile][other_tile]
        else:
            weights = np.zeros(len(rules), np.float32)
            a = rules[tile][DR - tile_type]
            b = rules[other_tile][tile_type]
            for ix in range(len(rules)):
                if a[ix] == 0 or b[ix] == 0:
                    continue
                weights[ix] = (a[ix] + b[ix]) ** 0.2
        if np.sum(weights) > 0:
            return choices(range(len(rules)), weights=weights)[0]
    return -1


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
            #total = 0
            for z in range(len(rules[x][y])):
                rules[x][y][z] = rules[x][y][z]
            #    total += rules[x][y][z]
            #for z in range(len(rules[x][y])):
            #    rules[x][y][z] /= total
    return rules

def get_environment():
    res = np.full((HEIGHT, WIDTH), -1, dtype = np.int32)
    for i in range(WIDTH):
        res[0][i] = 0
        res[HEIGHT - 1][i] = 0
    for i in range(HEIGHT):
        res[i][0] = 0
        res[i][WIDTH - 1] = 0
    return res


def AddToQueue(q, y, x):
    if x < 0 or y < 0:
        return
    if x > WIDTH or y > HEIGHT:
        return
    q.append((y, x))


def WFC_collapse_rules(res, rules, freqs, freqses, resses):
    failures = 50
    curr_freqs = np.full((len(rules)), 0, dtype=float)
    q = set()
    cx = WIDTH // 2
    cy = HEIGHT // 2
    res[cy][cx] = SEED
    curr_freqs[SEED] += (1 / (HEIGHT * WIDTH))

    p = []
    for sx in [LEFT, RIGHT, UP, DOWN]:
        AddToQueue(p, cy + DY[sx], cx + DX[sx])
    shuffle(p)
    for sp in p:
        q.add(sp)

    surr = np.full(8, -1, dtype=np.int32)
    while len(q) != 0:
        y, x = q.pop()

        p = []
        for sx in range(0, 8):
            dx, dy = DX[sx], DY[sx]
            tile = res[y + dy][x + dx]
            if tile == -1:
                AddToQueue(p, y + dy, x + dx)
            else:
                surr[sx] = tile
        shuffle(p)
        for sp in p:
            q.add(sp)

        res[y][x] = get_tile(rules, surr, freqs, curr_freqs)

        if res[y][x] == -1:
            failures -= 1
            if (failures == 0 or ((HEIGHT // 2) - 3 < y < (HEIGHT // 2) + 3 and (WIDTH // 2) - 3 < x < (WIDTH // 2) + 3)):
                return False
            p = []
            for i in range(max(0, y - 1), min(HEIGHT, y + 1)):
                for j in range(max(0, x - 1), min(WIDTH, x + 1)):
                    p.append((i, j))
            shuffle(p)
            for sp in p:
                q.add(sp)
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

def WFC_print_rules(rules):
    for tile_types in rules:
        for surrounding_tiles in tile_types:
            for weight in surrounding_tiles:
                print(f'{weight:5}', end=' | ')
            print('\b')
        print('-' * (len(surrounding_tiles) * 5 + 3 * len(surrounding_tiles) - 1))

thing = False
rules = WFC_create_rules(EXAMPLE)
WFC_print_rules(rules)
freqs = WFC_create_freqs(EXAMPLE, rules)
freqses = [0.0, 0.0]
resses = [[], []]
errs = []
least = 1.0
start = time_ns()
while least > 0.05:
    thing = False
    while not thing:
        res = get_environment()
        thing = WFC_collapse_rules(res, rules, freqs, freqses, resses)
    attempt = get_error(freqses[1], freqs)
    if len(resses[0]) == 0:
        least = attempt
        resses[0] = resses[1]
    elif attempt < least:
        least = attempt
        resses[0] = resses[1]

print('Finished in', (time_ns() - start) / 1000000)
if not exists(join('renders', 'wfc')):
    if not exists('renders'):
        mkdir('renders')
    mkdir(join('renders', 'wfc'))
gen_gif()
show_arr(resses[0])
