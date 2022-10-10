import json
from random import randint

class Piece:

    def __init__(self, item):
        self.grid = item["grid"]
        self.textures = "carre_" + str(item["textures"]) + ".png"

    def rotatePiece(piece, direction):
        
        newPiece = []
        for i in range(0, len(piece.grid[0])): #rotate array
            newPiece += [[0]*len(piece.grid)]

        if (direction == "left"):
            for i in range(0, len(piece.grid)):
                for j in range(0, len(piece.grid[0])):
                    newPiece[j][i] = piece.grid[i][len(piece.grid[0])-(j+1)]
        else:
            for i in range(0, len(piece.grid)):
                for j in range(0, len(piece.grid[0])):
                    newPiece[j][i] = piece.grid[len(piece.grid) - (i+1)][j]

        piece.grid = newPiece

def createPieceList(difficulty): #max difficulty is 2, normal and hard mode

    itemPieceList = []

    #init json
    with open('pieces.json') as pieceList:
        piece = json.load(pieceList)

    if(difficulty == 1):
        dim = 7
    else:
        dim = 11

    #create a list with the pieces
    for i in range(1, dim +1):
        pieceItem = piece[str(i)]
        itemPieceList.append(Piece(pieceItem))

    return itemPieceList
