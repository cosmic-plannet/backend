from os import name

from cassandra.cluster import EXEC_PROFILE_GRAPH_ANALYTICS_DEFAULT


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

    def __init__(self, other_user):
        self.name = other_user.name
        self.penalty = other_user.penalty
        self.attendance = other_user.attendance
        self.todo = dict(other_user.todo)
