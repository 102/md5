from math import sin


class MD5(object):
    rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                      5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                      4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                      6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    constants = [int(abs(2 ** 32 * sin(i + 1))) & 0xffffffff for i in range(64)]

    init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

    functions = 16 * [lambda b, c, d: (b & c) | (~b & d)] + \
                16 * [lambda b, c, d: (d & b) | (~d & c)] + \
                16 * [lambda b, c, d: b ^ c ^ d] + \
                16 * [lambda b, c, d: c ^ (b | ~d)]

    index_functions = 16 * [lambda i: i] + \
                      16 * [lambda i: (5 * i + 1) % 16] + \
                      16 * [lambda i: (3 * i + 5) % 16] + \
                      16 * [lambda i: (7 * i) % 16]

    @staticmethod
    def left_rotate(x, amount):
        x &= 0xffffffff
        return ((x << amount) | (x >> (32 - amount))) & 0xffffffff

    def md5_digest(self, message, encoding='UTF-8'):
        message = bytearray(message, encoding=encoding)
        orig_bits_len = (8 * len(message)) & 0xffffffffffffffff
        message.append(0x80)
        while len(message) % 64 != 56:
            message.append(0)
        message += orig_bits_len.to_bytes(8, byteorder='little')

        registers = self.init_values[:]

        for chunk_ofst in range(0, len(message), 64):
            a, b, c, d = registers
            chunk = message[chunk_ofst:chunk_ofst + 64]
            for i in range(64):
                f = self.functions[i](b, c, d)
                g = self.index_functions[i](i)
                to_rotate = a + f + self.constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
                new_b = (b + self.left_rotate(to_rotate, self.rotate_amounts[i])) & 0xffffffff
                a, b, c, d = d, new_b, b, c
            for i, val in enumerate([a, b, c, d]):
                registers[i] += val
                registers[i] &= 0xffffffff

        return sum(x << (32 * j) for j, x in enumerate(registers))

    @staticmethod
    def md5_to_hex(digest):
        raw = digest.to_bytes(16, byteorder='little')
        return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

    def md5(self, message, encoding='UTF-8'):
        return self.md5_to_hex(self.md5_digest(message, encoding))
