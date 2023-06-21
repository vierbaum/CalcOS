BUTTON = 0
SPACER = 1
UP = 0
DOWN = 1
class Button():
    def __init__(self, v=None, u=None, d=None, a=None, t=BUTTON):
        self.value = v
        self.up = u
        self.down = d
        self.type = t
        self.arrow = a


    def __str__(self):
        if (self.type == BUTTON):
            return(" | |{}\n-+-+-\n | | \n-+-+-\n | | \n-+-+-\n | |{}".format(self.up, self.down))
        elif(self.type == SPACER):
            return("||")

def printRow(row):
    #           info    row up gaps 1/2  row down
    print("%header")
    for b in row:
        if b != None:
            print("\\multicolumn{3}{|c||}{%s}&"%(b.value if b.value != None else ""))
        else:
            print("\\multicolumn{3}{|c||}{}&")
    print("\\\\\n\\hline\\hline")

    for b in row:
        if b != None:
            print("&&\\tikzmark{pinsFront%sul}%s\\tikzmark{pinsFront%sur}&"%(b.value, b.up if b.up != None else "", b.value), end="")
        else:
            print("&&&")
    print("\\\\\n\hline")

    for _ in [0, 1]:
        for b in row:
            print("&&&", end="")
        print("\\\\\n\\hline")

    for b in row:
        if b != None:
            print("&&\\tikzmark{pinsFront%sdl}%s\\tikzmark{pinsFront%sdr}&"%(b.value, b.down if b.down != None else "", b.value), end="")
        else:
            print("&&&")
    print("\\\\\n\hline\\hline")

def printRowBack(row):
    print("%header")
    for b in row[::-1]:
        if b != None:
            print("&\\multicolumn{3}{|c||}{%s}"%(b.value if b.value != None else ""))
        else:
            print("&\\multicolumn{3}{|c||}{ }")
    print("\\\\\n\\hline\\hline")

    for b in row[::-1]:
        if b != None:
            print("&\\tikzmark{pinsBack%sur}%s\\tikzmark{pinsBack%sul}&&"%(b.value, b.up if b.up != None else "", b.value), end="")
        else:
            print("&&&")
    print("\\\\\n\hline")

    for _ in [0, 1]:
        for b in row[::-1]:
            print("&&&", end="")
        print("\\\\\n\\hline")

    for b in row[::-1]:
        if b != None:
            print("&\\tikzmark{pinsBack%sdr}%s\\tikzmark{pinsBack%sdl}&&"%(b.value, b.down if b.down != None else "", b.value), end="")
        else:
            print("&&&")
    print("\\\\\n\hline\\hline")

def findRoute(origin, dest, board):
    o = None
    d = None
    for row in range(len(board)):
        for button in range(len(board[row])):
            if board[row][button] == origin:
                o = [button, row]
            if board[row][button] == dest:
                d = [button, row]
    return [d[0] - o[0], d[1] - o[1]]

