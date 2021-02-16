from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, ValueSequence, dict_factory
from datetime import datetime, date
from copy import deepcopy
import UDT


def create_user(email, name, interests):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query= 'INSERT INTO users (email, name, exp, interests, created_at) VALUES (%s, %s, 0, %s, %s)'
    session.execute(query, (email, name, interests, datetime.now()))
    
    query = 'SELECT * FROM users WHERE email=\'{}\''.format(email)
    result = session.execute(query).one()

    cluster.shutdown()

    return result


def login_user(email):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'SELECT * FROM users WHERE email=\'{}\''.format(email)
    result = session.execute(query).one()

    cluster.shutdown()

    if not result:
        return None
    
    return result


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


def recommend_room(email):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'SELECT interests FROM users WHERE email=\'{}\''.format(email)
    row = session.execute(query).one()

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


def study_rank(category=None):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory
    
    room_query = 'SELECT category, name, exp, progress, crew, status FROM rooms'
    attendance_query = 'SELECT category, name, attendee FROM attendance'
    penalty_query = 'SELECT category, name, penalty FROM penalty'

    if category:
        additional = ' WHERE category=\'{}\''.format(category)
        
        room_query += additional
        attendance_query += (additional + ' ALLOW FILTERING')
        penalty_query += additional


    rooms = session.execute(room_query)
    attendance = session.execute(attendance_query)
    penalty = session.execute(penalty_query)

    cluster.shutdown()

    all = dict()

    for room in rooms:
        if room['status']=='start':
            temp = dict()

            temp['exp'] = room['exp']
            temp['progress'] = room['progress']
            temp['crew_num'] = len(room['crew'])+1 if room['crew'] else 1

            all[room['category']+'&^%'+room['name']] = temp

    for attend in attendance:
        key = attend['category']+'&^%'+attend['name']

        if key in all.keys():
            if 'attendance' not in all[key]:
                all[key]['attendance'] = []
            
            attend_rate = []
            for attendee in attend['attendee']:
                attend_rate.append(len(attendee)/temp['crew_num'])
        
        all[key]['attendance'] += attend_rate
    
    for pen in penalty:
        key = attend['category']+'&^%'+attend['name']

        if key in all.keys():
            if 'penalty' not in all[key]:
                all[key]['penalty'] = []
        
            all[key]['penalty'].append(pen['penalty'])
    
    return all


def user_rank():
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory
    
    query = 'SELECT name, exp, achieves, evaluate FROM users'
    users = session.execute(query)

    cluster.shutdown()
    
    return users


def get_user(email):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'SELECT * FROM users WHERE email=\'{}\''.format(email)
    result = session.execute(query).one()

    cluster.shutdown()

    return result


def get_room(category, name, email):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'SELECT * FROM rooms WHERE category=%s and name=%s'
    result = session.execute(query, (category, name)).one()

    cluster.shutdown()

    is_member = True if email in dict(result['crew']) else False
    if not is_member:
        del result['crew']
        del result['max_penalty']
        del result['link']

    return is_member, result