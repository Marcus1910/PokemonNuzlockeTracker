import logging
open("trackerLogic.log", "w").close()
# Get the logger for your application
logger = logging.getLogger('PokemonNuzlockeTracker')
logicLogger = logging.getLogger('PokemonNuzlockeTracker logic')

logger.setLevel(logging.DEBUG)
logicLogger.setLevel(logging.INFO)

logger.propagate = False
logicLogger.propagate = False

handler = logging.StreamHandler()

fileHandler= logging.FileHandler("trackerLogic.log")
fileHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(filename)s - %(lineno)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
handler.setFormatter(formatter)

logger.addHandler(handler)
logicLogger.addHandler(handler)
logicLogger.addHandler(fileHandler)

