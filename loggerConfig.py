import logging
open("trackerLogic.log", "w").close()

formatter = logging.Formatter('%(filename)s - %(lineno)s - %(levelname)s - %(message)s')
# Get the logger for your application
logger = logging.getLogger('PokemonNuzlockeTracker')

logger.setLevel(logging.DEBUG)
logger.propagate = False
loggerHandler = logging.StreamHandler()
loggerHandler.setLevel(logging.DEBUG)
loggerHandler.setFormatter(formatter)
logger.addHandler(loggerHandler)

logicLogger = logging.getLogger('PokemonNuzlockeTracker logic')
logicLogger.setLevel(logging.DEBUG)
logicLogger.propagate = False
logicHandler = logging.StreamHandler()
logicHandler.setLevel(logging.DEBUG)
logicHandler.setFormatter(formatter)
logicLogger.addHandler(logicHandler)

sqlLogger = logging.getLogger('sqlalchemy')
sqlLogger.setLevel(logging.ERROR)
sqlLogger.propagate = False
sqlHandler = logging.StreamHandler()
sqlHandler.setLevel(logging.ERROR)
sqlHandler.setFormatter(formatter)
sqlLogger.addHandler(sqlHandler)

fileHandler= logging.FileHandler("trackerLogic.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
logicLogger.addHandler(fileHandler)



