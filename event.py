import sys, pygame
import support as s
import data
import gameLogic as gl
import cpu
import player
import time
import reset

def onEvent(screen):
    x, y = pygame.mouse.get_pos()
    cursorMotion(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            data.died = False
            x, y = event.pos[0], event.pos[1]
            if data.help:
                helpPress(event)
            if data.b3 - 25 < x < data.b3 + 200 + 50 and 500 < y < 550 and not data.custom:
                data.help = True
            if not data.startScreen and not data.makeCustomScreen:
                pressPromote(event)
                if not data.pause and data.startX0 + 10 < x < data.startX0 + 40 and 10 < y < 40:
                    data.pause = True
                    data.offset = time.time()
                nextEvent(event)
            if data.startScreen:
                eventCustom(x, y)
            if data.pause:
                paused(event)
            if data.custom:
                customPress()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if data.pause:
                    s.offsetTimers()
                    data.pauseAnim = True
                else:
                    data.offset = time.time()
                data.pause = not data.pause
            if event.key == pygame.K_ESCAPE and data.pause:
                s.offsetTimers()
                data.pauseAnim = True
                data.pause = False
            if data.text1 or data.text2:
                if data.text1:
                    if event.keysym == "BackSpace":
                        data.text1Num = data.text1Num[:-1]
                    elif event.keysym in "0123456789":
                        data.text1Num = data.text1Num + event.keysym
                elif data.text2:
                    if event.keysym == "BackSpace":
                        data.text2Num = data.text2Num[:-1]
                    elif event.keysym in "0123456789":
                        data.text2Num = data.text2Num + event.keysym

def initial():
    data.makeCustomScreen =False
    data.custom = False
    data.customAnim = False
    data.player2turn = True
    data.player1turn = False
    data.startScreen = False
    data.addScreen = True
    p2Pieces = {"pawn": [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), \
(6, 6), (6, 7)], "bishop": [(7, 2), (7, 5)], "rook": [(7, 0), (7, 7)], \
"queen": [(7, 4)], "king": [(7, 3)], "knight": [(7, 1), (7, 6)]}
    p1Pieces = {"pawn": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), \
(1, 6), (1, 7)], "bishop": [(0, 2), (0, 5)], "rook": [(0, 0), (0, 7)], \
"queen": [(0, 4)], "king": [(0, 3)], "knight": [(0, 1), (0, 6)]}
    data.playerOne = player.player(data.player1turn, p1Pieces, [], [], "p1")
    data.playerTwo = player.player(data.player2turn, p2Pieces, [], [], "p2")
    s.initializePieces(data.playerOne)
    s.initializePieces(data.playerTwo)
    s.getKings()
    data.rows = 8
    data.cols = 8

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

def getCustomCell(x, y):
    colNum = None
    RNum = None
    for col in range(data.cols): # determine cell coordinates of click
        colStartX = data.custommargin + data.customcellWidth * col
        colEndX = colStartX + data.customcellWidth
        if colStartX <= x <= colEndX: colNum = col; break
    for row in range(data.rows):
        rowStartX = data.custommargin + data.customcellHeight * row
        rowEndX = rowStartX + data.customcellHeight
        if rowStartX <= y <= rowEndX: RNum = row; break
    return (RNum, colNum)

def getcustomXY(row, col): # get x, y coordinates from row col
    x0 = data.custommargin + 0 + data.customcellWidth* col 
    y0 = data.custommargin + 0 + data.customcellHeight * row
    x = x0 + (data.customcellWidth/2)
    y = y0 + (data.customcellHeight/2)
    return x, y

