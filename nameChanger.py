#File Name Modifier Program; removes whitespaces, underscores and dashes from file names, and or replaces them with other characters
#The code structure needs improvement and many bugs require fixing, but basic functionality seems to be working

from tkinter import *
from tkinter import ttk, filedialog
import os
oldNames = [] #storage for the Undo function (multiple "Undos" in a row not yet supported)
newNames = []
root = Tk()
v=StringVar()
d=StringVar()
tkvar = StringVar(root)
symbols = {"Underscore","Dash","Whitespace"}
tkvar.set("Underscore")
tkvar2 = StringVar(root)
symbols2 = {"Underscore","Dash","Whitespace","(No character)"}
tkvar2.set("Whitespace")
symbols = {"Underscore":"_" , "Dash":"-", "Whitespace":" ","(No character)":""}
class Wrapper: #the value keeps getting reset after replaceChar() calls, so needed a class wrapper to get a "static" variable
    undo = dict() #will contain newname:oldname as key-value pairs for the undo function
    path = "" #another value I wanted to be "static", the directory path

def replace(): #replace a special character with another character, or remove it altogether, from the file names
    for filename in os.listdir(Wrapper.path):
        oldNames.append(filename)
        idx = (filename.find(symbols[tkvar.get()]))+1
        newname = filename.replace(symbols[tkvar.get()],symbols[tkvar2.get()])
        newNames.append(newname)
        os.rename(Wrapper.path+filename,Wrapper.path+newname)

def replaceR(): #recursive version that works with subdirectories
    for direc, subdir, listfilename in os.walk(Wrapper.path):
        for filename in listfilename:
            oldNames.append(filename)
            idx = (filename.find(symbols[tkvar.get()])) + 1
            newname = filename.replace(symbols[tkvar.get()], symbols[tkvar2.get()])
            newNames.append(newname)
            src = os.path.join(direc, filename)  # NOTE CHANGE HERE
            dst = os.path.join(direc, newname)  # AND HERE
            os.rename(src, dst)


def undoChange(): #reverts one function call of "change()"
    for filename in os.listdir(Wrapper.path):
        os.rename(Wrapper.path+filename,Wrapper.path+Wrapper.undo[filename])


def undoChangeR(): #reverts one function call of "changeR()"
    for direc, subdir, listfilename in os.walk(Wrapper.path):
        for filename in listfilename:
            src = os.path.join(direc, filename)
            dst = os.path.join(direc, Wrapper.undo[filename]) #dictionary being used to revert names
            os.rename(src, dst)

def setDirectory():
    Wrapper.path = filedialog.askdirectory()
    Wrapper.path += "/"
    d.set(Wrapper.path)
    Wrapper.cState = "normal" #allows the change button to be clicked as the directory has been set
    changeBtn.config(state = "normal")

def undoFunc():
    if rBool.get() == 1:
        undoChangeR()
    else:
        undoChange()
    oldNames.clear()
    newNames.clear()
    undoBtn.config(state="disabled")
    v.set("Renaming Undone!")

def replaceFunc():
    if rBool.get() == 1:
        replaceR()
    else:
        replace()
    Wrapper.undo = dict((zip(newNames, oldNames)))
    undoBtn.config(state="normal")
    v.set("Renaming done!")

#UI configuration code
v.set("Press the button!")
root.title("Rename Files")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

replacement = StringVar()
rBool=IntVar()
undoBtn = ttk.Button(mainframe,text="Undo",command=undoFunc,state="disabled")
undoBtn.grid(column=2, row=4)
changeBtn = ttk.Button(mainframe, text="Change", command=replaceFunc, state = "disabled")
changeBtn.grid(column=1, row=4)
ttk.Button(mainframe,text="Select Folder...",command=setDirectory).grid(column=1, row=1)
popupMenu = OptionMenu(mainframe,tkvar,*symbols)
popupMenu2 = OptionMenu(mainframe,tkvar2,*symbols2)
ttk.Label(mainframe, text="Symbol to remove:").grid(column=1, row=2)
ttk.Label(mainframe, text="Replacement symbol:").grid(column=2, row=2)
ttk.Label(mainframe, textvariable=d).grid(column=2, row=1)
popupMenu.grid(row=3,column=1)
popupMenu2.grid(row=3,column=2)
ttk.Label(mainframe, textvariable=v).grid(column=3, row=4)
ttk.Checkbutton(mainframe,text="Recursive",variable=rBool).grid(row=1,column=4)
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()