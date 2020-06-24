import re


class Student:
    def __init__(self, email, name, prog, worktime, strpartners):
        self.email = email
        self.name = name
        self.prog = 'JavaScript' in prog or 'språk' in prog
        self.worktime = worktime
        if strpartners:
            self.strpartners = re.split('[;,]', strpartners)
            self.strpartners = list(map(lambda p: p.strip(), self.strpartners))
        else:
            self.strpartners = []
        self.hasgroup = False
        self.partners = []

    def __str__(self):
        return 'Student{email: %s, name: %s, prog: %s, worktime: %s, hasgroup: %s, partners: %s}' % (
            self.email, self.name, self.prog, self.worktime, self.hasgroup, self.partners)
