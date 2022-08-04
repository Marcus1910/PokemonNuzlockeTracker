from abc import abstractmethod
from tkinter import *
from games.trainer import Trainer

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

        self._submitButton = Button(self._window, text = "Submit", command = self.validateInput)
        self._submitButton.grid(row = 4, column = 0, sticky = E)

        self._backButton = Button(self._window, text = "back", command = self.closeWindow)
        self._backButton.grid(row = 4, column = 0, sticky = W)

        self.showTrainer()

    def showTrainer(self):
        trainersFrame = Frame(self._window)
        trainersFrame.grid(row = 3, column = 0, sticky = NSEW)
        itemScrollbar = Scrollbar(trainersFrame)
        itemScrollbar.grid(row = 1, column = 1, sticky = NS)
        itemBox = Listbox(trainersFrame, yscrollcommand = itemScrollbar.set)
        itemBox.grid(row = 1, column = 0)
        for item in self._list:
            itemBox.insert(END, item.name)
        itemScrollbar.configure(command = itemBox.yview)
          
    def validateInput(self):
        notFound = 0
        input = self._input.get()
        print(f"validating... {input}")
        for attribute in self._list:
            if input == attribute.name:
                if self._delete:
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
                        self.createNewAttribute(input)
                        self.closeWindow()
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


# class AttributeWindow():
#     def __init__(self, parent, list, delete):
#         self._master = parent
#         self._delete = delete
#         self._list = list
#         self._text = None
#         self._window = Toplevel(parent)
#         self._window.geometry("300x300")
#         self._window.iconbitmap('nuzlocke.ico')
#         self._textLabel = Label(self._window, text = self._text)
#         self._textLabel.grid(row = 0, column = 0)
#         self._newAttribute = Entry(self._window)
#         self._newAttribute.grid(row = 0, column = 1)
#         #configure in later functions
#         self._submitButton = Button(self._window, text = "Submit", command = self.submitChange)
#         self._submitButton.grid(row = 0, column = 2)
#         self._retryLabel = Label(self._window, text = None)
#         self._retryLabel.grid(row = 1, column = 0, columnspan = 3)
#         self._validated = StringVar()
    
#     def submitChange(self):
#         newItem = self._newAttribute.get().title()
#         if newItem == "":
#             self._invalidText = "Invalid input, please try again"
#             self._retryLabel.configure(text = self._invalidText, font = 'bold', fg = 'red')
#             return
#         for index, item in enumerate(self._list):
#             if newItem == item.name:
#                 if self._delete:
#                     print('will delete', newItem)
#                     self._newItem = newItem
#                     self._validated.set("validated")
#                 else:
#                     self._invalidText = f"{newItem} already exists"
#                     self._retryLabel.configure(text = self._invalidText, font = 'bold', fg = 'red')
#                 break
#             elif index == len(self._list)-1:
#                 if self._delete:
#                     self._invalidText = f"{newItem} is not in the list"
#                     self._retryLabel.configure(text = self._invalidText, font = 'bold', fg = 'red')
#                 else:
#                     print(f"new attribute, {newItem}")
#                     self._newItem = newItem
#                     self._validated.set("validated")

#     def destroy(self):
#         self._window.destroy()
    
# class TrainerWindow(AttributeWindow):
#     def __init__(self, parent, list, delete):
#         super().__init__(parent, list, delete)
#         self._text = "Enter trainer's name"
#         self._textLabel.configure(text = self._text)  

# class ItemWindow(AttributeWindow):
#     def __init__(self, parent, list, delete):
#         super().__init__(parent, list, delete)
#         self._text = "Enter item name"
#         self._textLabel.configure(text = self._text)