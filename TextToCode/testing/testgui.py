from tkinter import *
from turtle import width

root = Tk()
root.title("kanker goede rekenmachine om te berekenen hoe get je bent")
root.geometry("450x450")
answer = "ja toch"
equation = ""
specialCharacters = ["*", "-", "+", "="]

answerLabel = Label(root, text = answer, height = 5)
answerLabel.grid(row=0, column=0, columnspan=3)
#print(answerLabel.cget("text"))
yes = IntVar()
yes.set(1)
print(yes.get())
yes.set(1)
print(yes.get())
def showNumber(number):
    global answer
    answer += str(number)

def queueNumber(number):
    global answer
    equation += str(number)

def createGrid(row, column):
    if row < 1:row = 1
    finalColumn = column+3
    for i in range(10):
        #number 0
        if i == 9:
            number = 0
            cspan = 3
        else:
            number = i+1
            cspan = 1

        x = Button(root, text = number, height=5, width = 7)
        x.grid(row = row, column = column, columnspan = cspan, sticky = EW)
        #print(f'number: {number}, cspan {cspan}')

        column +=1
        #go to a new row
        if column == finalColumn:
            row +=1
            column = 0


createGrid(0,0)
#print(eval("5*8"))
root.mainloop()