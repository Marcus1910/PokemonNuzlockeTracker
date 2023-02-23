# import tkinter as tk
# from pokemonFrame import PokemonFrame as pf

# class PokemonFrame(tk.Frame):
#     def __init__(self, master, button):
#         super().__init__(master)

#         # self.grid(columnspan = 5)
#         self.button = button
#         self.button.grid(row = 0, column = 0)

# root = tk.Tk()

# # Create a blue frame
# frame = pf(root, button = tk.Button(root, text="get"))
# frame.config(bg = "green")
# frame.grid(row = 10, column = 10, sticky=tk.NSEW)

# button=tk.Button(frame, text="Click me!")
# button.grid(row = 1, column = 0)

# # Create a red button
# thisbutton = tk.Button(root, text="Chatgpt liegt!")
# thisbutton.config(bg="red", command = thisbutton.destroy)
# thisbutton.grid(row = 0, column = 0)

# root.mainloop()

# import tkinter as tk

# def button_command(index, number):
#     print(f"Button {index} pressed with parameters {index} and {number}")

# root = tk.Tk()

# for i, num in enumerate(range(9, 0, -1), start=1):
#     # create a button with a command that calls the button_command function with the index and number as parameters
#     button = tk.Button(root, text=f"Button {i}", command=lambda idx=i, n=num: button_command(idx, n))
#     button.pack()

# root.mainloop()

