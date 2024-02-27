import os
import shutil
from loggerConfig import logicLogger as logger


class FileRetriever():
    def __init__(self, operatingSystem):
        print("file retriever")
        self.gameFolder = os.path.join(os.path.dirname(os.getcwd()), "games")
        #boolean if the internal storage is accessible, now used for Android
        self.internalStorage = False
        self.internalStoragePath = None

        self.internalGameStorage = False
        self.internalGameStoragePath = None
        self.operatingSystem = operatingSystem

        #call correct functions to setup filesystem inside program correctly or continue with leftover files
        if self.operatingSystem == "Android":
            self.internalStoragePath = self.getStoragePath()
            print(f"storage phone: {self.internalStoragePath}")
            if self.validateDirectory(self.internalStoragePath):
                self.internalGameStoragePath = self.getInternalGameStoragePath()
                print(self.internalStoragePath, self.internalGameStoragePath)
                self.moveAllFiles()
            else:
                logger.error(f"could not access internal storage, has it been removed?\ncontinuing with local files inside program")
        else:
            logger.info("did not detect Android, assuming Windows")

    def checkGames(self):
        #walks down the directory for other directories, retrieves the names and puts them in a list
        games = [gameName for gameName in next(os.walk(self.gameFolder))[1] if gameName != "Generic"]
        #no games found
        if not games:
            return ["New game"]
        games.append("New game")
        return games

    def validateDirectory(self, folder : str) -> bool:
        """checks if the directory existst otherwise creates it, returns 1 when succesful else 0"""
        if not os.path.isdir(folder):
            logger.debug(f"could not find {folder}")
            return 0
        return 1

    def getSaveFiles(self, gameName : str) -> list[str]:
        """returns a list of the attempts made with a 'New attempt' option"""
        saveFileFolder = os.path.join(os.path.dirname(os.getcwd()), "games", gameName, "saveFiles")
        if self.validateDirectory(saveFileFolder):
            #get every file, [0] because it returns a list inside of a list
            saveFiles = [x[2] for x in os.walk(saveFileFolder)][0]
            #keep files with attempt in its name, and remove the '.txt'
            saveFiles = [x[:-4] for x in saveFiles if("attempt" in x)]
        else:
            logger.error(f"could not find savefilefolder: {saveFileFolder}") 
        #give the option to make a new saveFile
        saveFiles.append("New attempt")
        return saveFiles

    def moveAllFiles(self):
        """moves all files from internal storage to program folder, depending on OS"""
        if self.operatingSystem == "Android":
            self.moveFiles(self.internalStoragePath, self.gameFolder)

    def getStoragePath(self) -> str | None:
        """get storagePath from android device, if failed returns None. sets internalStporage to True or False"""
        try:
            from android.storage import app_storage_path
        except ImportError as e:
            logger.error(f"could not import library to access internal storage from android device: {e}")
            self.internalStorage = False
            return None
        
        internalStoragepath = app_storage_path()
        if os.path.isdir(internalStoragepath):
            self.internalStorage = True
            return internalStoragepath
        return None

    def getInternalGameStoragePath(self) -> str | None:
        """get internalGamePath to store savefiles, sets internalGameStorage to True or False"""
        gamePath = os.path.join(self.internalStoragePath, "games")
        print(f"gamePath: {gamePath}")
        if not self.validateDirectory(gamePath):
            #directory does not exist but internal storage is accessible. create new folder
            os.mkdir(gamePath)
        return gamePath
    
    def retrieveGameFiles(self, gameName: str) -> bool:
        """places the correct gameFiles into the /games/gameName directory"""
        if self.operatingSystem == "Android":
            return self.copyGameFolderToProgramFolder(gameName)
        elif self.operatingSystem == "Windows":
            return 1
    
    def saveGameFiles(self, gameName: str) -> bool:
        """saves the gameFolder to the correct place depending on OS"""
        if self.operatingSystem == "Android":
            self.moveGameFilesToInternalStorage(gameName)
        if self.operatingSystem == "Windows":
            pass

    def copyGameFolderToProgramFolder(self, gameName) -> bool:
        """For Android, copy the game folder from internal memory to the programs games folder"""
        logger.debug(f"starting copy for {gameName}")
        savefileFolder = os.path.join(self.internalStoragePath, "games", gameName)
        if not os.path.isdir(savefileFolder):
            #popup asking what should happen?
            logger.error(f"{savefileFolder} is not correct, TODO continue with local files")
            self.internalGameStorage = False
            return 0

        logger.debug(f"fetching files from {savefileFolder}")
        self.internalGameStorage = True
        
        print("savefile directory")
        self.printDirectory(savefileFolder)
        gameNameFolder = os.path.join(self.gameFolder, gameName)
        self.moveFiles(savefileFolder, gameNameFolder)
        print("program folder after copy")
        self.printDirectory(gameNameFolder)
        return 1

    def moveGameFilesToInternalStorage(self, gameName: str) -> bool:
        """For Android, moves the program's gamefiles to the internal storage"""
        if not self.internalStorage:
            logger.error(f"internalStorage cannot be accessed, cannot save to internal storage")
            return 0
         
        programFolder = os.path.join(self.gameFolder, gameName)
        if not self.validateDirectory(programFolder):
            logger.error(f"programFolder: {programFolder} cannot be found, writing impossible")
            return 0
        
        internalFolder = os.path.join(self.internalStoragePath, "games", gameName)
        return self.moveFiles(programFolder, internalFolder)

    def moveFiles(self, sourceFolder: str, destinationFolder: str):
        """moves or copies directory tree from sourceFolder to destinationFolder"""
        logger.info(f"copying or moving {sourceFolder} to {destinationFolder}")
        #validate paths before copying or moving files
        if not self.validateDirectory(sourceFolder):
            logger.error(f"{sourceFolder} is incorrect, not copying")
            return 0

        for sourceDirectory, _, files in os.walk(sourceFolder):
            destinationDirectory = sourceDirectory.replace(sourceFolder, destinationFolder, 1)
            #create directory is it doesn't exist already
            if not os.path.exists(destinationDirectory):
                try:
                    os.makedirs(destinationDirectory)
                except OSError as e:
                    logger.error(f"could not create {destinationDirectory}, {e}")
                    return 0

            for file in files:
                sourceFile = os.path.join(sourceDirectory, file)
                destinationFile = os.path.join(destinationDirectory, file)
                if os.path.exists(destinationFile):
                    # in case of the src and dst are the same file
                    if os.path.samefile(sourceFile, destinationFile):
                        #continue loop, skips the os.remove
                        continue
                    #remove file if the filename exists
                    try:
                        os.remove(destinationFile)
                    except OSError as e:
                        logger.error(f"could not remove {destinationFile}, {e}")
                        return 0

                shutil.copy(sourceFile, destinationDirectory)
                print(f"copied {sourceFile} to {destinationDirectory}")
        return 1

    def printDirectory(self, path: str):
        """prints all files and subdirectories from given path"""
        print(f"path: {path}")
        if not os.path.isdir(path) or path == None:
            logger.error(f"could not read {path}, path is invalid")
            return
        totalSize = 0
        for root, dirs, files in os.walk(path):
            rootSize = 0
            print(f"Directory: {root}")
            for file in files:
                fp = os.path.join(root, file)
                if not os.path.islink(fp):
                    rootSize += os.path.getsize(fp)
                print(f"  File: {file}")
            totalSize += rootSize
            print(f"{root}: {rootSize}")
        print(f"total: {totalSize}")



    
# def addNewSaveFile():
#     #"new" has purposely not been removed, now len == attempt
#     saveFiles = self.getSaveFiles()
#     number = len(saveFiles)
#     #create the file then close it
#     open(f"{self.saveFileFolder}/attempt {number}.txt", "x").close()