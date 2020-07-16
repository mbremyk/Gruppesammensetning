from tkinter import *
from tkinter import filedialog
import re
from multicolumntreeview import MultiColumnTreeView
import csv

pad = 5
defaultmaxmembers = 5
groupheaders = (
    "Group Code", "Title", "Description", "Group Set", "Available", "Personalization", "Self Enroll", "Max Enrollment",
    "Show Members", "Sign Up From Group List", "Sign Up Name", "Sign Up Instructions")
memberheaders = ("Group Code", "User Name", "Student Id", "First Name", "Last Name")
filetypes = [('Comma separated values', '*.csv'), ('All files', '*.*')]
defaultextension = '.csv'


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
        self.curstudent = None
        self.maxmembers = IntVar()
        self.maxmembers.set(defaultmaxmembers)
        self.__setup()
        self.__config()

    def __setup(self):
        lblfile = Label(self.frame, text='Fil: ')
        lblfile.grid(column=0, row=0, sticky='nw')

        txtfilename = Label(self.frame, textvariable=self.filename)
        txtfilename.grid(column=1, row=0, sticky='nw')

        btnselectfile = Button(self.frame, text='Velg fil', command=self.__handleselectfile)
        btnselectfile.grid(column=2, row=0, sticky='nw')

        lblmaxmembers = Label(self.frame, text='Maks medlemmer per gruppe: ')
        lblmaxmembers.grid(column=0, row=1, sticky='nw')

        self.spinmaxmembers = Spinbox(self.frame, from_=2, to=10, textvariable=self.maxmembers)
        self.spinmaxmembers.grid(column=1, row=1, sticky='nw')

        lblnumstudents = Label(self.frame, text='Antall studenter: ')
        lblnumstudents.grid(column=0, row=2, sticky='nw')

        txtnumstudents = Label(self.frame, textvariable=self.numstudents)
        txtnumstudents.grid(column=1, row=2, sticky='nw')

        lblallstudents = Label(self.frame, text='Alle studenter')
        lblallstudents.grid(column=0, row=3, sticky='nw')

        btnframe = Frame(self.frame)
        btnframe.grid(column=1, row=3, columnspan=2, sticky='nsew')

        self.btncreategroups = Button(btnframe, text='Opprett grupper', command=self.__handlecreategroups,
                                      state='disabled')
        self.btncreategroups.grid(column=0, row=0, sticky='nw', padx=pad)

        self.btnexportgroups = Button(btnframe, text='Eksporter grupper...', command=self.__exportgroups,
                                      state='disabled')
        self.btnexportgroups.grid(column=1, row=0, sticky='nw', padx=pad)

        self.btnexportgroupmembers = Button(btnframe, text='Eksporter gruppemedlemmer...',
                                            command=self.__exportgroupmembers,
                                            state='disabled')
        self.btnexportgroupmembers.grid(column=2, row=0, sticky='nw', padx=pad)

        self.lststudentsframe = Frame(self.frame)
        self.lststudentsframe.grid(column=0, row=10, sticky='nsew')

        self.lststudents = Listbox(self.lststudentsframe)

        lststudentsscroll = Scrollbar(self.lststudentsframe, orient='vertical')
        lststudentsscroll.pack(side=RIGHT, fill=Y)
        self.lststudents.pack(fill=BOTH, expand=1)
        self.lststudents.config(yscrollcommand=lststudentsscroll.set)
        lststudentsscroll.config(command=self.lststudents.yview)

        groupframe = Frame(self.frame)
        groupframe.grid(column=1, row=10, columnspan=2, rowspan=2, sticky='nsew')

        canvas = Canvas(groupframe)

        self.grouplistframe = Frame(canvas)

        canvas.create_window((0, 0), window=self.grouplistframe, anchor="nw")

        groupscrollx = Scrollbar(groupframe, orient='vertical', command=canvas.yview)
        groupscrollx.pack(side=RIGHT, fill=Y)

        groupscrolly = Scrollbar(groupframe, orient='horizontal', command=canvas.xview)
        groupscrolly.pack(side=BOTTOM, fill=X)

        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        canvas.configure(yscrollcommand=groupscrollx.set, xscrollcommand=groupscrollx.set)

        self.grouplistframe.bind(
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

        labeltexts = ['Navn: ', 'Email: ', 'Prog. erfaring: \n', 'Arbeidstid: ']
        labels = []
        texts = []
        for ix, l in enumerate(labeltexts):
            labels.append(Label(studentinfoframe, text=l))
            texts.append(Label(studentinfoframe, textvariable=self.studentvariables[ix]))
        lblstudentgroup = Label(studentinfoframe, text='Gruppe: ')
        self.spinstudentgroup = Spinbox(studentinfoframe, from_=0, to=0, textvariable=self.studentgroup)

        for ix, (lbl, txt) in enumerate(zip(labels, texts)):
            txt.config(width=30)
            lbl.grid(column=0, row=ix, sticky='nw')
            txt.grid(column=1, row=ix, sticky='ne')
        lblstudentgroup.grid(column=0, row=len(labels), sticky='nw')
        self.spinstudentgroup.grid(column=1, row=len(labels), sticky='nw')
        studentinfoframe.grid(column=0, row=11, sticky='nsew')

        self.txtmovestudent = StringVar()
        self.fstrmovestudent = 'Flytt til gruppe %d'
        self.txtmovestudent.set(self.fstrmovestudent % self.studentgroup.get())
        self.btnmovestudent = Button(studentinfoframe, textvariable=self.txtmovestudent, command=self.handlemovestudent,
                                     state='disabled')
        self.btnmovestudent.grid(column=0, row=len(labels) + 1, sticky='nsew')

    def __config(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=2)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_rowconfigure(10, weight=1)
        self.frame.grid(column=0, row=0, sticky='nsew', padx=2 * pad, pady=2 * pad)
        self.lststudentsframe.grid_columnconfigure(0, weight=1)
        self.lststudentsframe.grid_rowconfigure(0, weight=1)

    def __handleselectfile(self):
        self.filename.set(filedialog.askopenfilename(filetypes=(('Excel spreadsheet', '*.xlsx'), ('All files', '*.*'))))
        if self.filename.get():
            self.numstudents.set(len(self.groupregister.students))
            self.lststudents.delete(0, END)
            for s in self.groupregister.students:
                self.lststudents.insert(END, s.name + ' - ' + s.email)
            self.btncreategroups['state'] = 'normal'
        else:
            self.btncreategroups['state'] = 'disabled'
            self.lststudents.delete(0, END)
            self.numstudents.set(0)

    def __handlecreategroups(self):
        self.groupregister.maxmembers = self.maxmembers.get()
        self.groupregister.creategroups(True)
        self.grouplists = []

        for child in self.grouplistframe.winfo_children():
            child.destroy()

        for ix, g in enumerate(self.groupregister.groups):
            self.grouplists.append(
                MultiColumnTreeView(self.grouplistframe, self.headers, g.membertuples(), 'Gruppe %s' % (ix + 1)))
            self.grouplists[-1].tree.bind('<<TreeviewSelect>>', self.handletreeselect)
        for gl in self.grouplists:
            gl.pack(fill=X, expand=True)
        self.spinstudentgroup.config(from_=1, to=len(self.groupregister.groups))
        if self.curstudent:
            self.studentgroup.set(self.groupregister.getgroupindexbystudentemail(self.curstudent.email))
        self.btnexportgroups['state'] = 'normal'
        self.btnexportgroupmembers['state'] = 'normal'

    def __exportgroups(self):
        filename = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=defaultextension,
                                                initialfile='Grupper.csv')
        if not filename:
            return
        rows = []
        for ix, g in enumerate(self.groupregister.groups):
            rows.append(('Gruppe_gc_%s' % (ix + 1), 'Gruppe %d' % (ix + 1), '', 'Gruppe_gc_0', 'Y', '', 'N', '', '', '',
                         '', ''))
        file = open(filename, 'w', newline='')
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(rows)
        pass

    def __exportgroupmembers(self):
        filename = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=defaultextension,
                                                initialfile='Gruppemedlemmer.csv')
        if not filename:
            return
        rows = []
        for ix, g in enumerate(self.groupregister.groups):
            for s in g.members:
                names = s.name.split()
                firstname = ' '.join(names[:-1])
                lastname = names[-1]
                rows.append(('Gruppe_gc_%s' % (ix + 1), s.username, '', firstname, lastname))
        file = open(filename, 'w', newline='')
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(rows)
        pass

    def handletreeselect(self, evt):
        tree = evt.widget
        if tree.selection():
            name = tree.set(tree.selection()[0], column='Navn')
            email = tree.set(tree.selection()[0], column='E-postadresse')
            self.lststudents.select_clear(0, END)
            self.lststudents.select_set(self.lststudents.get(0, END).index(name + ' - ' + email))
            self.curstudent = self.groupregister.getstudentbyemail(
                self.lststudents.get(self.lststudents.curselection()[0]).split('-')[-1].strip())
            self.updatestudentinfolabels()
            for gl in tree.master.master.winfo_children():
                if isinstance(gl, MultiColumnTreeView) and gl.tree is not tree:
                    gl.tree.selection_set()
        pass

    def updatestudentinfolabels(self):
        if len(self.groupregister.groups):
            self.studentgroup.set(self.groupregister.getgroupindexbystudentemail(self.curstudent.email) + 1)
        student = self.curstudent.gettuple()
        student = list(student)
        del (student[-1])
        student[2] = student[2].replace(';', '\n').strip('\n')
        for ix, s in enumerate(self.studentvariables):
            s.set(student[ix])
        self.txtmovestudent.set(self.fstrmovestudent % self.studentgroup.get())

    def handlespin(self, var, blank, mode):
        self.txtmovestudent.set(self.fstrmovestudent % self.studentgroup.get())
        if self.curstudent and self.groupregister.getgroupindexbystudentemail(
                self.curstudent.email) is not self.studentgroup.get():
            self.btnmovestudent['state'] = 'normal'
        else:
            self.btnmovestudent['state'] = 'disabled'

    def handlemovestudent(self):
        if self.curstudent:
            tree = self.grouplists[self.groupregister.getgroupindexbystudentemail(self.curstudent.email)].tree
            tree.delete(tree.selection())
            tree = self.grouplists[int(self.spinstudentgroup.get()) - 1].tree
            tree.insert('', END, values=self.curstudent.gettuple())
            self.groupregister.movestudent(self.curstudent,
                                           self.groupregister.groups[int(self.spinstudentgroup.get()) - 1], True)
        pass
