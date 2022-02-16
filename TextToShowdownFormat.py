class Pokemon():
    def __init__(self, name, ability):
        self.name = name
        self.ability = ability
        

    def __str__(self):
        return f"Pokemon: {self.name}"

class Trainer():
    def __init__(self, name):
        self.Roster = []
        


    def addPokemon(self, Pokemon):
        self.Roster.append(Pokemon)
        

    def printRoster(self):
        print(f'{self.Roster}')



def main():
    Steelix = Pokemon('Steelix', 'Sturdy')
    Buneary = Pokemon('Buneary', 'Limber')
    Barry = Trainer('Barry')
    Barry.addPokemon(Steelix)
    Barry.addPokemon(Buneary)
    Barry.printRoster()

def ConnectDatabase(game):
    import mysql.connector
    mydb = mysql.connector.connect(
    host="localhost",
    user="Pokemon",
    password="/hucVS3vYwuolPNu"
    )
    message = 'CREATE DATABASE ' + game
    mycursor = mydb.cursor()
    try:
        mycursor.execute(message)
    except mysql.connector.Error as err:
        print(f'database for this game already exists')

def askGame():
    print(f"what game are you playing?")
    game = input()
    #remove spaces from entered text
    game = game.replace(" ","_").lower()
    ConnectDatabase(game)

def askInput():
    askGame()




if __name__ == "__main__":
    #main()
    askInput()