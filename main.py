import time
import sys
import os

def changePath():

    currentpath = os.getcwd()
    mainPath = os.path.abspath(os.path.join(currentpath, "PokemonNuzlockeTracker", "PokemonNuzlockeTracker"))

    GUIPath = os.path.join(mainPath, "GUI")
    LogicPath = os.path.join(mainPath, "Logic")

    #set the path and working directory to the folder where all the GUI files are so importing goes 'smoothly'
    sys.path.append(GUIPath)
    sys.path.append(LogicPath)
    os.chdir(mainPath)

if __name__ == "__main__":
    changePath()
    GUI = True
    #editor doesn't recognize it, but it is still a valid import because of the path.append(GUIPath)
    if GUI:
        from selectGame import SelectGame
        SelectGame().run()
    else:
        from CLI import CLI
        CLI()