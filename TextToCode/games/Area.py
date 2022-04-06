class Area:
    def __init__(self, name, gym = 0):
        self.name = name
        #integer after which gym the area is unlocked
        self.gym = gym
        self.pokemonList = ['Purrloin']
        self.trainerList = ['Tristan']
        self.itemList = ['max repel']
    

    def changeGym(self):
        #should be asked in [game]
        #name = input(f'give the name of the area you want to change: \n')
        newBadge = input(f'after which badge can you access {self.name}?\n')
        self.gym = newBadge
        print(f'changed the availability of {self.name} to {newBadge}')
    
    def addPokemon(self, pokemon):
        if pokemon in self.pokemonList:
            print(f'{pokemon} has already been noted')
        else:
            self.pokemonList.append(pokemon)
        print(f'succesfully added {pokemon} to {self.name}') 
    def deletePokemon(self, pokemon):
        if pokemon in self.pokemonList:
            self.pokemonList.remove(pokemon)
            print(f'succesfully removed {pokemon}')
        else:
            print(f'{pokemon} not in {self.name}')
    
    def addTrainer(self, trainer):
        #make a new trainer object
        pass

    def deleteTrainer(self,trainer):
        #show list of available trainers
        pass

    def print(self):
        print(f'current Area is {self.name}')  
    def printGym(self):
        return(f'{self.name} can be found after gym {self.gym}.')
    def printAvailablePokemon(self):
        print(f'{self.name} has {len(self.pokemonList)} pokemon available.\n{self.pokemonList}')
    def printTrainers(self):
        print(f'{self.name} has {len(self.trainerList)} trainer.\n{self.trainerList}')
    def printItems(self):
        print(f'{self.name} has {len(self.itemList)} item.\n{self.itemList}')


#Route19 = Area("Route 19") 
#Route19.print()

'''
#add and remove pokemon
Route19.addPokemon('Dialga')
Route19.printAvailablePokemon()
Route19.deletePokemon('Purrloin')
Route19.printAvailablePokemon()
'''

'''
#change badge   
Route19.changeGym()   
Route19.print()
'''