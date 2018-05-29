import data

class player(object):

	def __init__(self, turn, pPieces, p, dead, player):
		self.turn = turn
		self.pPieces = pPieces
		self.p = p
		self.dead = dead
		self.player = player

	def getImage(self):
		if str(self.player) == "p1":
			pawn = data.Wpawn
			bishop = data.Wbishop
			knight = data.Wknight
			rook = data.Wrook
			queen = data.Wqueen
			king = data.Wking
			return pawn, bishop, knight, rook, queen, king
		else:
			pawn = data.Bpawn
			bishop = data.Bbishop
			knight = data.Bknight
			rook = data.Brook
			queen = data.Bqueen
			king = data.Bking
			return pawn, bishop, knight, rook, queen, king

	def getPlayerData(self):
		if str(self.player) == "p1":
			piece = data.p1King
		else:
			piece = data.p2King
		return self.p, piece

	def setPlayer(self, playerTurn):
		self.turn = playerTurn