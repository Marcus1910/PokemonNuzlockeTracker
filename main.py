import time
import sys
import os
import argparse
import platform

def changePath():

    currentpath = os.getcwd()
    print(f"currentpath: {currentpath}")
    
    mainPath = os.path.abspath(os.path.join(currentpath, "PokemonNuzlockeTracker", "PokemonNuzlockeTracker"))

    # GUIPath = os.path.join(mainPath, "GUI")
    # LogicPath = os.path.join(mainPath, "Logic")

    #set the path and working directory to the folder where all the GUI files are so importing goes 'smoothly'
    sys.path.append(mainPath)
    #sys.path.append(LogicPath)
    os.chdir(mainPath)

def getOS() -> str:
    if platform.system() == 'Windows':
        return 'Windows'
    elif platform.system() == 'Darwin':  # macOS
        return 'macOS'
    elif platform.system() == 'Linux':
        if 'ANDROID_DATA' in os.environ:
            return 'Android'
        else:
            return 'Linux'
    else:
        return 'Unknown' 

if __name__ == "__main__":
    changePath()
    operatingSystem = getOS()
    print(f"OS: {operatingSystem}")
    parser = argparse.ArgumentParser(description = "Nuzlocke Tracker")
    parser.add_argument("--cli", action = "store_true", help = "Run in CLI mode", default = False)
    args = parser.parse_args(sys.argv[2:])


    #editor doesn't recognize it, but it is still a valid import because of the path.append(GUIPath)
    # if args.cli:
    #     from Logic.CLI import CLI
    #     CLI(operatingSystem)
    # else:
    from GUI.trackerApp import TrackerApp
    
    try:
        TrackerApp(operatingSystem).run()
    except Exception as e:
        print(f"exception occurred: {e}")

