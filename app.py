from tkinter import *
from tkinter import filedialog
from groupregister import GroupRegister
from student import Student
import openpyxl as opxl
import re

pad = 10
defaultmaxmembers = 5
global filename
filename = StringVar()
global maxmembers
maxmembers = IntVar()
maxmembers.set(defaultmaxmembers)


class App(Tk):
    def __init__(self, title='', geometry='', groupregister=None):
        super().__init__()
        if title:
            self.title(title)
        if re.fullmatch("[1-9][0-9]*x[1-9][0-9]*", geometry):
            self.geometry(geometry)
        self.frame = Frame(self)
        self.numstudents = IntVar()
        self.numstudents.set(0)
        self.filename = StringVar()
        self.groupregister = groupregister
        self.__setup()

    def __setup(self):
        lblfile = Label(self.frame, text='Fil: ')
        lblfilename = Label(self.frame, textvariable=filename)
        btnselectfile = Button(self.frame, text='Velg fil', command=self.__handleselectfile)

        spinmaxmembers = Spinbox(self.frame, from_=2, to=10, textvariable=maxmembers)
        lblmaxmembers = Label(self.frame, text='Maks medlemmer per gruppe: ')

        lblnumstudentstxt = Label(self.frame, text='Antall studenter: ')
        lblnumstudents = Label(self.frame, textvariable=self.numstudents)

        lblallstudents = Label(self.frame, text='Alle studenter')
        global btncreategroups
        btncreategroups = Button(self.frame, text='Opprett grupper', command=self.__handlecreategroups, state='disabled')

        lststudentsframe = Frame(self.frame)

    def __handleselectfile(self):
        filename.set(filedialog.askopenfilename(filetypes=(('Excel spreadsheet', '*.xlsx'), ('All files', '*.*'))))
        if filename.get():
            global groupregister
            groupregister = GroupRegister(maxmembers.get())
            wb = opxl.load_workbook(filename.get())
            ws = wb.active
            global headers
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

            self.numstudents.set(len(groupregister.students))

            lststudents.delete(0, END)
            for s in groupregister.students:
                lststudents.insert(END, s.name)
            btncreategroups['state'] = 'normal'
        else:
            btncreategroups['state'] = 'disabled'
            lststudents.delete(0, END)
            numstudents.set(0)

    def __handlecreategroups(self):
        groupregister.maxmembers = maxmembers.get()
        groupregister.creategroups(True)
        grouplists = []

        for ix, g in enumerate(groupregister.groups):
            grouplists.append(MultiColumnTreeView(grouplistframe, headers, g.membertuples(), 'Gruppe %s' % (ix + 1)))
        for gl in grouplists:
            gl.pack(fill=X, expand=True)
        spinstudentgroup.config(from_=1, to=len(groupregister.groups))
        studentgroup.set(1)
        if curstudent:
            btnmovestudent['state'] = 'normal'

        for s in groupregister.students:
            print(s)

        for g in groupregister.groups:
            print(g)

    def handletreeselect(self, evt):
        tree = evt.widget
        if tree.selection():
            name = tree.set(tree.selection()[0], column='Navn')
            lststudents.select_clear(0, END)
            lststudents.select_set(lststudents.index(name))
        pass
