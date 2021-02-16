from cassandra import NullHandler
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, ValueSequence, dict_factory
from datetime import datetime
import UDT


def create_user(email, name, interests):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory
    insert_user = session.prepare('INSERT INTO users (category, email, name, exp, interests, created_at) VALUES (?, ?, ?, 0, ?, ?)')

    batch = BatchStatement()

    created_at = datetime.now()

    for category in interests:
        batch.add(insert_user, (category, email, name, interests, created_at))

    session.execute(batch)
    
    query = 'SELECT * FROM users WHERE category=%s and email=%s'
    result = session.execute(query, (interests[0], email)).one()

    cluster.shutdown()

    return result


def login_user(email):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    row = session.execute('SELECT * FROM users WHERE email=\''+email+'\' ALLOW FILTERING').one()

    cluster.shutdown()

    if not row:
        return None
    
    return row


def create_room(category, name, captain_email, captain_name, max_penalty, description=None):
    cluster = Cluster(['127.0.0.1'])
    cluster.register_user_type('plannet', 'user', UDT.user)

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    captain = dict()
    captain[captain_email] = UDT.user(name=captain_name)

    query = 'INSERT INTO rooms (category, name, description, level, exp, status, captain, max_penalty, progress, created_at) VALUES (%s, %s, %s, 0, 0, \'open\', %s, %s, 0, %s)'
    session.execute(query, (category, name, description, captain, max_penalty, datetime.now()))

    query = 'SELECT * FROM rooms WHERE category=%s and name=%s'
    result = session.execute(query, (category, name)).one()

    cluster.shutdown()

    return result


def enroll_room(category, name, crew_email, crew_name):
    cluster = Cluster(['127.0.0.1'])
    cluster.register_user_type('plannet', 'user', UDT.user)

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    crew = dict()
    crew[crew_email] = UDT.user(name=crew_name)

    query = 'UPDATE rooms SET crew = crew + %s WHERE category=%s and name=%s'
    session.execute(query, (crew, category, name))

    query = 'SELECT * FROM rooms WHERE category=%s and name=%s'
    result = session.execute(query, (category, name)).one()

    cluster.shutdown()

    return result


def recommend_room(email, name):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    row = session.execute('SELECT interests FROM users WHERE email=\''+email+'\' ALLOW FILTERING').one()

    query = ('SELECT * FROM rooms WHERE category in %s')
    rows = session.execute(query, [ValueSequence(row['interests'])])

    cluster.shutdown()

    result = []
    for row in rows:
        captain =dict(row['captain'])
        for key in captain.keys():
            row['captain'][key] = UDT.user(captain[key])
        
        crew = dict(row['crew'])
        for key in crew.keys():
            crew[key] = UDT.user(crew[key])

        row['captain'] = captain
        row['crew'] = crew
        
        result.append(row)

    return result


def close_room(category, name):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'UPDATE rooms SET status = \'start\' WHERE category=%s and name=%s'
    session.execute(query, (category, name))

    query = 'SELECT * from rooms WHERE category=%s and name=%s'
    result = session.execute(query, (category, name)).one()

    cluster.shutdown()

    return result


def adjust_progress(category, name, progress):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'UPDATE rooms SET progress = %s WHERE category=%s and name=%s'
    session.execute(query, (progress, category, name))

    query = 'SELECT * from rooms WHERE category=%s and name=%s'
    result = session.execute(query, (category, name)).one()

    cluster.shutdown()

    return result