def drawArrow(origin, dest, board):
    if (type(origin) == type([])):
        pathVec = findRoute(origin[0], dest[0], board)
        TeXorigin = "pinsFront" + str(origin[0])
        TeXorigin += "u" if origin[1] == UP else "d"
        TeXorigin += "l" if pathVec[0] < 0 else "r"

        TeXdest = "pinsFront" + str(dest[0])
        TeXdest += "u" if dest[1] == UP else "d"
        TeXdest += "r" if pathVec[0] <= 0 else "l"
        print("\\draw [->] ({pic cs:%s}) to ({pic cs:%s});"%(TeXorigin, TeXdest))
        TeXorigin = "pinsBack" + str(origin[0])
        TeXorigin += "u" if origin[1] == UP else "d"
        TeXorigin += "l" if pathVec[0] < 0 else "r"

        TeXdest = "pinsBack" + str(dest[0])
        TeXdest += "u" if dest[1] == UP else "d"
        TeXdest += "r" if pathVec[0] <= 0 else "l"
        print("\\draw [->] ({pic cs:%s}) to ({pic cs:%s});"%(TeXorigin, TeXdest))
    else:
        pathVec = findRoute(origin, dest, board)
        TeXorigin = "pinsFront" + str(origin)
        TeXorigin += "u" if pathVec[1] < 0 else "d"
        TeXorigin += "r"

        TeXdest = "pinsFront" + str(dest)
        TeXdest += "d" if pathVec[1] < 0 else "u"
        TeXdest += "r"
        if pathVec[1] > 0:
            print("\\draw [->] ({pic cs:%s}) [bend left] to ({pic cs:%s});"%(TeXorigin, TeXdest))
        else:
            print("\\draw [->] ({pic cs:%s}) [bend right] to ({pic cs:%s});"%(TeXorigin, TeXdest))
        TeXorigin = "pinsBack" + str(origin)
        TeXorigin += "u" if pathVec[1] < 0 else "d"
        TeXorigin += "l"

        TeXdest = "pinsBack" + str(dest)
        TeXdest += "d" if pathVec[1] < 0 else "u"
        TeXdest += "l"
        if pathVec[1] > 0:
            print("\\draw [->] ({pic cs:%s}) [bend left] to ({pic cs:%s});"%(TeXorigin, TeXdest))
        else:
            print("\\draw [->] ({pic cs:%s}) [bend right] to ({pic cs:%s});"%(TeXorigin, TeXdest))


rows = []
board = [[0 for _ in range(9)] for _2 in range(6)]
rows.append([Button(1,1), Button(2,2), Button(4,4), Button(8,8), Button(32, 32), Button(33,None,1), Button(38,2,4, 37), None, None])
rows.append([Button(3,2,1), Button(5,1,4), Button(6,2,4), Button(7,1, a=[DOWN, [6, DOWN]]), Button(34,2), Button(35,1,2), Button(37,4,1), Button(39,None,2, [UP, [37, UP]]), Button(40,8)])
rows.append([Button(9,1,8), Button(10,2,8), Button(12,4,8), Button(13,None,1, [UP, [12, UP]]), Button(25,1,8), Button(36,4), Button(41,1,8), Button(42,2,8), Button(43,1, a=[UP, [42, UP]])])
rows.append([Button(16,16), Button(11,None,1, 10), Button(14,None,2,12), Button(15,1), Button(26,8,2), Button(27,1,a=[DOWN, [26, DOWN]]), Button(45,None,1, a=[UP, [44, UP]]), Button(44,8,4), Button(46,2, a=[DOWN, [44,DOWN]])])
rows.append([Button(17,1), Button(19,1,2), Button(21,1,4), Button(24,8), Button(28,8,4), Button(29,None,1, [UP, [28, UP]]), Button(48,None,16), Button(49,1,16), Button(47,None,1, 46)])
rows.append([Button(18,2), Button(20,4), Button(22,4,2), Button(23,1, a=[DOWN, [22, DOWN]]), Button(30,None,2, 28), Button(31,None,1, [UP, [30, UP]]), Button(50,16,2), Button(51,None,1, [UP, [50, UP]]), Button(52,16,4)])
for r in range(6):
    for b in range(len(rows[r])):
        board[r][b] = rows[r][b].value if rows[r][b] != None else None

print("\\documentclass{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{tikzmark}")
print("\\begin{document}")
print("\\begin{tabular}{|l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|}")
for r in rows:
    printRow(r)
print("\\end{tabular}")

print("\\begin{tabular}{|l||l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|l|l||l|}")
for r in rows:
    printRowBack(r)
print("\\end{tabular}")

print("\\begin{tikzpicture}[overlay, remember picture, shorten >=.5pt, shorten <=.5pt, transform canvas={yshift=.25\\baselineskip}]")
for row in rows:
    for button in row:
        if button != None and button.arrow:
            drawArrow([button.value, button.arrow[0]] if type(button.arrow) == type([]) else button.value, button.arrow if type(button.arrow) == type(1) else button.arrow[1], board)
print("\\end{tikzpicture}")



print("\\end{document}")