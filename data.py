import pygame
import os
import support as s
import player

pygame.init()
width = 700
height = 700
screen = pygame.display.set_mode((height, width))
fps = pygame.time.Clock()
rows = 8
cols = 8
font = "Helvetica 0"
moved = False
drawCPU = False
gameover = False
margin = 90
player1turn = True
player2turn = False
titleY = 10
CPUXY = (None, None)
pauseAnim = False
moveAnim = False
xOne = 100
yOne = 600
xTwo = 150
yTwo = 650
b1 = 850
b2 = 900
b3 = 950
b4 = 1000
text1 = False
text1Num = ""
text2Num = ""
text2 = False
pause = False
cheat = False
drawingpiece = None
pieceValues = {"pawn" : 1, "bishop" : 3, "knight" : 3, "rook" : 5, \
"queen" : 9, "king" : 0}
cellWidth = (width - (margin * 2))/cols
cellHeight = (height - (margin * 2))/rows
board = [([None] * cols) for row in range(rows)]
kingMoves = [[(0, 1)], [(1, 0)], [(-1, 0)], [(0, -1)], [(1, 1)], [(-1, -1)], \
[(-1, 1)], [(1, -1)]]
queenMoves = [ \
[(i, i) for i in range(1, max(cols, rows) + 1)], \
[(i, -i) for i in range(1, max(cols, rows) + 1)], \
[(-i, i) for i in range(1, max(cols, rows) + 1)], \
[(-i, -i) for i in range(1, max(cols, rows) + 1)], \
[(0, i) for i in range(1, max(cols, rows) + 1)], \
[(i, 0) for i in range(1, max(cols, rows) + 1)], \
[(-i, 0) for i in range(1, max(cols, rows) + 1)], \
[(0, -i) for i in range(1, max(cols, rows) + 1)], \
]
rookMoves = [ \
[(0, i) for i in range(1, max(cols, rows) + 1)], \
[(i, 0) for i in range(1, max(cols, rows) + 1)], \
[(-i, 0) for i in range(1, max(cols, rows) + 1)], \
[(0, -i) for i in range(1, max(cols, rows) + 1)], \
]
bishopMoves = [ \
[(i, i) for i in range(1, max(cols, rows) + 1)], \
[(i, -i) for i in range(1, max(cols, rows) + 1)], \
[(-i, i) for i in range(1, max(cols, rows) + 1)], \
[(-i, -i) for i in range(1, max(cols, rows) + 1)], \
]
pawnMovesp1 = [[(1, 0), (1, 1), (1, -1)]]
pawnMovesp2 = [[(-1, 0), (-1, -1), (-1, 1)]]
pawnMovesp1First = [[(1, 0), (1, 1), (1, -1), (2, 0)]]
pawnMovesp2First = [[(-1, 0), (-1, -1), (-1, 1), (-2, 0)]]
pawnMovesp1Elem = [(1, 0), (1, 1), (1, -1), (2, 0)]
pawnMovesp2Elem = [(-1, 0), (-1, -1), (-1, 1), (-2, 0)]
knightMoves = [ \
[(2, 1), (2, -1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, -2), (1, -2), \
(-1, 2)]]
x0 = width / 2
x1 = width / 2
y0 = height / 2
usedplaces = []
xOne = -100
y1 = height / 2
customAnim = False
makeCustomScreen = False
fontNum = 0
timertime1 = ""
timertime2 = ""
counter = 0
player2Attack = False
error = False
piecedraw = []
custommargin = 0
customcellWidth = 0
customclick1 = False
customcellHeight = 0
custompieces = {}
depth = 3
backHelp = pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/wood/backHelp.jpg"))
startWood = pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/wood/startWood.png"))
woodDark = pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/wood/woodDark.png"))
woodLight = pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/wood/woodLight.jpg"))
backWood = pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/wood/backWood.jpg"))
Wpawn = pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/WPawn.png"))
Bpawn =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/BPawn.png"))
Wbishop =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/WBishop.png"))
Bbishop =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/BBishop.png"))
Bknight =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/BKnight.png"))
Wknight =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/WKnight.png"))
Brook =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/BRook.png"))
Wrook =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/WRook.png"))
Bking =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/BKing.png"))
Wking =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/WKing.png"))
Bqueen =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/BQueen.png"))
Wqueen =  pygame.image.load(os.path.join("C:/Users/Anshul Modh/Desktop/cmu/15-112 Files/Finished/Pictures/pieces/WQueen.png"))
startField = False
piecenames = [[["pawn", "p1"], ["rook", "p1"], ["bishop", "p1"], ["knight", "p1"], ["king", "p1"], ["queen", "p1"]], \
                   [["pawn", "p2"], ["rook", "p2"], ["bishop", "p2"], ["knight", "p2"], ["king", "p2"], ["queen", "p2"]]]
