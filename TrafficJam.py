import pygame, sys, random
from pygame.locals import *

# set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 620

# set up the board
BOARDWIDTH = 6  # number of columns in the board
BOARDHEIGHT = 6 # number of rows in the board
TILESIZE = 60

LEVELS = 5
FPS = 30
##BLANK = None

# set up the colors
DARKTURQUOISE = (3, 54, 73)
WHITE = (255, 255, 255)
DARKGRAY = (128, 128, 128)
LIGHTGRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TURQUOISE = (0, 102, 51)
AQUA = (0, 255, 255)
PURPLE = (128,  0, 128)
OLIVE = (128, 128, 0)
YELLOW = (255, 255, 0)
FUCHSIA = (255, 0, 255)
NAVY_BLUE = ( 0, 0, 128)
ORANGE = (255, 128, 0)

BGCOLOR = DARKTURQUOISE
TEXTCOLOR = LIGHTGRAY
BASICFONTSIZE = 30
TITLEFONTSIZE = BASICFONTSIZE * 5 / 4
BUTTONCOLOR = DARKGRAY

# set up the board
BOARDWIDTH = 6  # number of columns in the board
BOARDHEIGHT = 6 # number of rows in the board
TILESIZE = 60
TILECOLOR = LIGHTGRAY
BOARDCOLOR = DARKGRAY
XMARGIN = 80
YMARGIN = 180

LEVELWIDTH = 4
LEVELHEIGHT = 2

def main():
    global windowSurface, basicFont, FPSCLOCK, titleFont
       
    # set up pygame
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    windowSurface.fill(BGCOLOR)
    pygame.display.set_caption('Traffic Jam')
    basicFont = pygame.font.SysFont('freesansbold.ttf', BASICFONTSIZE)
    titleFont = pygame.font.SysFont('freesansbold.ttf', TITLEFONTSIZE)

    puzzle = "test"
    puzzlestr = "puzzles/" + puzzle + ".txt" 
    mainBoard = reedpuzzle(puzzlestr)

    title = "Traffic Jam"
    makeTitle(title, TEXTCOLOR, BGCOLOR,  XMARGIN - 20, 30)
    levelcoords = makeLevelButtons()
    mousedownx, mousedowny = 0, 0
    mouseupx, mouseupy = 0, 0
    mousebuttondown = False
    mousebuttonup = False
    hidetext = 30 * " "
    while True:
        RedCar = mainBoard.getRedCar()
        left, top = getLeftTopOfTile(7, 0)
        makeText(hidetext, RED, BGCOLOR, left, top)
        if RedCar.x == 4:
            left, top = getLeftTopOfTile(7, 0)
            makeText("You win!", RED, BGCOLOR, left, top)
        else:
            firstline = 'Get the red car out!'
            secondline = 'Cars can only be moved within a straight line along the grid.'
            makeText(firstline, TEXTCOLOR, BGCOLOR, XMARGIN - 20, 70)
            makeText(secondline, TEXTCOLOR, BGCOLOR, XMARGIN - 20, 100)
        mainBoard.drawBoard()
        checkForQuit()
        for event in pygame.event.get():
             if event.type == MOUSEBUTTONDOWN:
                  mousedownx, mousedowny = event.pos
                  mousebuttondown = True
             elif event.type == MOUSEBUTTONUP:
                  mouseupx, mouseupy = event.pos
                  mousebuttonup = True                

        
        if mousebuttondown == True and mousebuttonup == True:
            choosedTile1 = getTileAtPixel(mousedownx, mousedowny)
            choosedTile2 = getTileAtPixel(mouseupx, mouseupy)
           
            carcoordinates = mainBoard.GetCoordinates()
            if choosedTile1 in carcoordinates:
                movingcar = carcoordinates[choosedTile1]
                
                if movingcar.isValidDirect(choosedTile1, choosedTile2):
                    direction, steps = movingcar.getStep(choosedTile1, choosedTile2)
                    
                    if mainBoard.isValidStep(movingcar, direction, steps):
                        movingcar.Move(direction, steps)
                        
            elif choosedTile2 == (None, None):
                level = getLevelTileAtPixel(mouseupx, mouseupy, levelcoords)
                if level:
                    puzzle = str(level)
                    puzzlestr = "puzzles/" + puzzle + ".txt"
                    mainBoard = reedpuzzle(puzzlestr)
                 
            mousebuttondown = False
            mousebuttonup = False

                             
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()
    
