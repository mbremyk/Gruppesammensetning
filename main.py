from tkinter import filedialog
import openpyxl as opxl
from student import Student
from group import Group
from groupregister import GroupRegister


if __name__ == '__main__':
    maxmembers = int(input('Maximum amount of members in each group: '))
    groupregister = GroupRegister(maxmembers)

    filename = filedialog.askopenfilename()
    wb = opxl.load_workbook(filename)
    ws = wb.active
    students = []
    for row in ws.iter_rows(2):
        vals = []
        for cell in row:
            vals.append(cell.value)
        students.append(Student(vals[3], vals[4], vals[5], vals[6], vals[7]))

    groupregister += students
    groupregister.creategroups()

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

    for s in students:
        print(s)

    for g in groupregister.groups:
        print(g)

    input()
