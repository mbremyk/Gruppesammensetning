import re


class Student:
    def __init__(self, email, name, username, prog, worktime, strpartners):
        self.email = email
        self.name = name
        self.username = username
        self.strprog = prog
        self.prog = 'JavaScript' in prog or 'språk' in prog
        self.worktime = worktime
        if strpartners:
            self.strpartners = re.split('[;,]', strpartners)
            self.strpartners = list(map(lambda p: p.strip(), self.strpartners))
        else:
            self.strpartners = []
        self.inputpartners = self.strpartners.copy()
        self.hasgroup = False
        self.partners = []

    def __str__(self):
        return 'Student{email: %s, name: %s, prog: %s, worktime: %s, hasgroup: %s, partners: %s}' % (
            self.email, self.name, self.prog, self.worktime, self.hasgroup, self.partners)

    def removepartner(self, partner):
        self.partners.remove(partner)

    def gettuple(self):
        return self.name, self.email, self.username, self.strprog, self.worktime, self.inputpartners

    def update(self, student):
        if not isinstance(student, Student):
            raise TypeError('Tried to update object of type Student with object not of type Student')
        self.email = student.email
        self.name = student.name
        self.username = student.username
        self.strprog = student.strprog
        self.prog = student.prog
        self.worktime = student.worktime
        self.strpartners = student.strpartners
        self.hasgroup = student.hasgroup
        self.partners = student.partners
