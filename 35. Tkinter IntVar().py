import tkinter as tk

master_window = tk.Tk()
master_window.geometry("250x150")
master_window.title("IntVar Example")

integer_variable = tk.IntVar(master_window, 255)
label = tk.Label(master_window, textvariable=integer_variable, height=250)
label.pack()

master_window.mainloop()