def customPress():
    x, y = pygame.mouse.get_pos()
    if data.custom and 600 < x < 675 and 30 < y < 60:
        initial()
    if data.custom and 600 < x < 675 and 90 < y < 120:
        initial()
        data.cpu = True
    row, col = getPieceCell(x, y)
    if row != None and col != None and data.customclick1 == False:
        if data.rows + data.cols > 24:
            if row == 0: files = data.row0Size
            else: files = data.row1Size
            image = files[col]
            data.piecedraw.append([image.copy(), data.piecenames[row][col]])
        else:
            if row == 0: files = data.row0
            else: files = data.row1
            image = files[col]
            data.piecedraw.append([image.copy(), data.piecenames[row][col]])
        data.customclick1 = True
    elif data.customclick1 and not (200 < x < 500) and y < 500:
        data.piecedraw = data.piecedraw[-1:]
        data.customclick1 = False
    if data.customclick1:
        newrow, newcol = getCustomCell(x, y)
        if newrow != None and newcol != None and ((newrow, newcol) not in data.usedplaces):
            x, y = getcustomXY(newrow, newcol)
            data.usedplaces.append((newrow, newcol))
            piece = data.piecedraw[0][0]
            data.custompieces[piece] = [x, y, newrow, newcol, data.piecedraw[0][1][0], data.piecedraw[0][1][1]]
            data.customclick1 = False
            data.piecedraw = []
        elif ((newrow, newcol) in data.usedplaces):
            data.piecedraw = data.piecedraw[-1:]
            data.customclick1 = False
    if not data.customAnim and data.xOne - ((data.yTwo - data.yOne)/2) < x < data.xTwo + ((data.yTwo - data.yOne)/2) and data.yOne < y < data.yTwo:
        reset.resetAll()
        # data.custom = False
        # data.customAnim = False
        # data.makeCustomScreen = False
        # data.startScreen = True
        # data.x0 = data.width/2
        # data.y0 = data.height/2
    if data.makeCustomScreen:
        if 101 < x < 175 and 30 < y < 60:
            data.text1 = True
            data.text2 = False
        elif 275 < x < 350 and 30 < y < 60:
            data.text1 = False
            data.text2 = True
        elif data.text1 or data.text2:
            data.text1 = False
            data.text2 = False

def nextEvent(event):
    if not data.cpu:
        if not data.cpu and not data.pause:
            mousePressPlay(event)
    else:
        if data.player2Attack:
            data.player1turn = True
            data.player2Attack = False
        # if data.player1turn:
        #     cpu.cpu(data.board)
        #     data.player1turn = False
        #     data.player2turn = True
        if data.player2turn:
            mousePressPlay(event)
            if data.moved:
                print(2222222222222)
                data.player1turn = True
                data.player2turn = False
                data.moved = False    

def cursorMotion(screen):
    x, y = pygame.mouse.get_pos()
    if data.startScreen:
        if 200 < x < 500 and 300 < y < 350:
            data.tanB1 = 200, 178, 141
        elif 200 < x < 500 and 400 < y < 450:
            data.tanB2 = 200, 178, 141
        elif 200 < x < 500 and 500 < y < 550 and not data.custom:
            data.tanB3 = 200, 178, 141
        elif 200 < x < 500 and 600 < y < 650 and not data.help:
            data.tanB4 = 200, 178, 141
        else:
            s.resetColors()
    if data.help:
        r = 13
        if data.help1 + 300 - r < x < data.help1 + 400 - r + r*2 and data.help2 + 625 < y < data.help2 + 625 + r*2:
            data.brown1 = 141, 95, 59
        else:
            s.resetColors()
    if data.pause:
        if data.pauserect3 < x < data.pauserect3 + data.pauseW1 and data.pauserect4 < y < data.pauserect4 + data.pauseH1:
            s.resetColors()
            data.tan1 = 180, 158, 121
        elif data.pauserect3 < x < data.pauserect3 + data.pauseW1 and data.pauserect4 + data.margin1 < y < data.pauserect4 + data.margin1 + data.pauseH1:
            s.resetColors()
            data.tan2 = 180, 158, 121
        elif data.pauserect3 < x < data.pauserect3 + data.pauseW1/4 and data.pauserect4 + data.margin1*2 < y < data.pauserect4 + data.margin1*2 + data.pauseH1:
            s.resetColors()
            data.tan3 = 180, 158, 121
        elif data.pauserect3 + (data.pauseW1*3)/8 < x < data.pauserect3 + (data.pauseW1*3)/8 + data.pauseW1/4 and data.pauserect4 + data.margin1*2 < y < data.pauserect4 + data.margin1*2 + data.pauseH1:
            s.resetColors()
            data.tan4 = 180, 158, 121
        elif data.pauserect3 + (data.pauseW1*3)/4 < x < data.pauserect3 + (data.pauseW1*3)/4 + data.pauseW1/4 and data.pauserect4 + data.margin1*2 < y < data.pauserect4 + data.margin1*2 + data.pauseH1:
            s.resetColors()
            data.tan5 = 180, 158, 121
        else:
            s.resetColors()
    if not data.startScreen and not data.pause:
        if 100 < x < 600 and 100 < y < 600:
            r, c = s.getCell(x, y)
            data.x = data.margin + (data.cellWidth*c)
            data.y = data.margin + (data.cellHeight*r)
            data.tran = True
        else:
            data.tran = False