pieces = []
countering = True
drawpiecex = 0
drawpiecey = 0
currentdrawingpiece = None
helpAnim = False
help1 = width
help2 = - height
starttext = ""
drawCPUagain = False
click1 = False
check = False
p1promote = False
p2promote = False
enPass = False
cpu = False
startScreen = True
died = False
help = False
custom = False
half = width / 2
time1 = 0
time2 = 0
start1 = None
start2 = None
timer1 = False
timer2 = False
startX0 = width
animatefirst = False
pauserect1 = 0
pauserect2 = 0
pauseW = 0
pauseH = 0
darken_percent = .01
Pfont = 10
pauseFont = pygame.font.SysFont("impact", int(Pfont))
alpha = 0
pauserect3 = 0
pauserect4 = 0
pauseW1 = 0
pauseH1 = 0
margin1 = 0
Pfont1Size = 0
Pfont1 = pygame.font.SysFont("impact", int(Pfont1Size))
textX = 0
textY = 0
playerOne = player.player(player1turn, {}, [], [], "p1")
playerTwo = player.player(player2turn, {}, [], [], "p2")
reset = False
offset = None
black = 0, 0, 0
white = 255, 255, 255
green = 124, 252, 0
gray = 130, 130, 230
tanB1 = 240, 218, 181
tanB2 = 240, 218, 181
tanB3 = 240, 218, 181
tanB4 = 240, 218, 181
tan = 240, 218, 181
tan1 = 220, 198, 161
tan2 = 220, 198, 161
brown = 181, 135, 99
brown1 = 181, 135, 99
x = 0
y = 0
tran = False
# p1Pieces = {}
# p2Pieces = {}
# p1 = []
# p2 = []
# p2dead = []
# p1dead = []
# BknightSSize = Bknight.subsample(4)
# WknightSSize = Wknight.subsample(4)
# BrookSSize = Brook.subsample(4)
# WrookSSize = Wrook.subsample(4)
# BkingSSize = Bking.subsample(4)
# WkingSSize = Wking.subsample(4)
# BqueenSSize = Bqueen.subsample(4)
# WqueenSSize = Wqueen.subsample(4)
# row0 = [WpawnSize, WrookSize, WbishopSize, WknightSize, WkingSize, WqueenSize]
# row1 = [BpawnSize, BrookSize, BbishopSize, BknightSize, BkingSize, BqueenSize]
# row0Size = [WpawnSSize, WrookSSize, WbishopSSize, WknightSSize, WkingSSize, WqueenSSize]
# row1Size = [BpawnSSize, BrookSSize, BbishopSSize, BknightSSize, BkingSSize, BqueenSSize]
# WpawnSize = Wpawn.subsample(2)
# BpawnSize =  Bpawn.subsample(2)
# WbishopSize = Wbishop.subsample(2)
# BbishopSize = Bbishop.subsample(2)
# BknightSize = Bknight.subsample(2)
# WknightSize = Wknight.subsample(2)
# BrookSize = Brook.subsample(2)
# WrookSize = Wrook.subsample(2)
# BkingSize = Bking.subsample(2)
# WkingSize = Wking.subsample(2)
# BqueenSize = Bqueen.subsample(2)
# WqueenSize = Wqueen.subsample(2)
# WpawnSSize = Wpawn.subsample(4)
# BpawnSSize =  Bpawn.subsample(4)
# WbishopSSize = Wbishop.subsample(4)
# BbishopSSize = Bbishop.subsample(4)