def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def makeTitle(text, color, bgcolor, top, left):
     # create the Surface and Rect objects for some text.
     textSurf = titleFont.render(text, True, color, bgcolor)
     textRect = textSurf.get_rect()
     textRect.topleft = (top, left)
     windowSurface.blit(textSurf, textRect)

def makeText(text, color, bgcolor, top, left):
     # create the Surface and Rect objects for some text.
     textSurf = basicFont.render(text, True, color, bgcolor)
     textRect = textSurf.get_rect()
     textRect.topleft = (top, left)
     windowSurface.blit(textSurf, textRect)

def makeLevelButtons():
    levelleft, leveltop = getLeftTopOfTile(7, 2)
    makeText("Levels", TEXTCOLOR, BGCOLOR, levelleft, leveltop + TILESIZE / 3)
    tileborder = 4
    number = 0
    levelcoords = {}
    for j in range(LEVELHEIGHT):
        for i in range(LEVELWIDTH):
            left, top = getLeftTopOfTile(7 + i, 3 + j)
            pygame.draw.rect(windowSurface, BUTTONCOLOR, (left + tileborder, top + tileborder, TILESIZE - 2 * tileborder, TILESIZE - 2 * tileborder))
            number += 1
            textSurf = basicFont.render(str(number), True, TEXTCOLOR)
            textRect = textSurf.get_rect()
            textRect.center = left + int(TILESIZE / 2), top + int(TILESIZE / 2)
            windowSurface.blit(textSurf, textRect)
            levelcoords[(left,top)] = number
    return levelcoords
           
def getLeftTopOfTile(tileX, tileY):
     left = XMARGIN + (tileX * TILESIZE)
     top = YMARGIN + (tileY * TILESIZE)
     return (left, top)

def getTileAtPixel(x, y):
     for tileY in range(BOARDHEIGHT):
         for tileX in range(BOARDWIDTH):
             left, top = getLeftTopOfTile(tileX, tileY)
             tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
             if tileRect.collidepoint(x, y):
                 return (tileX, tileY)
     return (None, None)

def getLevelTileAtPixel(x, y, levelcoords):
    for tileY in range(3, 3 + LEVELHEIGHT):
         for tileX in range(7, 7 + LEVELWIDTH):
             left, top = getLeftTopOfTile(tileX, tileY)
             tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
             if tileRect.collidepoint(x, y):
                 return levelcoords[(left, top)]
    return None

def drawBoard():
     left, top = getLeftTopOfTile(0, 0)
     width = BOARDWIDTH * TILESIZE
     height = BOARDHEIGHT * TILESIZE
     borderwidth = 20
     tileborder = 4
     pygame.draw.rect(windowSurface, TILECOLOR, (left - borderwidth, top - borderwidth, width + 2 * borderwidth, height + 2 * borderwidth))
     pygame.draw.rect(windowSurface, BOARDCOLOR, (left - tileborder, top - tileborder, width + 2 * tileborder, height + 2 * tileborder))
     for j in range(BOARDHEIGHT):
         for i in range(BOARDWIDTH):
            pygame.draw.rect(windowSurface, TILECOLOR, (left + i * TILESIZE + tileborder, top + j * TILESIZE + tileborder, TILESIZE - 2 * tileborder, TILESIZE - 2 * tileborder)) 
     pygame.draw.rect(windowSurface, BOARDCOLOR, (left + BOARDWIDTH * TILESIZE , top + 2 * TILESIZE - tileborder, borderwidth, TILESIZE + 2 * tileborder))

def reedpuzzle(puzzle):
    cars = []
    with open(puzzle, "r") as puzzle:
        for sor in puzzle:
            c = sor.split()
            cars.append(Car(int(c[0]), int(c[1]), c[2], int(c[3]), c[4]))
    return Table(cars)

