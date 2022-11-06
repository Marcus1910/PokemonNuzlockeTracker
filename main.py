import time
import sys
import os



def changePath():
    currentpath = os.getcwd()

    if currentpath[-16:] != "PokemonNuzlockes":
        print(f"not in the correct folder, please go to the PokemonNuzlockes folder and start the program from there, you are currently in {os.getcwd()}")
        time.sleep(1)
        exit()

    if not os.path.isdir(f"{currentpath}\PokemonNuzlockeTracker"):
        print("please go to the correct PokemonNuzlockes directory which has 'PokemonNuzlockeTracker as sub directory'")

    #set the path and working directory to the folder where all the GUI files are so importing goes 'smoothly'
    mainPath = currentpath + "\PokemonNuzlockeTracker\PokemonNuzlockeTracker"
    GUIPath = mainPath + "\GUI"
    LogicPath = mainPath + "\Logic"
    
    sys.path.append(GUIPath)
    sys.path.append(LogicPath)
    os.chdir(mainPath)
    print(os.getcwd())

if __name__ == "__main__":
    changePath()
    from selectGameWindow import SelectGameWindow
    x = SelectGameWindow()