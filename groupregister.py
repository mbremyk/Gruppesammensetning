from group import Group
from student import Student
from math import ceil


class GroupRegister:
    def __init__(self, maxmembers):
        self.groups = []
        self.students = []
        self.maxmembers = maxmembers

    def __iadd__(self, other):
        if isinstance(other, GroupRegister):
            self.groups += other.groups
        elif isinstance(other, Group):
            self.groups += other
        elif isinstance(other, Student):
            self.students += other
        elif isinstance(other, list) and all(isinstance(g, Group) for g in other):
            self.groups += other
        elif isinstance(other, list) and all(isinstance(s, Student) for s in other):
            self.students += other
        else:
            raise TypeError('Cannot add non-GroupRegister, -Group, or -Student to object of type GroupRegister')
        self.__updatepartners()
        return self

    def __getstudentbyname(self, name):
        for s in self.students:
            if s.name == name:
                return s

    def creategroups(self):
        day = [s for s in self.students if s.worktime == 'Dagtid']
        night = [s for s in self.students if s.worktime == 'Kveldstid']
        flex = [s for s in self.students if s.worktime == 'Fleksibel']
        self.groups += self.__creategroups(day)
        self.groups += self.__creategroups(night)
        self.__fill(flex + [s for s in day if not s.hasgroup] + [s for s in night if not s.hasgroup])
        notgrouped = [s for s in day if not s.hasgroup] + [s for s in night if not s.hasgroup] + [s for s in flex if not s.hasgroup]
        self.groups += self.__creategroups(notgrouped)

    def __creategroups(self, students):
        groups = []
        for n in range(ceil(len(students) / self.maxmembers)):
            groups.append(Group())
        for s in students:
            if not s.hasgroup:
                for g in groups:
                    for p in s.partners:
                        if g.hasmember(p) and len(g.members) < self.maxmembers and not s.hasgroup:
                            self.__addmembertogroup(s, g)
                            s.partners.remove(p)
                            break
                    if s.hasgroup:
                        break
                    if len(g.members) < self.maxmembers - len(s.partners) and not s.hasgroup:
                        self.__addmembertogroup(s, g)
                        for p in s.partners:
                            if not p.hasgroup:
                                self.__addmembertogroup(p, g)
                                s.partners.remove(p)
                        break
        return groups

    def __addmembertogroup(self, student, group):
        if len(group) >= self.maxmembers:
            raise OverflowError('Group is full')
        if student.hasgroup:
            raise ValueError('Student already in a group')
        group.addmember(student)
        for p in student.partners:
            if len(group) < self.maxmembers and not p.hasgroup:
                try:
                    self.__addmembertogroup(p, group)
                except OverflowError as error:
                    print(error)
                    break
                except ValueError as error:
                    print(error)
                    continue
        for m in group.members:
            if m in student.partners:
                student.partners.remove(m)

    def __updatestrpartners(self):
        for s in self.students:
            for p in s.strpartners:
                partner = self.__getstudentbyname(p)
                if partner and s.name not in partner.strpartners:
                    partner.strpartners.append(s.name)

    def __updatepartners(self):
        self.__updatestrpartners()
        for s in self.students:
            for p in s.strpartners:
                partner = self.__getstudentbyname(p)
                if partner and partner not in s.partners:
                    s.partners.append(self.__getstudentbyname(p))

    def __fill(self, students):
        for g in self.groups:
            if len(g) < self.maxmembers:
                if not g.prog:
                    for s in students:
                        if s.prog and not s.hasgroup:
                            self.__addmembertogroup(s, g)
                else:
                    for s in students:
                        if len(g) < self.maxmembers - len(s.partners) and not s.hasgroup:
                            self.__addmembertogroup(s, g)
                        else:
                            break
                for s in students:
                    if len(g) < self.maxmembers and not s.hasgroup:
                        self.__addmembertogroup(s, g)
