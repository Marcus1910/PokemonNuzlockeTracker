from reading import BlazeBlack2ReduxReader

textfile = "area.txt"
textfile1 = "Wild Area Changes.txt"
textfile2 = "Wild Area Changes last.txt"
x = BlazeBlack2ReduxReader()
x.openFile(textfile2)
x.removeEmptyLines()
x.createSeperateLists()
x.createAreas()
#x.createPokemonBlocks()
#x.createPokemonObjectList()
x.writeDataToFile()
#print(x.data)

#print(x)
