from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, dict_factory
from datetime import datetime


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

    rows = session.execute('SELECT * FROM users WHERE email=\''+email+'\' ALLOW FILTERING')

    cluster.shutdown()

    if not rows:
        return None
    
    return rows[0]