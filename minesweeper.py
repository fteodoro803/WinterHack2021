# IMPORTS
import tkinter
from tkinter import *
import re
from random import randrange


# SETUP SCREEN FUNCTIONS
# Selects One among Two Buttons (Either)
def clickSelectOne2(selfButton, otherButton, buttonType, settings):
    selfButton['state'] = tkinter.DISABLED  # Note: disabled denotes that it has been Selected
    otherButton['state'] = tkinter.NORMAL

    if buttonType == 'manual' or buttonType == 'automatic':
        settings['solveType'] = buttonType
    elif buttonType == 'generate' or buttonType == 'load':
        settings['generation'] = buttonType

# Selects One Button among Four Buttons (Either)
def clickSelectDifficulty(selfButton, otherButton1, otherButton2, otherButton3, difficulty, settings):
    settings['difficulty'] = difficulty
    selfButton['state'] = tkinter.DISABLED  # Disabled State denotes that it has been Selected
    otherButton1['state'] = tkinter.NORMAL
    otherButton2['state'] = tkinter.NORMAL
    otherButton3['state'] = tkinter.NORMAL

# Checks if Game has Valid Settings
def checkGameValidity(self, settings):
    # Checks if Bombs < Board Spaces
    boardSpaces = settings['rows'] * settings['columns']
    if settings['bombs'] > boardSpaces:
        print('Invalid Game: too many Bombs')
        return -1

    # Checks if Game has at least 3 Rows and Columns
    if settings['rows'] < 3 or settings['columns'] < 3:
        print('Invalid Game: too few Rows or Columns')
        return -1

    # Checks if within Upper Limit

    # Checks if there is at least 1 Bomb
    if settings['bombs'] <= 0:
        print('Invalid Game: too few Bombs')
        return -1

    # Check if Required Buttons were Pressed

    # For Custom, check if Blanks were Filled

    # For Custom, check if Rows x Column is in correct format

    # Check if Valid Board(all rows and columns are of equal len, numbers are same as what would be generated when placed in bomb locations, etc)

    return 1

# MINESWEEPER FUNCTIONS
# Applies inputted Settings
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

# Checks Tiles adjacent to Bomb and adds to Count
def incrementSurroundingBombCount(board, row, column):
    ROWCOLNUM = 3  # Max Number of Columns and Rows surrounding a Tile

    for currRow in range(ROWCOLNUM):
        # Row Boundaries
        rowBoundaryIndex = row - 1 + currRow  # the -1 is to take the Above Row into Account
        if rowBoundaryIndex >= 0 and rowBoundaryIndex <= len(board) - 1:  # -1 in len(board)-1 is to make sure it's within Row Boundaries

            # Column Boundaries
            for currColumn in range(ROWCOLNUM):
                columnBoundaryIndex = column - 1 + currColumn
                if columnBoundaryIndex >= 0 and columnBoundaryIndex <= len(board[currRow]) - 1:
                    currPoint = str(board[rowBoundaryIndex][columnBoundaryIndex])  # You could either get a num or a str, and this checks by converting fully to str
                    if currPoint.isnumeric():
                        board[rowBoundaryIndex][columnBoundaryIndex] += 1  # The Current Point is Incremented

# Generates the Minesweeper Board
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

        if newBomb not in coordinatesPlacedBombs:  # Checks if Bomb isn't already there, then Places it
            board[randomRow][randomColumn] = 'B'
            coordinatesPlacedBombs.append(newBomb)
            incrementSurroundingBombCount(board, randomRow, randomColumn)
            numBombsPlaced += 1

    printBoard(board)#test

    return 0

def buttonLeftClick(coordinates, dictionary):
    print(dictionary[coordinates])

    currButton = dictionary[coordinates]

    currButton['button']['bg'] = 'red'


    currButton['state'] = 1 # 1 denotes that it has been pressed


def buttonRightClick(coordinates, dictionary):
    dictionary[coordinates]['button']['bg'] = 'red'


