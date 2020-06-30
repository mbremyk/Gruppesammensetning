from tkinter import *
from tkinter import filedialog
import openpyxl as opxl
from student import Student
from group import Group
from groupregister import GroupRegister

pad = 10
defaultmaxmembers = 5


def handleselectfile():
    filename.set(filedialog.askopenfilename(filetypes=(('Excel spreadsheet', '*.xlsx'), ('All files', '*.*'))))
    if filename.get():
        btncreategroups['state'] = 'normal'
    else:
        btncreategroups['state'] = 'disabled'


def handlecreategroups():
    global groupregister
    groupregister = GroupRegister(maxmembers.get())
    wb = opxl.load_workbook(filename.get())
    ws = wb.active
    students = []
    for row in ws.iter_rows(2):
        vals = []
        for cell in row:
            vals.append(cell.value)
        students.append(Student(vals[3], vals[4], vals[5], vals[6], vals[7]))

    groupregister += students
    groupregister.creategroups()
    for s in students:
        print(s)

    for g in groupregister.groups:
        print(g)


def createapp():
    app = Tk()
    app.title('Gruppesammensetning')
    app.geometry('900x600')
    frame = Frame(app)
    global filename
    filename = StringVar()
    global maxmembers
    maxmembers = IntVar()
    maxmembers.set(defaultmaxmembers)

    lblfile = Label(frame, text='Fil: ')
    lblfilename = Label(frame, textvariable=filename)
    btnselectfile = Button(frame, text='Velg fil', command=handleselectfile)

    spinmaxmembers = Spinbox(frame, from_=2, to=10, textvariable=maxmembers)
    lblmaxmembers = Label(frame, text='Maks medlemmer per gruppe')

    global btncreategroups
    btncreategroups = Button(frame, text='Opprett grupper', command=handlecreategroups, state='disabled')

    lblfile.grid(column=0, row=0, sticky='nw')
    lblfilename.grid(column=1, row=0, sticky='nw')
    btnselectfile.grid(column=2, row=0, sticky='nw')

    lblmaxmembers.grid(column=0, row=1, sticky='nw')
    spinmaxmembers.grid(column=1, row=1, sticky='nw')

    btncreategroups.grid(column=0, row=2, sticky='nw')

    frame.grid_columnconfigure(0, weight=0)
    frame.grid_columnconfigure(1, weight=2)
    frame.grid_columnconfigure(2, weight=0)
    frame.grid(column=0, row=0, sticky='nsew', padx=pad, pady=pad)
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    return app


if __name__ == '__main__':
    app = createapp()
    app.mainloop()

    # for s in students:
    #     if not s.hasgroup:
    #         for g in groups:
    #             for p in s.partnersStr:
    #                 if g.hasmember(p) and len(g.members) < max_members:
    #                     g.addmember(s)
    #                     break
    #             if s.hasgroup:
    #                 break
    #             if len(g.members) < max_members - len(s.partnersStr):
    #                 g.addmember(s)
    #                 for p in s.partnersStr:
    #                     if not p.hasgroup:
    #                         g.addmember(p)
    #                         s.partnersStr.remove(p)
    #                 break
