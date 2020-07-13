from tkinter import *
from tkinter.ttk import *
import openpyxl as opxl
from student import Student
from group import Group
from groupregister import GroupRegister
from app import App

defaultmaxmembers = 5


def handlelistchange(evt):
    lst = evt.widget
    if len(app.groupregister.groups):
        app.btnmovestudent['state'] = 'normal'
    if not lst.curselection():
        return
    index = lst.curselection()[0]
    app.curstudent = app.groupregister.getstudentbyname(lst.get(index))
    if len(app.groupregister.groups):
        app.studentgroup.set(app.groupregister.getgroupindexbystudentname(app.curstudent.name) + 1)
    student = app.curstudent.gettuple()
    student = list(student)
    del (student[-1])
    student[2] = student[2].replace(';', '\n').strip('\n')
    for ix, s in enumerate(app.studentvariables):
        s.set(student[ix])
    app.txtmovestudent.set(app.fstrmovestudent % app.studentgroup.get())


def handlefilenamechange(filename):
    global groupregister
    if filename.get():
        wb = opxl.load_workbook(filename.get())
        ws = wb.active
        headers = [c.value[:27] for c in ws[1][3:]]
        headers[0], headers[1] = headers[1], headers[0]
        app.headers = headers
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
    temp = App(title='Gruppesammensetning', geometry='1400x700')
    temp.filename.trace_add('write', lambda name, index, mode, filename=temp.filename: handlefilenamechange(filename))
    temp.lststudents.bind('<<ListboxSelect>>', handlelistchange)

    return temp


if __name__ == '__main__':
    app = createapp()
    groupregister = GroupRegister(defaultmaxmembers)
    app.groupregister = groupregister
    app.mainloop()
