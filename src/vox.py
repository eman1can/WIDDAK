import builtins
import numpy as np

from gdpc.template import Template

default_palette = np.array([
    0x00000000, 0xffffffff, 0xffccffff, 0xff99ffff, 0xff66ffff, 0xff33ffff, 0xff00ffff, 0xffffccff, 0xffccccff, 0xff99ccff, 0xff66ccff, 0xff33ccff, 0xff00ccff, 0xffff99ff, 0xffcc99ff, 0xff9999ff,
    0xff6699ff, 0xff3399ff, 0xff0099ff, 0xffff66ff, 0xffcc66ff, 0xff9966ff, 0xff6666ff, 0xff3366ff, 0xff0066ff, 0xffff33ff, 0xffcc33ff, 0xff9933ff, 0xff6633ff, 0xff3333ff, 0xff0033ff, 0xffff00ff,
    0xffcc00ff, 0xff9900ff, 0xff6600ff, 0xff3300ff, 0xff0000ff, 0xffffffcc, 0xffccffcc, 0xff99ffcc, 0xff66ffcc, 0xff33ffcc, 0xff00ffcc, 0xffffcccc, 0xffcccccc, 0xff99cccc, 0xff66cccc, 0xff33cccc,
    0xff00cccc, 0xffff99cc, 0xffcc99cc, 0xff9999cc, 0xff6699cc, 0xff3399cc, 0xff0099cc, 0xffff66cc, 0xffcc66cc, 0xff9966cc, 0xff6666cc, 0xff3366cc, 0xff0066cc, 0xffff33cc, 0xffcc33cc, 0xff9933cc,
    0xff6633cc, 0xff3333cc, 0xff0033cc, 0xffff00cc, 0xffcc00cc, 0xff9900cc, 0xff6600cc, 0xff3300cc, 0xff0000cc, 0xffffff99, 0xffccff99, 0xff99ff99, 0xff66ff99, 0xff33ff99, 0xff00ff99, 0xffffcc99,
    0xffcccc99, 0xff99cc99, 0xff66cc99, 0xff33cc99, 0xff00cc99, 0xffff9999, 0xffcc9999, 0xff999999, 0xff669999, 0xff339999, 0xff009999, 0xffff6699, 0xffcc6699, 0xff996699, 0xff666699, 0xff336699,
    0xff006699, 0xffff3399, 0xffcc3399, 0xff993399, 0xff663399, 0xff333399, 0xff003399, 0xffff0099, 0xffcc0099, 0xff990099, 0xff660099, 0xff330099, 0xff000099, 0xffffff66, 0xffccff66, 0xff99ff66,
    0xff66ff66, 0xff33ff66, 0xff00ff66, 0xffffcc66, 0xffcccc66, 0xff99cc66, 0xff66cc66, 0xff33cc66, 0xff00cc66, 0xffff9966, 0xffcc9966, 0xff999966, 0xff669966, 0xff339966, 0xff009966, 0xffff6666,
    0xffcc6666, 0xff996666, 0xff666666, 0xff336666, 0xff006666, 0xffff3366, 0xffcc3366, 0xff993366, 0xff663366, 0xff333366, 0xff003366, 0xffff0066, 0xffcc0066, 0xff990066, 0xff660066, 0xff330066,
    0xff000066, 0xffffff33, 0xffccff33, 0xff99ff33, 0xff66ff33, 0xff33ff33, 0xff00ff33, 0xffffcc33, 0xffcccc33, 0xff99cc33, 0xff66cc33, 0xff33cc33, 0xff00cc33, 0xffff9933, 0xffcc9933, 0xff999933,
    0xff669933, 0xff339933, 0xff009933, 0xffff6633, 0xffcc6633, 0xff996633, 0xff666633, 0xff336633, 0xff006633, 0xffff3333, 0xffcc3333, 0xff993333, 0xff663333, 0xff333333, 0xff003333, 0xffff0033,
    0xffcc0033, 0xff990033, 0xff660033, 0xff330033, 0xff000033, 0xffffff00, 0xffccff00, 0xff99ff00, 0xff66ff00, 0xff33ff00, 0xff00ff00, 0xffffcc00, 0xffcccc00, 0xff99cc00, 0xff66cc00, 0xff33cc00,
    0xff00cc00, 0xffff9900, 0xffcc9900, 0xff999900, 0xff669900, 0xff339900, 0xff009900, 0xffff6600, 0xffcc6600, 0xff996600, 0xff666600, 0xff336600, 0xff006600, 0xffff3300, 0xffcc3300, 0xff993300,
    0xff663300, 0xff333300, 0xff003300, 0xffff0000, 0xffcc0000, 0xff990000, 0xff660000, 0xff330000, 0xff0000ee, 0xff0000dd, 0xff0000bb, 0xff0000aa, 0xff000088, 0xff000077, 0xff000055, 0xff000044,
    0xff000022, 0xff000011, 0xff00ee00, 0xff00dd00, 0xff00bb00, 0xff00aa00, 0xff008800, 0xff007700, 0xff005500, 0xff004400, 0xff002200, 0xff001100, 0xffee0000, 0xffdd0000, 0xffbb0000, 0xffaa0000,
    0xff880000, 0xff770000, 0xff550000, 0xff440000, 0xff220000, 0xff110000, 0xffeeeeee, 0xffdddddd, 0xffbbbbbb, 0xffaaaaaa, 0xff888888, 0xff777777, 0xff555555, 0xff444444, 0xff222222, 0xff111111
], dtype=np.uint32)

