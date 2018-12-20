import pygame
import data
import gameLogic as gl

black = 0, 0, 0
white = 255, 255, 255
green = 124, 252, 0
gray = 130, 130, 230
tan = 240, 218, 181
brown = 181, 135, 99

def redrawAll(screen): # control all canvas draw functions
    drawGame(screen) 
    if data.moveAnim:
        moveAnimation()
    if data.check:
        check(screen, "CHECK", 350, 650)
    if not data.startScreen and gl.checkmate(data.board) and not data.gameover:
        check(screen, "CHECKMATE!", 350, 650)
    if data.p1promote or data.p2promote:
        check(screen, "Pawn Promotion!", 525, 650)
    if not data.cpu:
        drawPlayer(screen)
    if data.gameover:
        gameover(screen)
    if data.pause or data.pauseAnim:
        pauseScreen(screen)
    if not data.startScreen and not data.pause and data.tran and data.startX0 <= 0 and not data.pauseAnim:
        drawTrans(screen)

def moveAnimation():
    if data.moveAnim and data.drawingpiece != None:
        piece = data.drawingpiece
        x = data.piecex
        y = data.piecey
        piece.move(x, y, data.end[0], data.end[1])
        data.piecex += data.xdis
        data.piecey += data.ydis
        xorg = data.orgpiecex
        yorg = data.orgpiecey
        if xorg >= data.CPUXY[0] and yorg >= data.CPUXY[1]:
            if data.piecex <= data.CPUXY[0] and data.piecey <= data.CPUXY[1]:
                piece.move(data.CPUXY[0], data.CPUXY[1], data.end[0], data.end[1])
                data.moveAnim = False
        elif xorg >= data.CPUXY[0] and yorg <= data.CPUXY[1]:
            if data.piecex <= data.CPUXY[0] and data.piecey >= data.CPUXY[1]:
                piece.move(data.CPUXY[0], data.CPUXY[1], data.end[0], data.end[1])
                data.moveAnim = False
        elif xorg <= data.CPUXY[0] and yorg >= data.CPUXY[1]:
            if data.piecex >= data.CPUXY[0] and data.piecey <= data.CPUXY[1]:
                piece.move(data.CPUXY[0], data.CPUXY[1], data.end[0], data.end[1])
                data.moveAnim = False
        elif xorg <= data.CPUXY[0] and yorg <= data.CPUXY[1]:
            if data.piecex >= data.CPUXY[0] and data.piecey >= data.CPUXY[1]:
                piece.move(data.CPUXY[0], data.CPUXY[1], data.end[0], data.end[1])
                data.moveAnim = False

def setScreen(screen):
    for elem in data.playerOne.p:
        elem.screen = screen
    for elem in data.playerTwo.p:
        elem.screen = screen

def startingScreen(screen):
    screen.fill(white)
    pygame.display.set_caption("Chess")
    drawStart(screen)
    animateScreen()
    if data.help:
        drawHelp(screen)
        if data.help1 > 0 and data.help2 < 0:
            data.help1 -= 50
            data.help2 += 50
        if data.helpAnim:
            if data.help1 >= -data.width and data.help2 <= data.height:
                data.help1 -= 50
                data.help2 += 50
            else:
                data.helpAnim = False
                data.help = False
        if not data.help and not data.helpAnim:
            data.help1 = data.width
            data.help2 = - data.height
    if not (data.titleY >= 200):
        data.titleY += 7

