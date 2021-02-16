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

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    captain = dict()
    captain[captain_email] = captain_name

    query = 'INSERT INTO rooms (category, name, description, level, exp, status, captain, max_penalty, progress, created_at) VALUES (%s, %s, %s, 0, 0, \'open\', %s, %s, 0, %s)'
    session.execute(query, (category, name, description, captain, max_penalty, datetime.now()))

    query = 'SELECT * FROM rooms WHERE category=%s and name=%s'
    result = session.execute(query, (category, name)).one()

    cluster.shutdown()

    return result


def enroll_room(category, name, crew_email, crew_name):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    crew = dict()
    crew[crew_email] = crew_name

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

    return rows


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


def add_todo(category, name, email, todo):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'INSERT INTO todo (category, name, email, todo, done) VALUES (%s, %s, %s, %s, False)'
    session.execute(query, (category, name, email, todo))

    query = 'SELECT * from todo WHERE category=%s and name=%s and email=%s and todo=%s'
    result = session.execute(query, (category, name, email, todo))

    cluster.shutdown()

    return result


def clear_todo(category, name, email, todo):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'UPDATE todo SET done = True WHERE category=%s and name=%s and email=%s and todo=%s'
    session.execute(query, (category, name, email, todo))

    query = 'SELECT * from todo WHERE category=%s and name=%s and email=%s and todo=%s'
    result = session.execute(query, (category, name, email, todo))

    cluster.shutdown()

    return result