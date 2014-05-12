# -*- coding: utf-8 -*-
import sys
from binary_compare import Comparator

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print('Pass a two file paths as parameters')
        sys.exit(1)

    Comparator(args[1], args[2]).compare()