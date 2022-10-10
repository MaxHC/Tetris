from area import *
from classPiece import *
from random import *
from IA import *
from IA_V2 import *
from hole import *
import pygame
from pygame.locals import *
from tkinter import *
import socket

#for high PPI screen
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

class Tetris:

    def scaleBlock(info, area, scaling): #function to have a block scaled on the screen

        height = info.current_h // area.height
        width = (info.current_w // scaling) // area.width

        #return the smaller value to have a perfect square and not a rectangle
        if(height > width):
            return width - 5
        else:
            return height - 5

    def affGrid(zoneJeu, info, fenetre, piece, nextPiece, score): #function to display grid on pygame

        #setup the square
        cassePiece = pygame.image.load("images/carre_gris-fond.png").convert()
        cassePiece_1 = pygame.image.load("images/carre_bleu.png").convert()
        cassePiece_2 = pygame.image.load("images/" + piece.textures).convert()
        cassePiece_3 = pygame.image.load("images/" + nextPiece.textures).convert()
        cassePiece_4 = pygame.image.load("images/carre_noir.png").convert()
        carre_rouge = pygame.image.load("images/carre_rouge.png").convert()

        blockSize = Tetris.scaleBlock(info, zoneJeu, 2) #get block size from scaling block

        scoref = pygame.font.SysFont("big", 50)
        score_display = scoref.render(str("score : " + str(score)), 1,(255, 255, 0))
        fenetre.blit(score_display, (30, 12))

        #init position of the block on the screen
        pos_x_Piece = info.current_w/2 - (blockSize+5)*(zoneJeu.width/2)
        pos_y_Piece = info.current_h - blockSize

        #display next piece
        image_droite = pygame.image.load("images/a_droite.png").convert()
        fenetre.blit(pygame.transform.scale(image_droite,(int((pos_x_Piece+(blockSize+5)*zoneJeu.width)+10),info.current_h)), (pos_x_Piece+(blockSize+5)*zoneJeu.width+10, 0))

        for i in range(0, len(nextPiece.grid)):
            for j in range(0, len(nextPiece.grid[0])):
                if(nextPiece.grid[i][len(nextPiece.grid[0]) - (j+1)] == 1):
                    fenetre.blit(pygame.transform.scale(cassePiece_3, (50,50)), (info.current_w - (j+2)*55, i*55 + 30))

        #display the grid
        for i in range(0, zoneJeu.height):
            for j in range(0, zoneJeu.width):

                if zoneJeu.grid[i][j] == 0 :
                    fenetre.blit(pygame.transform.scale(cassePiece, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))
                if zoneJeu.grid[i][j] == 1 :
                    fenetre.blit(pygame.transform.scale(cassePiece_1, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))
                if zoneJeu.grid[i][j] == 2 :
                    fenetre.blit(pygame.transform.scale(cassePiece_2, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))
                if zoneJeu.grid[i][j] == 3 :
                    fenetre.blit(pygame.transform.scale(cassePiece_4, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))

                pos_x_Piece += blockSize + 5

            pos_y_Piece -= blockSize + 5
            pos_x_Piece = info.current_w/2 - (blockSize+5)*(zoneJeu.width/2)
            pygame.display.flip()

    def scaleGrid(): #function to chose the height and width of the area using tkinter

        window = Tk() #create window

        buttonLevel = Button(window, text="Normal", command = lambda: Tetris.tetrisJouer(window, 20, 10, 1), bg = 'red') #button to confirm => go to closeWindow function // use a lambda function to give argument
        buttonLevel.grid(row=0, column=0)

        label = Label(window, text="Selectionnez la hauteur ( 10 à 30) :") #label of the entry
        label.grid(row=1, column=0)

        height = Entry(window, width="20") #entry
        height.grid(row=1, column=1)

        label = Label(window, text="Selectionnez la largeur (10 à 25) :") #label of 2sd entry
        label.grid(row=2, column=0)

        width = Entry(window, width="20") #2sd entry
        width.grid(row=2, column=1)

        label = Label(window, text="Selectionnez la difficultée (1 : facile; 2 : difficile) :") #label of 2sd entry
        label.grid(row=3, column=0)

        difficulty = Entry(window, width="20") #2sd entry
        difficulty.grid(row=3, column=1)

        button = Button(window, text="Confirmer", command = lambda: Tetris.tetrisJouer(window, int(height.get()), int(width.get()), int(difficulty.get()))) #button to confirm => go to closeWindow function // use a lambda function to give argument
        button.grid(row = 4)

        window.mainloop()

    #fonction qui defini l'écran principale pour la navigation
    def tetrisStart():

        #initialisation de pygame
        pygame.init()

        info = pygame.display.Info()

        #initialisation du fond
        fenetre = pygame.display.set_mode((info.current_w,info.current_h), FULLSCREEN)

        fond = pygame.image.load("images/fond.png").convert()
        fond = pygame.transform.scale(fond, (info.current_w,info.current_h))
        fenetre.blit(fond, (0,0))

        boutonJouer = pygame.image.load("images/bouton_jouer.png").convert()
        fenetre.blit(boutonJouer, (info.current_w/2.4,info.current_h/2))

        boutonIA = pygame.image.load("images/bouton_IA.png").convert()
        fenetre.blit(boutonIA, (info.current_w/2.4, info.current_h/1.75))

        boutonMulti = pygame.image.load("images/bouton_multijoueur.png").convert()
        fenetre.blit(boutonMulti, (info.current_w/2.4,info.current_h/1.55))

        boutonSplit = pygame.image.load("images/bouton_split.png").convert()
        fenetre.blit(boutonSplit, (info.current_w/2.4,info.current_h/1.39))

        boutonQuitter = pygame.image.load("images/bouton_quitter.png").convert()
        fenetre.blit(boutonQuitter, (info.current_w/2.4,info.current_h/1.26))

        #ligne qui sers à actualiser
        pygame.display.flip()

        #initialisation bouton

        #centre boutons
        xPlay = (info.current_w/2.4)
        yPlay = (info.current_h/2)

        xIA = (info.current_w/2.4)
        yIA = (info.current_h/1.75)

        xMulti = (info.current_w/2.4)
        yMulti = (info.current_h/1.55)

        xSplit = (info.current_w/2.4)
        ySplit = (info.current_h/1.39)

        xQuit = (info.current_w/2.4)
        yQuit = (info.current_h/1.26)

        #place le bouton sur les images
        boutonPlay = boutonJouer.get_rect()
        boutonPlay.center = (xPlay + boutonPlay[2]/2 , yPlay + boutonPlay[3]/2)

        boutonAI = boutonIA.get_rect()
        boutonAI.center = (xIA + boutonAI[2]/2 , yIA + boutonAI[3]/2)

        boutonMultiplayer = boutonMulti.get_rect()
        boutonMultiplayer.center = (xMulti + boutonMultiplayer[2]/2 , yMulti + boutonMultiplayer[3]/2)

        boutonSplitScreen = boutonSplit.get_rect()
        boutonSplitScreen.center = (xSplit + boutonSplitScreen[2]/2 , ySplit + boutonSplitScreen[3]/2)

        boutonQuit = boutonQuitter.get_rect()
        boutonQuit.center = (xQuit + boutonQuit[2]/2 , yQuit + boutonQuit[3]/2)

        #action sur les boutons
        while True :
            
            for event in pygame.event.get():
                    
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE :
                        pygame.quit()
                        #sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    xMouse, yMouse = event.pos
                    if boutonPlay.collidepoint(xMouse, yMouse):
                        pygame.quit()
                        Tetris.scaleGrid()
                    elif boutonAI.collidepoint(xMouse, yMouse):
                        pygame.quit()
                        Tetris.IASelector()
                    elif boutonMultiplayer.collidepoint(xMouse, yMouse):
                        Multi.selectHost()
                    elif boutonSplitScreen.collidepoint(xMouse, yMouse):
                        pygame.quit()
                        Split.scaleGrid()
                    elif boutonQuit.collidepoint(xMouse, yMouse):
                        pygame.quit()
                        #sys.exit()

    def tetrisJouer(window, height, width, difficulty):

        window.destroy() #close tkinter window

        #initialisation de pygame
        pygame.init()
        pygame.font.init()


        info = pygame.display.Info()
        #initialisation du fond
        fenetre = pygame.display.set_mode((info.current_w,info.current_h), FULLSCREEN)

        #ligne qui sers à actualiser
        pygame.display.flip()

        zoneJeu = Area(height, width)
        pieceList = createPieceList(difficulty) #set difficulty

        blockSize = Tetris.scaleBlock(info, zoneJeu, 2)
        pos_x_Piece = info.current_w/2 - (blockSize+5)*(zoneJeu.width/2)
        pos_y_Piece = info.current_h - blockSize

        son = pygame.mixer.music.load("images/musique_in_game.wav")
        pygame.mixer.music.play()
        #==========image de fonds=======#
        image_gauche = pygame.image.load("images/a_gauche.png").convert()
        fenetre.blit(pygame.transform.scale(image_gauche,(int(pos_x_Piece-15),int(info.current_h))), (0, 0))
        image_droite = pygame.image.load("images/a_droite.png").convert()
        fenetre.blit(pygame.transform.scale(image_droite,(int((pos_x_Piece+(blockSize+5)*zoneJeu.width)+10),info.current_h)), (pos_x_Piece+(blockSize+5)*zoneJeu.width, 0))

        #==========image de score=======#
        image_score = pygame.image.load("images/fenetre_score.png").convert()
        fenetre.blit(pygame.transform.scale(image_score, (300, 60)), (0, 0))

        #==========ligne rouge=======#
        carre_rouge = pygame.image.load("images/carre_rouge.png").convert()
        fenetre.blit(pygame.transform.scale(carre_rouge, (10, pos_y_Piece + blockSize)), (pos_x_Piece-15, 0))
        fenetre.blit(pygame.transform.scale(carre_rouge, (10, pos_y_Piece + blockSize)), (pos_x_Piece+(blockSize+5)*zoneJeu.width, 0))

        Tetris.mainLoop(zoneJeu, info, fenetre, pieceList, difficulty)

    def mainLoop(zoneJeu, info, fenetre, pieceList, difficulty):

        score = 0

        currentPiece = pieceList[randint(0, len(pieceList)-1)]
        nextPiece = pieceList[randint(0, len(pieceList)-1)]

        Area.placePiece(zoneJeu, currentPiece.grid)
        #Area.phantomPiece(zoneJeu)

        while True:

            Area.gravity(zoneJeu, 2)
            Tetris.affGrid(zoneJeu, info, fenetre, currentPiece, nextPiece, score)

            #evenements sur la fenetre
            for event in pygame.event.get():

                timer = 150

                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE :
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RIGHT :
                        Area.rightDisplacement(zoneJeu)
                        #Area.phantomPiece(zoneJeu)
                    if event.key == K_LEFT :
                        Area.leftDisplacement(zoneJeu)
                        #Area.phantomPiece(zoneJeu)
                    if event.key == K_UP or event.key == K_DOWN :
                        if event.key == K_UP:
                            direction = "left"
                        else:
                            direction = "right"
                        Area.integrateRotatedPiece(zoneJeu, currentPiece, direction)
                        #Area.phantomPiece(zoneJeu)
                    if event.key == K_LALT :
                        if(Area.checkPieceChangePiece(zoneJeu, nextPiece)):
                            currentPiece, nextPiece = nextPiece, currentPiece
                            Area.changePiece(currentPiece, zoneJeu)
                            #Area.phantomPiece(zoneJeu)
                            Tetris.affGrid(zoneJeu, info, fenetre, currentPiece, nextPiece, score)
                    if event.key == K_LCTRL:
                        timer = 0
            
            if (Area.tranformPieceCheck(zoneJeu, 2)):
                Area.transformPiece(zoneJeu)
                if(Area.finishGame(zoneJeu)):
                    pygame.mixer.music.stop()
                    Tetris.tetrisEnd(score)
                n = randint(0, len(pieceList)-1)
                currentPiece = nextPiece
                nextPiece = pieceList[n]
                if(not(Area.placePiece(zoneJeu,currentPiece.grid))):
                    Tetris.tetrisEnd(score)
                Area.placePiece(zoneJeu,currentPiece.grid)
                #Area.phantomPiece(zoneJeu)
                score = Area.checkLine(zoneJeu, fenetre, score, difficulty)
            
            pygame.time.wait(timer)

    def IASelector():

        window = Tk() #create window

        label = Label(window, text="Selectionnez la hauteur ( 10 à 30) :") #label of the entry
        label.grid(row=1, column=0)

        height = Entry(window, width="20") #entry
        height.grid(row=1, column=1)

        label = Label(window, text="Selectionnez la largeur (10 à 25) :") #label of 2sd entry
        label.grid(row=2, column=0)

        width = Entry(window, width="20") #2sd entry
        width.grid(row=2, column=1)

        label = Label(window, text="Selectionnez la difficultée (1 : facile; 2 : difficile) :") #label of 2sd entry
        label.grid(row=3, column=0)

        difficulty = Entry(window, width="20") #2sd entry
        difficulty.grid(row=3, column=1)

        button = Button(window, text="IA débile", command = lambda: Tetris.IA(window, "dumb", int(height.get()), int(width.get()), int(difficulty.get()))) #button to confirm => go to closeWindow function // use a lambda function to give argument
        button.grid(row = 4, column=0)

        button = Button(window, text="IA Intelligente", command = lambda: Tetris.IA(window, "smart", int(height.get()), int(width.get()), int(difficulty.get()))) #button to confirm => go to closeWindow function // use a lambda function to give argument
        button.grid(row = 4, column=1)

        window.mainloop()

    def IA(window, brain, height, width, difficulty): #dumb or smart stringify

        window.destroy()

        score = 0

        #initialisation de pygame
        pygame.init()
        pygame.font.init()


        info = pygame.display.Info()
        #initialisation du fond
        fenetre = pygame.display.set_mode((info.current_w,info.current_h), FULLSCREEN)

        #ligne qui sers à actualiser
        pygame.display.flip()

        zoneJeu = Area(height, width)
        pieceList = createPieceList(difficulty) #set difficulty

        blockSize = Tetris.scaleBlock(info, zoneJeu, 2)
        pos_x_Piece = info.current_w/2 - (blockSize+5)*(zoneJeu.width/2)
        pos_y_Piece = info.current_h - blockSize

        #son = pygame.mixer.music.load("images/musique_in_game.wav")
        #pygame.mixer.music.play()
        #==========image de fonds=======#
        image_gauche = pygame.image.load("images/a_gauche.png").convert()
        fenetre.blit(pygame.transform.scale(image_gauche,(int(pos_x_Piece-15),int(info.current_h))), (0, 0))
        image_droite = pygame.image.load("images/a_droite.png").convert()
        fenetre.blit(pygame.transform.scale(image_droite,(int((pos_x_Piece+(blockSize+5)*zoneJeu.width)+10),info.current_h)), (pos_x_Piece+(blockSize+5)*zoneJeu.width, 0))

        #==========image de score=======#
        image_score = pygame.image.load("images/fenetre_score.png").convert()
        fenetre.blit(pygame.transform.scale(image_score, (300, 60)), (0, 0))

        #==========ligne rouge=======#
        carre_rouge = pygame.image.load("images/carre_rouge.png").convert()
        fenetre.blit(pygame.transform.scale(carre_rouge, (10, pos_y_Piece + blockSize)), (pos_x_Piece-15, 0))
        fenetre.blit(pygame.transform.scale(carre_rouge, (10, pos_y_Piece + blockSize)), (pos_x_Piece+(blockSize+5)*zoneJeu.width, 0))

        currentPiece = pieceList[randint(0, len(pieceList)-1)]
        nextPiece = pieceList[randint(0, len(pieceList)-1)]

        Area.placePiece(zoneJeu, currentPiece.grid)
        if(brain == "dumb"):
            hole = IA.findHole(zoneJeu)
        else:
            IA_v2.move(zoneJeu, currentPiece)

        while True:

            Area.gravity(zoneJeu, 2)
            Tetris.affGrid(zoneJeu, info, fenetre, currentPiece, nextPiece, score)

            #evenements sur la fenetre
            for event in pygame.event.get():

                timer = 20
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE :
                        pygame.quit()
                        sys.exit()
            
            if(brain == "dumb"):
                IA.reachHole(hole, zoneJeu, currentPiece)

            if (Area.tranformPieceCheck(zoneJeu,2)) :
                Area.transformPiece(zoneJeu)
                if(Area.finishGame(zoneJeu)):
                    pygame.mixer.music.stop()
                    Tetris.tetrisEnd(score)
                n = randint(0, len(pieceList)-1)
                currentPiece = nextPiece
                nextPiece = pieceList[n]
                if(not(Area.placePiece(zoneJeu,currentPiece.grid))):
                    Tetris.tetrisEnd(score)
                score = Area.checkLine(zoneJeu, fenetre, score, difficulty)
                if(brain == "dumb"):
                    hole = IA.findHole(zoneJeu)
                else:
                    IA_v2.move(zoneJeu, currentPiece)
            
    def tetrisEnd(score):

        pygame.init()
        pygame.mixer.stop()
        info = pygame.display.Info()

        fenetre = pygame.display.set_mode((info.current_w,info.current_h), FULLSCREEN)

        fond = pygame.image.load("images/end.png").convert()
        fond = pygame.transform.scale(fond, (info.current_w,info.current_h))
        fenetre.blit(fond, (0,0))

        scoref = pygame.font.SysFont("big", 50)
        score_display = scoref.render(str("score final: " + str(score)), 1,(255, 255, 0))
        fenetre.blit(score_display, (info.current_w/2.5, info.current_h/2))

        font=pygame.font.Font(None, 54)
        text = font.render("Game Over !",1,(255,0,0))

        boutonRetour = pygame.image.load("images/bouton_retour.png").convert()
        fenetre.blit(boutonRetour, (info.current_w/2.5,info.current_h/1.25))

        xReturn = (info.current_w/2.5)
        yReturn = (info.current_h/1.25)

        boutonReturn = boutonRetour.get_rect()
        boutonReturn.center = (xReturn + boutonReturn[2]/2 , yReturn + boutonReturn[3]/2)

        continuer = 1

        while continuer:

            for event in pygame.event.get():
                if event.type == QUIT:
                    continuer = 0
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE :
                        Tetris.tetrisStart()
                if event.type == MOUSEBUTTONDOWN:
                        xMouse, yMouse = event.pos
                        if boutonReturn.collidepoint(xMouse, yMouse):
                            Tetris.tetrisStart()

            fenetre.blit(text, (info.current_w/2.5, info.current_h/2.5))

            pygame.display.flip()

    pygame.quit()

class Multi:

    def displayEnnemyScore(info, fenetre, score):

        image_score = pygame.image.load("images/fenetre_score.png").convert()
        fenetre.blit(pygame.transform.scale(image_score, (300, 60)), (0, 100))
        scoref = pygame.font.SysFont("big", 50)
        score_display = scoref.render(str("l'autre : " + str(score)), 1,(255, 255, 0))
        fenetre.blit(score_display, (30, 112))
        pygame.display.flip()

    def selectHost():

        #init pygame
        pygame.init()
        pygame.font.init()

        #init window
        info = pygame.display.Info()
        window = pygame.display.set_mode((info.current_w, info.current_h))

        fond = pygame.image.load("images/multi.png").convert()
        fond = pygame.transform.scale(fond, (info.current_w,info.current_h))
        window.blit(fond, (0,0))

        #init text to select the mode
        boutonCreer = pygame.image.load("images/bouton_creer.png").convert()
        window.blit(boutonCreer, (info.current_w/2,info.current_h/1.5))

        boutonRejoin = pygame.image.load("images/bouton_rejoindre.png").convert()
        window.blit(boutonRejoin, (info.current_w/2,info.current_h/1.3))

        boutonRetour = pygame.image.load("images/bouton_retour.png").convert()
        window.blit(boutonRetour, (info.current_w/2,info.current_h/1.15))

        pygame.display.flip()

        #initialisation bouton

        #centre boutons
        xCreat = (info.current_w/2)
        yCreat = (info.current_h/1.5)

        xJoin = (info.current_w/2)
        yJoin = (info.current_h/1.3)

        xReturn = (info.current_w/2)
        yReturn = (info.current_h/1.15)

        #place le bouton sur les images
        boutonCreat = boutonCreer.get_rect()
        boutonCreat.center = (xCreat + boutonCreat[2]/2 , yCreat + boutonCreat[3]/2)

        boutonJoin = boutonRejoin.get_rect()
        boutonJoin.center = (xJoin + boutonJoin[2]/2 , yJoin + boutonJoin[3]/2)

        boutonReturn = boutonRetour.get_rect()
        boutonReturn.center = (xReturn + boutonReturn[2]/2 , yReturn + boutonReturn[3]/2)


        pygame.display.flip()

        while True:
                for event in pygame.event.get():
                    if event.type == KEYDOWN :
                        if event.key == K_ESCAPE :
                            pygame.quit()
                            sys.exit()
                    if event.type == MOUSEBUTTONDOWN:
                        xMouse, yMouse = event.pos
                        if boutonCreat.collidepoint(xMouse, yMouse):
                            Multi.initHost()
                        elif boutonJoin.collidepoint(xMouse, yMouse):
                            Multi.initClient()
                        elif boutonReturn.collidepoint(xMouse, yMouse):
                            Tetris.tetrisStart()

    def initHost(): #window to select the port use for connexion by host

        window = Tk()

        label = Label(window, text="Connexion :")
        label.grid(row = 0, column = 0)

        label = Label(window, text="Entrez le port :")
        label.grid(row = 1, column = 0)

        port = Entry(window, width=20)
        port.grid(row = 1, column = 1)

        label = Label(window, text="Paramètre de votre partie :")
        label.grid(row = 2, column = 0)

        label = Label(window, text="Selectionnez la hauteur :") #label of the entry
        label.grid(row=3, column=0)

        height = Entry(window, width="20") #entry
        height.grid(row=3, column=1)

        label = Label(window, text="Selectionnez la largeur :") #label of 2sd entry
        label.grid(row=4, column=0)

        width = Entry(window, width="20") #2sd entry
        width.grid(row=4, column=1)

        label = Label(window, text="Selectionnez la difficultée (1 : facile; 2 : difficile) :") #label of 2sd entry
        label.grid(row=5, column=0)

        difficulty = Entry(window, width="20") #2sd entry
        difficulty.grid(row=5, column=1)

        button = Button(window, text="Confirmer", command = lambda: Multi.host(window, int(port.get()), [int(height.get()), int(width.get()), int(difficulty.get())]))
        button.grid(row = 6)

        window.mainloop()

    def initClient(): #window to select IP and port use by Host

        window = Tk()

        label = Label(window, text="Connexion :")
        label.grid(row = 0, column = 0)

        label = Label(window, text="Entrez l'ip :")
        label.grid(row = 1, column = 0)

        ip = Entry(window, width=20)
        ip.grid(row = 1, column = 1)

        label = Label(window, text="Entrez le port :")
        label.grid(row = 2, column = 0)

        port = Entry(window, width=20)
        port.grid(row = 2, column = 1)

        label = Label(window, text="Paramètre de votre partie :")
        label.grid(row = 3, column = 0)

        label = Label(window, text="Selectionnez la hauteur :") #label of the entry
        label.grid(row=4, column=0)

        height = Entry(window, width="20") #entry
        height.grid(row=4, column=1)

        label = Label(window, text="Selectionnez la largeur :") #label of 2sd entry
        label.grid(row=5, column=0)

        width = Entry(window, width="20") #2sd entry
        width.grid(row=5, column=1)

        label = Label(window, text="Selectionnez la difficultée (1 : facile; 2 : difficile) :") #label of 2sd entry
        label.grid(row=6, column=0)

        difficulty = Entry(window, width="20") #2sd entry
        difficulty.grid(row=6, column=1)

        button = Button(window, text="Confirmer", command = lambda: Multi.client(window, str(ip.get()) ,int(port.get()), [int(height.get()), int(width.get()), int(difficulty.get())]))
        button.grid(row = 7)

        window.mainloop()

    def host(window, port, parametre):

        window.destroy()

        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.bind(("", port))
        connexion.listen(1)
        clientConnexion, clientInfo = connexion.accept()

        scores = Multi.multiTetris(clientConnexion, parametre[0], parametre[1], parametre[2])

        clientConnexion.close()
        connexion.close()

        Tetris.tetrisEndServer(scores[0], scores[1])

    def client(window, ip, port, parametre):

        window.destroy()

        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion.connect((ip, port))
        scores = Multi.multiTetris(connexion, parametre[0], parametre[1], parametre[2])

        connexion.close()

        Tetris.tetrisEndServer(scores[0], scores[1])

    def multiTetris(connexion, height, width, difficulty):

        score = 0

        #initialisation de pygame
        pygame.init()
        pygame.font.init()


        info = pygame.display.Info()
        #initialisation du fond
        fenetre = pygame.display.set_mode((info.current_w,info.current_h), FULLSCREEN)

        image_score = pygame.image.load("images/fenetre_score.png").convert()
        fenetre.blit(pygame.transform.scale(image_score, (300, 60)), (0, 0))

        scoref = pygame.font.SysFont("big", 50)
        score_display = scoref.render(str("score : " + str(score)), 1,(255, 255, 0))
        fenetre.blit(score_display, (30, 12))

        #ligne qui sers à actualiser
        pygame.display.flip()

        zoneJeu = Area(height, width)
        pieceList = createPieceList(difficulty) #set difficulty

        currentPiece = pieceList[randint(0, len(pieceList)-1)]
        nextPiece = pieceList[randint(0, len(pieceList)-1)]

        Area.placePiece(zoneJeu, currentPiece.grid)
        Area.phantomPiece(zoneJeu)

        while True:

            Area.gravity(zoneJeu)
            Tetris.affGrid(zoneJeu, info, fenetre, currentPiece, nextPiece, score)

            #evenements sur la fenetre
            for event in pygame.event.get():
                
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE :
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RIGHT :
                        Area.rightDisplacement(zoneJeu)
                    if event.key == K_LEFT :
                        Area.leftDisplacement(zoneJeu)
                    if event.key == K_UP or event.key == K_DOWN :
                        if event.key == K_UP:
                            direction = "left"
                        else:
                            direction = "right"
                        Area.integrateRotatedPiece(zoneJeu, currentPiece, direction)
                        Area.phantomPiece(zoneJeu)
            
            if (Area.tranformPieceCheck(zoneJeu, 2)) :
                Area.transformPiece(zoneJeu)
                if(Area.finishGame(zoneJeu)):
                    while True:
                        font=pygame.font.Font(None, 54)
                        text = font.render("PERDU !",1000,(255,0,0))
                        fenetre.blit(pygame.transform.scale(text, (info.current_w//3, info.current_h//10)),(300, 300))
                        pygame.display.flip()
                        connexion.send("perdu".encode())
                        ennemyScore = connexion.recv(1024).decode()

                        if(ennemyScore == "perdu"):
                            connexion.send(str(score).encode())
                            ennemyScore = connexion.recv(1024).decode()
                            return [score, int(ennemyScore)]
                        else:
                            displayEnnemyScore(info, fenetre, ennemyScore)

                        pygame.time.wait(150)

                n = randint(0, len(pieceList)-1)
                currentPiece = nextPiece
                nextPiece = pieceList[n]
                if(not(Area.placePiece(zoneJeu,currentPiece.grid))):
                    Tetris.tetrisEnd(score)
                Area.placePiece(zoneJeu,currentPiece.grid)
                Area.phantomPiece(zoneJeu)
                score = Area.checkLine(zoneJeu, fenetre, score, difficulty)

            #send score
            connexion.send(str(score).encode())
            #receive score
            ennemyScore = connexion.recv(1024).decode()

            if (ennemyScore != "perdu"):
                displayEnnemyScore(info, fenetre, ennemyScore)

            pygame.time.wait(150)

    def tetrisEndServer(score, ennemyScore):

        pygame.init()

        info = pygame.display.Info()

        fenetre = pygame.display.set_mode((1280,720))

        scoref = pygame.font.SysFont("big", 50)
        score_display = scoref.render(str("Votre score: " + str(score)), 1,(255, 255, 0))
        fenetre.blit(score_display, (530, 500))

        scoref = pygame.font.SysFont("big", 50)
        score_display = scoref.render(str("Score de l'adversaire: " + str(ennemyScore)), 1,(255, 255, 0))
        fenetre.blit(score_display, (530, 700))

        if(score > ennemyScore):
            font=pygame.font.Font(None, 54)
            text = font.render("Vous avez gagné !",1,(255,255,255))
        elif(score == ennemyScore):
            font=pygame.font.Font(None, 54)
            text = font.render("Egalité",1,(255,255,255))
        else :
            font=pygame.font.Font(None, 54)
            text = font.render("Vous avez perdu !",1,(255,255,255))

        boutonRetour = pygame.image.load("images/bouton_quitter.png").convert()
        fenetre.blit(boutonRetour, (0,0))

        xReturn = (0)
        yReturn = (0)

        boutonReturn = boutonRetour.get_rect()
        boutonReturn.center = (xReturn + boutonReturn[2]/2 , yReturn + boutonReturn[3]/2)

        continuer = 1

        while continuer:

            for event in pygame.event.get():
                if event.type == QUIT:
                    continuer = 0
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE :
                        Tetris.tetrisStart()
                if event.type == MOUSEBUTTONDOWN:
                        xMouse, yMouse = event.pos
                        if boutonReturn.collidepoint(xMouse, yMouse):
                            Tetris.tetrisStart()

            fenetre.blit(text, (510, 360))

            pygame.display.flip()

        pygame.quit()

class Split:

    def scaleGrid(): #function to chose the height and width of the area using tkinter

        window = Tk() #create window

        buttonLevel = Button(window, text="Normal", command = lambda: Split.jouerSplit(window, 20, 10, 1), bg = 'red') #button to confirm => go to closeWindow function // use a lambda function to give argument
        buttonLevel.grid(row=0, column=0)

        label = Label(window, text="Selectionnez la hauteur ( 10 à 30) :") #label of the entry
        label.grid(row=1, column=0)

        height = Entry(window, width="20") #entry
        height.grid(row=1, column=1)

        label = Label(window, text="Selectionnez la largeur (10 à 25) :") #label of 2sd entry
        label.grid(row=2, column=0)

        width = Entry(window, width="20") #2sd entry
        width.grid(row=2, column=1)

        label = Label(window, text="Selectionnez la difficultée (1 : facile; 2 : difficile) :") #label of 2sd entry
        label.grid(row=3, column=0)

        difficulty = Entry(window, width="20") #2sd entry
        difficulty.grid(row=3, column=1)

        button = Button(window, text="Confirmer", command = lambda: Split.jouerSplit(window, int(height.get()), int(width.get()), int(difficulty.get()))) #button to confirm => go to closeWindow function // use a lambda function to give argument
        button.grid(row = 4)

        window.mainloop()

    def affGrid(zoneJeu, info, fenetre, piece, nextPiece, score, score2, place):

        cassePiece = pygame.image.load("images/carre_gris-fond.png").convert()
        cassePiece_1 = pygame.image.load("images/carre_bleu.png").convert()
        cassePiece_2 = pygame.image.load("images/" + piece.textures).convert()
        cassePiece_3 = pygame.image.load("images/" + nextPiece.textures).convert()
        cassePiece_4 = pygame.image.load("images/carre_noir.png").convert()
        carre_rouge = pygame.image.load("images/carre_rouge.png").convert()
        image_score = pygame.image.load("images/fenetre_score.png").convert()
        
        blockSize = Tetris.scaleBlock(info, zoneJeu, 3)

        fenetre.blit(pygame.transform.scale(image_score, (250, 60)), (info.current_w/2.5, 0))
        scoref = pygame.font.SysFont("big", 50)
        score_display = scoref.render(str("score j1: " + str(score)), 1,(255, 255, 0))
        fenetre.blit(score_display, (info.current_w/2.5, 12))
        
        if place == 2 :
            fenetre.blit(pygame.transform.scale(image_score, (250, 60)), (info.current_w/2.5,60))
            score_display2 = scoref.render(str("score j2: " + str(score2)), 1,(255, 255, 0))
            fenetre.blit(score_display2, (info.current_w/2.5, 70))


        if place == 2 :
            pos_x_Piece = info.current_w/20
        else :
            pos_x_Piece = info.current_w/3*2
            
        pygame.display.flip()

        pos_y_Piece = info.current_h - blockSize

        if(place == 2):
            gap = 0
            x = info.current_w/1.65
        else:
            gap = info.current_h/1.6
            x = info.current_w/3*2
            
        for i in range(0, len(nextPiece.grid)):
            for j in range(0, len(nextPiece.grid[0])):
                if(nextPiece.grid[i][len(nextPiece.grid[0]) - (j+1)] == 1):
                    fenetre.blit(pygame.transform.scale(cassePiece_3, (50,50)), (x - (j+2)*55, i*55 + 175+gap))

        for i in range(0, zoneJeu.height):
            for j in range(0, zoneJeu.width):


                if zoneJeu.grid[i][j] == 0 :
                    fenetre.blit(pygame.transform.scale(cassePiece, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))
                if zoneJeu.grid[i][j] == 1 :
                    fenetre.blit(pygame.transform.scale(cassePiece_1, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))
                if zoneJeu.grid[i][j] == 2 :
                    fenetre.blit(pygame.transform.scale(cassePiece_2, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))
                if zoneJeu.grid[i][j] == 3 :
                    fenetre.blit(pygame.transform.scale(cassePiece_4, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))

                pos_x_Piece += blockSize + 5

            pos_y_Piece -= blockSize + 5

            if place == 2 :
                pos_x_Piece = info.current_w/20
            else :
                pos_x_Piece = info.current_w/3*2
            pygame.display.flip()

    def jouerSplit(window, height, width, difficulty):

        window.destroy() #close tkinter window

        score = 0
        score2 = 0
        
        #initialisation de pygame
        pygame.init()
        pygame.font.init()


        info = pygame.display.Info()
        #initialisation du fond
        fenetre = pygame.display.set_mode((info.current_w,info.current_h), FULLSCREEN)

        zoneJeu = Area(height, width)
        zoneJeu2 = Area(height, width)
        pieceList = createPieceList(difficulty) #set difficulty

        blockSize = Tetris.scaleBlock(info, zoneJeu, 3)
        pos_x_Piece = info.current_w/2 - (blockSize+5)*(zoneJeu.width/2)
        pos_y_Piece = info.current_h - blockSize

        #==========image de score=======#
        image_score = pygame.image.load("images/fenetre_score.png").convert()
        fenetre.blit(pygame.transform.scale(image_score, (250, 60)), (info.current_w/2.5, 0))
        fenetre.blit(pygame.transform.scale(image_score, (250, 60)), (info.current_w/2.5,60))

        image_split_gauche = pygame.image.load("images/gauche_split.png").convert()
        fenetre.blit(pygame.transform.scale(image_split_gauche, (int(info.current_w/20-5), info.current_h)),(0, 0))
        image_split_centre = pygame.image.load("images/centre_split.png").convert()
        fenetre.blit(pygame.transform.scale(image_split_centre, (int(info.current_w/3.5), info.current_h)),(info.current_w/20+(blockSize+5)*zoneJeu.width, 0))
        image_split_droite = pygame.image.load("images/droite_split.png").convert()
        fenetre.blit(pygame.transform.scale(image_split_droite, (int((info.current_w)-(info.current_w/3*2+(blockSize+5)*zoneJeu.width)), info.current_h)),(info.current_w/3*2+(blockSize+5)*zoneJeu.width, 0))
      

        #ligne qui sers à actualiser
        pygame.display.flip()

        #son = pygame.mixer.music.load("images/musique_in_game.wav")
        #pygame.mixer.music.play()

        currentPiece = pieceList[randint(0, len(pieceList)-1)]
        nextPiece = pieceList[randint(0, len(pieceList)-1)]
        currentPiece2 = pieceList[randint(0, len(pieceList)-1)]
        nextPiece2 = pieceList[randint(0, len(pieceList)-1)]

        Area.placePiece(zoneJeu, currentPiece.grid)
        Area.placePiece(zoneJeu2, currentPiece2.grid)
        #Area.phantomPiece(zoneJeu)
        #Area.phantomPiece(zoneJeu2)
        
        while True:

            Area.gravity(zoneJeu, 2)
            Area.gravity(zoneJeu2, 2)
            Split.affGrid(zoneJeu, info, fenetre, currentPiece, nextPiece, score, score2, 1)
            Split.affGrid(zoneJeu2, info, fenetre, currentPiece2, nextPiece2, score, score2, 2)

            #evenements sur la fenetre
            for event in pygame.event.get():

                timer = 150
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE :
                        pygame.quit()
                        sys.exit()

                #=====joueur 1========#
                    if event.key == K_RIGHT :
                        Area.rightDisplacement(zoneJeu)
                        #Area.phantomPiece(zoneJeu)
                    if event.key == K_LEFT :
                        Area.leftDisplacement(zoneJeu)
                        #Area.phantomPiece(zoneJeu)
                    if event.key == K_UP or event.key == K_DOWN :
                        if event.key == K_UP:
                            direction = "left"
                        else:
                            direction = "right"
                        Area.integrateRotatedPiece(zoneJeu, currentPiece, direction)
                        #Area.phantomPiece(zoneJeu)
                    if event.key == K_RCTRL:
                        timer = 0
 
                #=====joueur 2========#
                    if event.key == K_d :
                        Area.rightDisplacement(zoneJeu2)
                        #Area.phantomPiece(zoneJeu2)
                    if event.key == K_a :
                        Area.leftDisplacement(zoneJeu2)
                        #Area.phantomPiece(zoneJeu2)
                    if event.key == K_w or event.key == K_s :
                        if event.key == K_w:
                            direction = "left"
                        else:
                            direction = "right"
                        Area.integrateRotatedPiece(zoneJeu2, currentPiece2, direction)
                        #Area.phantomPiece(zoneJeu2)

            #=====joueur 1========#
            if (Area.tranformPieceCheck(zoneJeu, 2)):
                Area.transformPiece(zoneJeu)
                if(Area.finishGame(zoneJeu)):
                    pygame.mixer.music.stop()
                    Split.tetrisEnd(score, score2)
                n = randint(0, len(pieceList)-1)
                currentPiece = nextPiece
                nextPiece = pieceList[n]
                image_split_centre = pygame.image.load("images/centre_split.png").convert()
                fenetre.blit(pygame.transform.scale(image_split_centre, (int(info.current_w/3.5), info.current_h)),(info.current_w/20+(blockSize+5)*zoneJeu.width, 0))
                if(not(Area.placePiece(zoneJeu,currentPiece.grid))):
                    Split.tetrisEnd(score, score2)
                #Area.phantomPiece(zoneJeu)
                score = Area.checkLine(zoneJeu, fenetre, score, difficulty)
            #=====fin=============#
                
            #=====joueur 2========#
            if (Area.tranformPieceCheck(zoneJeu2, 2)):
                Area.transformPiece(zoneJeu2)
                if(Area.finishGame(zoneJeu2)):
                    pygame.mixer.music.stop()
                    Split.tetrisEnd(score, score2)
                n = randint(0, len(pieceList)-1)
                currentPiece2 = nextPiece2
                nextPiece2 = pieceList[n]
                image_split_centre = pygame.image.load("images/centre_split.png").convert()
                fenetre.blit(pygame.transform.scale(image_split_centre, (int(info.current_w/3.5), info.current_h)),(info.current_w/20+(blockSize+5)*zoneJeu.width, 0))
                if(not(Area.placePiece(zoneJeu2,currentPiece2.grid))):
                    Split.tetrisEnd(score, score2)
                #Area.phantomPiece(zoneJeu2)
                score2 = Area.checkLine(zoneJeu2, fenetre, score2, difficulty)
            #=====fin=============#

            #pygame.time.wait(timer)

    def tetrisEnd(score1, score2):

        pygame.init()
        pygame.mixer.stop()
        info = pygame.display.Info()

        fenetre = pygame.display.set_mode((info.current_w,info.current_h), FULLSCREEN)

        fond = pygame.image.load("images/end.png").convert()
        fond = pygame.transform.scale(fond, (info.current_w,info.current_h))
        fenetre.blit(fond, (0,0))

        scoref = pygame.font.SysFont("big", 50)
        score_display = scoref.render(str("score du joueur 1: " + str(score1)), 1,(255, 255, 0))
        fenetre.blit(score_display, (info.current_w/2.5, info.current_h/2.5))
        score_display = scoref.render(str("score du joueur 2: " + str(score2)), 1,(255, 255, 0))
        fenetre.blit(score_display, (info.current_w/2.5, info.current_h/2.25))
        text = scoref.render(str("Game Over !"),3,(255,0,0))
        fenetre.blit(text, (info.current_w/2.5, info.current_h/4))

        boutonRetour = pygame.image.load("images/bouton_retour.png").convert()
        fenetre.blit(boutonRetour, (info.current_w/2.5,info.current_h/1.25))

        xReturn = (info.current_w/2.5)
        yReturn = (info.current_h/1.25)

        boutonReturn = boutonRetour.get_rect()
        boutonReturn.center = (xReturn + boutonReturn[2]/2 , yReturn + boutonReturn[3]/2)

        continuer = 1

        while continuer:

            for event in pygame.event.get():
                if event.type == QUIT:
                    continuer = 0
                if event.type == KEYDOWN :
                    if event.key == K_ESCAPE :
                        Tetris.tetrisStart()
                if event.type == MOUSEBUTTONDOWN:
                        xMouse, yMouse = event.pos
                        if boutonReturn.collidepoint(xMouse, yMouse):
                            Tetris.tetrisStart()

            pygame.display.flip()

    pygame.quit()

Tetris.tetrisStart()
