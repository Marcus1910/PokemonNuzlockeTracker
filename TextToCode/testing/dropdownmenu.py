from tkinter import *

root = Tk()
root.title = "drop dwon menu"
root.geometry = "400x400"

List = [1,2,3,4,5]


var = StringVar(root)
w = OptionMenu(root, var, *List)
w.pack()
root.mainloop()