class Car(object):
    
    def __init__(self, x, y, lie, length, sign):
        """
        Stores the position datas of the car.

        (x,y): gives the position of upper left side of the car, in Descartes coordinate system.
               positive direct: x:right y:down        
        direction: gives, whether the car lie horizontally or vertically
        """
        self.x = x
        self.y = y
        self.lie = lie
        self.len = length
        self.sign = sign

    def Move(self, direction, steps):
        operator = {'f': 1 , 'b': -1}
        if self.lie == 'h':
            self.x += (operator[direction]*steps)
        elif self.lie == 'v':
            self.y += (operator[direction]*steps)

    def GetCoordinates(self):
        if self.lie == 'v':
            return[(self.x,self.y + i) for i in range(self.len)]
        elif self.lie == 'h':
            return[(self.x + i,self.y) for i in range(self.len)]

    def GetCoordinatesDict(self):
        return dict(map(lambda t:(t,self),self.GetCoordinates()))

    def GetCarColor(self):
        colors = [RED, GREEN, BLUE, TURQUOISE, AQUA, PURPLE, OLIVE, YELLOW, FUCHSIA, NAVY_BLUE, ORANGE]
        signs = ['R','A','B','C','D','E','F','G','H','I','J']
        carcolors = dict([(signs[i],colors[i]) for i in range(len(signs))])
        return carcolors[self.sign]

    def drawCar(self):
        left, top = getLeftTopOfTile(self.x, self.y)
        if self.lie == 'h':
            width, height = self.len * TILESIZE, TILESIZE
        elif self.lie == 'v':
            width, height = TILESIZE, self.len * TILESIZE
        carborder = 2
        pygame.draw.rect(windowSurface, self.GetCarColor(), (left + carborder, top + carborder, width - 2 * carborder, height - 2 * carborder))

    def isValidDirect(self, tile1, tile2):
        fixindex = {'h':1,'v':0}
        return tile1[fixindex[self.lie]] == tile2[fixindex[self.lie]]

    def getStep(self, tile1, tile2):
        movingindex = {'h':0,'v':1}
        movingcoords = map(lambda t: t[movingindex[self.lie]], self.GetCoordinates())
        if tile2[movingindex[self.lie]] > tile1[movingindex[self.lie]]:
            direction = 'f'            
            steps = tile2[movingindex[self.lie]] - max(movingcoords)
        elif tile2[movingindex[self.lie]] < tile1[movingindex[self.lie]]: 
            direction = 'b'
            steps = min(movingcoords) - tile2[movingindex[self.lie]]
        else:
            direction = 'b'
            steps = 0
        return (direction, steps)

class Table(object):
    
    def __init__(self, cars, size = 6):
        self.size = size
        self.cars = cars

    def getRedCar(self):
        return dict([(c.sign,c) for c in self.cars])['R']

    def GetCoordinates(self):
        d = {}
        for c in self.cars:
            d.update(c.GetCoordinatesDict())
        return d

    def drawBoard(self):
        drawBoard()
        for car in self.cars:
            car.drawCar()

    def isValidStep(self, c, direction, steps):
        carcoordinates = self.GetCoordinates()  
        movingcoord = {'h': c.x , 'v': c.y}
        startpos = {'f': movingcoord[c.lie] + c.len , 'b': movingcoord[c.lie] - 1}
        endpos = {'f': movingcoord[c.lie] + c.len + steps , 'b':  movingcoord[c.lie] - steps - 1}
        rangesteps = {'f': 1 , 'b': -1}
        route = range(startpos[direction] , endpos[direction] , rangesteps[direction])
        if c.lie == 'h':
             freecoordinates = map(lambda i:(i,c.y) not in carcoordinates, route)
        elif c.lie == 'v':
             freecoordinates = map(lambda i:(c.x,i) not in carcoordinates, route)
        freecoordinates.append(True)
        return reduce(lambda a, b: a and b , freecoordinates) and endpos[direction] <= self.size and endpos[direction] + 1 >= 0

   
if __name__ == '__main__':
        main()
