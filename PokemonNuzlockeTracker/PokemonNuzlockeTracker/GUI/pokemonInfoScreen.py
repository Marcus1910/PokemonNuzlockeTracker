from .nuzlockeScreen import NuzlockeScreen

class PokemonInfoScreen(NuzlockeScreen):
    def __init__(self, screenName, **kwargs):
        super().__init__(screenName = screenName, **kwargs)