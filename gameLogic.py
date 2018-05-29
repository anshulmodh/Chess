import data
import support as s

def checkCastle(newrow, newcol): # check if player is castling
    if not data.board[newrow][newcol] == None:
        piece = data.board[newrow][newcol]
        oldrow, oldcol = data.board[data.drow][data.dcol].getPos()
        if data.player1turn:
            if (piece.compareName("rook")) and (piece in data.playerOne.p) and (piece.getMoved() == 0):
                if data.p1King.getMoved() == 0:
                    if checkInBetween(oldrow, oldcol, newrow, newcol, newrow - oldrow, newcol - oldcol, data.p1King, data.board):
                        if checkBoard(data.board, oldrow, oldcol, newrow, newcol):
                            return True
        else:
            if piece.compareName("rook") and piece in data.playerTwo.p and (piece.getMoved() == 0):
                if data.p2King.getMoved() == 0:
                    if checkInBetween(oldrow, oldcol, newrow, newcol, newrow - oldrow, newcol - oldcol, data.p2King, data.board):
                        if checkBoard(data.board, oldrow, oldcol, newrow, newcol):
                            return True
    return False

def checkGameOver():
    try:
        if data.p1King in data.playerOne.dead or data.p2King in data.playerTwo.dead:
            data.gameover = True
            data.checkmate = False
    except:
        data.gameover = True
        data.checkmate = False

def checking(): # check for check in the game
    if checkKing(data.board):
        data.check = True
    else:
        data.check = False  
    data.player1turn, data.player2turn = not data.player1turn, not data.player2turn
    if checkKing(data.board):
        data.check = True
    else:
        data.check = False
    data.player1turn, data.player2turn = not data.player1turn, not data.player2turn

def checkAttack(newrow, newcol, newpiece): # check if move was an attack on another piece
    if newpiece.compareName("pawn") and data.board[newrow][newcol] == None and (newrow - data.drow, newcol - data.dcol) in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
        if data.player1turn:
            piece = data.board[newrow - 1][newcol]
        else:
            piece = data.board[newrow + 1][newcol]
    elif data.board[newrow][newcol] == None: return
    else: 
        piece = data.board[newrow][newcol]
    if data.player1turn == True: player = data.playerTwo.p
    else: player = data.playerOne.p
    if piece in data.playerOne.p:
        data.playerOne.p.remove(piece)
        data.playerOne.dead.append(piece)
        data.died = True
    else:
        data.playerTwo.p.remove(piece)
        data.playerTwo.dead.append(piece)
        data.died = True
    for elem in data.board:
        if piece in elem:
            i  = elem.index(piece)
            elem.remove(piece)
            elem.insert(i, newpiece)

def drawNew(newrow, newcol, x, y): # draw new piece in current state
    if data.player1turn: player = 1
    else: player = 2
    oldRow, oldCol = data.drow, data.dcol
    for piece in data.pieces:
            if piece.getPos() == (data.drow, data.dcol):
                if isValidMove(newrow, newcol, piece, oldRow, oldCol, player, data.board, data.playerOne.p, data.playerTwo.p):
                    checkAttack(newrow, newcol, piece)
                    #resizeImages(data, data.p1dead)
                    #resizeImages(data, data.p2dead)
                    piece.move(x, y, newrow, newcol)
                    data.board[newrow][newcol] = piece
                    data.board[data.drow][data.dcol] = None
                    #checkPromotion()
                    if checkKing(data.board):
                        drawNewFromCheck(piece, oldRow, oldCol, newrow, newcol)
                    else:
                        data.click1 = False
                        data.player2turn, data.player1turn = not data.player2turn, not data.player1turn
                        data.moved = True
                else:
                    data.click1 = False
                    x, y = s.getXY((data.drow, data.dcol))
                    piece.move(x, y, data.drow, data.dcol)
                    data.died = False

def checkP(pieces):
    if len(pieces) == 1:
        if pieces[0].compareName("pawn"):
            return False
    elif len(pieces) == 0:
        return False
    return True

def drawOld(): # undraw the last piece
    for piece in data.pieces:
        if piece.getPos() == (data.drow, data.dcol):
            x, y = s.getXY((data.drow, data.dcol))
            piece.move(x, y, data.drow, data.dcol)
            data.click1 = False

