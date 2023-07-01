import sqlite3
from pydantic import BaseModel


path_database = "C:/Users/Andrea/Desktop/pf3/database/database.db"

class EditUser(BaseModel):
    state: int
    id_user: str 

class InfoTicket(BaseModel):
    subject: str
    fullname: str
    email: str
    category: int



def getUser(username: str):
    c = sqlite3.connect(path_database)
    user = c.execute("SELECT * from admin where username=?", (username,)).fetchone()
    c.commit()
    c.close()
    return user

def get_users_data():
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()

    query = '''
        SELECT users.id_user, auth.username, auth.email, 
        COUNT(DISTINCT post.id_post) AS num_posts, 
        COUNT(DISTINCT comments.id_comment) AS num_comments,
        users.state, users.registration_date
        FROM users
        INNER JOIN auth on users.id_user = auth.id_user
        LEFT JOIN post ON users.id_user = post.id_user
        LEFT JOIN comments ON users.id_user = comments.id_user
        GROUP BY users.id_user
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    user_objects = []
    for row in results:
        user_object = {
            'id_user': row[0],
            'username': row[1],
            'email': row[2],
            'num_posts': row[3],
            'num_comments': row[4],
            'state': row[5],
            'registration_date': row[6]
        }
        user_objects.append(user_object)
    conn.close()
    return user_objects


def changeState(data: EditUser):
    try:
        c = sqlite3.connect(path_database)
        if data.state == 1:
            query = "UPDATE users SET state = 2 WHERE id_user =?"
        elif data.state == 2:
            query = "UPDATE users SET state = 3 WHERE id_user =?"
        elif data.state == 3:
            query = "UPDATE users SET state = 2 WHERE id_user =?"
        
        c.execute(query, (data.id_user,))
        c.commit()
        c.close()
        return True
    except:
        print('error')
        return False

def get_tickets():
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tickets")
    tickets = []
    for row in cursor.fetchall():
        ticket = {
            'id_ticket': row[0],
            'id_user': row[1],
            'username': get_username_from_id_user(id_user=row[1]),
            'category': row[2],
            'content': row[3],
            'creation_date': row[4],
            'answer': row[5],
            'subject': row[6]
            #'email': get_email_from_id_user(id_user=row[1])
        }
        tickets.append(ticket)
    
    conn.close()
    return tickets

def getInfoTicket(id_ticket: str):
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()

    query = """
    SELECT tickets.subject, users.fullname, auth.email, tickets.category
    FROM tickets
    INNER JOIN users ON tickets.id_user = users.id_user
    INNER JOIN auth ON users.id_user = auth.id_user
    WHERE tickets.id_ticket = ?
    """
    cursor.execute(query, (id_ticket,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        subject, fullname, email, category = result
        return InfoTicket(subject=subject, fullname=fullname, email=email, category=category)
    else:
        return None


def get_email_from_id_user(id_user: str):
    c = sqlite3.connect(path_database)
    id_user = c.execute(
        "SELECT email FROM auth WHERE id_user=?", (id_user,)).fetchone()
    c.close()
    if not id_user:
        return None
    return id_user[0]

def get_username_from_id_user(id_user: str):
    c = sqlite3.connect(path_database)
    id_user = c.execute(
        "SELECT username FROM auth WHERE id_user=?", (id_user,)).fetchone()
    c.close()
    if not id_user:
        return None
    return id_user[0]

def setTicket(id_ticket: str):
    try:
        c = sqlite3.connect(path_database)
        query = "UPDATE tickets SET answer = 1 WHERE id_ticket =?"
        c.execute(query, (id_ticket,))
        c.commit()
        c.close()
        return True
    except:
        print('error')
        return False
    

def get_users_4_notification():
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()
    cursor.execute("SELECT auth.email, users.fullname FROM auth JOIN users ON auth.id_user = users.id_user WHERE users.notification = 1")
    results = cursor.fetchall()
    conn.close()
    user_list = [{'email': email, 'fullname': fullname} for email, fullname in results]
    return user_list

