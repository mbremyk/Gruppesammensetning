import re


class Student:
    def __init__(self, email, name, prog, worktime, partners):
        self.email = email
        self.name = name
        self.prog = 'JavaScript' in prog or 'språk' in prog
        self.worktime = worktime
        if partners:
            self.partners = re.split('[;,]', partners)
            self.partners = list(map(lambda p: p.strip(), self.partners))
        else:
            self.partners = []

    def __str__(self):
        return 'Student{email: %s, name: %s, prog: %s, worktime: %s, partners: %s}' % (
            self.email, self.name, self.prog, self.worktime, self.partners)
