import openpyxl as opxl
from student import Student
from groupregister import GroupRegister
from app import App

defaultmaxmembers = 5


def handlelistchange(evt):
    lst = evt.widget
    if not lst.curselection():
        return
    index = lst.curselection()[0]
    app.curstudent = app.groupregister.getstudentbyemail(lst.get(index).split('-')[-1].strip())
    app.updatestudentinfolabels()
    if len(app.groupregister.groups) and app.groupregister.getgroupindexbystudentemail(app.curstudent.email) >= 0:
        tree = app.grouplists[app.groupregister.getgroupindexbystudentemail(app.curstudent.email)].tree
        for item in tree.get_children():
            if tree.set(item, column='E-postadresse') == app.curstudent.email.lower():
                tree.selection_set(item)
                tree.focus(item)
                break


def handlefilenamechange(filename):
    global groupregister
    groupregister = GroupRegister(app.spinmaxmembers.get())
    app.groupregister = groupregister
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
            # vals[3:8] == [email, name, username, programming experience, preferred worktime, string of desired partners]
            student = Student(vals[3], vals[4], vals[5], vals[6], vals[7], vals[8])
            if not groupregister.getstudentbyemail(vals[3]):
                groupregister += student
            else:
                groupregister.updatestudent(vals[3], student)


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