def drawNewFromCheck(piece, oldRow, oldCol, newrow, newcol):
    if data.died ==True: # check and draw new piece if state is in check
        Nx, Ny = s.getXY((oldRow, oldCol))
        piece.move(Nx, Ny, oldRow, oldCol)
        data.board[newrow][newcol] = None
        data.board[data.drow][data.dcol] = piece
        if data.player1turn:
            piece1 = data.playerTwo.dead[-1]
            data.board[newrow][newcol] = piece1
            piece1.move(Nx, Ny, newrow, newcol)
            if len(data.playerOne.dead) > 0:
                data.playerTwo.dead = data.playerTwo.dead[:-1]
        else:
            piece1 = data.playerOne.dead[-1]
            data.board[newrow][newcol] = piece1
            piece1.move(Nx, Ny, newrow, newcol)
            if len(data.playerOne.dead) > 0:
                data.playerOne.dead = data.playerOne.dead[:-1]
        data.click1 = False
    else:
        Nx, Ny = s.getXY((oldRow, oldCol))
        piece.move(Nx, Ny, oldRow, oldCol)
        data.board[newrow][newcol] = None
        data.board[data.drow][data.dcol] = piece
        data.click1 = False

def changeAfterCastle(newrow, newcol): # update pieces when castling
    if newcol < data.dcol:
        newCol = data.dcol - 2
        othernewcol = newCol + 1
    else:
        newCol = data.dcol + 2
        othernewcol = newCol - 1
    piece = data.board[data.drow][data.dcol]
    data.board[data.drow][data.dcol] = None
    data.board[data.drow][newCol] = piece
    otherPiece = data.board[newrow][newcol]
    data.board[newrow][newcol] = None
    data.board[data.drow][othernewcol] = otherPiece
    x, y = s.getXY((data.drow, newCol))
    piece.move(x, y, data.drow, newCol)
    Nx, Ny = s.getXY((data.drow, othernewcol))
    otherPiece.move(Nx, Ny, data.drow, othernewcol)
    data.player2turn, data.player1turn = not data.player2turn, not data.player1turn
    data.click1 = False

def checkBoard(board, oldrow, oldcol, newrow, newcol): # make moves on board
    temp = s.copyBoard(board)
    drow = newrow - oldrow
    dcol = newcol - oldcol
    if drow < 0: dr = -1
    elif drow == 0: dr = 0
    else: dr = 1
    if dcol < 0: dc = -1
    elif dcol == 0: dc = 0
    else: dc = 1
    i = 0
    while True:
        currow = oldrow + (dr * i)
        curcol = oldcol + (dc * i)
        piece = temp[oldrow][oldcol]
        x, y = s.getXY((currow, curcol))
        piece.move(x, y, currow, curcol)
        if checkKing(temp):
            return False
        if currow == newrow and curcol == newcol:
            return True
        i += 1

def goBack(): # undo move
    for piece in data.pieces:
        if piece.getPos() == (data.drow, data.dcol):
            x, y = s.getXY((data.drow, data.dcol))
            piece.move(x, y, data.drow, data.dcol)
    data.click1 = False

def checkKing(board, row = None, col = None): # check if game is in check
    s.getKings()
    if data.player1turn: playing = 2
    else: playing = 1
    if data.player1turn:
        pieces, piece = data.playerOne.getPlayerData()
        otherPlayer, otherpiece = data.playerTwo.getPlayerData()
    else:
        pieces, piece = data.playerTwo.getPlayerData()
        otherPlayer, otherpiece = data.playerOne.getPlayerData()
    dirs = data.kingMoves
    if row == None or col == None:
        row, col = piece.getPos()
    if checkKnight(row, col, otherPlayer, piece): return True
    for dir in dirs:
        for elem in dir:
            for i in range(max(data.rows, data.cols)):
                newrow, newcol = s.getRowCol(elem, row, col, i)
                if 0 <= newrow < data.rows and 0 <= newcol < data.cols:
                    # if board[newrow][newcol] in otherPlayer:
                    #     break
                    if board[newrow][newcol] in otherPlayer: 
                        if checkOtherPlayer(newrow, newcol, row, col, board, playing):
                            return True
    return False

