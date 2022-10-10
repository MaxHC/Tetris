from area import *
from classPiece import *
from random import *
import pygame
from pygame.locals import *
from tkinter import *
import socket


#===fenetre pour navigation===#

def tetrisStart():

    #initialisation de pygame
    pygame.init()

    info = pygame.display.Info()

    #initialisation du fond
    fenetre = pygame.display.set_mode((info.current_w,info.current_h))

    fond = pygame.image.load("images/fond.png").convert()
    fond = pygame.transform.scale(fond, (info.current_w,info.current_h))
    fenetre.blit(fond, (0,0))

    boutonJouer = pygame.image.load("images/bouton_jouer.png").convert()
    fenetre.blit(boutonJouer, (info.current_w/2.4,info.current_h/1.705))

    boutonMulti = pygame.image.load("images/bouton_multijoueur.png").convert()
    fenetre.blit(boutonMulti, (info.current_w/2.4,info.current_h/1.475))

    boutonQuitter = pygame.image.load("images/bouton_quitter.png").convert()
    fenetre.blit(boutonQuitter, (info.current_w/2.4,info.current_h/1.3))

    #ligne qui sers à actualiser
    pygame.display.flip()

    #initialisation bouton

    #centre boutons
    xPlay = (info.current_w/2.4)
    yPlay = (info.current_h/1.705)

    xMulti = (info.current_w/2.4)
    yMulti = (info.current_h/1.475)

    xQuit = (info.current_w/2.4)
    yQuit = (info.current_h/1.3)

    #place le bouton sur les images
    boutonPlay = boutonJouer.get_rect()
    boutonPlay.center = (xPlay + boutonPlay[2]/2 , yPlay + boutonPlay[3]/2)

    boutonMultiplayer = boutonMulti.get_rect()
    boutonMultiplayer.center = (xMulti + boutonMultiplayer[2]/2 , yMulti + boutonMultiplayer[3]/2)

    boutonQuit = boutonQuitter.get_rect()
    boutonQuit.center = (xQuit + boutonQuit[2]/2 , yQuit + boutonQuit[3]/2)

    #action sur les boutons
    while True :
        
        for event in pygame.event.get():
                
            if event.type == KEYDOWN :
                if event.key == K_ESCAPE :
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                xMouse, yMouse = event.pos
                if boutonPlay.collidepoint(xMouse, yMouse):
                    pygame.quit()
                    scaleGrid()
                elif boutonMultiplayer.collidepoint(xMouse, yMouse):
                    selectHost()
                elif boutonQuit.collidepoint(xMouse, yMouse):
                    pygame.quit()
                    sys.exit()
#===fin de la fenetre pour navigation===#

                    
def scaleGrid(): #function to chose the height and width of the area

    window = Tk() #create window

    buttonLevel = Button(window, text="Normal", command = lambda: jouerSplit(window, 20, 10, 1), bg = 'red') #button to confirm => go to closeWindow function // use a lambda function to give argument
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

    button = Button(window, text="Confirmer", command = lambda: tetrisJouer(window, int(height.get()), int(width.get()), int(difficulty.get()))) #button to confirm => go to closeWindow function // use a lambda function to give argument
    button.grid(row = 4)

    window.mainloop()

