from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

app = Tk()
app.title('Test')
app.geometry('600x400')

filename = StringVar()

tabcontrol = Notebook(app)
tabs = [Frame(tabcontrol), Frame(tabcontrol)]
for t in tabs:
    tabcontrol.add(t, text=str(tabs.index(t)))


def handleselectfile():
    filename.set(filedialog.askopenfilename())


btnselectfile = Button(app, text='Velg fil', command=handleselectfile)
lblfilename = Label(app, textvariable=filename)
btnselectfile.grid(column=0, row=0, sticky='nw')
lblfilename.grid(column=1, row=0, sticky='nw')
tabcontrol.grid(column=0, row=10, columnspan=2, sticky='nsew')
app.grid_columnconfigure(0, weight=1)
app.mainloop()