MAGIC_BYTES = b'\x56\x4F\x58\x20'
voxReader = None


class VoxReader:
    def __init__(self):
        self._clear_data()

    def _clear_data(self):
        self._file = None
        self._model_index = 0
        self._model = None
        self._palette = None

    def read(self, path):
        self._file = open(path, 'rb')

        magic_bytes = self._file.read(4)
        if magic_bytes != MAGIC_BYTES:
            raise ValueError('This file is not a VOX file')

        version = int.from_bytes(self._file.read(4), 'little')
        if version != 150:
            raise ValueError(f'Invalid VOX version {version}')
        vox_file = VoxFile()
        self._parse_chunk(vox_file)
        self._file.close()
        self._clear_data()
        return vox_file

    def write(self, path, vox_file):
        self._file = open(path, 'wb')

        self._file.write(MAGIC_BYTES)
        self._file.write(int.to_bytes(150, 4, 'little'))

        main = [b'MAIN', b'', [[b'PACK', self._encode_int(vox_file.get_model_count()), []]]]
        for model in vox_file.get_models():
            for chunk in self._encode_model(model):
                main[2].append(chunk)
        main[2].append(self._encode_palette(vox_file.get_color_palette()))

        self._write_chunk(main)

        self._file.close()
        self._clear_data()

    def _parse_chunk(self, vox_file):
        identifier = self._file.read(4)
        length = self._read_int()
        child_length = self._read_int()
        data = None
        if length > 0:
            data = self._file.read(length)
        self._handle_chunk(vox_file, identifier, data)
        index = self._file.tell()
        if child_length > 0:
            while self._file.tell() - index < child_length:
                self._parse_chunk(vox_file)

    def _write_chunk(self, encoded_chunk):
        self._file.write(encoded_chunk[0])  # Identifier
        data_length = len(encoded_chunk[1])
        self._write_int(data_length)
        child_length = self._child_size(encoded_chunk[2])
        self._write_int(child_length)
        if data_length > 0:
            self._file.write(encoded_chunk[1])  # The chunk data
        if child_length > 0:
            for child in encoded_chunk[2]:
                self._write_chunk(child)

    def _child_size(self, child_list):
        result = 0
        for child in child_list:
            result += 4  # Identifier
            result += len(child[1])  # Data
            result += self._child_size(child[2])
        return result

    def _read_int(self):
        return self._parse_int(self._file.read(4))

    def _write_int(self, value):
        self._file.write(self._encode_int(value))

    def _encode_int(self, value):
        return int.to_bytes(value, 4, 'little')

    def _encode_int8(self, value):
        return int.to_bytes(value, 1, 'little')

    def _parse_int(self, data):
        return int.from_bytes(data[:4], 'little')

    def _parse_int8(self, data):
        return int.from_bytes(data[:1], 'little')

    def _handle_chunk(self, vox_file, identifier, data):
        if identifier == b'MAIN':
            return
        elif identifier == b'PACK':
            vox_file.set_model_count(self._parse_int(data))
            self._model_index = -1
        elif identifier == b'SIZE':
            x = self._parse_int(data)
            z = self._parse_int(data[4:])
            y = self._parse_int(data[8:])
            self._model = np.zeros((y, x, z), dtype=np.uint32)
            self._model_index += 1
        elif identifier == b'XYZI':
            voxel_count = self._parse_int(data)
            for vi in range(voxel_count):
                di = vi * 4 + 4
                x = self._parse_int8(data[di:])
                z = self._parse_int8(data[di + 1:])
                y = self._parse_int8(data[di + 2:])
                ci = self._parse_int8(data[di + 3:])
                self._model[y][x][z] = ci
            vox_file.set_model(self._model, self._model_index)
        elif identifier == b'RGBA':
            self._palette = np.zeros(256)
            for ix in range(255):
                di = ix * 4
                rgba = self._parse_int(data[di:])
                self._palette[1 + ix] = rgba
            vox_file.set_color_palette(self._palette)

    def _encode_palette(self, palette):
        data = b''
        for c in palette[1:256]:  # We only allow 255 colors (Skips first)
            data += self._encode_int(int(c))
        return [b'RGBA', data, []]

    def _encode_model(self, model):
        result = [[b'SIZE', b'', []], [b'XYZI', b'', []]]
        y, x, z = model.shape
        result[0][1] += self._encode_int(x)
        result[0][1] += self._encode_int(z)
        result[0][1] += self._encode_int(y)
        voxel_count = x * y * z
        result[1][1] += self._encode_int(voxel_count)
        for zi in range(z):
            for xi in range(x):
                for yi in range(y):
                    ci = model[yi][xi][zi]
                    result[1][1] += self._encode_int8(xi)
                    result[1][1] += self._encode_int8(zi)
                    result[1][1] += self._encode_int8(yi)
                    result[1][1] += self._encode_int8(int(ci))
        return result