def scaleBlock(info, area):

    height = info.current_h // area.height
    width = (info.current_w // 2) // area.width

    if(height > width):
        return width - 5
    else:
        return height - 5

def affGrid(zoneJeu, info, fenetre, piece, nextPiece, score, score2, place):

    cassePiece = pygame.image.load("images/carre_gris-fond.png").convert()
    cassePiece_1 = pygame.image.load("images/carre_bleu.png").convert()
    cassePiece_2 = pygame.image.load("images/" + piece.textures).convert()
    cassePiece_3 = pygame.image.load("images/" + nextPiece.textures).convert()
    cassePiece_4 = pygame.image.load("images/carre_noir.png").convert()
    carre_rouge = pygame.image.load("images/carre_rouge.png").convert()
    image_score = pygame.image.load("images/fenetre_score.png").convert()
    
    blockSize = scaleBlock(info, zoneJeu)

    fenetre.blit(pygame.transform.scale(image_score, (250, 60)), (info.current_w/2.5, 0))
    scoref = pygame.font.SysFont("big", 50)
    score_display = scoref.render(str("score j1: " + str(score)), 1,(255, 255, 0))
    fenetre.blit(score_display, (info.current_w/2.5, 12))
    
    if place == 2 :
        fenetre.blit(pygame.transform.scale(image_score, (250, 60)), (info.current_w/2.5,60))
        score_display2 = scoref.render(str("score j2: " + str(score2)), 1,(255, 255, 0))
        fenetre.blit(score_display2, (info.current_w/2.5, 70))


    pos_x_Piece = info.current_w/2 - (blockSize+5)*(zoneJeu.width/2)
    pos_y_Piece = info.current_h - blockSize



    for i in range(0, len(nextPiece.grid)):
        for j in range(0, len(nextPiece.grid[0])):
            if(nextPiece.grid[i][len(nextPiece.grid[0]) - (j+1)] == 1):
                fenetre.blit(pygame.transform.scale(cassePiece_3, (50,50)), (info.current_w/1.6 - (j+2)*55, i*55 + 175))

    for i in range(0, zoneJeu.height):
        for j in range(0, zoneJeu.width):


            if zoneJeu.grid[i][j] == 0 :
                fenetre.blit(pygame.transform.scale(cassePiece, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))



            if zoneJeu.grid[i][j] == 1 :
                fenetre.blit(pygame.transform.scale(cassePiece_1, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))


            if zoneJeu.grid[i][j] == 2 :

                fenetre.blit(pygame.transform.scale(cassePiece_2, (blockSize,blockSize)), (pos_x_Piece, pos_y_Piece))


            pos_x_Piece += blockSize + 5

        pos_y_Piece -= blockSize + 5

        if place == 2 :
            pos_x_Piece = 0
        else :
            pos_x_Piece = info.current_w/1.65
        pygame.display.flip()



#===========eiyfgzmiufgzmeof=========#

def jouerSplit(window, height, width, difficulty):
    window.destroy() #close tkinter window

    score = 0
    score2 = 100
    
    #initialisation de pygame
    pygame.init()
    pygame.font.init()


    info = pygame.display.Info()
    #initialisation du fond
    fenetre = pygame.display.set_mode((info.current_w,info.current_h))

    #==========image de score=======#
    image_score = pygame.image.load("images/fenetre_score.png").convert()
    fenetre.blit(pygame.transform.scale(image_score, (250, 60)), (info.current_w/2.5, 0))
    fenetre.blit(pygame.transform.scale(image_score, (250, 60)), (info.current_w/2.5,60))
  

    #ligne qui sers à actualiser
    pygame.display.flip()

    zoneJeu = Area(height, width)
    zoneJeu2 = Area(height, width)
    pieceList = createPieceList(difficulty) #set difficulty

    blockSize = scaleBlock(info, zoneJeu)
    pos_x_Piece = info.current_w/2 - (blockSize+5)*(zoneJeu.width/2)
    pos_y_Piece = info.current_h - blockSize

    #son = pygame.mixer.music.load("images/musique_in_game.wav")
    #pygame.mixer.music.play()

    currentPiece = pieceList[randint(0, len(pieceList)-1)]
    nextPiece = pieceList[randint(0, len(pieceList)-1)]

    Area.placePiece(zoneJeu, currentPiece.grid)
    Area.placePiece(zoneJeu2, currentPiece.grid)
    
    while True:

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

                if event.key == K_LEFT :

                    Area.leftDisplacement(zoneJeu)

                if event.key == K_UP or event.key == K_DOWN :

                    if event.key == K_UP:
                        direction = "left"
                    else:
                        direction = "right"
                    Area.integrateRotatedPiece(zoneJeu, currentPiece, direction)

                if event.key == K_RCTRL:
                    timer = 0

                    
            #=====joueur 2========#
                if event.key == K_d :

                    Area.rightDisplacement(zoneJeu2)

                if event.key == K_q :

                    Area.leftDisplacement(zoneJeu2)

                if event.key == K_z or event.key == K_s :

                    if event.key == K_z:
                        direction = "left"
                    else:
                        direction = "right"
                    Area.integrateRotatedPiece(zoneJeu2, currentPiece, direction)

        #=====joueur 1========#
        if (Area.tranformPieceCheck(zoneJeu)) :
            if(Area.finishGame(zoneJeu)):
                pygame.mixer.music.stop()
                tetrisEnd(score)
            n = randint(0, len(pieceList)-1)
            currentPiece = nextPiece
            nextPiece = pieceList[n]
            Area.placePiece(zoneJeu,currentPiece.grid)
            score = Area.checkLine(zoneJeu, fenetre, score, difficulty)
        #=====fin=============#
            
        #=====joueur 2========#
        if (Area.tranformPieceCheck(zoneJeu2)) :
            if(Area.finishGame(zoneJeu2)):
                pygame.mixer.music.stop()
                tetrisEnd(score)
            n = randint(0, len(pieceList)-1)
            currentPiece = nextPiece
            nextPiece = pieceList[n]
            Area.placePiece(zoneJeu2,currentPiece.grid)
            score2 = Area.checkLine(zoneJeu2, fenetre, score2, difficulty)
        #=====fin=============#
        text = "je suis le score"
        affGrid(zoneJeu, info, fenetre, currentPiece, nextPiece, score, score2, 1)
        affGrid(zoneJeu2, info, fenetre, currentPiece, nextPiece, score, score2, 2)
        Area.gravity(zoneJeu)
        Area.gravity(zoneJeu2)

        pygame.time.wait(timer)

tetrisStart()




