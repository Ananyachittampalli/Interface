import tkinter as tk
from tkinter import ttk

def update_lbl(val):
    manual_label.config(text="Scale at " + val)

root = tk.Tk()
root.geometry("300x150")
root.title("Scale and Label Example")

num = tk.StringVar()
manual_label = ttk.Label(root)
manual_label.grid(column=0, row=1, sticky='we')

scale = ttk.Scale(root, orient='horizontal', length=200, from_=1.0, to=100.0, variable=num, command=update_lbl)
scale.grid(column=0, row=2, sticky='we')
scale.set(20)

auto_update_label = ttk.Label(root, textvariable=num)
auto_update_label.grid(column=0, row=0, sticky='we')

root.mainloop()

