# IMPORTS
import tkinter
from tkinter import *
import re
from random import randrange


# SETUP SCREEN FUNCTIONS
# Selects One among Two Buttons (Either)
def clickSelectOne2(self_button, other_button, button_type, settings):
    self_button['state'] = tkinter.DISABLED  # Note: disabled denotes that it has been Selected
    other_button['state'] = tkinter.NORMAL

    if button_type == 'manual' or button_type == 'automatic':
        settings['solveType'] = button_type
    elif button_type == 'generate' or button_type == 'load':
        settings['generation'] = button_type


# Selects One Button among Four Buttons (Either)
def clickSelectDifficulty(self_button, other_button_1, other_button_2, other_button_3, difficulty, settings):
    settings['difficulty'] = difficulty
    self_button['state'] = tkinter.DISABLED  # Disabled State denotes that it has been Selected
    other_button_1['state'] = tkinter.NORMAL
    other_button_2['state'] = tkinter.NORMAL
    other_button_3['state'] = tkinter.NORMAL


# Checks if Game has Valid Settings
def checkGameValidity(settings_screen, settings):
    # For Custom, check if Rows x Column is in correct format  # these seem not to be processed until filled
    # For Custom, check if Blanks were Filled

    # Checks if num Bombs < num Board Spaces
    boardSpaces = settings['rows'] * settings['columns']
    if settings['bombs'] > boardSpaces:
        print('Invalid Game: too many Bombs')
        return -1

    # Checks if Game has at least 3 Rows and Columns
    if settings['rows'] < 3 or settings['columns'] < 3:
        print('Invalid Game: too few Rows or Columns')
        return -1

    # Checks if there is at least 1 Bomb
    if settings['bombs'] <= 0:
        print('Invalid Game: too few Bombs')
        return -1

    # Check if Required Buttons were Pressed (Uncomment when Load feature is Implemented)
    """inputList = list(settings.values())
    if 'EMPTY' in inputList:
        print('Invalid Game: Not all required Settings chosen')
        return -1"""

    # Check if Valid Board(all rows and columns are of equal len, numbers are same as what would be generated when placed in bomb locations, etc, for Load feature)


    return 1


# MINESWEEPER FUNCTIONS
# Applies inputted Settings
def applySettings(settings, custom_size=0, custom_num_bombs=0):
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
        customSizeValues = re.split('x', custom_size.get())  # Regex to Split by 'x'
        settings['rows'] = int(customSizeValues[0])
        settings['columns'] = int(customSizeValues[1])
        settings['bombs'] = int(custom_num_bombs.get())


# Checks Tiles adjacent to Bomb and adds to Surrounding-Bomb Count
def incrementSurroundingBombCount(board, row, column):
    ROWCOLNUM = 3  # Max Number of Columns and Rows surrounding a Tile

    # Row Boundaries
    for currentRow in range(ROWCOLNUM):
        rowBoundaryIndex = row - 1 + currentRow  # the -1 is to take the Above Row into Account
        if 0 <= rowBoundaryIndex <= len(board) - 1:  # '-1' is to ensure it's within Game Borders

            # Column Boundaries
            for currentColumn in range(ROWCOLNUM):
                columnBoundaryIndex = column - 1 + currentColumn
                if 0 <= columnBoundaryIndex <= len(board[currentRow]) - 1:
                    currentTileValue = str(board[rowBoundaryIndex][columnBoundaryIndex])
                    if currentTileValue.isnumeric():
                        board[rowBoundaryIndex][columnBoundaryIndex] += 1  # the Current Point is Incremented


# Generates the Minesweeper Board
def generateBoard(num_rows, num_columns, num_bombs):
    board = []

    # Initialise Board
    for row in range(num_rows):
        emptyRow = []
        for column in range(num_columns):
            emptyRow.append(0)
        board.append(emptyRow)

    # Places Random Bombs
    coordinatesPlacedBombs = []
    numBombsPlaced = 0
    while numBombsPlaced != num_bombs:
        randomRow = randrange(0, num_rows)
        randomColumn = randrange(0, num_columns)
        newBomb = [randomRow, randomColumn]

        if newBomb not in coordinatesPlacedBombs:  # Checks if Bomb isn't already there, then Places it
            board[randomRow][randomColumn] = 'B'
            coordinatesPlacedBombs.append(newBomb)
            incrementSurroundingBombCount(board, randomRow, randomColumn)
            numBombsPlaced += 1

    printBoard(board)  # testing purposes

    return board


