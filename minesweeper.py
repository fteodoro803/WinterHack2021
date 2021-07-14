# IMPORTS
import tkinter
from tkinter import *

# MINESWEEPER FUNCTIONS


# MAIN
windowSettings = Tk()
windowSettings.title("Minesweeper")
windowSettings.geometry("500x500") #arbitrary number, change later to be customisable (have a max size based on grid count)

# Grid Type/Difficulty
settings_GridType = Label(windowSettings, text='Select Grid Type').grid(row=0, column=0)
settings_Difficulty = Label(windowSettings, text='Difficulty').grid(row=1, column=1)
settings_Size = Label(windowSettings, text='Size').grid(row=1, column=2)
settings_Bombs = Label(windowSettings, text='Bombs').grid(row=1, column=3)
settings_Easy = Button(windowSettings, text='Easy').grid(row=2, column=1)
settings_EasySize = Label(windowSettings, text='9x9').grid(row=2, column=2)
settings_EasyBombs = Label(windowSettings, text='10').grid(row=2, column=3)

settings_Medium = Button(windowSettings, text='Medium').grid(row=3, column=1)
settings_MediumSize = Label(windowSettings, text='16x16').grid(row=3, column=2)
settings_MediumBombs = Label(windowSettings, text='40').grid(row=3, column=3)

settings_Hard = Button(windowSettings, text='Hard').grid(row=4, column=1)
settings_HardSize = Label(windowSettings, text='16x30').grid(row=4, column=2)
settings_HardBombs = Label(windowSettings, text='99').grid(row=4, column=3)

settings_Custom = Button(windowSettings, text='Custom').grid(row=5, column=1)
settings_CustomSize = tkinter.Entry(windowSettings).grid(row=5, column=2)
settings_CustomBombs = tkinter.Entry(windowSettings).grid(row=5, column=3)

# Solver Mode
settings_SolveType = Label(windowSettings, text='Select Solve Type').grid(row=6, column=0)
settings_Manual = Button(windowSettings, text='Manual').grid(row=7, column=1)
settings_Automatic = Button(windowSettings, text='Automatic').grid(row=7, column=2)

# Board Generation
settings_Board = Label(windowSettings, text=f"Minesweeper Board \n(Default is 'Generate')").grid(row=8, column=0)
settings_Generate = Button(windowSettings, text='Generate').grid(row=9, column=1)
settings_Load = Button(windowSettings, text='Load').grid(row=9, column=2) #test - add functionality for this later

settings_start = Button(windowSettings, text='Start').grid(row=10, column=3)

def minesweeper():
    windowSettings.destroy()

mainloop()