import data
import time
import pieceClass
import gameLogic

def offsetTimers():
    timePassed = time.time() - data.offset
    if data.player1turn:
        data.start1 += timePassed
    else:
        data.start2 += timePassed
    data.offset = None

def getKings(): # get position of kings on the board
    for elem in data.playerOne.p:
        if elem.compareName("king"):
            data.p1King = elem
    for elem in data.playerTwo.p:
        if elem.compareName("king"):
            data.p2King = elem

def incTimers():
    if data.player1turn:
        data.timer2 = False
        data.time2 = 0
        data.start2 = None
        if data.start1 == None:
            data.start1 = time.time()
        data.timer1 = True
    else:
        data.timer1 = False
        data.time1 = 0
        data.start1 = None
        if data.start2 == None:
            data.start2 = time.time()
        data.timer2 = True
    timers()

def getPieceCell(x, y):
    colNum = None
    RNum = None
    for col in range(6): # determine cell coordinates of click
        colStartX = 300 + 0 + 50 * col
        colEndX = colStartX + 50
        if colStartX <= x <= colEndX: colNum = col; break
    for row in range(2):
        rowStartX = 575 + 0 + 50 * row
        rowEndX = rowStartX + 50
        if rowStartX <= y <= rowEndX: RNum = row; break
    return (RNum, colNum)

def printBoard(board): # print board in a readable way
    newboard = copyBoard(board)
    for row in range(data.rows):
        for col in range(data.cols):
            piece = newboard[row][col]
            if piece != None:
                newboard[row][col] = piece.getName()
    return newboard

def getRowCol(elem, row, col, i): # get row, col info
    drow, dcol = 0, 0
    if elem[0] != 0:
        drow = elem[0] + elem[0] * i
    else:
        drow = elem[0]
    if elem[1] != 0:
        dcol = elem[1] + elem[1] * i
    else:
        dcol = elem[1]
    newrow = row + drow
    newcol = col + dcol
    return newrow, newcol

def getCell(x, y):
    height = data.height - data.margin*2
    width = data.width - data.margin*2
    data.cellWidth = width/data.cols
    data.cellHeight = height/data.rows
    for col in range(data.cols): # determine cell coordinates of click
        colStartX = data. margin + 0 + data.cellWidth * col
        colEndX = colStartX + data.cellWidth
        if colStartX <= x <= colEndX: colNum = col; break
        else: colNum = 0    
    for row in range(data.rows):
        rowStartX = data.margin + 0 + data.cellHeight * row
        rowEndX = rowStartX + data.cellHeight
        if rowStartX <= y <= rowEndX: RNum = row; break
        else: RNum = 0
    return (RNum, colNum)

def getXY(elem): # get x, y coordinates from row col
    height = data.height - data.margin*2
    width = data.width - data.margin*2
    data.cellWidth = width/data.cols
    data.cellHeight = height/data.rows
    row = elem[0]
    col = elem[1]
    x0 = data. margin + 0 + data.cellWidth* col 
    y0 = data.margin + 0 + data.cellHeight * row
    x = x0 + (data.cellWidth/2)
    y = y0 + (data.cellHeight/2)
    return x, y

def copyBoard(board): # make a copy of the game board
    temp = [([None] * data.cols) for row in range(data.rows)]
    for row in range(data.rows):
        for col in range(data.cols):
            if board[row][col] != None:
                piece = board[row][col]
                newpiece = piece.copy()
                temp[row][col] = piece
    return temp

def AllPieces(board, pieces): # get piece moves
    moves = []
    temp = copyBoard(board)
    for piece in pieces:
        for elem in piece.getMoves():
            for dir in elem:
                temp = copyBoard(board)
                moves = gameLogic.evaluateMoves(temp, dir, piece, pieces, moves)
    return moves

def formatTimers():
    time1 = data.time1
    #print(time1)
    seconds1=time1%60
    minutes1=time1/60%60
    if seconds1 < 10:
        sec1 = "0" + str(int(seconds1))
    else:
        sec1 = str(int(seconds1))
    if minutes1 < 10:
        min1 = "0" + str(int(minutes1))
    else:
        min1 = str(int(minutes1))
    data.timertime1 = min1 + ":" + sec1
    time2 = data.time2
    seconds2=time2%60
    minutes2=time2/60%60
    if seconds2 < 10:
        sec2 = "0" + str(int(seconds2))
    else:
        sec2 = str(int(seconds2))
    if minutes2 < 10:
        min2 = "0" + str(int(minutes2))
    else:
        min2 = str(int(minutes2))
    data.timertime2 = min2 + ":" + sec2

def resetColors():
    data.white = 255, 255, 255
    data.green = 124, 252, 0
    data.gray = 130, 130, 230
    data.tan = 240, 218, 181
    data.brown = 181, 135, 99
    data.brown1 = 181, 135, 99
    data.tanB1 = 240, 218, 181
    data.tanB2 = 240, 218, 181
    data.tanB3 = 240, 218, 181
    data.tanB4 = 240, 218, 181
    data.tan1 = 220, 198, 161
    data.tan2 = 220, 198, 161
    data.tan3 = 220, 198, 161
    data.tan4 = 220, 198, 161
    data.tan5 = 220, 198, 161

def timers():
    if data.timer1:
        data.time1 = time.time() - data.start1
    if data.timer2:
        data.time2 = time.time() - data.start2
    formatTimers()

def changePieces():
    data.queenMoves = [ \
    [(i, i) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(i, -i) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(-i, i) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(-i, -i) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(0, i) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(i, 0) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(-i, 0) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(0, -i) for i in range(1, max(data.cols, data.rows) + 1)], \
    ]
    data.rookMoves = [ \
    [(0, i) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(i, 0) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(-i, 0) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(0, -i) for i in range(1, max(data.cols, data.rows) + 1)], \
    ]
    data.bishopMoves = [ \
    [(i, i) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(i, -i) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(-i, i) for i in range(1, max(data.cols, data.rows) + 1)], \
    [(-i, -i) for i in range(1, max(data.cols, data.rows) + 1)], \
    ]

def initializePieces(player): # draw images and make objects for all the pieces
    pawn, bishop, knight, rook, queen, king = player.getImage()
    pieces = player.pPieces
    for key in pieces:
        for elem in pieces[key]:
            if key == "pawn":
                file = pawn
                if player.player == "p1":
                    moves = data.pawnMovesp1
                else: moves = data.pawnMovesp2
            turn = player.player
            if key == "bishop": moves = data.bishopMoves; file = bishop
            if key == "king": moves = data.kingMoves; file = king
            if key == "rook": moves = data.rookMoves; file = rook
            if key == "queen": moves = data.queenMoves; file = queen
            if key == "knight": moves = data.knightMoves; file = knight
            if data.rows + data.cols >= 24:
                #file = file.subsample(2)
                pass
            x, y = getXY(elem)
            row, col = getCell(x, y)
            elem = pieceClass.pieces(key, moves, x, y, row, col, turn, file)
            data.pieces.append(elem)
            data.board[row][col] = elem
            if player.player == "p1":
                if elem not in data.playerOne.p:
                    player.p.append(elem)
            elif player.player == "p2":
                if elem not in data.playerTwo.p:
                    player.p.append(elem)