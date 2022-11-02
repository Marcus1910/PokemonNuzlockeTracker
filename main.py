import time
import sys
import os

currentpath = os.getcwd()

if currentpath[-16:] != "PokemonNuzlockes":
    print(f"not in the correct folder, please go to the PokemonNuzlockes folder and start the program from there, you are currently in {os.getcwd()}")
    time.sleep(1)
    exit()

if not os.path.isdir(f"{currentpath}\PokemonNuzlockeTracker"):
    print("please go to the correct PokemonNuzlockes directory which has 'PokemonNuzlockeTracker as sub directory'")

#set the path to the folder where all the GUI files are so importing goes 'smoothly'
GUIpath = currentpath + "\PokemonNuzlockeTracker\PokemonNuzlockeTracker"
sys.path.append(GUIpath)

if __name__ == "__main__":
    from selectGameWindow import SelectGameWindow
    x = SelectGameWindow()