from student import Student


class Group:
    def __init__(self, maxmembers: int):
        self.members = []
        self.javascript = False
        self.olang = False
        self.time = ''
        self.maxmembers = maxmembers

    def getmemberbyname(self, name):
        for m in self.members:
            if m.name.lower() == name.lower():
                return m

    def addmember(self, member):
        if self.hasmember(member):
            raise ValueError('Member already in group')
        self.members.append(member)
        member.hasgroup = True
        for p in member.partners:
            if len(self) < self.maxmembers and not p.hasgroup:
                try:
                    self.addmember(p)
                except ValueError as error:
                    print(error)
                    continue
                except Exception as error:
                    print(error)
                    break
        for m in self.members:
            if m in member.partners:
                member.partners.remove(m)
        if member.javascript:
            self.javascript = True
        if member.olang:
            self.olang = True
        if not self.time:
            if 'tid' in member.worktime:
                self.time = member.worktime

    def hasmember(self, member):
        return member in self.members

    def __str__(self):
        s = 'Group{ members: {'
        for m in self.members:
            s += m.name + ', '
        s += '}, hasjavascript: %s, ' % self.javascript
        s += 'hasotherlanguage: %s' % self.olang
        s += 'worktime: %s' % self.time
        s += ' }'
        return s

    def __len__(self):
        return len(self.members)

    def __iadd__(self, other):
        if isinstance(other, Group):
            self.members += other.members
            if not self.time and other.time:
                self.time = other.time
            if other.javascript:
                self.javascript = True
            if other.olang:
                self.olang = True
        elif isinstance(other, Student):
            self.members += other
            if other.javascript:
                self.javascript = True
            if other.olang:
                self.olang = True
        else:
            raise TypeError('Cannot add non-Group or -Student object to object of type Group')
        return self

    def __bool__(self):
        return bool(self.members)

    __nonzero__ = __bool__

    def removemember(self, member):
        if member in self.members:
            self.members.remove(member)
            member.hasgroup = False
            if not any(s.javascript for s in self.members):
                self.javascript = False
            if not any(s.olang for s in self.members):
                self.olang = False
            if not any('tid' in s.worktime for s in self.members):
                self.time = ''
        else:
            raise ValueError('Student not member of group')

    def membertuples(self):
        tuples = []
        for m in self.members:
            tuples.append(m.gettuple())
        return tuples
