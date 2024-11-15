import copy
from cmu_graphics import *
import math
import random
#store any legal values in dictionary
#legal values per cell
#legal values stores in a seperate 2 d list
# splash screen: helper guidlines just labels
# indication of incorrect values by back trackers
# displaying the legals
# hint, implementing the legal move, the list with less legals

def onAppStart(app):
    app.rows = 9
    app.cols = 9
    app.boardLeft = 65
    app.boardTop = 65
    app.boardWidth = 270
    app.boardHeight = 270
    app.cellBorderWidth = 1
    app.width=700;
    app.selection = (0, 0)
    app.hover =(0,0);
    app.numbers=[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]];

def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    i=0;
    j = 0;
    for r in range(len(app.numbers)):
        for c in range(len(app.numbers[0])):
            drawnumberatcell(app, app.numbers[r][c], r, c);
def onMouseMove(app, mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        app.hover = selectedCell
def onMousePress(app,mouseX,mouseY):
    r,c=getCell(app,mouseX,mouseY)
    app.selection=r,c;
def onKeyPress(app,key):
    r,c=app.selection;
    if(0<=int(key)<=9):
        app.numbers[c][r]=int(key);
    else:
        pass;
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
            #print(app.numbers[row][col])
def drawBoardBorder(app):
    # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=None, border='black',
             borderWidth=2 * app.cellBorderWidth)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if (row, col) == app.hover:
        color = 'cyan'
    elif (row, col) == app.selection and app.numbers[row][col]!=3:
        color = 'yellow'
    elif  app.numbers[row][col]==3:
        color = 'green'
    elif app.numbers[row][col]==1:
        color= 'blue'
    elif app.numbers[row][col]==2:
        color= 'red';
    else:
        color = 'white'
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)


def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)

    else:
        return None

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)
def drawnumberatcell(app,number,r,c):
    n=str(number);
    x,y=getCellSize(app);
    if(number!=0):
        drawLabel(n,r*x+app.boardLeft+0.5*x,c*y+app.boardTop+0.5*y);
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
def main():
    runApp()

# inspired by USC professor Quan Nyugen and CMU Professor David Cosbie
main()