def eventCustom(x, y):
    if not data.makeCustomScreen:
        if 200 < x < 500 and 300 < y < 350:
            data.startScreen = False
            data.animatefirst = True
            p2Pieces = {"pawn": [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), \
        (6, 6), (6, 7)], "bishop": [(7, 2), (7, 5)], "rook": [(7, 0), (7, 7)], \
        "queen": [(7, 4)], "king": [(7, 3)], "knight": [(7, 1), (7, 6)]}
            p1Pieces = {"pawn": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), \
        (1, 6), (1, 7)], "bishop": [(0, 2), (0, 5)], "rook": [(0, 0), (0, 7)], \
        "queen": [(0, 4)], "king": [(0, 3)], "knight": [(0, 1), (0, 6)]}
            data.playerOne = player.player(data.player1turn, p1Pieces, [], [], "p1")
            data.playerTwo = player.player(data.player2turn, p2Pieces, [], [], "p2")
            s.initializePieces(data.playerOne)
            s.initializePieces(data.playerTwo)
            data.addScreen = True
            s.getKings()
            data.rows = 8
            data.cols = 8
        elif 200 < x < 500 and 400 < y < 450:
            data.player2turn = True
            data.player1turn = False
            data.startScreen = False
            data.animatefirst = True
            data.addScreen = True
            p2Pieces = {"pawn": [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), \
        (6, 6), (6, 7)], "bishop": [(7, 2), (7, 5)], "rook": [(7, 0), (7, 7)], \
        "queen": [(7, 4)], "king": [(7, 3)], "knight": [(7, 1), (7, 6)]}
            p1Pieces = {"pawn": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), \
        (1, 6), (1, 7)], "bishop": [(0, 2), (0, 5)], "rook": [(0, 0), (0, 7)], \
        "queen": [(0, 4)], "king": [(0, 3)], "knight": [(0, 1), (0, 6)]}
            data.playerOne = player.player(data.player1turn, p1Pieces, [], [], "p1")
            data.playerTwo = player.player(data.player2turn, p2Pieces, [], [], "p2")
            s.initializePieces(data.playerOne)
            s.initializePieces(data.playerTwo)
            s.getKings()
            data.rows = 8
            data.cols = 8
            data.cpu = True
        elif 200 < x < 500 and 500 < y < 550 and not data.custom:
            data.help = True
        elif 200 < x < 500 and 600 < y < 650 and not data.help:
            print("custom")
            data.custom = True
            data.makeCustomScreen = True
            data.customAnim = True
        elif 200 < x < 500 and 660 < y < 680:
            data.startField = True
        else:
            data.startField = False

def mousePressPlay(event):# look for mouse press in play
    if not (data.p1promote or data.p2promote):
        if gl.checkKing(data.board): data.check = True
        if data.click1 == False:
            if (data.margin <= event.pos[0] <= (data.width - data.margin)) and (data.margin <= event.pos[1] <= (data.height - data.margin)):
                data.drow, data.dcol = s.getCell(event.pos[0], event.pos[1])
                if gl.checkPlayerPiece():
                    if data.board[data.drow][data.dcol] != None: 
                        data.click1 = True 
                else:
                    gl.drawOld()
        elif (data.margin <= event.pos[0] <= (data.width - data.margin)) and (data.margin <= event.pos[1] <= (data.height - data.margin)) and data.click1 == True:
            secondClick(event)
        else:
            gl.goBack()

def secondClick(event): # manage second click
    print(1111111111111)
    if data.check == True:
        secondClickCheck(event)
    else:  
        newrow, newcol = s.getCell(event.pos[0], event.pos[1]) 
        x, y = s.getXY((newrow, newcol))
        if data.board[data.drow][data.dcol] == data.p1King or data.board[data.drow][data.dcol] == data.p2King:
            if gl.checkCastle(newrow, newcol):
                gl.changeAfterCastle(newrow, newcol)
                data.moved = True
            else:
                gl.drawNew(newrow, newcol, x, y)
                piece = data.board[newrow][newcol]
                if piece != None:
                    piece.setMoved()
        else:
            gl.drawNew(newrow, newcol, x, y)
            piece = data.board[newrow][newcol]
            if piece != None:
                piece.setMoved()
    gl.checking()

def secondClickCheck(event): # check for second click
    newrow, newcol = s.getCell(event.pos[0], event.pos[1]) 
    x, y = s.getXY((newrow, newcol))
    if data.board[data.drow][data.dcol] == data.p1King or data.board[data.drow][data.dcol] == data.p2King:  
        gl.drawNew(newrow, newcol, x, y)
        if gl.checkKing(data.board, (newrow, newcol)):
            gl.goBack() # if check, undo
            piece = data.board[newrow][newcol]
            if piece != None:
                piece.setMoved()
        else:
            gl.drawNew(newrow, newcol, x, y)
            data.check = False
    else:
        if gl.checkKing(data.board):
            gl.drawNew(newrow, newcol, x, y)
            piece = data.board[newrow][newcol]
            if piece != None:
                piece.setMoved()
        else:
            gl.drawNew(newrow, newcol, x, y)
            data.check = False

