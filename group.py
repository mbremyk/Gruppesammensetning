class Group:
    def __init__(self):
        self.members = []
        self.prog = False

    def getmemberbyname(self, name):
        for m in self.members:
            if m.name == name:
                return m

    def addmember(self, member):
        if member in self.members:
            raise ValueError('Member already in group')
        self.members.append(member)
        if member.prog:
            self.prog = True

    def __str__(self):
        s = 'Group{'
        for m in self.members:
            s += m.name + ','
        s += 'hasprogrammer: %s' % self.prog
        s += '}'
        return s
