from tkinter import *

app = Tk()
var = StringVar()
var.set("")
var.trace_add('write', lambda a, b, c: handlechange())


def handlechange():
    print('Handle')


def change():
    var.set("Noe")
    if var.get():
        print('If')

change()
