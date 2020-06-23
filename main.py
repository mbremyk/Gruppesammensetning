from tkinter import filedialog
import openpyxl as opxl
from student import Student
from group import Group
from math import ceil

if __name__ == '__main__':
    max_members = int(input('Maximum amount of members in each group: '))

    filename = filedialog.askopenfilename()
    wb = opxl.load_workbook(filename)
    ws = wb.active
    students = []
    for row in ws.iter_rows(2):
        vals = []
        for cell in row:
            vals.append(cell.value)
        students.append(Student(vals[3], vals[4], vals[5], vals[6], vals[7]))
    for s in students:
        print(str(s))

    groups = []
    for n in range(ceil(int(len(students)) / max_members)):
        groups.append(Group())

    allstudents = Group()
    for s in students:
        allstudents.addmember(s)

    for s in students:
        partners = []
        for p in s.partners:
            partners.append(allstudents.getmemberbyname(p))
        s.partners = partners
        print(s)