def mouseMotion(): # set piece to mouse placement
    x, y = pygame.mouse.get_pos()
    if data.click1 == True:
        # setEventInfo(event, data, "mouseMotion")
        data.motionPosn = (x, y)
        for piece in data.pieces:
            if piece.getPos() == (data.drow, data.dcol):
                piece.move(x, y, data.drow, data.dcol)
    if data.customclick1:
        # setEventInfo(event, data, "mouseMotion")
        data.motionPosn = (x, y)
        data.currentdrawingpiece = data.piecedraw[0][0]
        data.drawpiecex = x
        data.drawpiecey = y

def helpPress(event):
    delta1 = 300
    delta2 = 50
    #data.help1 + delta1,data.help2 + delta1 * 2, data.help1 + delta1 + delta2*2, data.help2 + (delta1 * 2) + delta2
    #data.help1 + 300, data.help2 + 625, 100, 26]
    if data.help1 + 300 - 13 <= event.pos[0] <= data.help1 + 400 + 13 and data.help2 + 625 <= event.pos[1] <= data.help2 + 651:
        data.helpAnim = True

def paused(event):
    # x1 = data.pauserect1 + 150
    # x2 = data.pauserect1 + 250
    x = event.pos[0]
    y = event.pos[1]
    if (data.pauserect3 < x < (data.pauserect3 + data.pauseW1) and data.pauserect4 < y < (data.pauserect4 + data.pauseH1)):
        data.reset = True
    if (data.pauserect3 < x < (data.pauserect3 + data.pauseW1) and (data.pauserect4 + data.margin1) < y < (data.pauserect4 + data.pauseH1 + data.margin1)):
        s.offsetTimers()
        data.pauseAnim = True
        data.pause = False
    if data.cpu:
        if data.pauserect3 < x < data.pauserect3 + data.pauseW1/4 and data.pauserect4 + data.margin1*2 < y < data.pauserect4 + data.margin1*2 + data.pauseH1:
            data.depth = 3
            s.offsetTimers()
            data.pauseAnim = True
            data.pause = False
        elif data.pauserect3 + (data.pauseW1*3)/8 < x < data.pauserect3 + (data.pauseW1*3)/8 + data.pauseW1/4 and data.pauserect4 + data.margin1*2 < y < data.pauserect4 + data.margin1*2 + data.pauseH1:
            data.depth = 7
            s.offsetTimers()
            data.pauseAnim = True
            data.pause = False
        elif data.pauserect3 + (data.pauseW1*3)/4 < x < data.pauserect3 + (data.pauseW1*3)/4 + data.pauseW1/4 and data.pauserect4 + data.margin1*2 < y < data.pauserect4 + data.margin1*2 + data.pauseH1:
            data.depth = 15
            s.offsetTimers()
            data.pauseAnim = True
            data.pause = False
        # if x1 < event.pos[0] < x2 and 375 < event.pos[1] < 400:
        #     data.depth = 3
        # if x1 < event.pos[0] < x2 and 425 < event.pos[1] < 450:
        #     data.depth = 7
        # if x1 < event.pos[0] < x2 and 475 < event.pos[1] < 500:
        #     data.depth = 15

def pressPromote(event): # check which piece to promote
    if data.p1promote:
        p1promote(event)
    elif data.p2promote:
        p2promote(event) 

def p1promote(event): # promote player1
    x, y = event.pos[0], event.pos[1]
    if len(data.playerOne.dead) == 0: data.p1promote = False
    for piece in data.playerOne.dead:
        px, py = piece.getCoor()
        if px - 30 <= x <= px + 30 and py - 30 <= y <= py + 30:
            # if piece.compareName("pawn"):
            #     data.b1promote = False
            #     return
            row, col = data.prow, data.pcol
            Nx, Ny = s.getXY((row, col))
            gl.replace(row, col, Nx, Ny, piece, data.playerOne.dead)
            data.p1promote = False
            break
    #resizeImages(data, data.p1dead)
            
def p2promote(event):# promotep2
    x, y = event.pos[0], event.pos[1]
    if len(data.playerTwo.dead) == 0: data.p2promote = False
    for piece in data.playerTwo.dead:
        px, py = piece.getCoor()
        if px - 30 <= x <= px + 30 and py - 30 <= y <= py + 30:
            # if piece.compareName("pawn"):
            #     data.b2promote = False
            #     return
            row, col = data.prow, data.pcol
            Nx, Ny = s.getXY((row, col))
            gl.replace(row, col, Nx, Ny, piece, data.playerTwo.dead)
            data.p2promote = False
            break
   # resizeImages(data, data.p2dead)