class VoxFile:
    def __init__(self):
        self._model_count = 0
        self._models = [None]
        self._palette = default_palette

    def to_file(self, path):
        global voxReader
        if voxReader is None:
            voxReader = VoxReader()
        voxReader.write(path, self)

    @staticmethod
    def from_file(path):
        global voxReader
        if voxReader is None:
            voxReader = VoxReader()
        return voxReader.read(path)

    def get_models(self):
        return self._models

    def get_model(self, index=0):
        if index < 0 or index >= self._model_count:
            raise IndexError('Not a valid model index')
        return self._models[index]

    def set_model(self, model, index=0):
        if index < 0 or index > self._model_count:
            raise IndexError('Not a valid model index')
        if index == self._model_count:
            self._model_count += 1
            self._models.append(model)
        else:
            self._models[index] = model

    def get_model_count(self):
        return self._model_count

    def set_model_count(self, count):
        self._model_count = count
        self._models = [None for _ in range(count)]

    def get_color_palette(self):
        return self._palette

    def set_color_palette(self, palette):
        self._palette = palette

    def get_color_for_index(self, ci):
        return self._palette[ci]


vox_file = VoxFile.from_file('MarkovJunior/output/ModernHouseMOD2_45348516.vox')
vox_file.to_file('MarkovJunior/output/ModernHouse.vox')