def drawStart(screen): # draw start screen
    screen.blit(data.startWood, [0, 0])
    r = 25
    pygame.draw.ellipse(screen, data.tanB1, [data.b1 - r, 325 - r, r*2, r*2])
    pygame.draw.ellipse(screen, data.tanB1, [data.b1 + 200 - r, 325 - r, r*2, r*2])
    pygame.draw.rect(screen, data.tanB1, [data.b1, 300, 200, 50])
    font = pygame.font.SysFont("impact", 20)
    text = font.render("2-Player", True, black)
    textRect = text.get_rect(center = (data.b1 + 100, 325))
    screen.blit(text, textRect)
    pygame.draw.ellipse(screen, data.tanB2, [data.b2 - r, 425 - r, r*2, r*2])
    pygame.draw.ellipse(screen, data.tanB2, [data.b2 + 200 - r, 425 - r, r*2, r*2])
    pygame.draw.rect(screen, data.tanB2, [data.b2, 400, 200, 50])
    text = font.render("1-Player v CPU", True, black)
    textRect = text.get_rect(center = (data.b1 + 100, 425))
    screen.blit(text, textRect)
    pygame.draw.ellipse(screen, data.tanB3, [data.b3 - r, 525 - r, r*2, r*2])
    pygame.draw.ellipse(screen , data.tanB3, [data.b3 + 200 - r, 525 - r, r*2, r*2])
    pygame.draw.rect(screen, data.tanB3, [data.b3, 500, 200, 50])
    text = font.render("Help Menu", True, black)
    textRect = text.get_rect(center = (data.b3 + 100, 525))
    screen.blit(text, textRect)
    pygame.draw.ellipse(screen, data.tanB4, [data.b4 - r, 625 - r, r*2, r*2])
    pygame.draw.ellipse(screen, data.tanB4, [data.b4 + 200 - r, 625 - r, r*2, r*2])
    pygame.draw.rect(screen, data.tanB4, [data.b4, 600, 200, 50])
    text = font.render("Custom Game", True, black)
    textRect = text.get_rect(center = (data.b4 + 100, 625))
    screen.blit(text, textRect)
    font = pygame.font.SysFont("impact", 50)
    text = font.render("Welcome to Chess", True, tan)
    textRect = text.get_rect(center = (350, data.titleY))
    screen.blit(text, textRect)

def drawHelp(screen): # draw help screen text
    textOne = """\
    You can play chess with a friend by clicking on \'2 Player\' in the main menu,
    or you can play against CPU by clicking 1 \'vs CPU\'. You can also play in the
    custom mode by clicking \'custom\', here you can change the size of the board,
    as well as drag and drop the pieces you want to play with. Play begins with
    player 1 on the far side of the board(or CPU in AI mode). Click the piece
    you want to move and click again to drop it, if you change your mind, click
    outside the board or on the original spot. This version of chess supports all
    moves, including pawn promotion, en Passant, castling, as well as knowing
    check and checkmate. Press \'p\' at any time to reach the pause menu where
    you can quit the game and go back to the main menu. The custom game mode
    allows you to change the number of rows and columns on the board as well as
    the amount and type of pieces you can play with. Drag and drop pieces from
    the grid at the bottom of the screen onto the board to place them. You can
    also trash selected pieces by dropping them to the left. Input your row and
    column number into the text fields at the top. Make sure to place a king down
    for each player and your're ready to go! 
    """
    r = 13
    screen.blit(data.backHelp, [data.help1, data.help2])
    font = pygame.font.SysFont("impact", 30)
    text = font.render("Help Menu...", True, brown)
    textRect = text.get_rect(center = (data.help1 + (data.width/2), data.help2 + 30))
    screen.blit(text, textRect)
    text1 = font.render("Welcome to Chess", True, brown)
    textRect = text1.get_rect(center = (data.help1 + (data.width/2), data.help2 + 60))
    screen.blit(text1, textRect)
    text2 = font.render("How to Play:", True, brown)
    textRect = text2.get_rect(center = (data.help1 + 80, data.help2 + 90))
    screen.blit(text2, textRect)
    text3 = render_textrect(textOne, pygame.font.SysFont("impact", 20), pygame.Rect(10, 130, data.width - 50, data.height - 150), brown, white, 0)
    screen.blit(text3, [data.help1 + 25, data.help2 + 110])
    pygame.draw.rect(screen, data.brown1, [data.help1 + 300, data.help2 + 625, 100, 26])
    font = pygame.font.SysFont("impact", 15)
    text4 = font.render("back", True, white)
    textRect = text4.get_rect(center = (data.help1 + 350, data.help2 + 637))
    screen.blit(text4, textRect)
    pygame.draw.ellipse(screen, data.brown1, [data.help1 + 300 - r, data.help2 + 625, r*2, r*2])
    pygame.draw.ellipse(screen, data.brown1, [data.help1 + 400 - r, data.help2 + 625, r*2, r*2])

