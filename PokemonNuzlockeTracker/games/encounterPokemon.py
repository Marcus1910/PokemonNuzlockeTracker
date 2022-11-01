class EncounterPokemon():
    def __init__(self, name, level, percentage):
        self.name= name
        self.levels = level
        self.percentage = percentage
    
    def __str__(self):
        return f"I am {self.name}, spawn at levels {self.levels} and have a percentage of: {self.percentage}"