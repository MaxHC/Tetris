from classPiece import *
import pygame
from pygame.locals import *
from copy import copy, deepcopy

class Area:

    def __init__(self, height, width):

        self.width = width
        self.height = height
        self.grid = Area.createGrid(width, height)

    def createGrid(width, height):

        grid = []

        for i in range(0, height):
            grid += [[0]*width]
            
        return grid

    #M/A
    def placePiece(area, piece):

        middle = (((area.width -1) - len(piece[0]))//2)
        for i in range(0, len(piece)):
            for j in range(0, len(piece[i])):
                if(area.grid[area.height - (1+i)][middle + j] == 1):
                    return False
                elif(piece[i][j] == 1):
                    area.grid[area.height - (1+i)][middle + j] = 2
        return True

    def phantomPiece(area):

        Area.resetPhantom(area)

        areaCopied = deepcopy(area)

        for i in range(0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][j] == 2):
                    areaCopied.grid[i][j] = 3

        while not(Area.tranformPieceCheck(areaCopied, 3)):
            Area.gravity(areaCopied, 3)

        for i in range(0, area.height):
            for j in range(0, area.width):
                if(areaCopied.grid[i][j] == 3 and area.grid[i][j] != 2):
                    area.grid[i][j] = 3

    def resetPhantom(area):
        
        for i in range(0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][j] == 3):
                    area.grid[i][j] = 0

    #M/A            
    def gravity(area, state):

        for i in range(0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][j] == state and i > 0):
                    area.grid[i][j] = 0
                    area.grid[i-1][j] = state

    #M/A
    def leftDisplacement(area):

        for i in range(0, area.height):
            for j in range(0, area.width):
                if (j - 1 >= 0):
                    if ((area.grid[i][j] == 2 and area.grid[i][j-1] == 1) or area.grid[i][0] == 2):
                        return False

        for i in range(0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][j] == 2):
                    area.grid[i][j] = 0
                    area.grid[i][j-1] = 2

    #M/A
    def rightDisplacement(area):

        for i in range(0, area.height):
            for j in range(0, area.width):
                if (j + 1 < area.width):
                    if ((area.grid[i][j] == 2 and area.grid[i][j+1] == 1) or area.grid[i][area.width - 1] == 2):
                        return False

        for i in range(0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][area.width - (1+j)] == 2):
                    area.grid[i][area.width - (1+j)] = 0
                    area.grid[i][area.width - (j)] = 2
    
    def printGrid(area): #temp

        for i in range(0, len(area.grid)):
            for j in range(0, len(area.grid[i])):
                print(area.grid[len(area.grid) - (1+i)][j], end=" ")
            print("")

    #M/A
    def tranformPieceCheck(area, state): #check if the piece has to be transform as a inert solid

        for i in range(0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][j] == state and (i == 0 or area.grid[i-1][j] == 1)): #if reach bottom of the playable area or a solid
                    return True #to stop the function to don't do useless calculation

    def transformPiece(area):

        for i in range(0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][j] == 2):
                    area.grid[i][j] = 1

    #M/A
    def checkLine(area,fenetre, score, difficulty): #use after the tranformation of the piece
        i = 0

        while i != (area.height-1):
            if (sum(area.grid[i]) == area.width):
                Area.destroyLine(area, i)
                i -= 1 #to verify if the the new line [i] is full too
                score += ((100 * area.width)//area.height)*difficulty

                image_score = pygame.image.load("images/fenetre_score.png").convert()
                fenetre.blit(pygame.transform.scale(image_score, (300, 60)), (0, 0))
                scoref = pygame.font.SysFont("big", 50)
                score_display = scoref.render(str("score : " + str(score)), 1,(255, 255, 0))
                fenetre.blit(score_display, (30, 12))
                pygame.display.flip()
            
            i += 1

        return score

    def destroyLine(area, line):
        
        for i in range(line, area.height -1): #down all of the line over the destroyed line (don't check the highest line to don't be out of index)
            area.grid[i] = area.grid[i+1]
        area.grid[area.height -1] = [0]*area.width #set the highest line to default

    #M/A
    def integrateRotatedPiece(area, piece, direction): #direction must be "left" or "right"

        placement = Area.findPiece(area)

        if(placement):
            if((placement[1] + len(piece.grid)) < area.width and placement[0] + len(piece.grid[0]) < area.height): #is rotation is possible
                Piece.rotatePiece(piece, direction)


                #explore second time to erase the piece
                for i in range(0, area.height):
                    for j in range(0, area.width):
                        if (area.grid[i][j] == 2):
                            area.grid[i][j] = 0

                for i in range(0, len(piece.grid)):
                    for j in range(0, len(piece.grid[0])):
                        if(piece.grid[i][j] == 1):
                            area.grid[placement[0]+len(piece.grid) - i-1][placement[1]+j] = 2

    def findPiece(area):

        #explore 1 time to find the piece
        placement = []
        for j in range(0, area.width):
            for i in range(0, area.height):
                if(area.grid[i][j] == 2):
                    if(placement == []):
                        placement = [i, j]
                    elif(placement != []):
                        if(placement[0] > i):
                            placement[0] = i
        
        if(placement != []):
            return placement

    def finishGame(area) :

        for i in range (0, area.width):
            if(area.grid[area.height -2][i] == 1):
                return True

    def checkPieceChangePiece(area, newPiece):

        coord = Area.findPiece(area)
        
        i = coord[0]
        tempi = coord[0]
        while(tempi != i+len(newPiece.grid)):
            j = coord[1]
            tempj = coord[1]
            while(tempj != j+len(newPiece.grid[0])):
                if(newPiece.grid[tempi - coord[0]][tempj - coord[1]] == 1):
                    if(area.grid[tempi][tempj] == 1):
                        return False
                tempj += 1
            tempi += 1
                       
        return True
                

    def changePiece(newPiece, area):

        coord = Area.findPiece(area)

        for i in range(0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][j] == 2):
                   area.grid[i][j] = 0

        for i in range(0, len(newPiece.grid)):
            for j in range(0, len(newPiece.grid[0])):
                if(newPiece.grid[i][j] == 1):
                   area.grid[i + coord[0]][j + coord[1]] = 2


