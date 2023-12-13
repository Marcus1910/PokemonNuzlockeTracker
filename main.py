import time
import sys
import os
import argparse

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
    parser = argparse.ArgumentParser(description = "Nuzlocke Tracker")
    parser.add_argument("--cli", action = "store_true", help = "Run in CLI mode", default = False)
    args = parser.parse_args(sys.argv[2:])

    #editor doesn't recognize it, but it is still a valid import because of the path.append(GUIPath)
    if args.cli:
        from CLI import CLI
        CLI()
    else:
        from selectGame import SelectGame
        SelectGame().run()

