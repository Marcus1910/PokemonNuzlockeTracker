from tkinter import *
root = Tk()
pidgeyVar = IntVar()

dict = {"pidgey" : pidgeyVar,
        "get": IntVar(),
        "pidgeot" : pidgeyVar}

for key, value in dict.items():
    print(key, value.get())

dict["pidgey"].set(1)

for key, value in dict.items():
    print(key, value.get())
