import pygame
import data
import gameLogic
import event
import graphics as g
import support as s
import reset
import cpu as cpu

def run(): 
    screen = data.screen
    data.dark = pygame.Surface(data.backWood.get_size()).convert_alpha() # Background and initialize vars
    data.dark.fill((0, 0, 0, data.darken_percent*255))
    initPics()
    while True: # Game Loop
        if data.reset: # Reset game vars
            data.reset = False
            reset.resetAll()
            # data.pause = False
            continue
        if data.startX0 > 0 and data.animatefirst: # Animate Loading Screen
            data.startX0 -= 25
        else:
            data.animatefirst = False
        if data.startScreen: # Display Starting Screen
            g.startingScreen(screen)
        if data.pause: # Animate the pausing sequence
            pauseAnim()
        if data.pauseAnim: # Update the pause animation vars
            pauseAnimVals()
        if data.custom or data.customAnim or data.makeCustomScreen: # Display the custom game screen
            customScreen(screen)
        if not data.pause and not data.pauseAnim: # Update unused animation vars
            data.Pfont1Size = data.margin1 = data.pauserect1 = data.pauserect2 = data.pauseW = data.pauseH = 0
            data.Pfont = data.alpha = data.pauserect3 = data.pauserect4 = data.pauseW1 = data.pauseH1 = 0
        if not data.startScreen and not data.pause and not data.makeCustomScreen and not data.gameover:
            gameCheckFuncs(screen)    # check game validity
        if not data.startScreen and not data.gameover: 
            refreshValues(screen)
        data.fps.tick(100)
        pygame.display.flip()
        event.onEvent(screen)

def refreshValues(screen): # Update player data during the game
    if data.player1turn: 
        pieces2 = data.playerOne.dead
    else:
        pieces2 = data.playerTwo.dead
    if gameLogic.checkP(pieces2):
        gameLogic.checkPromotion()
    if not data.makeCustomScreen:
        g.redrawAll(screen)

def gameCheckFuncs(screen):
    if (data.startScreen):
        g.setScreen(screen)
    s.getKings()
    data.playerOne.setPlayer = data.player1turn # Increment player turns
    data.playerTwo.setPlayer = data.player2turn
    s.incTimers()
    if data.player1turn and data.cpu: 
        g.drawPieces(screen) # Move the CPU pieces if AI is playing
        cpu.cpu(data.board)
        #print("change turnMain")
        data.player2turn = True
        data.player1turn = False
    if gameLogic.checkKing(data.board): # Check is any of the two kings are in check
        data.check = True
    if data.check:
        g.check(screen, "CHECK", 175, 650) # Display the check message
    event.mouseMotion()
    gameLogic.checkGameOver()

def customScreen(screen):
    if len(data.text1Num) > 0: # Assign row col values from text box input
        if 3 <= int(data.text1Num) <= 20:
            data.rows = int(data.text1Num)
        else:
            if not data.text1:
                data.text1Num = "8"
                data.cols = 8
    if len(data.text2Num) > 0:
        if 3 <= int(data.text2Num) <= 20:
            data.cols = int(data.text2Num)
        else:
            if not data.text2:
                data.text2Num = "8"
                data.cols = 8
    g.drawCustomScreen(screen)
    data.startScreen = False # animate the custom screen
    if (data.customSize < 700):
            data.customSize += 10
            data.x0 -= 5
            data.y0 -= 5
    if data.customFontSize < 30:
        data.customFontSize +=1
    if not (0 >= data.x1 and data.x2 >= data.width and data.y1 <= 0 and data.y2 >= data.height):
        data.x1 -= 5
        data.x2 += 5
        data.y1 -= 5
        data.y2 += 5
    else:
        data.customAnim = False

def pauseAnim(): # Animation vars for the pause screen
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
    if data.Pfont1Size < 13:
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
    if data.margin1 < 60:
        data.margin1 += 5
    if data.textX < 350:
        data.textX += 35
    if data.textY < 310:
        data.textY += 30

def pauseAnimVals(): # Animation vars for retracting the pause screen
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

def initPics(): # initialize pics from the Pictures/ dir
    data.WpawnSize = pygame.transform.scale(data.Wpawn, (30, 30))
    data.BpawnSize =  pygame.transform.scale(data.Bpawn, (30, 30))
    data.WbishopSize = pygame.transform.scale(data.Wbishop, (30, 30))
    data.BbishopSize = pygame.transform.scale(data.Bbishop, (30, 30))
    data.BknightSize = pygame.transform.scale(data.Bknight, (30, 30))
    data.WknightSize = pygame.transform.scale(data.Wknight, (30, 30))
    data.BrookSize = pygame.transform.scale(data.Brook, (30, 30))
    data.WrookSize = pygame.transform.scale(data.Wrook, (30, 30))
    data.BkingSize = pygame.transform.scale(data.Bking, (30, 30))
    data.WkingSize = pygame.transform.scale(data.Wking, (30, 30))
    data.BqueenSize = pygame.transform.scale(data.Bqueen, (30, 30))
    data.WqueenSize = pygame.transform.scale(data.Wqueen, (30, 30))
    data.WpawnSSize = pygame.transform.scale(data.Wpawn, (14, 14))
    data.BpawnSSize =  pygame.transform.scale(data.Bpawn, (14, 14))
    data.WbishopSSize = pygame.transform.scale(data.Wbishop, (14, 14))
    data.BbishopSSize = pygame.transform.scale(data.Bbishop, (14, 14))
    data.startField = False
    data.BknightSSize = pygame.transform.scale(data.Bknight, (14, 14))
    data.WknightSSize = pygame.transform.scale(data.Wknight, (14, 14))
    data.BrookSSize = pygame.transform.scale(data.Brook, (14, 14))
    data.WrookSSize = pygame.transform.scale(data.Wrook, (14, 14))
    data.BkingSSize = pygame.transform.scale(data.Bking, (14, 14))
    data.WkingSSize = pygame.transform.scale(data.Wking, (14, 14))
    data.BqueenSSize = pygame.transform.scale(data.Bqueen, (14, 14))
    data.WqueenSSize = pygame.transform.scale(data.Wqueen, (14, 14))
    data.row0Orig = [data.Wpawn, data.Wrook, data.Wbishop, data.Wknight, data.Wking, data.Wqueen]
    data.row1Orig = [data.Bpawn, data.Brook, data.Bbishop, data.Bknight, data.Bking, data.Bqueen]
    data.row0 = [data.WpawnSize, data.WrookSize, data.WbishopSize, data.WknightSize, data.WkingSize, data.WqueenSize]
    data.row1 = [data.BpawnSize, data.BrookSize, data.BbishopSize, data.BknightSize, data.BkingSize, data.BqueenSize]
    data.row0Size = [data.WpawnSSize, data.WrookSSize, data.WbishopSSize, data.WknightSSize, data.WkingSSize, data.WqueenSSize]
    data.row1Size = [data.BpawnSSize, data.BrookSSize, data.BbishopSSize, data.BknightSSize, data.BkingSSize, data.BqueenSSize]

run()