from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, ValueSequence, dict_factory
from datetime import datetime


'''
create_user(email: str, name:str, interests:[str]) -> dict

creates a new user and returns the created user's info
'''
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


'''
login_user(email: str) -> dict or None

returns the user's info if that user is a signed user else returns None
'''
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


'''
create_room(category: str, name: str, captain_email: str, captain_name: str, max_penalty: int, description: str)-> dict

creates a new room and returns the created room's info
'''
def create_room(category, name, captain_email, captain_name, max_penalty, description=None):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    batch = BatchStatement()

    captain = dict()
    captain[captain_email] = captain_name

    prepare = session.prepare('INSERT INTO rooms (category, name, description, level, exp, status, captain, max_penalty, progress, created_at) VALUES (?, ?, ?, 0, 0, \'open\', ?, ?, 0, ?)')
    batch.add(prepare, (category, name, description, captain, max_penalty, datetime.now()))

    prepare = session.prepare('UPDATE users SET room[?] = False WHERE email=?')
    batch.add(prepare, (category+'&^%'+name, captain_email))
    
    session.execute(batch)

    query = 'SELECT * FROM rooms WHERE category=%s and name=%s'
    result = session.execute(query, (category, name)).one()

    cluster.shutdown()

    return result


'''
enroll_room(category: str, name: str, crew_email: str, crew_name: str) -> dict

enrolls to the room and returns the room's info
'''
def enroll_room(category, name, crew_email, crew_name):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    batch = BatchStatement()

    crew = dict()
    crew[crew_email] = crew_name

    prepare = session.prepare('UPDATE rooms SET crew = crew + ? WHERE category=? and name=?')
    batch.add(prepare, (crew, category, name))

    prepare = session.prepare('UPDATE users SET room[?] = False WHERE email=?')
    batch.add(prepare, (category+'&^%'+name, crew_email))

    session.execute(batch)

    query = 'SELECT * FROM rooms WHERE category=%s and name=%s'
    result = session.execute(query, (category, name)).one()

    cluster.shutdown()

    return result


'''
recommend_room(email: str) -> ResultSet filled with dict

returns all rooms that the user interests in
'''
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


'''
recommend_crew(category: str, evaluate: [str]) -> dict filled with list

returns all users who interest in the category
'''
def recommend_crew(category, evaluate):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'SELECT email, name, interests, exp, achieve, evaluate FROM users'
    rows = session.execute(query)

    cluster.shutdown()

    result = dict()
    result['all'] = []
    result['category'] = []
    result['interests'] = []

    for row in rows:
        if category in row['interests'] and bool(set(evaluate).intersection(row['evaluate'] if bool(row['evaluate']) else set())):
            result['all'].append(row)
        
        elif category in row['interests']:
            result['category'].append(row)
        
        elif bool(set(evaluate).intersection(row['evaluate'] if bool(row['evaluate']) else set())):
            result['evaluate'].append(row)


    return result


'''
close_room(category: str, name: str) -> dict

changes the room's status and eturns the closed room's info
'''
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


'''
adjust_progress(categry: str, name: str, progress: int) -> dict

changes the room's progress and returns the room's info that the progress is adjusted
'''
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


'''
add_todo(category: str, name: str, email: str, todo: str) -> ResultSet filled with dict

adds todo into the user's list and returns the todo list of the user
'''
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


'''
clear_todo(category: str, name: str, email: str, todo: str) -> ResultSet filled with dict

changes the todo's status and returns the todo list of the user
'''
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


'''
end_room(category: str, name: str) -> dict

changes the room's status and each member's achieve, room list things and returns the ended room's info
'''
def end_room(category, name):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    batch = BatchStatement()

    query = 'UPDATE rooms SET status = \'end\' WHERE category=%s and name=%s'
    session.execute(query, (category, name))

    query = 'SELECT captain, crew from rooms WHERE category=%s and name=%s'
    room = session.execute(query, (category, name)).one()

    members = dict(room['captain'])
    members.update(dict(room['crew']))

    get_member = 'SELECT achieve, room FROM users WHERE email=\'{}\''
    get_attendance = 'SELECT attendee FROM attendance WHERE category=%s and name=%s'
    add_achieve = session.prepare('UPDATE users SET achieve = achieve + ? WHERE email=?')
    make_done = session.prepare('UPDATE users SET room[?] = True WHERE email=?')
    for email in members.keys():
        current_member = get_member.format(email)
        member = session.execute(current_member).one()

        member_room = dict(member['room'])
        
        done_num = 0
        for val in member_room.values():
            if val: done_num += 1

        if done_num==0:
            batch.add(add_achieve, ({'first study': datetime.now()}, email))
        
        elif done_num==9:
            batch.add(add_achieve, ({'tenth study': datetime.now()}, email))

        attendance = session.execute(get_attendance, (category, name))

        if attendance:
            is_absent = False

            for attendee in attendance['attendee']:
                if email not in attendee:
                    is_absent = True
                    break
        
            if not is_absent and 'regular attendance' not in member['achieve']:
                batch.add(add_achieve, ({'regular attendance': datetime.now()}, email))

        batch.add(make_done, (category+'&^%'+name, email))

    session.execute(batch)

    query = 'SELECT * from rooms WHERE category=%s and name=%s'
    result = session.execute(query, (category, name)).one()

    cluster.shutdown()

    return result


'''
update_user_exp(email: str, exp: str) -> dict

changes the user's exp and returns the user's info
'''
def update_user_exp(email, exp):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'UPDATE users SET exp = %s WHERE email=%s'
    session.execute(query, (exp, email))

    query = 'SELECT * from users WHERE email=\'{}\''.format(email)
    result = session.execute(query).one()

    cluster.shutdown()

    return result


'''
evaluate(email: str, eval: str) -> dict

adds into the user's evaluate list and returns the user's info
'''
def evaluate(email, eval):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'UPDATE users SET evaluate = evaluate + %s WHERE email=%s'
    session.execute(query, ([eval], email))

    query = 'SELECT * from users WHERE email=\'{}\''.format(email)
    result = session.execute(query).one()

    cluster.shutdown()

    return result


'''
study_rank(category: str) -> dict

returns all study's info related to category if category is specified else returns all study's info
'''
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


'''
user_rank() -> ResultSet filled with dict

returns all user's info
'''
def user_rank():
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory
    
    query = 'SELECT name, exp, achieve, evaluate FROM users'
    users = session.execute(query)

    cluster.shutdown()
    
    return users


'''
get_user(email: str) -> dict

returns the user's info
'''
def get_user(email):
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect('plannet')
    session.row_factory = dict_factory

    query = 'SELECT * FROM users WHERE email=\'{}\''.format(email)
    result = session.execute(query).one()

    cluster.shutdown()

    return result


'''
get_room(category: str, name: str, email: str) -> dict

returns the rooms's whole info if the user is the member of the room else returns the room's filtered info
'''
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