def drawTrans(screen):
    rect = pygame.Surface((data.cellWidth,data.cellHeight))
    rect.set_alpha(80)              
    rect.fill((0,0,0))         
    screen.blit(rect, (data.x, data.y))

def drawGame(screen): # draw game cells
    height = data.height - data.margin*2
    width = data.width - data.margin*2
    data.cellWidth = int(width/data.cols)
    data.cellHeight = int(height/data.rows)
    screen.blit(data.backWood, [data.startX0, 0])
    for row in range(data.rows):
        for col in range(data.cols):
            if (row + col)%2 == 1:
                fill = data.woodLight
            else:
                fill = data.woodDark
            x0 = data.startX0 + data. margin + 0 + data.cellWidth * col
            y0 = data.margin + 0 + data.cellHeight * row
            x1 = data.cellWidth
            y1 = data.cellHeight
            screen.blit(fill, [x0, y0])
        drawPieces(screen)
    font = pygame.font.SysFont("impact", 13)
    if not data.cpu:
        text1 = font.render("Player 2 dead pieces:", True, white)
        text2 = font.render("Player 1 dead pieces:", True, white)
    else:
        text1 = font.render("Player's dead pieces:", True, white)
        text2 = font.render("CPU dead pieces:", True, white)
    textRect = text1.get_rect(center = (data.startX0 + 80, 50))
    screen.blit(text1, textRect)
    textRect = text2.get_rect(center = (data.startX0 + 620, 50))
    screen.blit(text2, textRect)
    pygame.draw.rect(screen, white, [data.startX0 + 10, 10, 30, 30])
    pygame.draw.rect(screen, black, [data.startX0 + 12, 12, 26, 26])
    pygame.draw.rect(screen, white, [data.startX0 + 14, 14, 22, 22])
    font = pygame.font.SysFont("impact", 25)
    text = font.render("P", True, black)
    textRect = text.get_rect(center = (data.startX0 + 25, 25))
    screen.blit(text, textRect)
    drawTimers(screen)

def drawPlayer(screen):
    font = pygame.font.SysFont("impact", 20)
    if data.player1turn:
        text = font.render("Player 1 Turn", True, white)
    else:
        text = font.render("Player 2 Turn", True, white)
    textRect = text.get_rect(center = (data.startX0 + 350, 20))
    screen.blit(text, textRect)

def gameover(screen):
    pygame.draw.rect(screen, black, [0, 0, data.width, data.height])
    font = pygame.font.SysFont("impact", 30)
    text = font.render("Game Over!", True, white)
    textRect = text.get_rect(center = (350, 100))
    screen.blit(text, textRect)
    text = font.render("Back to Main", True, white)
    textRect = text.get_rect(center = (350, 325))
    pygame.draw.rect(screen, green, [300, 300, 100, 50])
    screen.blit(text, textRect)

def drawPieces(screen): # draw all pieces
    for elem in data.pieces:
        elem.draw()
    mid = (data.margin  + 20)/ 2
    for i in range(len(data.playerTwo.dead)):
        data.playerTwo.dead[i].move(mid, data.margin + (i * mid), None, None)
    for i in range(len(data.playerOne.dead)):
        data.playerOne.dead[i].move(data.width - mid, data.margin + (i * mid), None, None)

def drawTimers(screen):
    font = pygame.font.SysFont("impact", 30)
    text = font.render(data.timertime1, True, black)
    textRect = text.get_rect(center = (data.startX0 + 200, 45))
    pygame.draw.rect(screen, black, [data.startX0 + 150, 30, 100, 30])
    pygame.draw.rect(screen, white, [data.startX0 + 151, 31, 98, 28])
    screen.blit(text, textRect)
    pygame.draw.rect(screen, black, [data.startX0 + 450, 30, 100, 30])
    pygame.draw.rect(screen, white, [data.startX0 + 451, 31, 98, 28])
    text = font.render(data.timertime2, True, black)
    textRect = text.get_rect(center = (data.startX0 + 500, 45))
    screen.blit(text, textRect)

