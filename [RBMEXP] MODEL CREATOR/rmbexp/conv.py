import struct
import os

class Float3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def clone(self):
        return Float3(self.x, self.y, self.z)

    def normalize(self):
        mag = (self.x**2 + self.y**2 + self.z**2)**0.5
        if mag > 0.0:
            one_over_mag = 1.0 / mag
            self.x *= one_over_mag
            self.y *= one_over_mag
            self.z *= one_over_mag
        return self

    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def umn(self, v):
        self.x *= v
        self.y *= v
        self.z *= v
        return self

    def div(self, v):
        self.x /= v
        self.y /= v
        self.z /= v
        return self

    def plus(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def minus(self, v):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def cross_product(self, v):
        out = Float3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z, self.x * v.y - self.y * v.x)
        return out

    def dot_product(self, v):
        out = 0.0
        out += (self.x * v.x)
        out += (self.y * v.y)
        out += (self.z * v.z)
        return out

    def prn(self, g=0):
        if g == 0:
            return f"{self.x}:{self.y}:{self.z}"
        if g == 1:
            return f"{self.x:.6f}:{self.y:.6f}:{self.z:.6f}"
        if g == 2:
            return ''


class DataReader:
    def __init__(self, buffer):
        self.dv = buffer
        self.offset = 0
        self.little_endian = True

    def get_int8(self):
        value = struct.unpack('b', self.dv[self.offset:self.offset + 1])[0]
        self.offset += 1
        return value

    def get_int8_array(self, size):
        a = []
        for i in range(size):
            a.append(self.get_int8())
        return a

    def get_uint8(self):
        value = struct.unpack('B', self.dv[self.offset:self.offset + 1])[0]
        self.offset += 1
        return value

    def get_uint8_array(self, size):
        a = []
        for i in range(size):
            a.append(self.get_uint8())
        return a

    def get_int16(self):
        value = struct.unpack('<h' if self.little_endian else '>h', self.dv[self.offset:self.offset + 2])[0]
        self.offset += 2
        return value

    def get_int16_array(self, size):
        a = []
        for i in range(size):
            a.append(self.get_int16())
        return a

    def get_uint16(self):
        value = struct.unpack('<H' if self.little_endian else '>H', self.dv[self.offset:self.offset + 2])[0]
        self.offset += 2
        return value

    def get_uint16_array(self, size):
        a = []
        for i in range(size):
            a.append(self.get_uint16())
        return a

    def get_int32(self):
        value = struct.unpack('<i' if self.little_endian else '>i', self.dv[self.offset:self.offset + 4])[0]
        self.offset += 4
        return value

    def get_int32_array(self, size):
        a = []
        for i in range(size):
            a.append(self.get_int32())
        return a

    def get_uint32(self):
        value = struct.unpack('<I' if self.little_endian else '>I', self.dv[self.offset:self.offset + 4])[0]
        self.offset += 4
        return value

    def get_uint32_array(self, size):
        a = []
        for i in range(size):
            a.append(self.get_uint32())
        return a

    def get_float32(self):
        value = struct.unpack('<f' if self.little_endian else '>f', self.dv[self.offset:self.offset + 4])[0]
        self.offset += 4
        return value

    def get_float32_array(self, size):
        a = []
        for i in range(size):
            a.append(self.get_float32())
        return a

    def get_float64(self):
        value = struct.unpack('<d' if self.little_endian else '>d', self.dv[self.offset:self.offset + 8])[0]
        self.offset += 8
        return value

    def get_float64_array(self, size):
        a = []
        for i in range(size):
            a.append(self.get_float64())
        return a


