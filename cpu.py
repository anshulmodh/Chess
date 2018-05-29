import data
import support as s
import gameLogic as gl

def getMoves(board, pieces): # find all possible moves in a state of the board 
    moves = []
    turn = 1
    other = data.playerTwo.p
    for piece in pieces:
        for elem in piece.getMoves():
            for dir in elem:
                temp = s.copyBoard(board)
                row, col = piece.getPos()
                row += dir[0]
                col += dir[1]
                if 0 <= row < data.rows and 0 <= col < data.cols:
                    oldRow, oldCol = piece.getPos()
                    if gl.isValidMove(row, col, piece, oldRow, oldCol, turn, temp, data.playerOne.p, other):
                        temp[row][col] = piece
                        temp[oldRow][oldCol] = None
                        moves.append(temp)
    return moves

def cpu(board): # control the chess ai functions
    if data.player1turn:
        depth = 0
        maxdepth = data.depth
        pieces = data.playerOne.p
        otherPieces = data.playerTwo.p
        moves = getMoves(board, pieces)
        move = checkStateWrapper(board, pieces, otherPieces, depth, maxdepth)
        moveCPU(move, pieces)

def checkStateWrapper(board, pieces, otherPieces, depth, maxdepth): # call the check state function with the appropriate parameters
    moves = getMoves(board, pieces)
    alpha = [None]
    beta = [None]
    state = "max"
    scores = []
    move = None
    alphaScore = None
    possibleMoves = {}
    for move in moves:
        alpha, beta = checkState(move, pieces, otherPieces, depth, maxdepth, scores, alpha, beta, state)
        possibleMoves[alpha[0]] = move
    for key in possibleMoves:
        if move == None:
            move = possibleMoves[key]
        if alphaScore == None:
            alphaScore = key
        elif key > alphaScore:
            alphaScore = key
            move = possibleMoves[key]
    return move

def checkState(board, pieces, otherPieces, depth, maxdepth, scores, alpha, beta, state): # find possible moves up to max depth and redturn min an max values
    if depth == maxdepth:
        score = getHeuristic(board, pieces, state, otherPieces, len(otherPieces))
        return score
    else:
        moves = getMoves(board, pieces)
        for move in moves:
            if state == "max":
                score = checkState(move, otherPieces, pieces, depth + 1, maxdepth, scores, alpha, beta, "min")
                if alpha[0] == None:
                    alpha[0] = score
                elif score > alpha[0]:
                    alpha[0] = score
                if alpha[0] !=None and beta[0] != None and alpha[0] >= beta[0]:
                    break
            else:
                 score = checkState(move, otherPieces, pieces, depth + 1, maxdepth, scores, alpha, beta, "max")
                 if beta[0] == None:
                     beta[0] = score
                 elif score < beta[0]:
                     beta[0] = score
                 if alpha[0] != None and beta[0] != None and beta[0] <= alpha[0]:
                     break
    if depth == 0:
        return alpha, beta
    else: return score

def getHeuristic(board, pieces, state, otherPieces, length): # get the heuristic score for a state of a board
    score = 0
    for piece in pieces:
        score += data.pieceValues[piece.getName()]
    if length > len(otherPieces):
        score += 5
    for row in range(data.rows):
        for col in range(data.cols):
            piece = board[row][col]
            if piece != None:
                if piece in pieces:
                    if row > 2:
                        score += 1
            if piece in pieces and data.board[row][col] in otherPieces:
                score += 100
    if gl.checkKing(board):
        score =  -1000
    if state == "max":
        return score
    else:
        return 0 - score

def moveCPU(move, pieces):
    for row in range(data.rows):
        for col in range(data.cols):
            piece = move[row][col]
            boardPiece = data.board[row][col]
            if piece == None and boardPiece != None and boardPiece in pieces:
                startPiece = (row, col)
            if piece != None and (boardPiece == None):
                endPiece = (row, col)
            elif piece != None and (boardPiece not in pieces) and piece in pieces:
                endPiece = (row, col)
    data.start = startPiece
    data.end = endPiece
    data.CPUXY = s.getXY(endPiece)
    data.drawCPU = True


def drawCPUMove():
    oldRow = data.start[0]
    oldCol = data.start[1]
    otherPiece = data.board[data.end[0]][data.end[1]]
    piece = data.board[oldRow][oldCol]
    if piece in data.p1:
        if piece != None:
            data.drawingpiece = piece
        if otherPiece != None and otherPiece in data.p2:
            data.p2dead.append(otherPiece)
            data.board[data.end[0]][data.end[1]] = None
            data.p2.remove(otherPiece)
        data.orgpiecex = piece.getCoor()[0]
        data.orgpiecey = piece.getCoor()[1]
        data.piecex = piece.getCoor()[0]
        data.piecey = piece.getCoor()[1]
        data.xdis = (data.CPUXY[0] - data.piecex) / 30
        data.ydis = (data.CPUXY[1] - data.piecey) / 30
        data.board[oldRow][oldCol] = None
        data.board[data.end[0]][data.end[1]] = piece
        data.moveAnim = True
    else:
        data.drawCPUagain = True
        cpu(data.board)