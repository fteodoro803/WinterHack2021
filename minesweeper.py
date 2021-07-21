# IMPORTS
import tkinter
from tkinter import *
import re
from random import randrange


# SETUP SCREEN FUNCTIONS
def clickSelectOne2(selfButton, otherButton, buttonType, settings):  # Selects One Button among Two Buttons (If disabled, then it's selected)
    #print(f"Initial -- Self: {selfButton['state']}, Other: {otherButton['state']}")
    selfButton['state'] = tkinter.DISABLED
    otherButton['state'] = tkinter.NORMAL

    # type is if it's for Board Generation or Solve Type
    if buttonType == 'manual' or buttonType == 'automatic':
        settings['solveType'] = buttonType
    elif buttonType == 'generate' or buttonType == 'load':
        settings['generation'] = buttonType
    #print(f"After -- Self: {selfButton['state']}, Other: {otherButton['state']}")

def clickSelectDifficulty(selfButton, otherButton1, otherButton2, otherButton3, difficulty, settings):  # Selects One Button among Four Buttons (If disabled, then it's selected)
    settings['difficulty'] = difficulty

    #print(f"Initial -- Self: {selfButton['state']}, Other: {otherButton['state']}")
    selfButton['state'] = tkinter.DISABLED
    otherButton1['state'] = tkinter.NORMAL
    otherButton2['state'] = tkinter.NORMAL
    otherButton3['state'] = tkinter.NORMAL
    #print(f"After -- Self: {selfButton['state']}, Other: {otherButton['state']}")

def checkGameValidity(self, settings):
    # Checks if Bombs < Board Spaces
    boardSpaces = settings['rows'] * settings['columns']
    if settings['bombs'] > boardSpaces:
        print('Invalid Game: too many Bombs')
        return -1

    # Checks if Game is at least 3x3
    if settings['rows'] < 3 or settings['columns'] < 3:
        print('Invalid Game: too few Rows or Columns')
        return -1

    # Check if Required Buttons were Pressed

    # For Custom, check if Blanks were Filled

    # For Custom, check if Rows x Column is in correct format

    return 1

# MINESWEEPER FUNCTIONS
def applySettings(settings, customSize=0, customBombs=0):
    if settings['difficulty'] == 'easy':
        settings['rows'] = 9
        settings['columns'] = 9
        settings['bombs'] = 10
    elif settings['difficulty'] == 'medium':
        settings['rows'] = 16
        settings['columns'] = 16
        settings['bombs'] = 40
    elif settings['difficulty'] == 'hard':
        settings['rows'] = 16
        settings['columns'] = 30
        settings['bombs'] = 99
    elif settings['difficulty'] == 'custom':
        #print(f"Custom Size: {customSize.get()}, Custom Bombs: {customBombs.get()}")
        customSizeValues = re.split('x', customSize.get())  # Regex to Split by 'x'
        #print(f"Custom Board: {customSizeValues}, Custom Bombs: {customBombs.get()}")

        settings['rows'] = int(customSizeValues[0])
        settings['columns'] = int(customSizeValues[1])
        settings['bombs'] = int(customBombs.get())

def generateBoard(numRows, numColumns, numBombs):
    board = []

    # Initialise Board
    for row in range(numRows):
        emptyRow = []
        for column in range(numColumns):
            emptyRow.append(0)
        board.append(emptyRow)

    # Places Random Bombs
    coordinatesPlacedBombs = []
    numBombsPlaced = 0
    while numBombsPlaced != numBombs:
        randomRow = randrange(0, numRows)
        randomColumn = randrange(0, numColumns)
        newBomb = [randomRow, randomColumn]
        #print(f"New Bomb Location: {newBomb}")

        if newBomb not in coordinatesPlacedBombs:  # Checks if Bomb isn't there, then Places it
            board[randomRow][randomColumn] = 'B'
            coordinatesPlacedBombs.append(newBomb)

            #add adjacentBombCount to surrounding points
            # Checks Tiles Adjacent to Bomb and adds Number
            for i in range(3):
                # Row Boundaries
                rowBoundaryIndex = randomRow - 1 + i  # the -1 is to take the Above Row into Account
                if rowBoundaryIndex >= 0 and rowBoundaryIndex <= len(
                        board) - 1:  # -1 in len(board)-1 is to make sure it's within Row Boundaries
                    # print(board[selectedRow-1+i])

                    # Column Boundaries
                    for j in range(3):
                        columnBoundaryIndex = randomColumn - 1 + j
                        # print(f"Column Boundary Index: {columnBoundaryIndex}")
                        if columnBoundaryIndex >= 0 and columnBoundaryIndex <= len(board[i]) - 1:
                            #print(board[selectedRow - 1 + i][selectedColumn - 1 + j])
                            #print(f"Point {board[rowBoundaryIndex][columnBoundaryIndex]}")
                            currPoint = str(board[rowBoundaryIndex][columnBoundaryIndex])  # You could either get a num or a str, and this checks by converting fully to str
                            if currPoint.isnumeric():
                                board[rowBoundaryIndex][columnBoundaryIndex] += 1  # The Current Point is Incremented

            numBombsPlaced += 1

    # Checks Surrounding Bombs
    #numSurroundingBombs = 0
    for row in range(numRows):
        #print(f"Row: {board[row]}")
        for column in range(numColumns):
            currentPoint = board[row][column]
            #numSurroundingBombs = countBombNeighbours(board, currentPoint)

    #test, prints out the board
    # makes everything on the board a string so grid is aligned in print testing
    for i in range(numRows):
        for j in range(numColumns):
            board[i][j] = str(board[i][j])

    print('\n---------------------------------------------------------------------')
    for i in range(len(board)):
        print(board[i])
    print('---------------------------------------------------------------------')

    return 0