# Opens/Activates a Tile
def buttonLeftClick(coordinates, dictionary, board, window):
    global bombCounter
    currentTile = dictionary[coordinates]

    # State Changes of Tile
    if dictionary[coordinates]['state'] != 2:  # if Tile isn't marked as a Bomb
        currentTile['button']['bg'] = '#bebebe'

        value = board[coordinates[0]][coordinates[1]]
        currentTile['button']['text'] = value  # the Text of the Tile/Button

        currentTile['state'] = 0  # button is Pressed
        currentTile['button']['state'] = tkinter.DISABLED

        if board[coordinates[0]][coordinates[1]] == '0':
            clearZeroes(coordinates, dictionary, board, window)

        # Lose Condition
        elif board[coordinates[0]][coordinates[1]] == 'B':
            openLoseScreen(window)

    # Win Condition
    if bombCounter == 0:
        checkWin(dictionary, board, window)


# Marks Bomb Location
def buttonRightClick(coordinates, dictionary, board, remaining_bombs_Label, window):
    global bombCounter
    currentButton = dictionary[coordinates]

    # State Changes
    if currentButton['state'] != 0:  # Checks if Button is still Enabled
        if currentButton['button']['bg'] == 'SystemButtonFace':  # Select, note SystemButtonFace is the default Colour
            dictionary[coordinates]['button']['bg'] = 'red'
            currentButton['state'] = 2  # 2 means that it's been right-clicked
            bombCounter -= 1
        else:  # Deselect
            dictionary[coordinates]['button']['bg'] = 'SystemButtonFace'
            currentButton['state'] = 1
            bombCounter += 1

    remaining_bombs_Label['text'] = f"Bombs Remaining: {bombCounter}"  # Changes to remaining Bombs in Display

    # Win Condition
    if bombCounter == 0:
        checkWin(dictionary, board, window)


# Clears Zones without Adjacent Bombs
def clearZeroes(coordinates, dictionary, board, game_window):
    canLeft = 0  # Ability to expand leftwards
    canRight = 0  # Ability to expand rightwards
    canUp = 0  # Ability to expand upwards
    canDown = 0  # Ability to expand downwards

    # Up
    upElement = board[coordinates[0] - 1][coordinates[1]]
    if coordinates[0] - 1 >= 0:  # ensures no wrapping
        if upElement != 'B':  # checks if can go up (not a bomb)
            upElementCoordinates = (coordinates[0] - 1, coordinates[1])
            upElementState = dictionary[upElementCoordinates]['state']
            canUp = 1
            if upElementState == 1:  # button still active
                # print('expand up')
                buttonLeftClick(upElementCoordinates, dictionary, board, game_window)

    # Down
    try:  # ensures that there is a row below
        downElement = board[coordinates[0] + 1][coordinates[1]]
        if downElement != 'B':
            downElementCoordinates = (coordinates[0] + 1, coordinates[1])
            downElementState = dictionary[downElementCoordinates]['state']
            canDown = 1
            if downElementState == 1:
                # print('expand down')
                buttonLeftClick(downElementCoordinates, dictionary, board, game_window)
    except IndexError:
        pass

    # Left
    leftElement = board[coordinates[0]][coordinates[1] - 1]
    if coordinates[1] - 1 >= 0:  # ensures no wrapping
        if leftElement != 'B':
            leftElementCoordinates = (coordinates[0], coordinates[1] - 1)
            leftElementState = dictionary[leftElementCoordinates]['state']
            canLeft = 1
            if leftElementState == 1:
                # print('expand left')
                buttonLeftClick(leftElementCoordinates, dictionary, board, game_window)

    # Right
    try:  # ensures that there is a row below
        rightElement = board[coordinates[0]][coordinates[1] + 1]
        if rightElement != 'B':
            rightElementCoordinates = (coordinates[0], coordinates[1] + 1)
            rightElementState = dictionary[rightElementCoordinates]['state']
            canRight = 1
            if rightElementState == 1:
                # print('expand right')
                buttonLeftClick(rightElementCoordinates, dictionary, board, game_window)
    except IndexError:
        pass

    # Diagonals
    # Upleft
    if canUp == 1 and canLeft == 1:
        upleftElementCoordinates = (coordinates[0] - 1, coordinates[1] - 1)
        upleftElementState = dictionary[upleftElementCoordinates]['state']
        if upleftElementState == 1:
            buttonLeftClick(upleftElementCoordinates, dictionary, board, game_window)

    # Upright
    if canUp == 1 and canRight == 1:
        uprightElementCoordinates = (coordinates[0] - 1, coordinates[1] + 1)
        uprightElementState = dictionary[uprightElementCoordinates]['state']
        if uprightElementState == 1:
            buttonLeftClick(uprightElementCoordinates, dictionary, board, game_window)

    # Downleft
    if canDown == 1 and canLeft == 1:
        downLeftElementCoordinates = (coordinates[0] + 1, coordinates[1] - 1)
        downleftElementState = dictionary[downLeftElementCoordinates]['state']
        if downleftElementState == 1:
            buttonLeftClick(downLeftElementCoordinates, dictionary, board, game_window)

    # Downright
    if canDown == 1 and canRight == 1:
        downRightElementCoordinates = (coordinates[0] + 1, coordinates[1] + 1)
        downRightElementState = dictionary[downRightElementCoordinates]['state']
        if downRightElementState == 1:
            buttonLeftClick(downRightElementCoordinates, dictionary, board, game_window)


