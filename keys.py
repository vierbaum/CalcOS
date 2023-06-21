#!/usr/bin/env python3

for i in range(1,63):
    bin = str(format(i, 'b'))[::-1]
    bin += "     "
    print("{}&{}&{}&{}&{}&{}&{}\\\\".format(i, bin[0], bin[1], bin[2], bin[3], bin[4], bin[5]))
