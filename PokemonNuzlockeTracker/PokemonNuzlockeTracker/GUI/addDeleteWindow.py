from abc import abstractmethod
from tkinter import *

class AddDeleteWindow():
    def __init__(self, parent, list, currentRoute, delete, attribute):
        self._parent = parent
        self._list = list
        self._currentRoute = currentRoute
        self._delete = delete
        self._attribute = attribute
        self._window = Toplevel(self._parent)
        self._window.geometry("250x250")
        self._window.resizable(0,0)
        self._window.attributes("-topmost", True)
        self._window.rowconfigure(0, weight = 2)
        self._window.columnconfigure(0, weight = 2)
        self._addingText = f"adding {self._attribute} to {self._currentRoute}"
        self._deletingText = f"deleting {self._attribute} from {self._currentRoute}"
        self._attributeText = f"enter {self._attribute}'s name"

        self._routeVerificationLabel = Label(self._window, text = self._deletingText if self._delete else self._addingText)
        self._routeVerificationLabel.grid(row = 0, column = 0)

        self._inputLabel = Label(self._window, text = self._attributeText)
        self._inputLabel.grid(row = 1, column = 0)

        self._input = Entry(self._window)
        self._input.grid(row = 2, column = 0, sticky = N)

        self._trainerText = Label(self._window, text = f"current {self._attribute}s on {self._currentRoute}")
        self._trainerText.grid(row = 3, column = 0, sticky = W)

        self._submitButton = Button(self._window, text = "Submit", command = self.validateInput)
        self._submitButton.grid(row = 5, column = 0, sticky = E)

        self._backButton = Button(self._window, text = "back", command = self.closeWindow)
        self._backButton.grid(row = 5, column = 0, sticky = W)

        self.showTrainer()

    def showTrainer(self):
        trainersFrame = Frame(self._window)
        trainersFrame.grid(row = 4, column = 0, sticky = NSEW)
        itemScrollbar = Scrollbar(trainersFrame)
        itemScrollbar.grid(row = 1, column = 1, sticky = NS)
        itemBox = Listbox(trainersFrame, yscrollcommand = itemScrollbar.set)
        itemBox.grid(row = 1, column = 0)
        for item in self._list:
            itemBox.insert(END, item.name)
        itemScrollbar.configure(command = itemBox.yview)
          
    def validateInput(self):
        notFound = 0
        input = self._input.get().capitalize()
        print(f"validating... {input}")
        #check if there are letters in the input
        if "  " in input or input == " ":
            print("try again, detected double space or only space. please enter valid name")
            return
        #first trainer
        if len(self._list) == 0:
            print(f"adding {input}")
            self.createNewAttribute(input)
            self.closeWindow()
            return

        for attribute in self._list:
            if input == attribute.name:
                if self._delete:
                    print(f"deleting {input}")
                    print(self._list)
                    #delete function
                    self.deleteNewAttribute(attribute)
                    #update list and close window
                    self.closeWindow()
                if not self._delete:
                    print(f"{input} already exists")
                    #TODO error message
            else:
                #looped through every name and not found, cannot delete but can make a new entry
                notFound += 1
                if notFound == len(self._list):
                    if not self._delete:
                        print(f"adding {input}")
                        self.createNewAttribute(input)
                        self.closeWindow()
                        break
                    else:
                        print(f"{input} does not exist")
        
                        

    @abstractmethod
    def createNewAttribute(self, input):
        pass

    @abstractmethod
    def deleteNewAttribute(self, input):
        pass

    def closeWindow(self):
        print("closing window")
        self._window.destroy()