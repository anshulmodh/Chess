import pygame
import os
import support as s
import player
import data

def resetAll():
    data.dir = os.getcwd() + "/Pictures"
    data.rows = 8
    data.cols = 8
    cols, rows = data.cols, data.rows
    data.customFontSize = 0
    data.font = pygame.font.SysFont("impact", data.customFontSize)
    data.moved = False
    data.drawCPU = False
    data.gameover = False
    data.tan1 = 220, 198, 161
    data.tan2 = 220, 198, 161
    data.x = 0
    data.y = 0
    data.startScreen = False
    data.tan3 = 220, 198, 161
    data.tan4 = 220, 198, 161
    data.tan5 = 220, 198, 161
    data.tran = True
    data.margin = 90
    data.player1turn = True
    data.player2turn = False
    data.titleY = 10
    data.CPUXY = (None, None)
    data.pauseAnim = False
    data.moveAnim = False
    data.brown1 = 181, 135, 99
    data.xOne = 100
    data.yOne = 600
    data.xTwo = 200
    data.yTwo = 650
    data.b1 = 850
    data.black = 0, 0, 0
    data.white = 255, 255, 255
    data.green = 124, 252, 0
    data.gray = 130, 130, 230
    data.tan = 240, 218, 181
    data.brown = 181, 135, 99
    data.b2 = 900
    data.b3 = 950
    data.b4 = 1000
    data.text1 = False
    data.text1Num = "8"
    data.text2Num = "8"
    data.text2 = False
    data.cheat = False
    data.drawingpiece = None
    data.pieceValues = {"pawn" : 1, "bishop" : 3, "knight" : 3, "rook" : 5, \
    "queen" : 9, "king" : 0}
    data.cellWidth = (data.width - (data.margin * 2))/data.cols
    data.cellHeight = (data.height - (data.margin * 2))/data.rows
    data.board = [([None] * cols) for row in range(rows)]
    data.kingMoves = [[(0, 1)], [(1, 0)], [(-1, 0)], [(0, -1)], [(1, 1)], [(-1, -1)], \
    [(-1, 1)], [(1, -1)]]
    data.queenMoves = [ \
    [(i, i) for i in range(1, max(cols, rows) + 1)], \
    [(i, -i) for i in range(1, max(cols, rows) + 1)], \
    [(-i, i) for i in range(1, max(cols, rows) + 1)], \
    [(-i, -i) for i in range(1, max(cols, rows) + 1)], \
    [(0, i) for i in range(1, max(cols, rows) + 1)], \
    [(i, 0) for i in range(1, max(cols, rows) + 1)], \
    [(-i, 0) for i in range(1, max(cols, rows) + 1)], \
    [(0, -i) for i in range(1, max(cols, rows) + 1)], \
    ]
    data.rookMoves = [ \
    [(0, i) for i in range(1, max(cols, rows) + 1)], \
    [(i, 0) for i in range(1, max(cols, rows) + 1)], \
    [(-i, 0) for i in range(1, max(cols, rows) + 1)], \
    [(0, -i) for i in range(1, max(cols, rows) + 1)], \
    ]
    data.bishopMoves = [ \
    [(i, i) for i in range(1, max(cols, rows) + 1)], \
    [(i, -i) for i in range(1, max(cols, rows) + 1)], \
    [(-i, i) for i in range(1, max(cols, rows) + 1)], \
    [(-i, -i) for i in range(1, max(cols, rows) + 1)], \
    ]
    data.pawnMovesp1 = [[(1, 0), (1, 1), (1, -1)]]
    data.pawnMovesp2 = [[(-1, 0), (-1, -1), (-1, 1)]]
    data.pawnMovesp1First = [[(1, 0), (1, 1), (1, -1), (2, 0)]]
    data.pawnMovesp2First = [[(-1, 0), (-1, -1), (-1, 1), (-2, 0)]]
    data.pawnMovesp1Elem = [(1, 0), (1, 1), (1, -1), (2, 0)]
    data.pawnMovesp2Elem = [(-1, 0), (-1, -1), (-1, 1), (-2, 0)]
    data.knightMoves = [ \
    [(2, 1), (2, -1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, -2), (1, -2), \
    (-1, 2)]]
    data.x0 = data.width / 2
    data.x1 = data.width / 2
    data.y0 = data.height / 2
    data.y1 = data.height / 2
    data.x2 = data.width / 2
    data.y2 = data.height / 2
    data.usedplaces = []
    data.customAnim = False
    data.makeCustomScreen = False
    data.fontNum = 0
    data.timertime1 = ""
    data.timertime2 = ""
    data.player2Attack = False
    data.error = False
    data.piecedraw = []
    data.custommargin = 0
    data.startingScreen = True
    data.customcellWidth = 0
    data.customclick1 = False
    data.customcellHeight = 0
    data.custompieces = {}
    data.depth = 3
    data.backHelp = pygame.image.load(os.path.join(data.dir + "/wood/backHelp.jpg"))
    data.startWood = pygame.image.load(os.path.join(data.dir + "/wood/startWood.png"))
    data.woodDark = pygame.image.load(os.path.join(data.dir + "/wood/woodDark.png"))
    data.woodLight = pygame.image.load(os.path.join(data.dir + "/wood/woodLight.jpg"))
    data.backWood = pygame.image.load(os.path.join(data.dir + "/wood/backWood.jpg"))
    data.Wpawn = pygame.image.load(os.path.join(data.dir + "/pieces/WPawn.png"))
    data.Bpawn =  pygame.image.load(os.path.join(data.dir + "/pieces/BPawn.png"))
    data.Wbishop =  pygame.image.load(os.path.join(data.dir + "/pieces/WBishop.png"))
    data.Bbishop =  pygame.image.load(os.path.join(data.dir + "/pieces/BBishop.png"))
    data.Bknight =  pygame.image.load(os.path.join(data.dir + "/pieces/BKnight.png"))
    data.Wknight =  pygame.image.load(os.path.join(data.dir + "/pieces/WKnight.png"))
    data.Brook =  pygame.image.load(os.path.join(data.dir + "/pieces/BRook.png"))
    data.Wrook =  pygame.image.load(os.path.join(data.dir + "/pieces/WRook.png"))
    data.Bking =  pygame.image.load(os.path.join(data.dir + "/pieces/BKing.png"))
    data.Wking =  pygame.image.load(os.path.join(data.dir + "/pieces/WKing.png"))
    data.Bqueen =  pygame.image.load(os.path.join(data.dir + "/pieces/BQueen.png"))
    data.Wqueen =  pygame.image.load(os.path.join(data.dir + "/pieces/WQueen.png"))
    data.customWood = data.backHelp.copy()
    data.customWoodCur = data.customWood
    data.customSize = 1
    data.startField = False
    data.piecenames = [[["pawn", "p1"], ["rook", "p1"], ["bishop", "p1"], ["knight", "p1"], ["king", "p1"], ["queen", "p1"]], \
                       [["pawn", "p2"], ["rook", "p2"], ["bishop", "p2"], ["knight", "p2"], ["king", "p2"], ["queen", "p2"]]]
    data.pieces = []
    data.countering = True
    data.drawpiecex = 0
    data.drawpiecey = 0
    data.currentdrawingpiece = None
    data.helpAnim = False
    data.help1 = data.width
    data.help2 = - data.height
    data.starttext = ""
    data.drawCPUagain = False
    data.click1 = False
    data.check = False
    data.p1promote = False
    data.p2promote = False
    data.offset = None
    data.enPass = False
    data.cpu = False
    data.startScreen = True
    data.died = False
    data.help = False
    data.custom = False
    data.half = data.width / 2
    data.time1 = 0
    data.time2 = 0
    data.startingScreen = True
    data.start1 = None
    data.start2 = None
    data.timer1 = False
    data.timer2 = False
    data.startX0 = data.width
    data.animatefirst = False
    data.pauserect1 = 0
    data.pauserect2 = 0
    data.pauseW = 0
    data.pauseH = 0
    data.darken_percent = .01
    data.Pfont = 10
    data.pauseFont = pygame.font.SysFont("impact", int(data.Pfont))
    data.alpha = 0
    data.pauserect3 = 0
    data.pauserect4 = 0
    data.pauseW1 = 0
    data.pauseH1 = 0
    data.margin1 = 0
    data.Pfont1Size = 0
    data.Pfont1 = pygame.font.SysFont("impact", int(data.Pfont1Size))
    data.textX = 0
    data.textY = 0
    data.playerOne = player.player(data.player1turn, {}, [], [], "p1")
    data.playerTwo = player.player(data.player2turn, {}, [], [], "p2")
    data.pause = False
    data.p1Pieces = {}
    data.p2Pieces = {}
    s.getKings()