# Verifies Win Condition
def checkWin(dictionary, board, game_window):
    keyList = list(dictionary.keys())
    numMarkedBombs = 0
    numSafeTiles = 0  # tiles that aren't bombs
    numTiles = len(board) * len(board[0])  # numRows = len(board); numColumns = len(board[0])

    # Counts the Tiles in 'Opened' and 'Marked' States
    for key in keyList:
        tileState = dictionary[key]['state']
        if tileState == 0:
            numSafeTiles += 1
        elif tileState == 2:
            numMarkedBombs += 1

    # Win Condition
    if numMarkedBombs + numSafeTiles == numTiles:
        openWinScreen(game_window)


# Displays the Minesweeper Board
def displayBoard(settings):
    # Creates and Configures Root
    root = Tk()
    Grid.rowconfigure(root, 0, weight=1)
    Grid.columnconfigure(root, 0, weight=1)

    # Create and Configures Frame
    frame = Frame(root)
    frame.grid(row=0, column=0, sticky=N + S + E + W)

    # Bomb Counter
    global bombCounter
    bombCounter = settings['bombs']

    # Creates a Rows x Columns Grid of Buttons
    buttonDictionary = {}

    # Attributes of each Button
    for row in range(settings['rows']):
        for column in range(settings['columns']):
            button = Button(frame, height=1, width=2, text='')
            button.bind("<Button-1>", lambda event, coord=(row, column): buttonLeftClick(coord, buttonDictionary,
                                                                                         settings['board'], root))
            button.bind("<Button-3>", lambda event, coord=(row, column): buttonRightClick(coord, buttonDictionary,
                                                                                          settings['board'],
                                                                                          bombCountLabel, root))

            coords = (row, column)
            buttonDictionary[coords] = {'button': button, 'coordinates': coords, 'state': 1}

    # Rendering each Button
    for row in range(settings['rows']):
        Grid.rowconfigure(frame, row, weight=1)
        for column in range(settings['columns']):
            Grid.columnconfigure(frame, column, weight=1)
            buttonDictionary[(row, column)]['button'].grid(row=row, column=column, sticky=N + S + E + W)
    bombCountLabel = Label(text=f"Bombs Remaining: {bombCounter}")
    bombCountLabel.grid(row=settings['rows'] + 1, column=0)


# Win Game Window
def openWinScreen(game_window):
    winScreen = Tk()
    win = Label(winScreen, text='Congratulations, you win!')
    win.grid(row=0, column=1)
    retry = Button(winScreen, text='retry', state='disabled')
    retry.grid(row=1, column=0)
    escape = Button(winScreen, text='exit', command=lambda: exitGame(game_window, winScreen))
    escape.grid(row=1, column=2)


# Loss Game Window
def openLoseScreen(game_window):
    loseScreen = Tk()
    lose = Label(loseScreen, text='Sorry, you lose :(')
    lose.grid(row=0, column=1)
    retry = Button(loseScreen, text='retry', state='disabled')
    retry.grid(row=1, column=0)
    escape = Button(loseScreen, text='exit', command=lambda: exitGame(game_window, loseScreen))
    escape.grid(row=1, column=2)


# Closes Windows
def exitGame(game_window, end_window):
    game_window.destroy()
    end_window.destroy()


# TESTING FUNCTIONS
def printBoard(board):
    # test, prints out the board
    # makes everything on the board a string so grid is aligned in print testing
    for i in range(len(board)):
        for j in range(len(board[0])):  # assumption that every row has the same amount of tiles
            board[i][j] = str(board[i][j])

    print('\n---------------------------------------------------------------------')
    for i in range(len(board)):
        print(board[i])
    print('---------------------------------------------------------------------')


# MAIN
gameSettings = {'difficulty': 'EMPTY', 'rows': 'EMPTY', 'columns': 'EMPTY', 'bombs': 'EMPTY',
                'solveType': 'EMPTY', 'generation': 'EMPTY', 'board': 'EMPTY'}

# Default Values
gameSettings['solveType'] = 'manual'
gameSettings['generation'] = 'generate'

windowSettings = Tk()
windowSettings.title("Minesweeper")
windowSettings.geometry("500x350")  # Size of Window

# Board Type/Difficulty
settings_BoardType = Label(windowSettings, text='Select Board Type')
settings_BoardType.grid(row=0, column=0)
settings_Difficulty = Label(windowSettings, text='Difficulty')
settings_Difficulty.grid(row=1, column=1)
settings_Size = Label(windowSettings, text='Size')
settings_Size.grid(row=1, column=2)
settings_Bombs = Label(windowSettings, text='Bombs')
settings_Bombs.grid(row=1, column=3)

