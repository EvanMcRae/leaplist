# reference file for other widget types
# (most important one for us is obviously the checkbox -- it uses a BooleanVar() to reflect checked state)

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.resizable(False, False)
#padding defines left, top, right, bottom
content = ttk.Frame(root, padding=(3,3,12,12))
#(flat, sunken, raised, groove, ridge) defined by Tk
frame = ttk.Frame(content, borderwidth=2, relief="sunken", width=640,
height=480)
label = ttk.Label(content, text="Name")
entry = ttk.Entry(content)
onevar = tk.BooleanVar()
twovar = tk.BooleanVar()
threevar = tk.BooleanVar()
onevar.set(True)
twovar.set(False)
threevar.set(True)
one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar,
onvalue=True)
ok = ttk.Button(content, text="Okay")
cancel = ttk.Button(content, text="Cancel")
content.grid(column=0, row=0, sticky=('NSEW'))
frame.grid(column=0, row=0, columnspan=3, rowspan=3, sticky=('NSEW'))
label.grid(column=3, row=0, columnspan=2, sticky=('NW'), padx=5)
entry.grid(column=3, row=1, columnspan=2, sticky=('NEW'), pady=5, padx=5)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)
#('aqua', 'clam', 'alt', 'default', 'classic') defined by ttk
style = ttk.Style()
style.theme_use('default')
root.mainloop()