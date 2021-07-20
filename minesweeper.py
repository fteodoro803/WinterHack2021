# IMPORTS
import tkinter
from tkinter import *


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
    #print(f"Initial -- Self: {selfButton['state']}, Other: {otherButton['state']}")
    selfButton['state'] = tkinter.DISABLED
    otherButton1['state'] = tkinter.NORMAL
    otherButton2['state'] = tkinter.NORMAL
    otherButton3['state'] = tkinter.NORMAL
    settings['difficulty'] = difficulty
    if difficulty == 'easy':
        settings['rows'] = 9
        settings['columns'] = 9
        settings['bombs'] = 10
    elif difficulty == 'medium':
        settings['rows'] = 16
        settings['columns'] = 16
        settings['bombs'] = 40
    elif difficulty == 'hard':
        settings['rows'] = 16
        settings['columns'] = 30
        settings['bombs'] = 99
    elif difficulty == 'custom': #test
        settings['rows'] = 'NOT DONE YET'
        settings['columns'] = 'NOT DONE YET'
        settings['bombs'] = 'NOT DONE YET'
    #print(f"After -- Self: {selfButton['state']}, Other: {otherButton['state']}")


# MINESWEEPER FUNCTIONS
def displayGrid(settings):
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
gameSettings = {'difficulty':0, 'solveType':0, 'generation':0, 'board':0}
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

settings_Start = Button(windowSettings, text='Start', command=lambda:minesweeper(windowSettings, gameSettings))
settings_Start.grid(row=10, column=3)


def minesweeper(self, settings):  # Minesweeper Game
    print(settings)
    self.destroy()
    displayGrid(settings)

mainloop()

"""
EXTERNAL CODE REFERENCSE:
1. generateGrid() adapted from: https://stackoverflow.com/a/38809894
"""