import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter

import tensorflow as tf

import os


class VideoWriter:
    def __init__(self, filename=None, scale=None, fps=30.0, **kw):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.scale = scale
        self.writer = None
        self.params = dict(filename=filename, fps=fps, **kw)
        self.frames = np.array([])

    def add_img(self, img):
        img = np.asarray(img)
        if self.writer is None:
            h, w = img.shape[:2]
            self.writer = FFMPEG_VideoWriter(size=(w, h), **self.params)
        if img.dtype in [np.float32, np.float64]:
            img = np.uint8(img.clip(0, 1)*255)
        if len(img.shape) == 2:
            img = np.repeat(img[..., None], 3, -1)
        self.writer.write_frame(img)

    # Creates a heat map image from a 2d numpy array and adds it to the video
    def add_grid(self, grid, scale=None, cmap="hot"):
        if self.scale is None:
            if scale is None:
                # 512 is the default size of the video, grids smaller than this will be upscaled
                self.scale = 512/grid.shape[1]
            else:
                self.scale = scale
        norm = mpl.colors.Normalize(grid.min(), grid.max())
        m = cm.ScalarMappable(norm=norm, cmap=cmap)
        img = m.to_rgba(grid)
        self.add_img(self.to_rgb(self.zoom(np.array(img), scale)))

    def add_concat_grids(self, grids, scale=None, cols=3, cmaps=None):
        if cmaps is None:
            cmaps = ["hot"]*len(grids)

        rows = (len(grids)-1)//cols+1
        h, w = grids[0].shape[:2]
        grid = np.zeros((h*rows, w*cols, 4))
        for i, (g, cmap) in enumerate(zip(grids, cmaps)):
            norm = mpl.colors.Normalize(g.min(), g.max())
            m = cm.ScalarMappable(norm=norm, cmap=cmap)
            grid[i//cols*h:(i//cols+1)*h, i %
                 cols*w:(i % cols+1)*w] = m.to_rgba(g)
            # self.to_alpha(
            #     self.zoom(self.to_rgb(m.to_rgba(g, cmap)), self.scale))
        if scale is None:
            # 512 is the default size of the video, grids smaller than this will be upscaled
            self.scale = 512/grid.shape[1]
        else:
            self.scale = scale
        self.add_img(self.to_rgb(self.zoom(grid, self.scale)))

    def add_img_buf(self, img_buf):
        img = tf.image.decode_png(img_buf, channels=3)
        self.add_img(img)

    def to_alpha(self, x):
        return tf.clip_by_value(x[..., 3:4], 0.0, 1.0)

    def to_rgb(self, x):
        # assume rgb premultiplied by alpha
        rgb, a = x[..., :3], self.to_alpha(x)
        return 1.0-a+rgb

    def zoom(self, img, scale=4):
        img = np.repeat(img, scale, 0)
        img = np.repeat(img, scale, 1)
        return img

    def close(self):
        if self.writer:
            self.writer.close()

    def __enter__(self):
        return self

    def __exit__(self, *kw):
        self.close()