def pauseScreen(screen): # pull out the pause screen
    s = pygame.Surface((700,700))  # the size of your rect
    s.set_alpha(data.alpha)                # alpha level
    s.fill((0,0,0))           # this fills the entire surface
    screen.blit(s, (0,0))
    pygame.draw.rect(screen, white, [data.pauserect1, data.pauserect2, data.pauseW, data.pauseH])
    pygame.draw.rect(screen, black, [data.pauserect1 + 10, data.pauserect2 + 10, data.pauseW - 20, data.pauseH - 20])
    pygame.draw.rect(screen, white, [data.pauserect1 + 20, data.pauserect2 + 20, data.pauseW - 40, data.pauseH - 40])
    text = data.pauseFont.render("Paused", True, black)
    textRect = text.get_rect(center = [data.pauserect1 + (data.pauseW/2), data.pauserect2 + 50])
    screen.blit(text, textRect)
    if not data.cpu:
        pygame.draw.rect(screen, data.tan1, [data.pauserect3, data.pauserect4, data.pauseW1, data.pauseH1])
        pygame.draw.rect(screen, data.tan2, [data.pauserect3, data.pauserect4 + data.margin1, data.pauseW1, data.pauseH1])
        text = data.Pfont1.render("Back to Main Menu", True, white)
        textRect = text.get_rect(center = (data.textX, data.textY))
        screen.blit(text, textRect)
        text = data.Pfont1.render("Back to Game", True, white)
        textRect = text.get_rect(center = (data.textX, data.textY + data.margin1))
        screen.blit(text, textRect)
    else:
        pygame.draw.rect(screen, data.tan1, [data.pauserect3, data.pauserect4, data.pauseW1, data.pauseH1])
        pygame.draw.rect(screen, data.tan2, [data.pauserect3, data.pauserect4 + data.margin1, data.pauseW1, data.pauseH1])
        text = data.Pfont1.render("Back to Main Menu", True, white)
        textRect = text.get_rect(center = (data.textX, data.textY))
        screen.blit(text, textRect)
        text = data.Pfont1.render("Back to Game", True, white)
        textRect = text.get_rect(center = (data.textX, data.textY + data.margin1))
        screen.blit(text, textRect)
        pygame.draw.rect(screen, data.tan3, [data.pauserect3, data.pauserect4 + data.margin1*2, data.pauseW1/4, data.pauseH1])
        pygame.draw.rect(screen, data.tan4, [data.pauserect3 + (data.pauseW1*3)/8, data.pauserect4 + data.margin1*2, data.pauseW1/4, data.pauseH1])
        pygame.draw.rect(screen, data.tan5, [data.pauserect3 + (data.pauseW1*3)/4, data.pauserect4 + data.margin1*2, data.pauseW1/4, data.pauseH1])
        text = data.Pfont1.render("Easy", True, white)
        textRect = text.get_rect(center = (data.textX - data.margin1*2, data.textY + data.margin1*2))
        screen.blit(text, textRect)
        text = data.Pfont1.render("Medium", True, white)
        textRect = text.get_rect(center = (data.textX, data.textY + data.margin1*2))
        screen.blit(text, textRect)
        text = data.Pfont1.render("Hard", True, white)
        textRect = text.get_rect(center = (data.textX + data.margin1*2, data.textY + data.margin1*2))
        screen.blit(text, textRect)
    #screen.blit(data.dark, (data.startX0, 0))
    # canvas.create_reccolor.tangle(data.pauserect1, 200, data.pauserect1 + 400, 500, fill = "yellow", width = 3, outline = "color.green")
    # canvas.create_reccolor.tangle(tdata.pauserect1 + 20, 220, data.pauserect1 + 380, 480, fill = "red", width = 0)
    # canvas.create_text(data.pauserect1 + 200, 230, font = "helvetica 26", text = "Paused!")
    # canvas.create_reccolor.tangle(data.pauserect1 + 150, 250, data.pauserect1 + 250, 300, fill = "color.brown")
    # canvas.create_text(data.pauserect1 + 200, 275, text = "Back to Main")
    # if data.cpu:
    #     canvas.create_reccolor.tangle(data.pauserect1 + 150, 375, data.pauserect1 + 250, 400, fill = "color.brown")
    #     canvas.create_text(data.pauserect1 + 200, 387, text = "CPU: Easy")
    #     canvas.create_reccolor.tangle(data.pauserect1 + 150, 425, data.pauserect1 + 250, 450, fill = "color.brown")
    #     canvas.create_text(data.pauserect1 + 200, 437, text = "CPU: Medium")
    #     canvas.create_reccolor.tangle(data.pauserect1 + 150, 475, data.pauserect1 + 250, 500, fill = "color.brown")
    #     canvas.create_text(data.pauserect1 + 200, 487, text = "CPU: Hard")

