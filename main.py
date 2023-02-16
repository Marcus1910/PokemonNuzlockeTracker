import time
import sys
import os



def changePath():
    currentpath = os.getcwd()
    mainPath = currentpath + "\PokemonNuzlockeTracker\PokemonNuzlockeTracker"
    GUIPath = mainPath + "\GUI"
    LogicPath = mainPath + "\Logic"

    if currentpath[-22:] != "PokemonNuzlockeTracker":
        print(f"not in the correct folder, please go to the PokemonNuzlockes folder and start the program from there, you are currently in {os.getcwd()}")
        time.sleep(1)
        exit()

    if not os.path.isdir(mainPath):
        print("please go to the correct PokemonNuzlockeTracker directory which has 'PokemonNuzlockeTracker as a sub directory'")

    #set the path and working directory to the folder where all the GUI files are so importing goes 'smoothly'
    sys.path.append(GUIPath)
    sys.path.append(LogicPath)
    os.chdir(mainPath)

if __name__ == "__main__":
    changePath()
    #editor doesn't recognize it, but it is still a valid import because of the path.append(GUIPath)
    from selectGameWindow import SelectGameWindow
    SelectGameWindow()