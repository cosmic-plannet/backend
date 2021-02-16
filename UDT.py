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