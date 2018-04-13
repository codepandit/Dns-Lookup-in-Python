from tkinter import *


root = Tk()

l1 = Label(root, text="NAME")
l2 = Label(root, text="PASS")
e1 = Entry(root)
e2 = Entry(root)
l1.grid(row=0, sticky=E)
l2.grid(row=1, sticky=E)
e1.grid(row=0,column=1)
e2.grid(row=1,column=1)
root.mainloop()