def animateScreen():
    if data.b1 >= 275:
        data.b1 -= 25
    if data.b2 >= 275:
        data.b2 -= 25
    if data.b3 >= 275:
        data.b3 -= 25
    if data.b4 >= 275:
        data.b4 -= 25

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):    
    final_lines = []
    requested_lines = string.splitlines()
    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " " 
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 
    surface = pygame.Surface(rect.size, pygame.SRCALPHA, 32) 
    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException
        accumulated_height += font.size(line)[1]
    return surface

def check(screen, text, x, y): # display check text if in check
    font = pygame.font.SysFont("impact", 27)
    text = font.render(text, True, black)
    textRect = text.get_rect(center = (x, y))
    screen.blit(text, textRect)
    
# xtRect[1] - 5, textRect[2] + 20, textRect[3] + 10])

def defineRect(x0, y0, x1, y1):
    obj = pygame.Rect(x0, y0, x1 - x0, y1 - y0)
    return obj

def redefinePics(xSize, ySize):
    data.woodLightCustom = pygame.transform.scale(data.woodLight.copy(), (xSize, ySize))
    data.woodDarkCustom = pygame.transform.scale(data.woodDark.copy(), (xSize, ySize))

def drawCustomScreen(screen):
    data.font = pygame.font.SysFont("impact", data.customFontSize)
    data.customWoodCur = pygame.transform.scale(data.customWood, (data.customSize, data.customSize))
    screen.blit(data.customWoodCur, (data.x0, data.y0))
    text = data.font.render("Welcome to Custom Mode!", True, white)
    textRect = text.get_rect(center = (data.x1 + (data.x2 - data.x1) / 2, data.y1 + data.margin))
    screen.blit(text, textRect)
    if not data.customAnim:
        pygame.draw.rect(screen, data.brown, defineRect(data.xOne, data.yOne, data.xTwo, data.yTwo))
        cx = data.xTwo
        cy = (data.yOne + (data.yTwo - data.yOne)/2)
        radius = (int)((data.yTwo - data.yOne)/2)
        pygame.draw.circle(screen, data.brown, ((int)(cx), (int)(cy)), (int)(radius), 0)
        cx = data.xOne
        cy = (data.yOne + (data.yTwo - data.yOne)/2)
        radius = (int)((data.yTwo - data.yOne)/2)
        pygame.draw.circle(screen, data.brown, ((int)(cx), (int)(cy)), (int)(radius), 0)
        text = data.font.render("Back", True, white)
        textRect = text.get_rect(center = (data.xOne + 50, data.yOne + data.margin/4))
        screen.blit(text, textRect)
        data.custommargin = data.margin + data.margin/2
        width = data.width - data.custommargin* 2
        height = data.height - data.custommargin * 2
        data.customcellWidth = (int)(width / data.cols)
        data.customcellHeight = (int)(height / data.rows)
        redefinePics(data.customcellWidth, data.customcellHeight)
        for row in range(data.rows):
            for col in range(data.cols):
                if (row + col)%2 == 1:
                    fill = data.woodLightCustom
                else:
                    fill = data.woodDarkCustom
                left = data.custommargin + data.customcellWidth * col
                top = data.custommargin + data.customcellHeight * row
                screen.blit(fill, [left, top])
        if data.text1:
            fill1 = data.gray
        else: fill1 = white
        if data.text2:
            fill2 = data.gray
        else: fill2 = white
        pygame.draw.rect(screen, fill1, defineRect(101, 30, 175, 60))
        pygame.draw.rect(screen, fill2, defineRect(275, 30, 350, 60))
        curFont = pygame.font.SysFont("impact", 14)
        text = curFont.render("Number of Rows:", True, white)
        textRect = text.get_rect(center = (50, 45))
        screen.blit(text, textRect)
        text = curFont.render("Number of Cols:", True, white)
        textRect = text.get_rect(center = (225, 45))
        screen.blit(text, textRect)
        text = curFont.render(data.text1Num, True, black)
        textRect = text.get_rect(center = (138, 45))
        screen.blit(text, textRect)
        text = curFont.render(data.text2Num, True, black)
        textRect = text.get_rect(center = (312, 45))
        screen.blit(text, textRect)
        pygame.draw.rect(screen, data.brown, defineRect(600, 30, 675, 60))
        pygame.draw.circle(screen, data.brown, (675, 45), 15)
        pygame.draw.circle(screen, data.brown, (600, 45), 15)
        pygame.draw.rect(screen, data.brown, defineRect(600, 90, 675, 120))
        pygame.draw.circle(screen, data.brown, (675, 105), 15)
        pygame.draw.circle(screen, data.brown, (600, 105), 15)
        text = curFont.render("1v1 Start", True, white)
        textRect = text.get_rect(center = (637, 45))
        screen.blit(text, textRect)
        text = curFont.render("1vCPU Start", True, white)
        textRect = text.get_rect(center = (637, 105))
        screen.blit(text, textRect)
        drawMenuPieces(screen)
        drawCustomHelp(screen)
        pygame.draw.rect(screen, black, defineRect(565, 135, 700, 560), 1)

