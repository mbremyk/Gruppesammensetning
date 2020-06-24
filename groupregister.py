from group import Group
from student import Student


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
        else:
            raise TypeError('Cannot add non-GroupRegister, -Group, or -Student to object of type GroupRegister')
        return self
