import logging

# Get the logger for your application
logger = logging.getLogger('PokemonNuzlockeTracker')
logicLogger = logging.getLogger('PokemonNuzlockeTracker logic')

logger.setLevel(logging.DEBUG)
logicLogger.setLevel(logging.DEBUG)

logger.propagate = False
logicLogger.propagate = False

handler = logging.StreamHandler()

formatter = logging.Formatter('%(filename)s - %(lineno)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logicLogger.addHandler(handler)