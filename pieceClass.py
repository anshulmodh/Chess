import pygame
import data

class pieces(object):

    def __init__(self, name, validMoves, x, y, row, col, player, file, moved = 0, resize = False):
        self.name = name
        self.moves = validMoves
        self.x = x
        self.moved = moved
        self.y = y
        self.row = row
        self.image = file
        self.col = col
        self.player = player
        self.resize = resize

    def copy(self): # make a copy of itself
        return pieces(self.name, self.x, self.y, self.row, self.col, self.player, self.image, self.moved)

    def setMoved(self):
        self.moved +=1
        
    def change(self, row, col):
        self.row = row
        self.col = col
        
    def getPlayer(self):
        return self.player
        
    def getResize(self):
        return self.resize
        
    def setResize(self):
        self.resize = not self.resize
        
    def getMoved(self):
        return int(self.moved)
        
    def comparePlayer(self, player):
        return str(self.player) == str(player)
    
    def getCoor(self):
        return (self.x, self.y)
    
    def getPos(self):
        return (self.row, self.col)
    
    def getMoves(self):
        return self.moves
        
    def getImage(self):
        return self.image
        
    def setImage(self, image):
        self.image = image
        
    def getName(self):
        return self.name
        
    def compareName(self, name):
        return str(self.name) == str(name)
        
    def move(self, Nx, Ny, Nrow, Ncol):
        self.y = Ny
        self.x = Nx
        self.row = Nrow
        self.col = Ncol
        
    def draw(self, screen):
        image = self.image
        imageRect = image.get_rect(center = (data.startX0 + self.x, self.y))
        screen.blit(image, imageRect)

    def getAllMoves(self): pass