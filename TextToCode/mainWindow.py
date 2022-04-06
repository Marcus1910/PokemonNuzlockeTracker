from tkinter import *
from PIL import ImageTk, Image
from templateWindow import templateWindow

class MainWindow():
    def __init__(self, x, y, game, debugMode):
        
        self.tempWindow = templateWindow(x, y)
        self.master = self.tempWindow.master
        self.masterX = x
        self.masterY = y
        self.game = game
        self.debugMode = debugMode
        self.numberOfBadges = 0
        self.listOfAreas = ["route 20", "route 21"]

        self.master.title(f"{self.game}")

        self.widgetFrame = Frame(self.master, width = self.masterX, height = self.masterY)
        self.widgetFrame.place(x=0,y=0,relheight=1,relwidth=1)

        #background
        self.photo = ImageTk.PhotoImage(Image.open("bg.jpg").resize([self.masterX, self.masterY]),Image.BOX)
        self.photoLabel = Label(self.widgetFrame, image = self.photo)
        self.photoLabel.grid(row=0, column = 0, rowspan=5, columnspan=5)

        #number of badges
        self.numberOfBadges = StringVar()
        self.numberOfBadges.set("number of badges")
        self.badgesMenu = OptionMenu(self.widgetFrame, self.numberOfBadges, *list(range(0,9)))
        self.badgesMenu.grid(row=0, column=0,rowspan=1, columnspan=1, sticky=NW) 

        #exitbutton
        self.createExitButton()

        self.itemFrame = Frame(self.widgetFrame)
        self.itemFrame.grid(row=1, column=1,rowspan=3, sticky=NSEW)

        self.trainerFrame = Frame(self.widgetFrame)
        self.trainerFrame.grid(row=1, column=3, rowspan=3, sticky=NSEW)

        self.itemButton = Button(self.itemFrame, text="Items komen hier terecht")
        self.itemButton.grid(row=0,column=0,sticky=N)


        self.selectedArea = StringVar()
        self.selectedArea.set("choose an Area")
        self.areaMenu = OptionMenu(self.widgetFrame, self.selectedArea, *self.listOfAreas)
        self.areaMenu.grid(row=0, column=2, sticky=N)

        self.encounterButton = Button(self.widgetFrame, text = "Encounters")
        self.encounterButton.grid(row=3,column=2)

        self.backButton = Button(self.widgetFrame, text = "back", command = self.createGameMenu)
        self.backButton.grid(row=4, column=4, sticky=SE)

        #let the window stay and rescale image
        self.resizeImage = self.master.after(300, self.tempWindow.update)
        self.master.mainloop()
    
    def createExitButton(self):
        self.exitButton = Button(self.widgetFrame, text = "exit", command = self.master.destroy)
        self.exitButton.grid(row=4, column = 0, sticky=SW)

    def createGameMenu(self):
        from GUI import SelectGameWindow
        self.tempWindow.stop()
        self.master.destroy()
        SelectGameWindow()




