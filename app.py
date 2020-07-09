from tkinter import *
from tkinter import filedialog
from groupregister import GroupRegister
from student import Student
import openpyxl as opxl
import re

pad = 10
defaultmaxmembers = 5
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
        lblfile.grid(column=0, row=0, sticky='nw')

        txtfilename = Label(self.frame, textvariable=self.filename)
        txtfilename.grid(column=1, row=0, sticky='nw')

        btnselectfile = Button(self.frame, text='Velg fil', command=self.__handleselectfile)
        btnselectfile.grid(column=2, row=0, sticky='nw')

        lblmaxmembers = Label(self.frame, text='Maks medlemmer per gruppe: ')
        lblmaxmembers.grid(column=0, row=1, sticky='nw')

        spinmaxmembers = Spinbox(self.frame, from_=2, to=10, textvariable=maxmembers)
        spinmaxmembers.grid(column=1, row=1, sticky='nw')

        lblnumstudents = Label(self.frame, text='Antall studenter: ')
        lblnumstudents.grid(column=0, row=2, sticky='nw')

        txtnumstudents = Label(self.frame, textvariable=self.numstudents)
        txtnumstudents.grid(column=1, row=2, sticky='nw')

        lblallstudents = Label(self.frame, text='Alle studenter')
        lblallstudents.grid(column=0, row=3, sticky='nw')
        self.btncreategroups = Button(self.frame, text='Opprett grupper', command=self.__handlecreategroups,
                                      state='disabled')
        self.btncreategroups.grid(column=2, row=3, sticky='nw')

        lststudentsframe = Frame(self.frame)
        lststudentsframe.grid(column=0, row=10, sticky='nsew')

        self.lststudents = Listbox(lststudentsframe)
        self.lststudents.pack(fill=BOTH, expand=1)

        lststudentsscroll = Scrollbar(lststudentsframe, orient='vertical')
        lststudentsscroll.pack(side=RIGHT, fill=Y)

        self.lststudents.config(yscrollcommand=lststudentsscroll.set)
        self.lststudentsscroll.config(command=self.lststudents.yview)

        groupframe = Frame(self.frame)
        canvas = Canvas(groupframe)
        grouplistframe = Frame(canvas)
        groupscroll = Scrollbar(groupframe, orient='vertical', command=canvas.yview)

        grouplistframe.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        self.studentvariables = [StringVar(), StringVar(), StringVar(), StringVar()]
        for s in self.studentvariables:
            s.set('')

        studentinfoframe = Frame(self.frame)
        self.studentgroup = IntVar()
        self.studentgroup.set(0)

        self.studentgroup.trace('w', self.handlespin)

        labeltexts = ['Navn: ', 'Email: ', 'Prog. erfaring: ', 'Arbeidstid: ']
        labels = []
        texts = []
        for ix, l in enumerate(labeltexts):
            labels.append(Label(studentinfoframe, text=l))
            texts.append(Label(studentinfoframe, textvariable=self.studentvariables[ix]))
        lblstudentgroup = Label(studentinfoframe, text='Gruppe: ')
        global spinstudentgroup
        spinstudentgroup = Spinbox(studentinfoframe, from_=0, to=0, textvariable=self.studentgroup)

        self.txtmovestudent = StringVar()
        self.fstrmovestudent = 'Flytt til gruppe %d'
        self.txtmovestudent.set(self.fstrmovestudent % self.studentgroup.get())
        self.btnmovestudent = Button(studentinfoframe, textvariable=self.txtmovestudent, command=self.handlemovestudent,
                                     state='disabled')
        self.btnmovestudent.grid(column=0, row=len(labels) + 1, sticky='nsew')

        for ix, (lbl, txt) in enumerate(zip(labels, texts)):
            txt.config(width=30)
            lbl.grid(column=0, row=ix, sticky='nw')
            txt.grid(column=1, row=ix, sticky='nw')
        lblstudentgroup.grid(column=0, row=len(labels), sticky='nw')
        spinstudentgroup.grid(column=1, row=len(labels), sticky='nw')
        studentinfoframe.grid(column=0, row=11, sticky='nsew')

    def __handleselectfile(self):
        self.filename.set(filedialog.askopenfilename(filetypes=(('Excel spreadsheet', '*.xlsx'), ('All files', '*.*'))))
        if self.filename.get():
            self.numstudents.set(len(self.groupregister.students))
            self.lststudents.delete(0, END)
            for s in self.groupregister.students:
                self.lststudents.insert(END, s.name)
            self.btncreategroups['state'] = 'normal'
        else:
            self.btncreategroups['state'] = 'disabled'
            self.lststudents.delete(0, END)
            self.numstudents.set(0)

    def __handlecreategroups(self):
        self.groupregister.maxmembers = maxmembers.get()
        self.groupregister.creategroups(True)
        grouplists = []

        for ix, g in enumerate(self.groupregister.groups):
            grouplists.append(MultiColumnTreeView(grouplistframe, headers, g.membertuples(), 'Gruppe %s' % (ix + 1)))
            grouplists[-1].tree.bind('<<TreeviewSelect>>', self.handletreeselect)
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
            self.lststudents.select_clear(0, END)
            self.lststudents.select_set(self.lststudents.index(name))
        pass

    def handlespin(self, var, blank, mode):
        self.txtmovestudent.set(self.fstrmovestudent % self.studentgroup.get())
