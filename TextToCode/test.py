# with open("empty.txt", "w+") as file:
#     file.truncate()
#     readData = file.readlines()

# print(len(readData))

from tkinter import *

root = Tk()
scrollbar = Scrollbar(root)
scrollbar.grid(row = 0, column = 1, sticky = NS)

mylist = Listbox(root, yscrollcommand = scrollbar.set )
for line in range(100):
   mylist.insert(END, "This is line number " + str(line))

mylist.grid(row=0, column = 0, sticky = NSEW)
scrollbar.config( command = mylist.yview )

mainloop()