# Displays the Minesweeper Board
def displayBoard(settings):
    # Creates and Configures Root
    root = Tk()
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)

    # Create and Configures Frame
    frame = Frame(root)
    frame.grid(row=0, column=0, sticky=N + S + E + W)

    # Creates a Rows x Columns Grid of Buttons
    buttonList = []  # Stores Button Locations
    buttonDictionary = {}
    #ORIGINAL IDEA
    """for row in range(settings['rows']):
        Grid.rowconfigure(frame, row, weight=1)

        for column in range(settings['columns']):
            Grid.columnconfigure(frame, column, weight=1) #original

            #button = Button(frame, height=1, width=2, text='', command=lambda coord=[row,column]: buttonLeftClick(coord))  # create a button inside frame  || future, should check where it is in the button list to correspond to a point
            button = Button(frame, height=1, width=2, text='', command=lambda coord=(row,column): buttonLeftClick(button, coord, buttonDictionary))  # create a button inside frame  || future, should check where it is in the button list to correspond to a point


            #button = Button(frame, height=1, width=2, text='', command=lambda ROW=row, COLUMN=column: buttonRightClick(button, ROW, COLUMN))  # right click test, delete

            button.grid(row=row, column=column, sticky=N + S + E + W) #original

            coords = (row, column)
            buttonDictionary[coords] = {'button':button, 'coordinates':coords, 'state':0}"""

    #NEW IDEA (SPLITTING THE BUTTON MODIFYING AND THE RENDERING)
    #modifying
    for row in range(settings['rows']):
        for column in range(settings['columns']):
            # button = Button(frame, height=1, width=2, text='', command=lambda coord=[row,column]: buttonLeftClick(coord))  # create a button inside frame  || future, should check where it is in the button list to correspond to a point
            button = Button(frame, height=1, width=2, text='',
                            command=lambda coord=(row, column): buttonLeftClick(coord,
                                                                                buttonDictionary))  # create a button inside frame  || future, should check where it is in the button list to correspond to a point

            # button = Button(frame, height=1, width=2, text='', command=lambda ROW=row, COLUMN=column: buttonRightClick(button, ROW, COLUMN))  # right click test, delete

            coords = (row, column)
            buttonDictionary[coords] = {'button': button, 'coordinates': coords, 'state': 0}

    #rendering
    for row in range(settings['rows']):
        Grid.rowconfigure(frame, row, weight=1)
        for column in range(settings['columns']):
            Grid.columnconfigure(frame, column, weight=1)  # original
            buttonDictionary[(row,column)]['button'].grid(row=row, column=column, sticky=N + S + E + W)  # original

    print(buttonDictionary)
    #root.mainloop()  #test, i think from a vid i saw it's bad to nest tkinter loops (check vid history)


# TESTING FUNCTIONS
def displaySettings():
    return
def printBoard(board):
    # test, prints out the board
    # makes everything on the board a string so grid is aligned in print testing
    for i in range(len(board)):
        for j in range(len(board[0])): # assumption that every row has the same amount of tiles
            board[i][j] = str(board[i][j])

    print('\n---------------------------------------------------------------------')
    for i in range(len(board)):
        print(board[i])
    print('---------------------------------------------------------------------')

# MAIN
gameSettings = {'difficulty':'EMPTY', 'rows':'EMPTY', 'columns':'EMPTY', 'bombs':'EMPTY', 'solveType':'EMPTY', 'generation':'EMPTY', 'board':'EMPTY'}
windowSettings = Tk()
windowSettings.title("Minesweeper")
windowSettings.geometry("500x350") #Size of Window

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

#settings_ApplySettings = Button(windowSettings, text='Apply Settings', command=lambda:applySettings(gameSettings))
settings_Rules = Label(windowSettings, text=f"Custom Game Rules:\nMinimum Rows and Columns is 3\nMinimum Number of Bombs is 1")
settings_Rules.grid(row=10, column=0)
settings_Start = Button(windowSettings, text='Start', command=lambda:minesweeper(windowSettings, gameSettings, settings_Custom, settings_CustomSize, settings_CustomBombs))
settings_Start.grid(row=20, column=3)


def minesweeper(self, settings, customButton, customSize, customBombs):  # Minesweeper Game
    print(f"Custom Button State: {customButton['state']}") #test
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


    print(f"Settings: {settings}") # test
    self.destroy()
    generateBoard(settings['rows'], settings['columns'], settings['bombs'])
    displayBoard(settings)

mainloop()

"""
EXTERNAL CODE REFERENCE:
1. generateGrid() adapted from: https://stackoverflow.com/a/38809894
"""