def addAdjacentBombCount(board, point):
    return

def displayBoard(settings):
    # Create & Configure root
    root = Tk()
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)

    # Create & Configure frame
    frame = Frame(root)
    frame.grid(row=0, column=0, sticky=N + S + E + W)

    # Creates a rows x columns grid of buttons
    for row in range(settings['rows']):
        Grid.rowconfigure(frame, row, weight=1)
        for column in range(settings['columns']):
            Grid.columnconfigure(frame, column, weight=1)
            button = Button(frame, height=1, width=2)  # create a button inside frame
            button.grid(row=row, column=column, sticky=N + S + E + W)

    root.mainloop()


# MAIN
gameSettings = {'difficulty':'EMPTY', 'rows':'EMPTY', 'columns':'EMPTY', 'bombs':'EMPTY', 'solveType':'EMPTY', 'generation':'EMPTY', 'board':'EMPTY'}
windowSettings = Tk()
windowSettings.title("Minesweeper")
windowSettings.geometry("450x300") #Size of Window

# Board Type/Difficulty
settings_BoardType = Label(windowSettings, text='Select Board Type')
settings_BoardType.grid(row=0, column=0)
settings_Difficulty = Label(windowSettings, text='Difficulty')
settings_Difficulty.grid(row=1, column=1)
settings_Size = Label(windowSettings, text='Size')
settings_Size.grid(row=1, column=2)
settings_Bombs = Label(windowSettings, text='Bombs')
settings_Bombs.grid(row=1, column=3)

settings_Easy = Button(windowSettings, text='Easy', command=lambda: clickSelectDifficulty(settings_Easy, settings_Medium, settings_Hard, settings_Custom, 'easy', gameSettings))
settings_Easy.grid(row=2, column=1)
settings_EasySize = Label(windowSettings, text='9x9')
settings_EasySize.grid(row=2, column=2)
settings_EasyBombs = Label(windowSettings, text='10')
settings_EasyBombs.grid(row=2, column=3)

settings_Medium = Button(windowSettings, text='Medium', command=lambda: clickSelectDifficulty(settings_Medium, settings_Easy, settings_Hard, settings_Custom, 'medium', gameSettings))
settings_Medium.grid(row=3, column=1)
settings_MediumSize = Label(windowSettings, text='16x16')
settings_MediumSize.grid(row=3, column=2)
settings_MediumBombs = Label(windowSettings, text='40')
settings_MediumBombs.grid(row=3, column=3)

settings_Hard = Button(windowSettings, text='Hard', command=lambda: clickSelectDifficulty(settings_Hard, settings_Medium, settings_Easy, settings_Custom, 'hard', gameSettings))
settings_Hard.grid(row=4, column=1)
settings_HardSize = Label(windowSettings, text='16x30')
settings_HardSize.grid(row=4, column=2)
settings_HardBombs = Label(windowSettings, text='99')
settings_HardBombs.grid(row=4, column=3)

settings_Custom = Button(windowSettings, text='Custom', command=lambda: clickSelectDifficulty(settings_Custom, settings_Medium, settings_Hard, settings_Easy, 'custom', gameSettings))
settings_Custom.grid(row=5, column=1)
settings_CustomSize = tkinter.Entry(windowSettings)
settings_CustomSize.grid(row=5, column=2)
settings_CustomBombs = tkinter.Entry(windowSettings)
settings_CustomBombs.grid(row=5, column=3)

# Solver Mode
settings_SolveType = Label(windowSettings, text='Select Solve Type')
settings_SolveType.grid(row=6, column=0)
settings_Manual = Button(windowSettings, text='Manual', command=lambda: clickSelectOne2(settings_Manual, settings_Automatic, 'manual', gameSettings))
settings_Manual.grid(row=7, column=1)
settings_Automatic = Button(windowSettings, text='Automatic', command=lambda: clickSelectOne2(settings_Automatic, settings_Manual, 'automatic', gameSettings))
settings_Automatic.grid(row=7, column=2)

# Board Generation
settings_Board = Label(windowSettings, text=f"Minesweeper Board \n(Default is 'Generate')")
settings_Board.grid(row=8, column=0)
settings_Generate = Button(windowSettings, text='Generate', command=lambda: clickSelectOne2(settings_Generate, settings_Load, 'generate', gameSettings))
settings_Generate.grid(row=9, column=1)
settings_Load = Button(windowSettings, text='Load', command=lambda: clickSelectOne2(settings_Load, settings_Generate, 'load', gameSettings)) #test - add functionality for this later
settings_Load.grid(row=9, column=2)

settings_ApplySettings = Button(windowSettings, text='Apply Settings', command=lambda:applySettings(gameSettings))
settings_Start = Button(windowSettings, text='Start', command=lambda:minesweeper(windowSettings, gameSettings, settings_Custom, settings_CustomSize, settings_CustomBombs))
settings_Start.grid(row=10, column=3)


def minesweeper(self, settings, customButton, customSize, customBombs):  # Minesweeper Game
    print(f"Custom Button State: {customButton['state']}")
    if customButton['state'] == 'disabled':  # Checking if Custom Button Was Pressed
        applySettings(settings, customSize, customBombs)
    else:
        applySettings(settings)

    # Make Assertion that most things cant be empty
    if checkGameValidity(self, settings) == -1:
        self.destroy()
        return
    else:
        print("Valid Game")


    print(f"Settings: {settings}")
    self.destroy()
    generateBoard(settings['rows'], settings['columns'], settings['bombs'])
    displayBoard(settings)

mainloop()

"""
EXTERNAL CODE REFERENCE:
1. generateGrid() adapted from: https://stackoverflow.com/a/38809894
"""