settings_Easy = Button(windowSettings, text='Easy',
                       command=lambda: clickSelectDifficulty(settings_Easy, settings_Medium, settings_Hard,
                                                             settings_Custom, 'easy', gameSettings))
settings_Easy.grid(row=2, column=1)
settings_EasySize = Label(windowSettings, text='9x9')
settings_EasySize.grid(row=2, column=2)
settings_EasyBombs = Label(windowSettings, text='10')
settings_EasyBombs.grid(row=2, column=3)

settings_Medium = Button(windowSettings, text='Medium',
                         command=lambda: clickSelectDifficulty(settings_Medium, settings_Easy, settings_Hard,
                                                               settings_Custom, 'medium', gameSettings))
settings_Medium.grid(row=3, column=1)
settings_MediumSize = Label(windowSettings, text='16x16')
settings_MediumSize.grid(row=3, column=2)
settings_MediumBombs = Label(windowSettings, text='40')
settings_MediumBombs.grid(row=3, column=3)

settings_Hard = Button(windowSettings, text='Hard',
                       command=lambda: clickSelectDifficulty(settings_Hard, settings_Medium, settings_Easy,
                                                             settings_Custom, 'hard', gameSettings))
settings_Hard.grid(row=4, column=1)
settings_HardSize = Label(windowSettings, text='16x30')
settings_HardSize.grid(row=4, column=2)
settings_HardBombs = Label(windowSettings, text='99')
settings_HardBombs.grid(row=4, column=3)

settings_Custom = Button(windowSettings, text='Custom',
                         command=lambda: clickSelectDifficulty(settings_Custom, settings_Medium, settings_Hard,
                                                               settings_Easy, 'custom', gameSettings))
settings_Custom.grid(row=5, column=1)
settings_CustomSize = tkinter.Entry(windowSettings)
settings_CustomSize.insert(0,'3x3')
settings_CustomSize.grid(row=5, column=2)
settings_CustomBombs = tkinter.Entry(windowSettings)
settings_CustomBombs.insert(0,'3')
settings_CustomBombs.grid(row=5, column=3)

# Solver Mode
settings_SolveType = Label(windowSettings, text='Select Solve Type')
settings_SolveType.grid(row=6, column=0)
settings_Manual = Button(windowSettings, text='Manual', state='disabled',
                         command=lambda: clickSelectOne2(settings_Manual, settings_Automatic, 'manual', gameSettings))
settings_Manual.grid(row=7, column=1)
settings_Automatic = Button(windowSettings, text='Automatic',
                            command=lambda: clickSelectOne2(settings_Automatic, settings_Manual,
                                                            'automatic', gameSettings))
settings_Automatic.grid(row=7, column=2)

# Board Generation
settings_Board = Label(windowSettings, text=f"Minesweeper Board \n(Default is 'Generate')")
settings_Board.grid(row=8, column=0)
settings_Generate = Button(windowSettings, text='Generate', state='disabled',
                           command=lambda: clickSelectOne2(settings_Generate, settings_Load, 'generate', gameSettings))
settings_Generate.grid(row=9, column=1)
settings_Load = Button(windowSettings, text='Load',
                       command=lambda: clickSelectOne2(settings_Load, settings_Generate, 'load', gameSettings))
settings_Load.grid(row=9, column=2)

settings_Rules = Label(windowSettings, text=f"Custom Game Rules:\nMinimum Rows and Columns is 3\nMinimum Number of "
                                            f"Bombs is 1")
settings_Rules.grid(row=10, column=0)
settings_Start = Button(windowSettings, text='Start',
                        command=lambda: minesweeper(windowSettings, gameSettings, settings_Custom, settings_CustomSize,
                                                                                  settings_CustomBombs))
settings_Start.grid(row=20, column=3)


def minesweeper(settingsWindow, settings, customButton, customSize, customBombs):  # Minesweeper Game
    # print(f"Custom Button State: {customButton['state']}") #test
    if customButton['state'] == 'disabled':  # Checking if Custom Button Was Pressed
        applySettings(settings, customSize, customBombs)
    else:
        applySettings(settings)

    # Make Assertion that most things cant be empty
    if checkGameValidity(settingsWindow, settings) == -1:
        settingsWindow.destroy()
        return
    else:
        print("Valid Game")

    settingsWindow.destroy()
    board = generateBoard(settings['rows'], settings['columns'], settings['bombs'])
    settings['board'] = board
    #print(f"Settings: {settings}")
    displayBoard(settings)


mainloop()

"""
EXTERNAL CODE REFERENCE:
1. generateGrid() adapted from: https://stackoverflow.com/a/38809894
"""
