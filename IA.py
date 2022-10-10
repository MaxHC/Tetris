from area import *
from hole import *

class IA:

    def findHole(area): #prototype

        possibleHoles = []
        
        for i in range(0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][j] == 0):
                    if(IA.checkAccess(area, i, j)):
                        holeLength = IA.holeLength(area, i, j)
                        possibleHoles += [Hole(j, i, holeLength)]

            if(possibleHoles != []):
                return possibleHoles

    def holeLength(area, i, j):

        length = 0

        for x in range(j, area.width):
            if(area.grid[i][x] != 1 and IA.checkAccess(area, i, x) and x < area.width):
                length += 1
        return length

    def checkAccess(area, i, j):

        for k in range (i, area.height):
            if(area.grid[k][j] == 1):
                return False
        return True

    def reachHole(holes, area, piece):

        coordPiece = IA.findPieceFromBottom(area)
        coordHole = IA.rotatePiece(piece, holes, area)

        if(coordHole[1] < coordPiece[1]):
            n = coordPiece[1] - coordHole[1]
            for i in range (0, n):
                Area.leftDisplacement(area)
                
        elif(coordHole[1] > coordPiece[1]):
            n = coordHole[1] - coordPiece[1]
            for i in range (0, n):
                Area.rightDisplacement(area)

    def findPieceFromBottom(area):

        for i in range (0, area.height):
            for j in range(0, area.width):
                if(area.grid[i][j] == 2):
                    return [i, j]

    def rotatePiece(piece, holes, area):
        lengthPiece = [sum(piece.grid[len(piece.grid)-1]), sum(piece.grid[0]), IA.length(0, piece.grid), IA.length(len(piece.grid[0])-1, piece.grid)]
        lengthSorted = sorted(lengthPiece)

        holeSelected = IA.findBetterHole(holes, lengthSorted)
        selectedRotation = IA.selectRotation(lengthPiece, holeSelected.length)

        if(selectedRotation != 0):
            for i in range(0, 3):
                Area.gravity(area, 2)
            if(selectedRotation == 2):
                Area.integrateRotatedPiece(area, piece, "left")
            elif(selectedRotation == 3):
                Area.integrateRotatedPiece(area, piece, "right")
            else :
                Area.integrateRotatedPiece(area, piece, "right")
                Area.integrateRotatedPiece(area, piece, "right")

        return [holeSelected.y, holeSelected.x]
                

    def length(column, piece):

        sums = 0

        for i in range (0, len(piece)):
            sums += piece[i][column]

        return sums

    def findBetterHole(holes, lengths):

        #return hole with same dims
        for x in holes:
            for y in lengths:
                if(x.length == y):
                    return x

        #else return hole bigger than piece
        for x in holes:
            for y in lengths:
                if(x.length >= y):
                    return x

        #security to return at least 1 hole
        return holes[0]

    def selectRotation(lengthList, holeLength):

        for i in range(0, len(lengthList)):
            if(lengthList[i] == holeLength):
                return i
        return 0

        
        
