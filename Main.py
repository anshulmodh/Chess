import pygame
import data
import gameLogic
import event
import graphics as g
import support as s
import reset

def run():
    screen = data.screen
    data.dark = pygame.Surface(data.backWood.get_size()).convert_alpha()
    data.dark.fill((0, 0, 0, data.darken_percent*255))
    while True:
        if data.reset:
            data.reset = False
            reset.resetAll()
            # data.pause = False
            continue
        if data.startX0 > 0 and data.animatefirst:
            data.startX0 -= 25
        else:
            data.animatefirst = False
        if data.startScreen:
            g.startingScreen(screen)
        if data.pause:
            pauseAnim()
        if data.pauseAnim:
            pauseAnimVals()
        if not data.pause and not data.pauseAnim:
            data.Pfont1Size = data.margin1 = data.pauserect1 = data.pauserect2 = data.pauseW = data.pauseH = data.Pfont = data.alpha = data.pauserect3 = data.pauserect4 = data.pauseW1 = data.pauseH1 = 0
        if not data.startScreen and not data.pause:
            s.getKings()
            data.playerOne.setPlayer = data.player1turn
            data.playerTwo.setPlayer = data.player2turn
            if not data.cpu:
                s.incTimers()
            if gameLogic.checkKing(data.board):
                data.check = True
            if data.check:
                g.check(screen, "CHECK", 175, 650)
            event.mouseMotion()
            gameLogic.checkGameOver()
        if not data.startScreen:
            if data.player1turn:
                pieces2 = data.playerOne.dead
            else:
                pieces2 = data.playerTwo.dead
            if gameLogic.checkP(pieces2):
                gameLogic.checkPromotion()
            g.redrawAll(screen)
        data.fps.tick(100)
        pygame.display.flip()
        event.onEvent(screen)

def initialize():
    for key in data.custompieces:
        newkey = data.custompieces[key][4]
        player = data.custompieces[key][5]
        row, col = data.custompieces[key][2], data.custompieces[key][3]
        p1Pieces = []
        p2Pieces = []
        if player == "p1":
            if newkey in p1Pieces:
                p1Pieces[newkey].append((row, col))
            else:
                p1Pieces[newkey] = [(row, col)]
        elif player == "p2":
            if newkey in data.p2Pieces:
                p2Pieces[newkey].append((row, col))
            else:
                p2Pieces[newkey] = [(row, col)]
    data.board = [([None] * data.cols) for row in range(data.rows)]
    changePieces()
    data.playerOne = player.player(data.player1turn, p1Pieces, [], [], "p1")
    data.playerTwo = player.player(data.player2turn, p2Pieces, [], [], "p2")
    initializePieces(data.playerOne)
    initializePieces(data.playerTwo)
    s.getKings()
    data.startScreen = False
    data.custom = False
    data.makeCustomScreen = False
    height = data.height - data.margin*2
    width = data.width - data.margin*2
    data.cellWidth = width/data.cols
    data.cellHeight = height/data.rows

def pauseAnim():
    if data.pauserect1 < 150:
        data.pauserect1 += 10
    if data.pauserect2 < 200:
        data.pauserect2 += 15
    if data.pauseW < 400:
        data.pauseW += 40
    if data.pauseH < 300:
        data.pauseH += 30
    if data.Pfont < 40:
        data.Pfont += 5
        data.pauseFont = pygame.font.SysFont("impact", int(data.Pfont))
    if data.Pfont1Size < 15:
        data.Pfont1Size += 3
        data.Pfont1 = pygame.font.SysFont("impact", int(data.Pfont))
    if data.alpha < 128:
        data.alpha += 12
    if data.pauserect3 < 200:
        data.pauserect3 += 20
    if data.pauserect4 < 300:
        data.pauserect4 += 25
    if data.pauseH1 < 50:
        data.pauseH1 += 5
    if data.pauseW1 < 300:
        data.pauseW1 += 25
    if data.margin1 < 75:
        data.margin1 += 5
    if data.textX < 350:
        data.textX += 35
    if data.textY < 310:
        data.textY += 30

def pauseAnimVals():
    data.pauserect1 -= 10
    data.pauserect2 -= 15
    data.pauseW -= 40
    data.pauseH -= 30
    if data.alpha > 0:
        data.alpha -= 12
    if data.Pfont > 0:
        data.Pfont -= 5
        data.pauseFont = pygame.font.SysFont("impact", int(data.Pfont))
    if data.Pfont1Size > 0:
        data.Pfont1Size -= 2
        data.Pfont1 = pygame.font.SysFont("impact", int(data.Pfont))
    if data.pauserect1  < 30 and data.pauserect2 < 30 and data.pauseW < 400 and data.pauseH < 300:
        data.pauseAnim = False
    if data.pauserect3 > 0:
        data.pauserect3 -= 15
    if data.pauserect4 > 0:
        data.pauserect4 -= 25
    if data.pauseH1 > 0:
        data.pauseH1 -= 5
    if data.pauseW1 > 0:
        data.pauseW1 -= 40
    if data.margin1 > 0:
        data.margin1 -= 10
    if data.textX > 0:
        data.textX -= 35
    if data.textY > 0:
        data.textY -= 30

run()

# def rightPressed(event, data):
#     x, y = event.pos[0], event.pos[1]
#     if 150 < x < 250 and 30 < y < 60:
#         data.timer1 = False
#         data.time1 = 0
#         data.start1 = None
#     elif 450 < x < 550 and 30 < y < 60:
#         data.timer2 = False
#         data.time2 = 0
#         data.start2 = None

# pygame.draw.ellipse(screen, brown, [data.help1 + 300 - r, data.help2 + 625, r*2, r*2])
# pygame.draw.ellipse(screen, brown, [data.help1 + 400 - r, data.help2 + 625, r*2, r*2])
# pygame.draw.rect(screen, brown, [data.help1 + 300, data.help2 + 625, 100, 26])

    # pygame.draw.rect(screen, white, [data.startX0 + 150, 30, 100, 30])
    # screen.blit(text, textRect)
    # pygame.draw.rect(screen, white, [data.startX0 + 450, 30, 100, 30])

# def checkTimers(data, event):
#     x, y = event.pos[0], event.pos[1]
#     if data.startX0 + 150 < x < 250 and 30 < y < 60:
#         if data.start1 == None:
#             data.start1 = time.time()
#         data.timer1 = not data.timer1
#     elif data.startX0 + 450 < x < 550 and 30 < y < 60:
#         if data.start2 == None:
#              data.start2 = time.time()
#         data.timer2 = not data.timer2

# def secondClickCheck(data, event): # check for second click
#     newrow, newcol = getCell(data, event.pos[0], event.pos[1]) 
#     x, y = getXY(data, (newrow, newcol))
#     if data.board[data.drow][data.dcol] == data.p1King or data.board[data.drow][data.dcol] == data.p2King:  
#         drawNew(data, newrow, newcol, x, y)
#         if checkKing(data, data.board, (newrow, newcol)):
#             goBack(data) # if check, undo
#             piece = data.board[newrow][newcol]
#             if piece != None:
#                 piece.setMoved()
#         else:
#             drawNew(data, newrow, newcol, x, y)
#             data.check = False
#     else:
#         if checkKing(data, data.board):
#             drawNew(data, newrow, newcol, x, y)
#             piece = data.board[newrow][newcol]
#             if piece != None:
#                 piece.setMoved()
#         else:
#             drawNew(data, newrow, newcol, x, y)
#             data.check = False