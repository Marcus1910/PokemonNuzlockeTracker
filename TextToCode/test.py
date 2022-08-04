import tkinter as tk
from tkinter import ttk

class MainGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Bolted Joint Analysis')
        self.geometry('500x500')
        # Adds tabs to main window
        self.nb = ttk.Notebook(self)
        self.nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')
        self.tab1 = ttk.Frame(self.nb)
        self.nb.add(self.tab1, text='Tab1')
        self.tab2 = ttk.Frame(self.nb)
        self.nb.add(self.tab2, text='Tab2')
        self.data = {}
        # defines a grid 50 x 50 cells in the main window & tabs
        rows = 0
        while rows < 50:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            self.tab1.rowconfigure(rows, weight=1)
            self.tab1.columnconfigure(rows, weight=1)
            self.tab2.rowconfigure(rows, weight=1)
            self.tab2.columnconfigure(rows, weight=1)
            rows += 1
        # Add Tab1 Labels
        self.boltLabel = tk.Label(self.tab1, text="Select A Bolt:")
        self.boltLabel.grid(column=0, row=1, sticky='SW')
        self.labelMajD = tk.Label(self.tab1, text="Bolt Major Dia. [in]:")
        self.labelMajD.grid(column=0, row=4, sticky='W')
        self.labelMinD = tk.Label(self.tab1, text="Bolt Minor Dia. [in]:")
        self.labelMinD.grid(column=0, row=5, sticky='W')
        self.labelPitchD = tk.Label(self.tab1, text="Bolt Pitch Dia. [in]:")
        self.labelPitchD.grid(column=0, row=6, sticky='W')
        # Add Tab1 Dropdown List - Bolt Choices
        self.boltValue = tk.StringVar()
        self.BoltList = ttk.Combobox(self.tab1, textvariable=self.boltValue, state='readonly')
        self.BoltList['values'] = ('', '#2-56 (UNC)', '1-1/2"-12 (UNF)', 'User Defined')
        self.BoltList.grid(column=0, row=2, sticky='NS')
        self.BoltList.current(0)
        self.BoltList.bind("<<ComboboxSelected>>", self.boltSelectFunc)
        # Add Tab1 Entry boxes to display values
        self.majDiaBox = tk.Entry(self.tab1)
        self.majDiaBox.insert(0, '0.0000')
        self.majDiaBox.configure(state='disabled')
        self.majDiaBox.grid(column=1, row=4, sticky='NS')
        self.minDiaBox = tk.Entry(self.tab1)
        self.minDiaBox.insert(0, '0.0000')
        self.minDiaBox.configure(state='disabled')
        self.minDiaBox.grid(column=1, row=5, sticky='NS')
        self.pitchDiaBox = tk.Entry(self.tab1)
        self.pitchDiaBox.insert(0, '0.0000')
        self.pitchDiaBox.configure(state='disabled')
        self.pitchDiaBox.grid(column=1, row=6, sticky='NS')

    def do_somthing_with_data(self):
        print(self.data)

    def boltSelectFunc(self, event):
        self.bolt = self.boltValue.get()
        print(self.bolt)

        if (self.bolt == ''):
            self.majDiaBox.configure(state='normal')
            self.majDiaBox.delete(0, 'end')
            self.majDiaBox.insert(0, '0.0000')
            self.majDiaBox.configure(state='disabled')
            self.minDiaBox.configure(state='normal')
            self.minDiaBox.delete(0, 'end')
            self.minDiaBox.insert(0, '0.0000')
            self.minDiaBox.configure(state='disabled')
            self.pitchDiaBox.configure(state='normal')
            self.pitchDiaBox.delete(0, 'end')
            self.pitchDiaBox.insert(0, '0.0000')
            self.pitchDiaBox.configure(state='disabled')

        elif (self.bolt == 'User Defined'):
            self.newBoltData = None
            ChildWindow(self)


            # self.boltSpecs = self.boltBasics(d, n)    # need to return d, n from child window to run this calculation

        else:
            if (self.bolt[0] == '#'):
                lhs, rhs = self.bolt.split("-")
                d = float(lhs[1:]) * 0.013 + .060
                n = float(rhs.split(" ")[0])
                self.boltSpecs = self.boltBasics(d, n)
                self.majDiaBox.configure(state='normal')
                self.majDiaBox.delete(0, 'end')
                self.majDiaBox.insert(0, format(self.boltSpecs['d'], '.4f'))
                self.majDiaBox.configure(state='disabled')
                self.minDiaBox.configure(state='normal')
                self.minDiaBox.delete(0, 'end')
                self.minDiaBox.insert(0, format(self.boltSpecs['dm'], '.4f'))
                self.minDiaBox.configure(state='disabled')
                self.pitchDiaBox.configure(state='normal')
                self.pitchDiaBox.delete(0, 'end')
                self.pitchDiaBox.insert(0, format(self.boltSpecs['dp'], '.4f'))
                self.pitchDiaBox.configure(state='disabled')
            else:
                lhs, rhs = self.bolt.split("\"-")
                n = float(rhs.split(" ")[0])
                if ("-" in lhs):
                    d = float(eval(lhs.replace("-", "+")))
                    self.boltSpecs = self.boltBasics(d, n)
                    self.majDiaBox.configure(state='normal')
                    self.majDiaBox.delete(0, 'end')
                    self.majDiaBox.insert(0, format(self.boltSpecs['d'], '.4f'))
                    self.majDiaBox.configure(state='disabled')
                    self.minDiaBox.configure(state='normal')
                    self.minDiaBox.delete(0, 'end')
                    self.minDiaBox.insert(0, format(self.boltSpecs['dm'], '.4f'))
                    self.minDiaBox.configure(state='disabled')
                    self.pitchDiaBox.configure(state='normal')
                    self.pitchDiaBox.delete(0, 'end')
                    self.pitchDiaBox.insert(0, format(self.boltSpecs['dp'], '.4f'))
                    self.pitchDiaBox.configure(state='disabled')
                else:
                    d = float(eval(lhs))
                    self.boltSpecs = self.boltBasics(d, n)
                    self.majDiaBox.configure(state='normal')
                    self.majDiaBox.delete(0, 'end')
                    self.majDiaBox.insert(0, format(self.boltSpecs['d'], '.4f'))
                    self.majDiaBox.configure(state='disabled')
                    self.minDiaBox.configure(state='normal')
                    self.minDiaBox.delete(0, 'end')
                    self.minDiaBox.insert(0, format(self.boltSpecs['dm'], '.4f'))
                    self.minDiaBox.configure(state='disabled')
                    self.pitchDiaBox.configure(state='normal')
                    self.pitchDiaBox.delete(0, 'end')
                    self.pitchDiaBox.insert(0, format(self.boltSpecs['dp'], '.4f'))
                    self.pitchDiaBox.configure(state='disabled')

    def boltBasics(self, d, n):
        P = 1.0 / n           # in - thread pitch
        dm = d - (1.299038 * P)  # in - external thread minor diameter
        dp = d - (0.649519 * P)  # in - bolt pitch Diameter
        return{'d': d, 'dm': dm, 'dp': dp}


class ChildWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.frame = tk.Frame(self)
        self.title('User Defined Bolt Info')
        self.geometry('350x250')
        self.focus_set()
        rows = 0
        while rows < 10:
            self.rowconfigure(rows, weight=1)
            self.columnconfigure(rows, weight=1)
            rows += 1

        self.boltName = tk.Label(self, text="Bolt Name (e.g. NewBolt1):")
        self.boltName.grid(column=5, row=1, sticky='NSEW')
        self.boltDia = tk.Label(self, text="Bolt Major Diameter [in]:")
        self.boltDia.grid(column=5, row=3, sticky='NSEW')
        self.boltTPI = tk.Label(self, text="Bolt Threads per Inch (TPI) [-]:")
        self.boltTPI.grid(column=5, row=5, sticky='NSEW')
        self.bName = tk.StringVar()
        self.bDia = tk.StringVar()
        self.bTPI = tk.StringVar()
        self.nameInput = tk.Entry(self, textvariable=self.bName)
        self.nameInput.insert(0, 'BoltName')
        self.nameInput.grid(column=5, row=2, sticky='NSEW')
        self.diaInput = tk.Entry(self, textvariable=self.bDia)
        self.diaInput.insert(0, '0.0000')
        self.diaInput.grid(column=5, row=4, sticky='NSEW')
        self.tpiInput = tk.Entry(self, textvariable=self.bTPI)
        self.tpiInput.insert(0, '0.0000')
        self.tpiInput.grid(column=5, row=6, sticky='NSEW')
        # Create button to save user defined bolt
        self.saveBoltBtn = tk.Button(self, text='Save Bolt', command=self.saveBolt)
        self.saveBoltBtn.bind('<Return>', self.saveBolt)
        self.saveBoltBtn.grid(column=5, row=8, sticky='NSEW')

    def saveBolt(self, *event):
        self.master.data = {}
        self.master.data['name'] = self.bName.get()
        self.master.data['d'] = float(self.bDia.get())
        self.master.data['n'] = float(self.bTPI.get())
        self.master.do_somthing_with_data()
        # NEED TO RETURN THIS DATA TO PARENT WINDOW
        self.destroy()


def main():
    MainGUI().mainloop()

if __name__ == '__main__':
    main()