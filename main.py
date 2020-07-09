from tkinter import *
from tkinter.ttk import *
import openpyxl as opxl
from student import Student
from group import Group
from groupregister import GroupRegister
from multicolumntreeview import MultiColumnTreeView
from app import App

global curstudent
global numstudents
numstudents = IntVar()
numstudents.set(0)
defaultmaxmembers = 5
global maxmembers
maxmembers = IntVar()
maxmembers.set(defaultmaxmembers)


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


def handlefilenamechange(filename):
    global groupregister
    if filename.get():
        wb = opxl.load_workbook(filename.get())
        ws = wb.active
        headers = [c.value[:27] for c in ws[1][3:]]
        headers[0], headers[1] = headers[1], headers[0]
        for row in ws.iter_rows(2):
            vals = []
            for cell in row:
                vals.append(cell.value)
            # vals[3:7] == [email, name, programming experience, preferred worktime, string of desired partners]
            student = Student(vals[3], vals[4], vals[5], vals[6], vals[7])
            if not groupregister.getstudentbyname(vals[4]):
                groupregister += student
            else:
                groupregister.updatestudent(vals[4], student)


def createapp():
    app = App(title='Gruppesammensetning', geometry='1200x700')
    app.filename.trace_add('write', lambda name, index, mode, filename=app.filename: handlefilenamechange(filename))
    app.lststudents.bind('<<ListboxSelect>>', handlelistchange)

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
    global app
    global groupregister
    app = createapp()
    groupregister = GroupRegister(maxmembers.get())
    app.groupregister = groupregister
    app.mainloop()
