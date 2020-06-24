from tkinter import filedialog
import openpyxl as opxl
from student import Student
from group import Group
from math import ceil
from groupregister import GroupRegister


def creategroups(students, maxmembers):
    groups = []
    for n in range(ceil(len(students)/maxmembers)):
        groups.append(Group())
    for s in students:
        if not s.hasgroup:
            for g in groups:
                for p in s.partners:
                    if g.hasmember(p) and len(g.members) < maxmembers:
                        g.addmember(s)
                        s.partners.remove(p)
                        break
                if s.hasgroup:
                    break
                if len(g.members) < maxmembers - len(s.partners):
                    g.addmember(s)
                    for p in s.partners:
                        print(s.partners)
                        if not p.hasgroup:
                            g.addmember(p)
                            s.partners.remove(p)
                    break
    return groups


def fill(groups, students, maxmembers):
    return True


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

    allstudents = Group()
    for s in students:
        allstudents.addmember(s)
        s.hasgroup = False

    groups = []

    for s in students:
        partners = []
        for p in s.strpartners:
            if allstudents.getmemberbyname(p):
                partners.append(allstudents.getmemberbyname(p))
        s.partners = partners

    day = [s for s in students if s.worktime == 'Dagtid']
    night = [s for s in students if s.worktime == 'Kveldstid']
    flex = [s for s in students if s.worktime == 'Fleksibel']

    studlist = [day, night, flex]

    groups += creategroups(day, maxmembers)
    groups += creategroups(night, maxmembers)
    fill(groups, flex, maxmembers)

    for s in day:
        if not s.hasgroup:
            for g in groups:
                for p in s.partners:
                    if g.hasmember(p) and len(g.members) < maxmembers:
                        g.addmember(s)
                        s.partners.remove(p)
                        break
                if s.hasgroup:
                    break
                if len(g.members) < maxmembers - len(s.partners):
                    g.addmember(s)
                    for p in s.partners:
                        if not p.hasgroup:
                            g.addmember(p)
                            s.partners.remove(p)
                    break

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

    for g in groups:
        print(g)