def checkOtherPlayer(newrow, newcol, row, col, board, player): # check pieces of the other player
    pos = board[newrow][newcol].getPos()
    if board[newrow][newcol] != None:
        piece = board[newrow][newcol]
    else: piece = None
    if piece != None:
        data.oldRow, data.oldCol = piece.getPos()
        if piece.compareName("pawn"):
            pawnDirs = [(-1, 1), (-1, -1)]
            if data.player1turn:
                drow = row - newrow
                dcol = col - newcol
                if (drow, dcol) in pawnDirs:
                    return True
            else:
                drow = newrow - row
                dcol = newcol - col
                if (drow, dcol) in pawnDirs:
                    return True
        if isValidMove(row, col, piece, data.oldRow, data.oldCol, player, board, data.playerOne.p, data.playerTwo.p):
            return True
        return False
    else: return False


def checkPawnAttack(drow, dcol, moves, newRow, newCol, board, p1, p2):
        if data.player1turn: # check if pawn is attacking
            if (board[newRow][newCol] in p2):
                return True
            elif (board[newRow - 1][newCol] in p2) and (board[newRow - 1][newCol].compareName("pawn")):
                data.enPass = True
                return True
            return False
        else:
            if (board[newRow][newCol] in p1):
                return True 
            elif (board[newRow + 1][newCol] in p1) and  (board[newRow + 1][newCol].compareName("pawn")):
                data.enPass = True
                return True
            return False
    
def checkPawn(piece, moves): # check if currernt piece is pawn and get moves
    if piece.compareName("pawn"):
        if piece.comparePlayer("p2"):
            if piece.getPos()[0] == 6:
                moves = data.pawnMovesp2First
        else:
            if piece.getPos()[0] == 1:
                moves = data.pawnMovesp1First
    return moves

def checkInBetween(oldRow, oldCol, newRow, newCol, drow, dcol, piece, board):
    if piece.compareName("knight"): return True
    if piece.compareName("pawn") and abs(drow) == 2:
        if drow < 0: dr = -1
        else: dr = 1
        if board[oldRow + dr][oldCol] != None:
            return False
        return True
    if piece.compareName("rook") or piece.compareName("bishop") or piece.compareName("queen") or piece.compareName("king"):
        if drow < 0: dr = -1
        elif drow == 0: dr = 0
        else: dr = 1
        if dcol < 0: dc = -1
        elif dcol == 0: dc = 0
        else: dc = 1
        while True:
            oldRow += dr
            oldCol += dc
            if oldRow == newRow and oldCol == newCol:
                return True
            if board[oldRow][oldCol] != None:
                return False
    else:
        return True

def isValidMove(newRow, newCol, piece, oldRow, oldCol, player, board, p1, p2):
    moves = piece.getMoves()
    moves = checkPawn(piece, moves)
    drow = newRow - oldRow
    dcol = newCol - oldCol
    if player == 1:
        if board[newRow][newCol] in p1: # check for other player
            return False
    else:
        if board[newRow][newCol] in p2:
            return False
    if piece.compareName("pawn"): # check pawn moves
        if board[newRow][newCol] != None and (drow, dcol) not in [(1, 1), (1, -1), (-1, -1), (-1, 1)]: 
            return False
        if data.player1turn == True and ((drow, dcol) not in data.pawnMovesp1Elem): 
            return False
        elif data.player2turn == True and ((drow, dcol) not in data.pawnMovesp2Elem):
            return False
        if (drow, dcol) in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
            if checkPawnAttack(drow, dcol, moves, newRow, newCol, board, p1, p2):
                return True
            return False
    for elem in moves: # check regular moves
        if (drow, dcol) in elem:
            if checkInBetween(oldRow, oldCol, newRow, newCol, drow, dcol, piece, board):
                return True
    return False

