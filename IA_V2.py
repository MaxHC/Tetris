from area import *
from copy import copy, deepcopy

class IA_v2:

	def checkAllMove(area, piece):

		bestMove = {"score":"-10"}
		pieceTest = deepcopy(piece)

		for i in range(0, 4):

			areaTest = deepcopy(area)
			x = i

			Area.integrateRotatedPiece(areaTest, pieceTest, "left")

			for j in range(0, area.width - len(pieceTest.grid[0])+1):
				antiInfinitLoop = 0
				if(Area.findPiece(areaTest)[1] > j):
					while(Area.findPiece(areaTest)[1] != j and antiInfinitLoop < area.width):
						Area.leftDisplacement(areaTest)
						antiInfinitLoop += 1
				elif(Area.findPiece(areaTest)[1] < j):
					while(Area.findPiece(areaTest)[1] != j and antiInfinitLoop < area.width):
						Area.rightDisplacement(areaTest)
						antiInfinitLoop += 1		
			
				Area.phantomPiece(areaTest)

				thisMove = {"score":str(IA_v2.calculateMoveValue(areaTest)), "rotation":str(i), "x":str(j)}
				if((int(thisMove["score"]) > int(bestMove["score"])) or (bestMove["score"] == "-10")):
					bestMove = thisMove

		return bestMove

	def calculateMoveValue(areaTest):

		line = 20
		classic = 1
		hole = -10
		score = 0
		lower = areaTest.height
		lowerValue = -1 #lower the value is, higest the importance of lower place is (lower the block is in the grid, better the score is)

		for i in range(0, areaTest.height):
			for j in range(0, areaTest.width):
				if(areaTest.grid[i][j] == 3):
					if(i < lower):
						lower = i
					if(i == 0 or areaTest.grid[i-1] == 1): #area[i-1] can cause issue, do elif area [.... to fix it if it's happened
						score += classic
					elif(areaTest.grid[i-1][j] == 0):
						low = i-1
						while(areaTest.grid[low][j] == 0 and low >= 0):
							score += hole
							low -= 1

				score += line*IA_v2.checkLine(areaTest)
		score += lower*lowerValue

		return score

	def checkLine(areaTest):

		lineComplete = areaTest.height

		for i in range(0, areaTest.height):
			for j in range(0, areaTest.width):
				if(areaTest.grid[i][j] == 0):
					lineComplete -= 1
					break

		return lineComplete

	def move(area, piece):

		if(len(piece.grid) < len(piece.grid[0])):
			maxLen = len(piece.grid[0])
		else :
			maxLen = len(piece.grid)

		for i in range(0, maxLen):
			if(not(Area.tranformPieceCheck(area,2))):
				Area.gravity(area, 2)

		move = IA_v2.checkAllMove(area, piece)

		x = int(move["rotation"])

		for i in range(0, x+1):

			Area.integrateRotatedPiece(area, piece, "left")

		antiInfinitLoop = 0

		while(Area.findPiece(area)[1] != int(move["x"]) and antiInfinitLoop < area.width):
			coord = Area.findPiece(area)[1]
			if(coord < int(move["x"])):
				Area.rightDisplacement(area)
			elif(coord > int(move["x"])):
				Area.leftDisplacement(area)
			antiInfinitLoop += 1
