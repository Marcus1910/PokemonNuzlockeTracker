with open("empty.txt", "w+") as file:
    file.truncate()
    readData = file.readlines()

print(len(readData))