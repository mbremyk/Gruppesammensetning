from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import openpyxl as opxl
from student import Student
from group import Group
from groupregister import GroupRegister
from multicolumntreeview import MultiColumnTreeView

pad = 10
defaultmaxmembers = 5


def handleselectfile():
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

        numstudents.set(len(groupregister.students))

        lststudents.delete(0, END)
        for s in groupregister.students:
            lststudents.insert(END, s.name)
        btncreategroups['state'] = 'normal'
    else:
        btncreategroups['state'] = 'disabled'
        lststudents.delete(0, END)
        numstudents.set(0)


def handlecreategroups():
    groupregister.maxmembers = maxmembers.get()
    groupregister.creategroups(True)

    groupframe = Frame(frame)
    groupframe.grid(column=1, row=10, columnspan=2, sticky='nsew')
    canvas = Canvas(groupframe)
    grouplists = []

    groupscroll = Scrollbar(groupframe, orient='vertical', command=canvas.yview)

    grouplistframe = Frame(canvas)
    grouplistframe.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=grouplistframe, anchor="nw")
    canvas.configure(yscrollcommand=groupscroll.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    groupscroll.pack(side=RIGHT, fill=Y)

    for ix, g in enumerate(groupregister.groups):
        grouplists.append(MultiColumnTreeView(grouplistframe, headers, g.membertuples(), 'Gruppe %s' % ix))
    for gl in grouplists:
        gl.pack(fill=X)

    for s in groupregister.students:
        print(s)

    for g in groupregister.groups:
        print(g)


def createapp():
    global app
    app = Tk()
    app.title('Gruppesammensetning')
    app.geometry('1100x700')
    global frame
    frame = Frame(app)
    global filename
    filename = StringVar()
    global maxmembers
    maxmembers = IntVar()
    maxmembers.set(defaultmaxmembers)
    global numstudents
    numstudents = IntVar()
    numstudents.set(0)

    lblfile = Label(frame, text='Fil: ')
    lblfilename = Label(frame, textvariable=filename)
    btnselectfile = Button(frame, text='Velg fil', command=handleselectfile)

    spinmaxmembers = Spinbox(frame, from_=2, to=10, textvariable=maxmembers)
    lblmaxmembers = Label(frame, text='Maks medlemmer per gruppe: ')

    lblnumstudentstxt = Label(frame, text='Antall studenter: ')
    lblnumstudents = Label(frame, textvariable=numstudents)

    lblallstudents = Label(frame, text='Alle studenter')
    global btncreategroups
    btncreategroups = Button(frame, text='Opprett grupper', command=handlecreategroups, state='disabled')

    lststudentsframe = Frame(frame)
    global lststudents
    lststudents = Listbox(lststudentsframe)
    lststudentsscroll = Scrollbar(lststudentsframe, orient='vertical')

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