def drawCustomHelp(screen):
    curFont = pygame.font.SysFont("impact", 10)
    text = curFont.render("Make sure to type in the rows and columns before placing pieces!", True, black)
    textRect = text.get_rect(center = (350, 125))
    screen.blit(text, textRect)
    text = curFont.render("Rows and Cols must be between 3 and 20", True, black)
    textRect = text.get_rect(center = (85, 20))
    screen.blit(text, textRect)
    text = curFont.render("Drag and drop pieces from here", True, black)
    textRect = text.get_rect(center = (500, 570))
    screen.blit(text, textRect)
    text = curFont.render("Don't forget to place 2 kings!", True, black)
    textRect = text.get_rect(center = (640, 15))
    screen.blit(text, textRect)
    curFont = pygame.font.SysFont("impact", 10)
    text = curFont.render("drag and drop here to trash", True, black)
    textRect = text.get_rect(center = (630, 150))
    screen.blit(text, textRect)
#     canvas.create_text(350, 130, text = "Make sure to type in the rows and columns before placing pieces!")
#     canvas.create_text(2, 20, text = "Rows and Cols can be between 2 and 20", anchor = W)
#     canvas.create_text(550, 200, text = """drop selected items here 
#                 to trash""", anchor = W)
#     canvas.create_text(550, 555, text = "Drag and drop pieces from here")
#     canvas.create_text(610, 20, text = "Don't forget to place 2 kings!")

def drawMenuPieces(screen):
    cellDim = 60
    xmargin = 300
    ymargin = 575
    if data.rows + data.cols < 25:
        margin = 15
        # files = data.row0
        # files1 = data.row1
    else:
        margin = 7
        # files = data.row0Size
        # files1 = data.row1Size
    files = data.row0Orig
    files1 = data.row1Orig
    for row in range(2):
        for col in range(6):
            left = xmargin + cellDim * col
            top = ymargin + cellDim * row
            right = left + cellDim
            bottom = top + cellDim
            pygame.draw.rect(screen, black, defineRect(left, top, right, bottom), 1)
            if row == 0:
                file = files[col]
                #canvas.create_image(left + cellDim/2, top + cellDim/2, image = file)
            else:
                file = files1[col]
                #canvas.create_image(left + cellDim/2, top + cellDim/2, image = file)
            screen.blit(file, (left, top))
    if data.customclick1:
        screen.blit(data.currentdrawingpiece, (data.drawpiecex - margin, data.drawpiecey - margin))
#         canvas.create_image(data.drawpiecex, data.drawpiecey, image = data.currentdrawingpiece)
    for piece in data.custompieces:
        stuff = data.custompieces[piece]
        screen.blit(piece, (stuff[0] - margin, stuff[1] - margin))
#         canvas.create_image(data.custompieces[piece][0], data.custompieces[piece][1], image = piece)