class DataWriter:
    def __init__(self):
        self.data = bytearray()

    def append(self, value, format_char):
        self.data.extend(struct.pack(format_char, value))

    def append_int8(self, value):
        self.append(value, 'b')

    def append_int8_array(self, values):
        for v in values:
            self.append_int8(v)

    def append_uint8(self, value):
        self.append(value, 'B')

    def append_uint8_array(self, values):
        for v in values:
            self.append_uint8(v)

    def append_int16(self, value):
        self.append(value, '<h')

    def append_int16_array(self, values):
        for v in values:
            self.append_int16(v)

    def append_uint16(self, value):
        self.append(value, '<H')

    def append_uint16_array(self, values):
        for v in values:
            self.append_uint16(v)

    def append_int32(self, value):
        self.append(value, '<i')

    def append_int32_array(self, values):
        for v in values:
            self.append_int32(v)

    def append_uint32(self, value):
        self.append(value, '<I')

    def append_uint32_array(self, values):
        for v in values:
            self.append_uint32(v)

    def append_float32(self, value):
        self.append(value, '<f')

    def append_float32_array(self, values):
        for v in values:
            self.append_float32(v)

    def append_float64(self, value):
        self.append(value, '<d')

    def append_float64_array(self, values):
        for v in values:
            self.append_float64(v)

    def to_byte_array(self):
        return bytes(self.data)

class RmbClass:
    def __init__(self):
        self.version = 0
        self.vlist = []
        self.indices = []
        self.flag = False
        self.buf_size = 0
        self.data = []

    def clone(self):
        rmb = RmbClass()
        rmb.version = self.version
        rmb.vlist = [v.clone() for v in self.vlist]
        rmb.indices = self.indices[:]
        rmb.flag = self.flag
        rmb.buf_size = self.buf_size
        rmb.data = self.data[:]
        return rmb

    def parse(self, data):
        reader = DataReader(data)
        self.version = reader.get_uint32()
        vcount = reader.get_uint32()
        self.vlist = []
        for i in range(vcount):
            v = Float3(reader.get_float32(), reader.get_float32(), reader.get_float32())
            self.vlist.append(v)
        icount = reader.get_uint32()
        self.indices = reader.get_uint32_array(icount)
        self.flag = reader.get_uint8()
        self.buf_size = reader.get_uint32()
        self.data = reader.get_uint8_array(self.buf_size)

    def save(self):
        writer = DataWriter()
        writer.append_uint32(self.version)
        writer.append_uint32(len(self.vlist))
        for v in self.vlist:
            writer.append_float32(v.x)
            writer.append_float32(v.y)
            writer.append_float32(v.z)
        writer.append_uint32(len(self.indices))
        for i in self.indices:
            writer.append_uint32(i)
        writer.append_uint8(self.flag)
        writer.append_uint32(self.buf_size)
        writer.append_uint8_array(self.data)
        return writer.to_byte_array()

class ObjClass:
    def __init__(self):
        self.vlist = []

    def clone(self):
        obj = ObjClass()
        obj.vlist = [v.clone() for v in self.vlist]
        return obj

    def parse(self, data):
        self.vlist = []
        lines = data.decode('utf-8').split('\n')
        for line in lines:
            parts = line.split()
            if len(parts) == 4 and parts[0] == 'v':
                v = Float3(float(parts[1]), float(parts[2]), float(parts[3]))
                self.vlist.append(v)

    def save(self):
        lines = []
        for v in self.vlist:
            lines.append(f'v {v.x:.6f} {v.y:.6f} {v.z:.6f}\n')
        return ''.join(lines).encode('utf-8')

def export_rmb_to_obj(rmb_data, obj_path):
    rmb = RmbClass()
    rmb.parse(rmb_data)

    obj = ObjClass()
    obj.vlist = rmb.vlist

    with open(obj_path, 'wb') as file:
        file.write(obj.save())

def import_obj_to_rmb(obj_path):
    with open(obj_path, 'rb') as file:
        obj_data = file.read()

    obj = ObjClass()
    obj.parse(obj_data)

    rmb = RmbClass()
    rmb.version = 1
    rmb.vlist = obj.vlist
    rmb.indices = [i for i in range(len(obj.vlist))]
    rmb.flag = 0
    rmb.buf_size = 0
    rmb.data = []

    return rmb.save()
