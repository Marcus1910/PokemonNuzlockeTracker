from games import MainGame

class CLI():
    game = MainGame("SacredGold")
    listAreas = game.retrieveGameData()
    newBark = listAreas[0]
    trainers = newBark.trainers
    items = newBark.items
    encounters = newBark.encounters
    # for trainer in trainers.values():
    #     print(trainer.name)
    #     for pokemon in trainer.pokemon:
    #         print(pokemon)
    # for item in items.values():
    #     print(item.name)
    game.writeToFile()
    #print(items)