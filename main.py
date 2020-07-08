from tkinter import *
from tkinter.ttk import *
import openpyxl as opxl
from student import Student
from group import Group
from multicolumntreeview import MultiColumnTreeView
from app import App


global curstudent
global lststudents
global numstudents
numstudents = IntVar()
numstudents.set(0)


def handlelistchange(evt):
    lst = evt.widget
    if len(groupregister.groups):
        btnmovestudent['state'] = 'normal'
    if not lst.curselection():
        return
    index = lst.curselection()[0]
    global curstudent
    curstudent = groupregister.getstudentbyname(lst.get(index))
    studentgroup.set(groupregister.getgroupindexbystudentname(curstudent.name) + 1)
    student = curstudent.gettuple()
    student = list(student)
    del (student[-1])
    student[2] = student[2].replace(';', '\n').strip('\n')
    for ix, s in enumerate(studentvariables):
        s.set(student[ix])
    txtmovestudent.set(fstrmovestudent % studentgroup.get())


def handlemovestudent():
    if curstudent:
        groupregister.movestudent(curstudent, groupregister.groups[int(spinstudentgroup.get()) - 1], True)
        print(groupregister.getgroupindexbystudentname(curstudent.name))
    pass


def handlespin(var, blank, mode):
    txtmovestudent.set(fstrmovestudent % studentgroup.get())


def createapp():
    global app
    app = App(title='Gruppesammensetning', geometry='1200x700')
    # global frame
    # frame = Frame(app)

    global lststudents
    lststudents = Listbox(lststudentsframe)
    lststudents.bind('<<ListboxSelect>>', handlelistchange)
    lststudentsscroll = Scrollbar(lststudentsframe, orient='vertical')

    groupframe = Frame(frame)
    canvas = Canvas(groupframe)
    global grouplistframe
    grouplistframe = Frame(canvas)
    groupscroll = Scrollbar(groupframe, orient='vertical', command=canvas.yview)

    grouplistframe.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    studentinfoframe = Frame(frame)
    global studentvariables
    studentvariables = [StringVar(), StringVar(), StringVar(), StringVar()]
    for s in studentvariables:
        s.set('')
    global studentgroup
    studentgroup = IntVar()
    studentgroup.set(0)

    studentgroup.trace('w', handlespin)

    labeltexts = ['Navn: ', 'Email: ', 'Prog. erfaring: ', 'Arbeidstid: ']
    labels = []
    texts = []
    for ix, l in enumerate(labeltexts):
        labels.append(Label(studentinfoframe, text=l))
        texts.append(Label(studentinfoframe, textvariable=studentvariables[ix]))
    lblstudentgroup = Label(studentinfoframe, text='Gruppe: ')
    global spinstudentgroup
    spinstudentgroup = Spinbox(studentinfoframe, from_=0, to=0, textvariable=studentgroup)

    for ix, (lbl, txt) in enumerate(zip(labels, texts)):
        txt.config(width=30)
        lbl.grid(column=0, row=ix, sticky='nw')
        txt.grid(column=1, row=ix, sticky='nw')
    lblstudentgroup.grid(column=0, row=len(labels), sticky='nw')
    spinstudentgroup.grid(column=1, row=len(labels), sticky='nw')
    studentinfoframe.grid(column=0, row=11, sticky='nsew')

    global fstrmovestudent
    global txtmovestudent
    global btnmovestudent
    txtmovestudent = StringVar()
    fstrmovestudent = 'Flytt til gruppe %d'
    txtmovestudent.set(fstrmovestudent % studentgroup.get())
    btnmovestudent = Button(studentinfoframe, textvariable=txtmovestudent, command=handlemovestudent, state='disabled')
    btnmovestudent.grid(column=0, row=len(labels) + 1, sticky='nsew')

    lblfile.grid(column=0, row=0, sticky='nw')
    lblfilename.grid(column=1, row=0, sticky='nw')
    btnselectfile.grid(column=2, row=0, sticky='nw')

    lblmaxmembers.grid(column=0, row=1, sticky='nw')
    spinmaxmembers.grid(column=1, row=1, sticky='nw')

    lblnumstudentstxt.grid(column=0, row=2, sticky='nw')
    lblnumstudents.grid(column=1, row=2, sticky='nw')

    lblallstudents.grid(column=0, row=3, sticky='nw')
    btncreategroups.grid(column=2, row=3, sticky='nw')

    lststudentsframe.grid(column=0, row=10, sticky='nsew')

    lststudentsscroll.pack(side=RIGHT, fill=Y)
    lststudents.pack(fill=BOTH, expand=1)

    lststudents.config(yscrollcommand=lststudentsscroll.set)
    lststudentsscroll.config(command=lststudents.yview)

    groupframe.grid(column=1, row=10, columnspan=2, rowspan=2, sticky='nsew')

    canvas.create_window((0, 0), window=grouplistframe, anchor="nw")
    canvas.configure(yscrollcommand=groupscroll.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    groupscroll.pack(side=RIGHT, fill=Y)

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=2)
    frame.grid_columnconfigure(2, weight=0)
    frame.grid_rowconfigure(10, weight=1)
    frame.grid(column=0, row=0, sticky='nsew', padx=pad, pady=pad)
    lststudentsframe.grid_columnconfigure(0, weight=1)
    lststudentsframe.grid_rowconfigure(0, weight=1)

    return app


if __name__ == '__main__':
    app = createapp()
    app.mainloop()
