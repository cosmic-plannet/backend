class achieve(object):
    def __init__(self, type, created_at):
        self.type = type
        self.created_at = created_at


class room(object):
    def __init__(self, name, category, level, exp):
        self.name = name
        self.category = category
        self.level = level
        self.exp = exp


class user(object):
    def __init__(self, name, penalty=0, attendance=[], todo={}):
        self.name = name
        self.penalty = penalty
        self.attendance = attendance
        self.todo = todo