def checkPlayerPiece(): # get the player of the piece 
    if data.player2turn == True:
        for piece in data.pieces:
            if piece.getPos() == (data.drow, data.dcol):
                if piece.comparePlayer("p2"):
                    return True
        return False
    else:
        for piece in data.pieces:
            if piece.getPos() == (data.drow, data.dcol):
                if piece.comparePlayer("p1"):
                    return True
        return False

def checkPromotion(): # check for pawn promotion
    if data.player2turn:
        for piece in data.playerTwo.p:
            if piece.compareName("pawn"):
                row, col = piece.getPos()
                if row == 0:
                    data.prow = row
                    data.pcol = col
                    data.p2promote = True
                    break
                else:
                    data.p2promote = False
    else:
        for piece in data.playerOne.p:
            if piece.compareName("pawn"):
                row, col = piece.getPos()
                if row == data.rows - 1:
                    data.prow = row
                    data.pcol = col
                    data.p1promote = True
                    break
                else:
                    data.p1promote = False

def checkKnight(row, col, otherPlayer, king):
    dirs = data.knightMoves # check if knight can attack the king
    for piece in otherPlayer:
        if piece.compareName("knight"):
            row, col = piece.getPos()
            for elem in dirs:
                for dir in elem:
                    newrow = row + dir[0]
                    newcol = col + dir[1]
                    if 0 <= newrow < data.rows and 0 <= newcol < data.cols:
                        if data.board[newrow][newcol] == king:
                            return True
    return False

def checkForCheckMate(board, pieces, otherPlayer, piece, kingPos = None):
    numDirs = 0
    if pieces == data.playerOne.p: playing = 2; turn = "p1"
    else: playing = 1; turn = "p2" # check if game is in checkmate
    dirs = data.kingMoves
    if kingPos == None: 
        for row1 in range(data.rows):
            for col1 in range(data.cols):
                curPiece = board[row1][col1]
                if curPiece != None:
                    if (curPiece.compareName("king")) and (curPiece.getPlayer() == turn): 
                        row, col = row1, col1
    for dir in dirs:
        for elem in dir:
            for i in range(max(data.rows, data.cols)):
                newrow, newcol = s.getRowCol(elem, row, col, i)
                if 0 <= newrow < data.rows and 0 <= newcol < data.cols:
                    numDirs += 1
                    if board[newrow][newcol] in pieces:
                        continue
                    elif board[newrow][newcol] in otherPlayer: 
                        if checkOtherPlayer(newrow, newcol, row, col, board, playing):
                            return True
    if checkKnight(row,  col, otherPlayer, piece) and numDirs == 0: return True
    return False

def checkmate(board): # check for checkmate
    if data.player1turn:
        pieces, piece = data.playerOne.getPlayerData()
        otherPlayer, otherpiece = data.playerTwo.getPlayerData()
    else:
        pieces, piece = data.playerTwo.getPlayerData()
        otherPlayer, otherpiece = data.playerOne.getPlayerData()
    moves = s.AllPieces(board, pieces)
    for move in moves:
        if not checkForCheckMate(move, pieces, otherPlayer, piece):
            return False
            
    return True

def evaluateMoves(board, dir, piece, pieces, moves): # eval all moves
    if pieces == data.playerOne.p: turn = 1; other = data.playerTwo.p
    else: turn = 2; other = data.playerOne.p
    row, col = piece.getPos()
    row += dir[0]
    col += dir[1]
    if 0 <= row < data.rows and 0 <= col < data.cols:
        oldRow, oldCol = piece.getPos()
        if isValidMove(row, col, piece, oldRow, oldCol, turn, board, data.playerOne.p, data.playerTwo.p):
            board[row][col] = piece
            board[oldRow][oldCol] = None
            moves.append(board)
    return moves

def replace(row, col, Nx, Ny, piece, player): # replace rook and king if castling
    if player == data.playerTwo.dead: list = data.playerTwo.p
    else: list = data.playerOne.p
    player.remove(piece)
    piece.move(Nx, Ny, row, col)
    oldPiece = data.board[row][col]
    data.board[row][col] = piece
    player.append(oldPiece)
    list.append(piece)
    list.remove(oldPiece)
    # if piece.getResize():
    #     piece.setResize
    #     image = piece.getImage()
    #     image = image.zoom(2)
    #     piece.setImage(image)