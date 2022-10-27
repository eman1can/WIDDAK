from PIL import Image
import numpy as np

WIDTH = 5
HEIGHT = 5

data = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 2, 1, 0],
    [1, 1, 2, 2, 1],
    [1, 3, 4, 3, 1]
]

min_num = 0
max_num = 7

image_data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
for rix, row in enumerate(data):
    for cix, p in enumerate(row):
        percent = p / (max_num - min_num)
        blue = percent * 0xFF
        green = (1 - percent) * 0xFF
        image_data[rix][cix] = 0, blue, green

image = Image.fromarray(image_data, mode='RGB')
image.show()
