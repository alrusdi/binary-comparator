# -*- coding: utf-8 -*-
import os
import struct

FMT_HEX = 1
FMT_DEC = 2


class TermColors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END_COLOR = '\033[0m'


class Comparator(object):
    """
    Utility for byte by byte compare contents of files
    producing output like:
    000 FF FF
    001 05 A9
    002 3B 3B
    ...
    """

    def __init__(self, *args):
        """
        Takes a paths for files
        """
        self.files = [open(f,'rb') for f in args]

    def __read_byte_as_int(self, stream):
        try:
            d = stream.read(1)
            if d == b'':
                return 0
            return struct.unpack('b', d)[0]
        except EOFError:
            return 0

    def __colorify(self, text, color):
        return color + text + TermColors.END_COLOR

    def __all_same(self, items):
        return all(x == items[0] for x in items)

    def compare(self, output_format=FMT_HEX):
        gs = os.path.getsize
        sizes = [os.fstat(f.fileno()).st_size for f in self.files]
        max_size = max(*sizes)
        ct = 0
        size_digits_count = len(str(max_size))
        for i in range(1, max_size + 1):
            ct += 1
            counter = str(ct).rjust(size_digits_count, '0')
            hexes = []
            ints = []
            for f in self.files:
                _int = self.__read_byte_as_int(f)
                _hex = "{0:0>2X}".format(_int)
                hexes.append(_hex)
                ints.append(str(_int) or '.')

            col = TermColors.GREEN
            if not self.__all_same(ints):
                col = TermColors.RED
            if ct % 4 == 1:
                print('')
            out = '%s | %s | %s' % (counter, ' '.join(hexes), ' '.join(ints))
            print(self.__colorify(out, col))
