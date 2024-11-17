import os
import shutil
from loggerConfig import logicLogger as logger
import time
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .databaseModels import Game, Attempt, Location
from .databaseModels.game import newGameString

class DataRetriever():
    def __init__(self, operatingSystem):
        """Dataretriever is responsible for all data transactions"""
        self.gameFolder = os.path.join(os.path.dirname(os.getcwd()), "games")
        #forward declaration
        self._gameNameFolder = None
        self._dataFolder = None
        self._saveFilesFolder = None
        self.databasePath = os.path.join("sqlite:///" + os.path.dirname(os.path.dirname(os.getcwd())),"mydb.db" )
        self.databaseEngine = create_engine(self.databasePath, echo = True)
        self.Session = sessionmaker(bind = self.databaseEngine)

        if not self.validateDirectory(self.gameFolder):
            logger.critical(f"Could not find own internal storage for games, exiting in 10 seconds")
            time.sleep(10)
            exit()
        
        #check database validity

        #boolean if the internal storage is accessible, now used for Android
        self.internalStorage = False
        self.internalStoragePath = None

        self.internalGameStorage = False
        self.internalGameStoragePath = None
        self.operatingSystem = operatingSystem

        #call correct functions to setup filesystem inside program correctly or continue with leftover files
        if self.operatingSystem == "Android":
            self.internalStoragePath = self.getStoragePath()
            logger.info(f"storage phone: {self.internalStoragePath}")
            # self.printDirectory(self.internalStoragePath)
            if self.validateDirectory(self.internalStoragePath):
                self.internalGameStoragePath = self.getInternalGameStoragePath()
                self.moveAllFiles()
            else:
                logger.warning(f"could not access internal storage, has it been removed?\ncontinuing with local files inside program")
        else:
            logger.info("did not detect Android, assuming Windows")
        
        #set folder variables correctly
        
    @contextmanager
    def databaseSession(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @property
    def gameNameFolder(self):
        return self._gameNameFolder
    
    @property
    def dataFolder(self):
        return self._dataFolder
    
    @property
    def saveFilesFolder(self):
        return self._saveFilesFolder

    def retrieveGameList(self):
        """returns a list of the games available with an option to create a new game"""
        # with self.databaseSession() as session:
        #     games = [game.name for game in session.query(Game).all()]
        #     games.append(newGameString)
        #     return game
        games = []
        with self.databaseSession() as session:
            games = [game.name for game in session.query(Game).all()]
            
        games.append(newGameString)
        return games

    def getGameRecordFromGameName(self, GameName: str) -> Game:
        # with self.databaseSession() as session:
        #     game = session.query(Game).filter(Game.name == GameName).first()
        #     return game
        session = self.Session()
        try:
            game = session.query(Game).filter(Game.name == GameName).first() 
        finally:
            session.close
        return game

    def getSaveFilesList(self, IDGame: int) -> list[str]:
        """returns a list of the attempts made with a 'New attempt' option. Should be called after the game is selected"""
        #creates all folders if they don't already exist
        #TODO wanneer nieuwe game wordt aangemaakt of wanneer validatie data
        #self.setFolderVariables(gameName)
        #self.createGameFolders(gameName)
        saveFiles = []
        
        with self.databaseSession() as session:
            saveFiles = ["attempt " + str(saveFile.attemptNumber) for saveFile in session.query(Attempt).filter(Attempt.IDGame == IDGame).all()]
            
        saveFiles.append("New attempt")
        return saveFiles

    def getAttemptRecord(self, attemptNumber: int, IDGame: int):
        attempt = None
        session = self.Session()
        try:
            attempt = session.query(Attempt).filter(Attempt.attemptNumber == attemptNumber).filter(Attempt.IDGame == IDGame).first()
        finally:
            session.close()
        return attempt


    def getLocationRecord(self, IDLocation: int) -> Location:
        session = self.Session()
        try:
            locationRecord = session.query(Location).filter(Location.IDGame == IDLocation).first()
        finally:
            session.close()
        return locationRecord

    def getLocationNames(self, IDGame: int) -> list[str]:
        locationNames = []
        session = self.Session()
        try:
            locationNames = [location.name for location in session.query(Location).filter(Location.IDGame == IDGame)]
        finally:
            session.close()
        return locationNames
        
    def validateDirectory(self, folder : str) -> bool:
        """checks if the directory exists returns 1 on success, 0 on failure"""
        if not os.path.isdir(folder):
            logger.info(f"could not find {folder}")
            return 0
        return 1
    
    def getSaveFile(self, saveFileName: str) -> str | None:
        logger.info(f"retrieving path to {saveFileName} from saveFileFolder: {self.saveFilesFolder}")
        saveFilePath = os.path.join(self._saveFilesFolder, f"{saveFileName}.txt")
        
        if not os.path.isfile(saveFilePath):
            logger.error(f"found saveFilePath is invalid: {saveFilePath}")
            return None
        logger.info(f"found path: {saveFilePath}")
        return saveFilePath



    def moveAllFiles(self):
        """moves all files from internal storage to program folder, depending on OS"""
        if self.operatingSystem == "Android":
            self.moveFiles(self.internalGameStoragePath, self.gameFolder)

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
        logger.info(f"found gamePath: {gamePath}")
        if not self.validateDirectory(gamePath):
            #directory does not exist but internal storage is accessible. create new folder
            os.mkdir(gamePath)
        return gamePath
    
    def copyGameFilesToProgram(self, gameName: str) -> bool:
        """places the correct gameFiles into the /games/gameName directory, gets called by game Object"""
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
        logger.info(f"starting copy for {gameName}")
        savefileFolder = os.path.join(self.internalStoragePath, "games", gameName)
        print(self.internalStoragePath)
        if not os.path.isdir(savefileFolder):
            #popup asking what should happen?
            logger.error(f"{savefileFolder} is not correct, TODO continue with local files")
            self.internalGameStorage = False
            return 0

        logger.info(f"fetching files from {savefileFolder}")
        self.internalGameStorage = True

        # self.printDirectory(savefileFolder)
        gameNameFolder = os.path.join(self.gameFolder, gameName)
        self.moveFiles(savefileFolder, gameNameFolder)
        logger.info("program folder after copy: ")
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
                logger.info(f"copied {sourceFile} to {destinationDirectory}")
        return 1

    def setFolderVariables(self, gameName: str) -> bool:
        """sets all neccessary folderpaths to correct paths"""
        self._gameNameFolder = os.path.join(self.gameFolder, gameName)
        self._saveFilesFolder = os.path.join(self._gameNameFolder, "saveFiles")
        self._dataFolder = os.path.join(self._gameNameFolder, "data")


    def createGameFolders(self, gameName: str) -> bool:
        """creates the neccessary folders GameName, datafolder, savefilesFolder if they don't already exist"""
        capGameName = gameName.capitalize()
        if capGameName == "Generic" or capGameName == "New":
            logger.error(f"cannot allow a game called 'Generic' or 'new'")
            return 0

        self.setFolderVariables(gameName)
        #create Game, savefiles and data Folder
        self.createNewFolder(self._gameNameFolder)
        self.createNewFolder(self._saveFilesFolder)
        self.createNewFolder(self._dataFolder)
        return 1
    
    def createNewFolder(self, path: str) -> None:
        """creates a new folder if the folder does not already exist"""
        if self.validateDirectory(path):
            logger.info(f"{path} already has a folder, not creating a new one")
        else:
            logger.info(f"creating {path}")
            os.mkdir(path)

    def printDirectory(self, path: str):
        """prints all files and subdirectories from given path"""
        if not os.path.isdir(path) or path == None:
            logger.error(f"could not read {path}, path is invalid")
            return
        totalSize = 0
        for root, dirs, files in os.walk(path):
            rootSize = 0
            logger.info(f"Directory: {root}")
            for file in files:
                fp = os.path.join(root, file)
                if not os.path.islink(fp):
                    rootSize += os.path.getsize(fp)
                logger.info(f"  File: {file}")
            totalSize += rootSize
            logger.info(f"{root} has a size of: {rootSize} bytes")
        logger.info(f"total bytes: {totalSize}")
    
    def checkGameExists(self, gameName: str) -> bool:
        #remove 'new' option
        return 1 if gameName in self.retrieveGameList()[:-1] else 0

    def addNewPokemonGame(self, gameName: str) -> bool:
        """checks if game already exists otherwise creates game and needed directories"""
        if self.checkGameExists(gameName):
            logger.error(f"{gameName} already exists")
            return 0
        if not self.createGameFolders(gameName):
            return 0
        return 1
    
    def createNewSaveFile(self, gameName: str, attempt: str) -> bool:
        self.setFolderVariables(gameName)
        if self.checkSaveFileExists(attempt):
            logger.error(f"savefile: {attempt} already exists for {gameName}, {saveFilePath}")
        else:
            saveFilePath = os.path.join(self._saveFilesFolder, f"{attempt}.txt")
            logger.info(f"creating new savefile, {saveFilePath}")
            open(saveFilePath, "x").close()
        
    def checkSaveFileExists(self, fileName: str) -> bool:
        """returns 1 when file already exists"""
        saveFilePath = os.path.join(self._saveFilesFolder, f"{fileName}.txt")
        return 1 if os.path.isfile(saveFilePath) else 0







    
# def addNewSaveFile():
#     #"new" has purposely not been removed, now len == attempt
#     saveFiles = self.getSaveFiles()
#     number = len(saveFiles)
#     #create the file then close it
#     open(f"{self.saveFileFolder}/attempt {number}.txt", "x").close()
