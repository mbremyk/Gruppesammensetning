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
progindex = 3


class App(Tk):
    """
    A class representing the tk app that handles all GUI related stuff

    Attributes
    ----------
    frame : Frame
        Contains all GUI elements of the app
    title : str
        The title of the app, appears in the top bar of the window
    geometry : str
        String matching /[1-9][0-9]*x[1-9][0-9]*/ representing the shape of the window
    debug : bool
        Sets whether the debug parts of the window are shown. Cant be toggled with F3
    """

    def __init__(self, title='', geometry='', debug=False):
        """
        :param title: The title of the app, appears in the top bar of the window
        :type title: str
        :param geometry: String matching /[1-9][0-9]*x[1-9][0-9]*/ representing the shape of the window
        :type geometry: str
        :param debug: Sets whether the debug parts of the window are shown. Cant be toggled with F3
        :type debug: bool
        """

        super().__init__()
        if title:
            self.title(title)
        if re.fullmatch("[1-9][0-9]*x[1-9][0-9]*", geometry):
            self.geometry(geometry)
        self.frame = Frame(self)
        self.numstudents = IntVar()
        self.numstudents.set(0)
        self.filename = StringVar()
        self.curstudent = None
        self.maxmembers = IntVar()
        self.maxmembers.set(defaultmaxmembers)
        self.__setup()
        self.__config()
        self.debug = debug
        self.debugstr = StringVar()

    def __setup(self):
        """
        Sets up all the static GUI elements of the app
        Should probably be separated into different methods

        :return: None
        :rtype: None
        """

        #
        #           Filename
        #
        lblfile = Label(self.frame, text='Fil: ')
        lblfile.grid(column=0, row=0, sticky='nw')

        txtfilename = Label(self.frame, textvariable=self.filename)
        txtfilename.grid(column=1, row=0, sticky='nw')

        btnselectfile = Button(self.frame, text='Velg fil', command=self.__handleselectfile)
        btnselectfile.grid(column=2, row=0, sticky='nw')

        #
        #           Max members
        #
        lblmaxmembers = Label(self.frame, text='Maks medlemmer per gruppe: ')
        lblmaxmembers.grid(column=0, row=1, sticky='nw')

        self.spinmaxmembers = Spinbox(self.frame, from_=2, to=10, textvariable=self.maxmembers)
        self.spinmaxmembers.grid(column=1, row=1, sticky='nw')

        #
        #           Number of students
        #
        lblnumstudents = Label(self.frame, text='Antall studenter: ')
        lblnumstudents.grid(column=0, row=2, sticky='nw')

        txtnumstudents = Label(self.frame, textvariable=self.numstudents)
        txtnumstudents.grid(column=1, row=2, sticky='nw')

        #
        #           All students label
        #
        lblallstudents = Label(self.frame, text='Alle studenter')
        lblallstudents.grid(column=0, row=3, sticky='nw')

        #
        #           Buttons related to creating and exporting groups
        #
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

        self.strexport = StringVar()
        self.exporttexts = ['', 'Grupper eksportert', 'Gruppemedlemmer eksportert', 'Eksport av grupper ble avbrutt',
                            'Eksport av gruppemedlemmer ble avbrutt', 'Siste endringer er ikke eksportert']
        self.strexport.set(self.exporttexts[0])
        self.txtexport = Label(btnframe, textvariable=self.strexport, font='TkDefaultFont 9 bold')
        self.txtexport.grid(column=10, row=0, sticky='se', padx=pad)

        #
        #           Scrollable list of students
        #
        self.lststudentsframe = Frame(self.frame)
        self.lststudentsframe.grid(column=0, row=10, sticky='nsew')

        self.lststudents = Listbox(self.lststudentsframe)

        lststudentsscroll = Scrollbar(self.lststudentsframe, orient='vertical')
        lststudentsscroll.pack(side=RIGHT, fill=Y)
        self.lststudents.pack(fill=BOTH, expand=1)
        self.lststudents.config(yscrollcommand=lststudentsscroll.set)
        lststudentsscroll.config(command=self.lststudents.yview)
        self.lststudents.bind('<<ListboxSelect>>', self.__handlelistchange)

        #
        #           Scrollable list of groups
        #
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

        #
        #           Information about selected student
        #
        self.studentvariables = [StringVar(), StringVar(), StringVar(), StringVar(), StringVar()]
        for s in self.studentvariables:
            s.set('')

        studentinfoframe = Frame(self.frame)
        self.studentgroup = IntVar()
        self.studentgroup.set(0)

        self.studentgroup.trace('w', self.__handlespin)

        labeltexts = ['Navn: ', 'Email: ', 'Brukernavn', 'Prog. erfaring: \n', 'Arbeidstid: ']
        labels = []
        texts = []
        for ix, l in enumerate(labeltexts):
            labels.append(Label(studentinfoframe, text=l))
            texts.append(Label(studentinfoframe, textvariable=self.studentvariables[ix], justify=LEFT))
        lblstudentgroup = Label(studentinfoframe, text='Gruppe: ')
        self.spinstudentgroup = Spinbox(studentinfoframe, from_=0, to=0, textvariable=self.studentgroup)

        for ix, (lbl, txt) in enumerate(zip(labels, texts)):
            txt.config(width=30)
            lbl.grid(column=0, row=ix, sticky='nw')
            txt.grid(column=1, row=ix, sticky='ne')
        lblstudentgroup.grid(column=0, row=len(labels), sticky='nw')
        self.spinstudentgroup.grid(column=1, row=len(labels), sticky='nw')
        studentinfoframe.grid(column=0, row=11, sticky='nsew')

        #
        #           Button for moving a student
        #
        self.txtmovestudent = StringVar()
        self.fstrmovestudent = 'Flytt til gruppe %d'
        self.txtmovestudent.set(self.fstrmovestudent % self.studentgroup.get())
        self.btnmovestudent = Button(studentinfoframe, textvariable=self.txtmovestudent,
                                     command=self.__handlemovestudent,
                                     state='disabled')
        self.btnmovestudent.grid(column=0, row=len(labels) + 1, sticky='nsew')

    def __config(self):
        """
        A method to separate the top level configurations from all the visible elements of the GUI

        :return: None
        :rtype: None
        """
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=0)
        self.frame.grid_columnconfigure(1, weight=2)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_rowconfigure(10, weight=1)
        self.frame.grid(column=0, row=0, sticky='nsew', padx=2 * pad, pady=2 * pad)
        self.lststudentsframe.grid_columnconfigure(0, weight=1)
        self.lststudentsframe.grid_rowconfigure(0, weight=1)
        self.bind_all('<F3>', self.__toggledebug)

    def __handleselectfile(self):
        """
        Event handler method for self.btnselectfile

        Prompts the user for a file
        The event handler of self.filename is called when self.filename changes
        Updates some values based on result of main.handlefilenamechange

        :return: None
        """
        self.filename.set(filedialog.askopenfilename(filetypes=(('Excel spreadsheet', '*.xlsx'), ('All files', '*.*'))))
        # Call to main.handlefilenamechange() here
        if self.filename.get():
            self.numstudents.set(len(self.groupregister.students))
            self.lststudents.delete(0, END)
            for s in self.groupregister.students:
                self.lststudents.insert(END, s.name + ' - ' + s.username)
            self.btncreategroups['state'] = 'normal'
        else:
            self.btncreategroups['state'] = 'disabled'
            self.lststudents.delete(0, END)
            self.numstudents.set(0)

    def __handlecreategroups(self):
        """
        Event handler method for self.btncreategroups

        Calls self.groupregister.creategroups and builds tables of the result in self.grouplistframe

        :return: None
        :rtype: None
        """
        self.strexport.set(self.exporttexts[5])
        self.txtexport['fg'] = 'blue'
        self.groupregister.maxmembers = self.maxmembers.get()
        self.groupregister.creategroups(True)
        self.grouplists = []

        for child in self.grouplistframe.winfo_children():
            child.destroy()

        for ix, g in enumerate(self.groupregister.groups):
            self.grouplists.append(
                MultiColumnTreeView(self.grouplistframe, self.headers, g.membertuples(), 'Gruppe %s' % (ix + 1)))
            self.grouplists[-1].tree.bind('<<TreeviewSelect>>', self.__handletreeselect)
        for gl in self.grouplists:
            gl.pack(fill=X, expand=True)
        self.spinstudentgroup.config(from_=1, to=len(self.groupregister.groups))
        if self.curstudent:
            self.studentgroup.set(self.groupregister.getgroupindexbystudentemail(self.curstudent.email))
        self.btnexportgroups['state'] = 'normal'
        self.btnexportgroupmembers['state'] = 'normal'

    def __exportgroups(self):
        """
        Event handler method for self.btnexportgroups

        Prompts the user for a location and a filename and saves a list of groups formatted for import into BlackBoard
        Most of the fields are empty, but could be filled if needed

        :return: None
        """
        filename = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=defaultextension,
                                                initialfile='Grupper.csv')
        if not filename:
            self.strexport.set(self.exporttexts[3])
            self.txtexport['fg'] = 'red'
            return
        rows = []
        for ix, g in enumerate(self.groupregister.groups):
            rows.append(('Gruppe_gc_%s' % (ix + 1), 'Gruppe %d' % (ix + 1), '', 'Gruppe_gc_0', 'Y', '', 'N', '', '', '',
                         '', ''))
        file = open(filename, 'w', newline='')
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(rows)
        self.strexport.set(self.exporttexts[1])
        self.txtexport['fg'] = 'green'
        pass

    def __exportgroupmembers(self):
        """
        Event handler method for self.btnexportgroups

        Prompts the user for a location and a filename and saves a list of group members formatted for import into BlackBoard

        :return: None
        """

        filename = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=defaultextension,
                                                initialfile='Gruppemedlemmer.csv')
        if not filename:
            self.strexport.set(self.exporttexts[4])
            self.txtexport['fg'] = 'red'
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
        self.strexport.set(self.exporttexts[2])
        self.txtexport['fg'] = 'green'
        pass

    def __handletreeselect(self, evt):
        """
        Event handler for user clicks in the groups lists

        Fetches information about the selected student, removes any selection from the other groups, and sets the
        appropriate selection in the student list

        :param evt: Event object for the TreeView selection
        :return: None
        """
        tree = evt.widget
        if tree.selection():
            name = tree.set(tree.selection()[0], column='Navn')
            username = tree.set(tree.selection()[0], column='Brukernavn')
            self.lststudents.select_clear(0, END)
            self.lststudents.select_set(self.lststudents.get(0, END).index(name + ' - ' + username))
            self.curstudent = self.groupregister.getstudentbyusername(
                self.lststudents.get(self.lststudents.curselection()[0]).split('-')[-1].strip())
            self.__updatestudentinfolabels()
            for gl in tree.master.master.winfo_children():
                if isinstance(gl, MultiColumnTreeView) and gl.tree is not tree:
                    gl.tree.selection_set()
        pass

    def __updatestudentinfolabels(self):
        """
        Method for updating the labels with info on the currentlyg selected student

        :return: None
        """
        if len(self.groupregister.groups):
            self.studentgroup.set(self.groupregister.getgroupindexbystudentusername(self.curstudent.username) + 1)
        student = self.curstudent.gettuple()
        student = list(student)
        self.debugstr.set(str(self.curstudent.strpartners) + '\n\n' + str(self.curstudent.partners))
        del (student[-1])
        student[progindex] = student[progindex].replace(';', '\n').strip('\n')
        for ix, s in enumerate(self.studentvariables):
            s.set(student[ix])
        self.txtmovestudent.set(self.fstrmovestudent % self.studentgroup.get())

    def __handlespin(self, var, blank, mode):
        """
        Event handler method for the spinbox representing the students group

        Updates the button for moving students to the appropriate number

        :param var: Variable from trace. Not used
        :param blank: Variable from trace. Not used
        :param mode: Variable from trace. Not used
        :return: None
        """
        self.txtmovestudent.set(self.fstrmovestudent % self.studentgroup.get())
        if self.curstudent and self.groupregister.getgroupindexbystudentemail(
                self.curstudent.email) != self.studentgroup.get() - 1:
            self.btnmovestudent['state'] = 'normal'
        else:
            self.btnmovestudent['state'] = 'disabled'

    def __handlemovestudent(self):
        """
        Event handler method for the button for moving a student

        Removes the student information from the old group view and adds it to the new group view.
        Moves the student with GroupRegister.movestudent

        :return: None
        """
        self.strexport.set(self.exporttexts[5])
        self.txtexport['fg'] = 'blue'
        if self.curstudent:
            tree = self.grouplists[self.groupregister.getgroupindexbystudentemail(self.curstudent.email)].tree
            tree.delete(tree.selection())
            tree = self.grouplists[int(self.spinstudentgroup.get()) - 1].tree
            tree.insert('', END, values=self.curstudent.gettuple())
            self.groupregister.movestudent(self.curstudent,
                                           self.groupregister.groups[int(self.spinstudentgroup.get()) - 1], True)
        pass

    def __toggledebug(self, event):
        """
        Toggles the debug view

        :param event: Keypress event for the F3 key
        :return: None
        """
        self.debug = not self.debug
        self.debugstr.set('Debug. Press F3 to close')
        if self.debug:
            self.txtdebug = Label(self.frame, textvariable=self.debugstr)
            self.txtdebug.grid(column=0, row=100, columnspan=100, sticky='nsew')
        else:
            if self.txtdebug:
                self.txtdebug.grid_forget()

    def __handlelistchange(self, evt):
        """
        Event handler method for clicks in the student list

        Fetches information about the selected student and updates the labels and TreeView selection of groups

        :param evt: Event object for the ListboxSelect event
        :return: None
        """
        lst = evt.widget
        if not lst.curselection():
            return
        index = lst.curselection()[0]
        self.curstudent = self.groupregister.getstudentbyusername(lst.get(index).split('-')[-1].strip())
        self.__updatestudentinfolabels()
        if len(self.groupregister.groups) and self.groupregister.getgroupindexbystudentemail(
                self.curstudent.email) >= 0:
            tree = self.grouplists[self.groupregister.getgroupindexbystudentusername(self.curstudent.username)].tree
            for item in tree.get_children():
                if tree.set(item, column='Brukernavn').lower() == self.curstudent.username.lower():
                    tree.selection_set(item)
                    tree.focus(item)
                    break
