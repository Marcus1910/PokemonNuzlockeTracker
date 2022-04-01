from tkinter import *

root = Tk()
root.title = "calculator"
root.geometry = "300x300"

equation = ""
AnswerLabel = Label(root, text = equation).grid(row=0, column = 0, columnspan=3, sticky = EW)

def updateLabel(par):
    global AnswerLabel
    if par:
        text = answer
    else:
        text = equation
    AnswerLabel = Label(text = text).grid(row=0, column = 0, columnspan=3, sticky = EW)

def buttonClick(addition):
    global equation
    equation += str(addition)

def calculate():
    global equation
    global answer 
    answer = eval(equation)
    equation = ""

Button1 = Button(root, text = 1, command = lambda:[buttonClick(1), updateLabel(0)])
Button2 = Button(root, text = 2, command = lambda:buttonClick(2))
Button3 = Button(root, text = 3, command = lambda:buttonClick(3))

Button4 = Button(root, text = 4, command = lambda:buttonClick(4))
Button5 = Button(root, text = 5, command = lambda:buttonClick(5))
Button6 = Button(root, text = 6, command = lambda:buttonClick(6))

Button7 = Button(root, text = 7, command = lambda:buttonClick(7))
Button8 = Button(root, text = 8, command = lambda:buttonClick(8))
Button9 = Button(root, text = 9, command = lambda:buttonClick(9))

Button0 = Button(root, text = 0, command = lambda:buttonClick(0))

ButtonPlus = Button(root, text = "+", command = lambda:buttonClick("+"))
ButtonMinus = Button(root, text = "-", command = lambda:buttonClick("-"))
ButtonMultiply = Button(root, text = "*", command = lambda:buttonClick("*"))
ButtonEquals = Button(root, text = "=", command = lambda: [calculate(), updateLabel(1)])


Button1.grid(row = 1, column = 0)
Button2.grid(row = 1, column = 1)
Button3.grid(row = 1, column = 2)

Button4.grid(row = 2, column = 0)
Button5.grid(row = 2, column = 1)
Button6.grid(row = 2, column = 2)

Button7.grid(row = 3, column = 0)
Button8.grid(row = 3, column = 1)
Button9.grid(row = 3, column = 2)

Button0.grid(row = 4, column = 0, columnspan = 3, stick = EW)

ButtonPlus.grid(row = 1, column = 3)
ButtonMinus.grid(row = 2, column = 3)
ButtonMultiply.grid(row = 3, column = 3)
ButtonEquals.grid(row = 4, column = 3)

root.mainloop()