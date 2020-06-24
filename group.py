from student import Student


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
        member.hasgroup = True
        if member.prog:
            self.prog = True

    def hasmember(self, member):
        if member in self.members:
            return True
        return False

    def __str__(self):
        s = 'Group{'
        for m in self.members:
            s += m.name + ', '
        s += 'hasprogrammer: %s' % self.prog
        s += '}'
        return s

    def __len__(self):
        return len(self.members)

    def __iadd__(self, other):
        if isinstance(other, Group):
            self.members += other.members
            for m in other.members:
                if m.prog:
                    self.prog = True
                    break
        elif isinstance(other, Student):
            self.members += other
            if other.prog:
                self.prog = True
        else:
            raise TypeError('Cannot add non-Group or -Student object to object of type Group')
        return self
