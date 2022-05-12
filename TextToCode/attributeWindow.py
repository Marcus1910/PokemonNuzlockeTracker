from tkinter import *

class AttributeWindow():
    def __init__(self, parent, list):
        self._parent = parent
        self._list = list
        self._window = Toplevel(self._parent)
        self._window.geometry("250x250")
        self._window.resizable(0,0)
        self._window.rowconfigure(0, weight = 2)
        self._window.columnconfigure(0, weight = 2)

        self._newAttributeLabel = Label(self._window, text = "enter Trainer's name")
        self._newAttributeLabel.grid(row = 0, column = 0)

        self._newAttribute = Entry(self._window)
        self._newAttribute.grid(row = 1, column = 0, sticky = N)

        self._submitButton = Button(self._window, text = "Submit")
        self._submitButton.grid(row = 3, column = 0)

        self.showTrainer()

    def showTrainer(self):
        trainersFrame = Frame(self._window)
        trainersFrame.grid(row = 2, column = 0, sticky = NSEW)
        itemScrollbar = Scrollbar(trainersFrame)
        itemScrollbar.grid(row = 0, column = 1, sticky = NS)
        itemBox = Listbox(trainersFrame, yscrollcommand = itemScrollbar.set)
        itemBox.grid(row = 0, column = 0)
        for item in self._list:
            itemBox.insert(END, item.name)
        itemScrollbar.configure(command = itemBox.yview)


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