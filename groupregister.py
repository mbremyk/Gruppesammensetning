from group import Group
from student import Student
from math import ceil
from typing import List


class GroupRegister:
    """
    A class representing a list of Groups and Students, with methods for working with those

    Attributes
    ---------
    groups : list
        list of Group objects
    students : list
        list of Student objects
    maxmembers : int
        used for setting maximum amount of members in Groups in this GroupRegister when they are created
    """

    def __init__(self, maxmembers: int):
        """
        :param maxmembers: int
        """
        self.groups = []
        self.students = []
        self.maxmembers = maxmembers

    def __iadd__(self, other: object):
        """
        :param other: Object of type GroupRegister, Group, Student, list of Groups or list of Students
        :return self: App
        :raises TypeError: if other is not of suitable type, see param other
        """
        if isinstance(other, GroupRegister):
            self.groups += other.groups
        elif isinstance(other, Group):
            self.groups += other
        elif isinstance(other, Student):
            self.addstudent(other)
        elif isinstance(other, list) and all(isinstance(g, Group) for g in other):
            self.groups += other
            self.groups = list(set(self.groups))
        elif isinstance(other, list) and all(isinstance(s, Student) for s in other):
            self.students += other
            self.students = list(set(self.students))
        else:
            raise TypeError(
                'Cannot add non-GroupRegister, -Group, or -Student type object to object of type GroupRegister')
        self.__updatepartners()
        return self

    def addstudent(self, student: Student):
        """
        Adds a student to this GroupRegister's list of students and updates all Student's list of partners

        :param student: The student to add
        :return: None
        :raises ValueError: if student is already in self.students
        """
        if student in self.students:
            raise ValueError('Student already in register')
        self.students.append(student)
        self.__updatepartners()

    def getstudentbyname(self, name: str):
        for s in self.students:
            if s.name.lower() == name.lower():
                return s

    def getstudentbyemail(self, email: str):
        for s in self.students:
            if s.email.lower() == email.lower():
                return s

    def getstudentbyusername(self, username: str):
        for s in self.students:
            if s.username.lower() == username.lower():
                return s

    def creategroups(self, resetgroups=False):
        if resetgroups:
            self.groups = [Group(self.maxmembers) for x in range(ceil(len(self.students) / self.maxmembers))]
            self.__setallhasgroup(False)
        else:
            while len(self.groups) < ceil(len(self.students) / self.maxmembers):
                self.groups.append(Group(self.maxmembers))
        partners = [s for s in self.students if len(s.partners)]
        self.__createpartnergroups(partners)
        day = [s for s in self.students if s.worktime == 'Dagtid' and not s.hasgroup]
        night = [s for s in self.students if s.worktime == 'Kveldstid' and not s.hasgroup]
        flex = [s for s in self.students if s.worktime == 'Fleksibel' and not s.hasgroup]
        self.__fill(day)
        self.__fill(night)
        self.__shrinkgroups()
        while any(not s.hasgroup for s in self.students):
            notgrouped = [s for s in day if not s.hasgroup] + [s for s in night if not s.hasgroup] + [s for s in flex if
                                                                                                      not s.hasgroup]
            self.__fill(notgrouped, False)
            self.__shrinkgroups()
        self.__removeemptygroups()
        self.__updatepartners()

    def updatestudent(self, student, email=None, username=None):
        if email:
            self.students[self.students.index(self.getstudentbyemail(email))].update(student)
        elif username:
            self.students[self.students.index(self.getstudentbyusername(email))].update(student)
        else:
            raise ValueError(
                'Cannot find Student without identifying information. Both email and username cannot be None')
        self.__updatepartners()
        pass

    def getgroupindexbystudentname(self, name):
        for g in self.groups:
            if g.hasmember(self.getstudentbyname(name)):
                return self.groups.index(g)

    def getgroupindexbystudentemail(self, email):
        for g in self.groups:
            if g.hasmember(self.getstudentbyemail(email)):
                return self.groups.index(g)

    def getgroupindexbystudentusername(self, username):
        for g in self.groups:
            if g.hasmember(self.getstudentbyusername(username)):
                return self.groups.index(g)

    def __shrinkgroups(self):
        for g1 in self.groups:
            for g2 in self.groups:
                if g1 is g2:
                    continue
                if len(g1) + len(g2) <= self.maxmembers:
                    g1 += g2
                    self.groups.remove(g2)
                    self.groups.append(Group(self.maxmembers))

    def __removeemptygroups(self):
        for g in self.groups:
            if len(g) == 0:
                self.groups.remove(g)

    def __creategroups(self, students: List[Student]) -> []:
        groups = []
        for n in range(ceil(len(students) / self.maxmembers)):
            groups.append(Group(self.maxmembers))
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

    def __createpartnergroups(self, students: List[Student]):
        for s in students:
            if not s.hasgroup:
                for g in self.groups:
                    if len(g) == 0:
                        self.__addmembertogroup(s, g)
                        break
                    elif all(len(g) > 0 for g in self.groups) and len(g) < self.maxmembers - len(s.partners):
                        self.__addmembertogroup(s, g)
                        break

    def __addmembertogroup(self, student: Student, group: Group, ignorelimit=False) -> None:
        if len(group) >= self.maxmembers and not ignorelimit:
            raise Exception('Group is full')
        if student.hasgroup:
            raise ValueError('Student already in a group')
        group.addmember(student)

    def __updatestrpartners(self):
        for s in self.students:
            for p in s.strpartners:
                partner = self.getstudentbyname(p)
                if not partner:
                    partner = self.getstudentbyusername(p)
                if partner and s.name not in partner.strpartners and s.username not in partner.strpartners:
                    partner.strpartners.append(s.name)

    def __updatepartners(self):
        self.__updatestrpartners()
        for s in self.students:
            for p in s.strpartners:
                partner = self.getstudentbyname(p)
                if not partner:
                    partner = self.getstudentbyusername(p)
                if partner and partner not in s.partners:
                    s.partners.append(partner)

    def __fill(self, students: List[Student], checktime=True):
        for g in self.groups:
            if len(g) < self.maxmembers:
                if not g.javascript:
                    for s in students:
                        if s.javascript and not s.hasgroup and (
                                g.time == s.worktime or s.worktime == 'Fleksibel' or g.time == ''):
                            self.__addmembertogroup(s, g)
                            break
        for g in self.groups:
            if len(g) < self.maxmembers:
                if not g.olang:
                    for s in students:
                        if s.olang and not s.hasgroup and (
                                g.time == s.worktime or s.worktime == 'Fleksibel' or g.time == ''):
                            self.__addmembertogroup(s, g)
                            break
        for g in self.groups:
            for s in students:
                if len(g) < self.maxmembers and not s.hasgroup and (
                        not checktime or g.time == s.worktime or s.worktime == 'Fleksibel' or g.time == ''):
                    self.__addmembertogroup(s, g)

    def movestudent(self, student: Student, togroup: Group, ignorelimit=False):
        if len(togroup) >= self.maxmembers and not ignorelimit:
            raise Exception('Cannot move student to full group')
        for g in self.groups:
            if student in g.members:
                g.removemember(student)
                self.__addmembertogroup(student, togroup, True)
                break

    def __setallhasgroup(self, hasgroup):
        for s in self.students:
            s.hasgroup = hasgroup
