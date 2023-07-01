import sqlite3
from threading import Lock
from datetime import datetime
from .models import (UserLoginSchema, UserSchema,
    PostSchema, UserTableSchema,
    myPost, UpdateMyInfo, GetPostSchema,
    CommentSchema, relationSchema, newCommentSchema,
    likeSchema, searchUser, messageOBJ, NewTicketSchema,
    EditPostSchema
)

import bcrypt

from .createid import createID
#path_database = "C:/Users/Andrea/Desktop/pf1/backend/routers/database.db"
path_database = "C:/Users/Andrea/Desktop/pf3/database/database.db"

# Auth
def storeInformation(id_user: str, user: UserSchema):
    try:
        if user.privacy_account == "True":
            privacy = 1
        else:
            privacy = 0
        today = datetime.now()
        
        with sqlite3.connect(path_database) as conn:
            conn.execute("BEGIN TRANSACTION")
            
            # Inserimento nella tabella "auth"
            conn.execute("INSERT INTO auth (id_user, email, username, password) VALUES (?, ?, ?, ?)",
                         (id_user, user.email, user.username, getHashedPassword(password=user.password)))
            
            # Inserimento nella tabella "users"
            conn.execute("INSERT INTO users (id_user, fullname, born_date, privacy_account, registration_date, state) VALUES (?, ?, ?, ?, ?, 1)",
                         (id_user, user.fullname, user.born_date, privacy, today))
            
            conn.execute("COMMIT")
            conn.commit()
        
        return True
    except sqlite3.Error as error:
        print(error)
        return False


def tryLogin(user: UserLoginSchema):
    c = sqlite3.connect(path_database)
    userData = c.execute("SELECT * FROM auth WHERE username=?", (user.username,)).fetchone()
    c.close()
    if userData and verify_password(password=user.password, hashed_password=userData[3]):
        return userData[0]
    return None


def checkUsername(username: str):
    c = sqlite3.connect(path_database)
    user = c.execute("SELECT * FROM auth WHERE username=?", (username,)).fetchone()
    c.close()
    if user:
        return False
    return True


def checkEmail(email: str):
    c = sqlite3.connect(path_database)
    user = c.execute("SELECT * FROM auth WHERE email=?", (email,)).fetchone()
    c.close()
    if user:
        return False
    return True

def setState(newState: int, id_user: str):
    try:
        c = sqlite3.connect(path_database)
        c.execute("UPDATE users SET state=? WHERE id_user=?", (newState, id_user))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        return False

def getState(id_user: str):
    conn = sqlite3.connect(path_database)
    c = conn.cursor()
    c.execute("SELECT state FROM users WHERE id_user=?", (id_user,))
    result = c.fetchone()
    conn.close()
    if result:
        return [True, result[0]]
    else:
        return [False, -1]
    
# updateinfo
def updatePW(id_user: str, password: str):
    try:
        c = sqlite3.connect(path_database)
        c.execute("UPDATE auth SET password=? WHERE id_user=?", (getHashedPassword(password=password), id_user))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        return False


def updateUsername(id_user: str, new: str):
    try:
        c = sqlite3.connect(path_database)
        c.execute("UPDATE auth SET username=? WHERE id_user=?", (new, id_user))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        return False


def changePic(id_user: str, new: str):
    try:
        c = sqlite3.connect(path_database)
        c.execute("UPDATE users SET profile_pic=? WHERE id_user=?",
                  (new, id_user))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        return False


def changeMyInfo(id_user: str, data: UpdateMyInfo):
    try:
        if(data.privacy_account == True):
            privacy = 1
        else:
            privacy = 0

        c = sqlite3.connect(path_database)
        query = """
            SELECT privacy_account
            FROM users
            WHERE id_user = ?
        """
        result = c.execute(query, (id_user,)).fetchone()
        if result != None:
            if result[0] != privacy:
                if not changeAllRelations(id_user=id_user, new_privacy=privacy):
                    return False
        c.execute("UPDATE users SET fullname = ?, born_date = ?, description = ?, privacy_account = ? WHERE id_user = ?", (data.fullname, data.born_date, data.description, privacy, id_user))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        return False

def changeAllRelations(id_user: str, new_privacy: int):
    c = sqlite3.connect(path_database)
    if new_privacy == 1:
        query = "UPDATE follows SET state = 0 WHERE id_recipient = ? AND state = 3"
    elif new_privacy == 0:
        query1 = "UPDATE follows SET state = 3 WHERE id_recipient = ? AND state = 0"
        query2 = "UPDATE follows SET state = 2 WHERE id_recipient = ? AND state = 1"
    try:
        if new_privacy == 1:
            c.execute(query, (id_user,))
        elif new_privacy == 0:
            c.execute(query1, (id_user,))
            c.commit()
            c.execute(query2, (id_user,))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as e:
        c.rollback()
        c.close()
        return False

# post
def newPost(id_user: str, id_post: str, post: PostSchema):
    try:
        today = datetime.now()
        c = sqlite3.connect(path_database)
        c.execute("INSERT INTO post (id_post, id_user, title, content, creation_date, comment_flag, public_flag) VALUES (?,?,?,?,?,?,?)",
                  (id_post, id_user, post.title, post.content, today, post.comment_flag, post.public_flag))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        return False


def getPostsFromID_user(id_user: str, rel: int):
    c = sqlite3.connect(path_database)
    if rel == 10:
        result = c.execute("SELECT * FROM post WHERE id_user = ?", (id_user,)).fetchall()
    else:
        result = c.execute(
            "SELECT * FROM post WHERE id_user = ? AND public_flag = 1", (id_user,)).fetchall()
    posts = []
    for row in result:
        post = myPost(
            id_post=row[0],
            id_user=row[1],
            title=row[2],
            content=row[3],
            creation_date=row[4],
            comment_flag=bool(row[5]),
            public_flag=bool(row[6])
        )
        posts.append(post)
    return posts


def get_post_info(id_post: str, id_user: str, rel: int):
    # Connessione al database
    conn = sqlite3.connect(path_database)
    c = conn.cursor()
    if rel == 10:
        post_data = c.execute('''SELECT post.id_post, users.fullname, users.profile_pic, post.title, post.content, 
                            post.creation_date, post.comment_flag, auth.username
                    FROM post JOIN users ON post.id_user=users.id_user
                        JOIN auth ON auth.id_user=users.id_user
                    
                    WHERE post.id_post=?''', (id_post,)).fetchone()
    else:
        post_data = c.execute('''SELECT post.id_post, users.fullname, users.profile_pic, post.title, post.content, 
                            post.creation_date, post.comment_flag, auth.username
                    FROM post JOIN users ON post.id_user=users.id_user
                        JOIN auth ON auth.id_user=users.id_user
                    
                    WHERE post.id_post=? AND post.public_flag=1''', (id_post,)).fetchone()
    if not post_data:
        return None

    post = GetPostSchema(
        id_post=post_data[0],
        fullname=post_data[1],
        profile_pic=post_data[2],
        title=post_data[3],
        content=post_data[4],
        creation_date=post_data[5],
        comment_flag=bool(post_data[6]),
        username=post_data[7],
    )
    # Query per ottenere il numero di like del post
    c.execute('SELECT COUNT(*) FROM like WHERE id_post=?', (id_post,))
    post.number_of_like = c.fetchone()[0]

    # Query per verificare se l'utente corrente ha già messo like a questo post
    # (qui supponiamo che l'id dell'utente corrente sia 1)
    c.execute('SELECT COUNT(*) FROM like WHERE id_post=? AND id_user=?', (id_post, id_user))
    post.is_there_like = bool(c.fetchone()[0])

    # Query per ottenere i commenti del post
    c.execute('''SELECT comments.id_comment, users.fullname, auth.username, users.profile_pic, comments.content, 
    comments.creation_date, comments.reference_comment
                 FROM comments JOIN users ON comments.id_user=users.id_user
                 JOIN auth ON auth.id_user=users.id_user
                 WHERE comments.id_post=?''', (id_post,))
    comments_data = c.fetchall()
    
    comments = []
    for comment_data in comments_data:
        comment = CommentSchema(
            id_comment=comment_data[0],
            fullname=comment_data[1],
            username=comment_data[2],
            profile_pic=comment_data[3],
            content=comment_data[4],
            creation_date=comment_data[5],
            reference_comment=comment_data[6]
        )
        # Query per ottenere il numero di like del post
        c.execute('SELECT COUNT(*) FROM like WHERE id_comment=?', (comment.id_comment,))
        comment.number_of_like = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM like WHERE id_comment=? AND id_user=?', (comment.id_comment, id_user))
        comment.is_there_like = bool(c.fetchone()[0])
        comments.append(comment)
        
    post.comments = comments

    # Chiusura della connessione e ritorno del risultato
    conn.close()
    return post


def editPublic(id_post: str, action: bool):
    try:
        c = sqlite3.connect(path_database)
        query = "UPDATE post SET public_flag = ? WHERE id_post = ?"
        c.execute(query, (int(action), id_post))
        c.commit()
        c.close()
        return True
    except:
        print("Errore")
        return False

def deletePost(id_post: str):
    try:
        conn = sqlite3.connect(path_database)
        conn.execute("PRAGMA foreign_keys = ON")  
        c = conn.cursor()
        conn.execute("BEGIN TRANSACTION")

        c.execute("DELETE FROM post WHERE id_post=?", (id_post,))
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(e)
        conn.rollback()
        return False

def getPost4Edit(id_post: str):
    conn = sqlite3.connect(path_database)
    c = conn.cursor()
    c.execute("SELECT title, content, comment_flag, public_flag FROM post WHERE id_post = ?", (id_post,))
    row = c.fetchone()
    post_object = {
        'title': row[0],
        'content': row[1],
        'comment_flag': row[2],
        'public_flag': row[3]
    }
    conn.close()
    return post_object

def editPost(post: EditPostSchema):
    try:
        conn = sqlite3.connect(path_database)
        c = conn.cursor()
        id_post = post.id_post
        title = post.title
        content = post.content
        comment_flag = post.comment_flag
        public_flag = post.public_flag

        c.execute("UPDATE post SET title=?, content=?, comment_flag=?, public_flag=? WHERE id_post=?", (title, content, comment_flag, public_flag, id_post))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as error:
        print(error)
        return False


# user
def getInfo(id_user: str):
    c = sqlite3.connect(path_database)
    username = c.execute(
        "SELECT username FROM auth WHERE id_user=?", (id_user,)).fetchone()
    row = c.execute("SELECT * FROM users WHERE id_user=?",
                    (id_user,)).fetchone()
    number_of_follower = c.execute(
        "SELECT COUNT(*) FROM follows WHERE state = 2 AND id_recipient = ?", (id_user,)).fetchone()
    number_of_posts = c.execute(
        "SELECT COUNT(*) FROM post WHERE public_flag = 1 AND id_user = ?", (id_user,)).fetchone()
    number_of_like = c.execute(
        "SELECT COUNT(*) FROM like JOIN post ON like.id_post = post.id_post WHERE post.id_user = ? AND post.public_flag=1", (id_user, )
        ).fetchone()
    c.close()
    if not row or not username:
        return None
    user = UserTableSchema(id_user=row[0], state=row[1], fullname=row[2], born_date=row[3], profile_pic=row[4], description=row[5],
                           privacy_account=row[6], registration_date=row[7], username=username[0], number_of_followers=number_of_follower[0], number_of_posts=number_of_posts[0], number_of_like=number_of_like[0])

    return user


def getInfoByRelation(id_user_recipient: str, relation: int):
    res = {
        "result": True,
        "info": getInfo(id_user=id_user_recipient),
        "relation": relation
    }

    if relation == 2 or relation == 3:
        res["posts"] = getPostsFromID_user(id_user=id_user_recipient, rel=relation)
    return res

# relations
def changeRelation(id_user_sender: str, id_user_recipient: str, new_state: int):
    try:
        c = sqlite3.connect(path_database)
        privacy = get_privacy(id_user=id_user_recipient)
        if new_state == 0 and privacy == False:
            new_state = 3
        c.execute("UPDATE follows set state = ? WHERE id_sender = ? AND id_recipient = ?",
                  (new_state, id_user_sender, id_user_recipient))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        return False


def get_relation(id_user_recipient: str, id_user_sender: str):
    if id_user_recipient == id_user_sender:
        return 10
    c = sqlite3.connect(path_database)
    state = c.execute("SELECT state FROM follows WHERE id_sender=? AND id_recipient=?",
                      (id_user_sender, id_user_recipient)).fetchone()
    c.close()
    if not state:
        res = createRelation(id_user_recipient=id_user_recipient, id_user_sender=id_user_sender)
        if res[0]:
            return res[1]
        return -99
    else:
        return state[0]


def createRelation(id_user_recipient: str, id_user_sender: str):
    try:
        today = datetime.now()
        id_follow = createID("follow")
        c = sqlite3.connect(path_database)
        query = """
            SELECT privacy_account
            FROM users
            WHERE id_user = ?
        """

        result = c.execute(query, (id_user_recipient,)).fetchone()
        if result != None:
            if bool(result[0]):
                newState = 0
            else:
                newState = 3
        else:
            return [False, "error"]
        
        c.execute("INSERT INTO follows (id_follow, id_sender, id_recipient, state, creation_date) VALUES (?,?,?,?,?)",
                (id_follow, id_user_sender, id_user_recipient, newState, today))
        c.commit()
        c.close()
        return [True, newState]
    except sqlite3.Error as error:
        return False


def getFollowRequests(id_user: str):
    # sostituisci "database.db" con il nome del tuo database
    conn = sqlite3.connect(path_database)
    c = conn.cursor()

    # Esegue una query per ottenere tutti i follower dell'utente con id_user
    query = """
        SELECT follows.state, follows.id_follow, follows.id_sender, follows.creation_date, auth.username, users.fullname, users.profile_pic
        FROM follows
        JOIN users ON users.id_user = follows.id_sender
        JOIN auth ON auth.id_user = users.id_user
        WHERE follows.id_recipient = ? AND follows.state = 1
    """
    c.execute(query, (id_user,))

    followers = []
    for row in c.fetchall():
        followers.append(relationSchema(
            state_request=row[0],
            id_follow=row[1],
            id_user_sender=row[2],
            date_creation=row[3],
            username=row[4],
            fullname=row[5],
            profile_pic=row[6]
        ))

    conn.close()
    return followers


def checkUserRequest(id_follow: str, id_user: str):
    c = sqlite3.connect(path_database)
    user_recipient = c.execute(
        "SELECT id_recipient FROM follows WHERE id_follow=?", (id_follow,)).fetchone()
    c.close()
    if user_recipient[0] == id_user:
        return True
    return False


def accept_refuse_request(id_follow: str, answer: bool):
    if answer:
        new_state = 2
    else:
        new_state = 0

    try:
        c = sqlite3.connect(path_database)
        c.execute("UPDATE follows set state = ? WHERE id_follow = ?",
                  (new_state, id_follow))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        return False

# comments


def canUserComment(id_user: str, id_post: str):
    c = sqlite3.connect(path_database)
    canPostBeCommented = c.execute(
        "SELECT comment_flag FROM post WHERE id_post=?", (id_post,)).fetchone()
    id_author = c.execute(
        "SELECT id_user FROM post WHERE id_post=?", (id_post,)).fetchone()
    c.close()
    if canPostBeCommented == None:
        return [False, "Il post non esiste, violazione individuata"]
    if not canPostBeCommented[0]:
        blockUser(id_user=id_user)
        return [False, "Il post non è commentabile, violazione individuata"]
    rel = get_relation(id_user_sender=id_user, id_user_recipient=id_author[0])
    if rel == 2 or rel == 10 or rel == 3:
        return [True]
    blockUser(id_user=id_user)
    return [False, "Utente non autorizzato, violazione individuata"]


def newComment(id_comment: str, id_user: str, commentObj: newCommentSchema):
    try:
        today = datetime.now()
        c = sqlite3.connect(path_database)
        c.execute("INSERT INTO comments (id_comment, id_user, id_post, content, reference_comment, creation_date) VALUES (?,?,?,?,?,?)",
                  (id_comment,  id_user, commentObj.id_post, commentObj.content, commentObj.reference_comment, today))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        print(error)
        return False

#like
def updateLike(id_user: str, id_like: str, like: likeSchema):
    try:
        query = ''
        if like.like:
            if like.id_element.split('_')[0] == "post":
                query = "INSERT INTO like (id_like, id_user, id_post, creation_date) VALUES (?,?,?,?)"
            elif like.id_element.split('_')[0] == "comment":
                query = "INSERT INTO like (id_like, id_user, id_comment, creation_date) VALUES (?,?,?,?)"
            today = datetime.now()
            params = (id_like, id_user, like.id_element, today)
        else:
            el = like.id_element.split('_')[0]
            if el == "comment":
                table = "comments"
            else:
                table = el
            query = f"DELETE FROM like WHERE id_{el} = ?"
            params = (like.id_element,)

        c = sqlite3.connect(path_database)
        c.execute(query,params)
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        print(error)
        return False


#search
def search(string: str):
    conn = sqlite3.connect(path_database)
    c = conn.cursor()

    # costruzione della query SQL per cercare profili corrispondenti
    query = '''SELECT u.fullname, a.username, u.profile_pic 
               FROM auth a JOIN users u ON a.id_user = u.id_user
               WHERE u.fullname LIKE ? OR a.username LIKE ?'''
    search_term = f"%{string}%" # aggiunta del carattere jolly % per effettuare una ricerca parziale
    c.execute(query, (search_term, search_term))

    # restituzione dei risultati della ricerca come una lista di tuple (fullname, username, profile_pic)
    tuples = c.fetchall()
    results = []
    for el in tuples:
        item = searchUser(fullname=el[0], username=el[1], profile_pic=el[2])
        results.append(item)
    conn.close()
    return results

#chat

def createChat(id_user_first: str, id_user_second: str):
    today = datetime.now()
    id_chat = createID('chat')
    query = "INSERT INTO chat (id_chat, id_user_first, id_user_second, last_update) VALUES (?,?,?,?)"
    data = (id_chat, id_user_first, id_user_second, today)
    try:
        c = sqlite3.connect(path_database)
        c.execute(query, data)
        c.commit()
        c.close
        return True
    except:
        return False



def check_chat_exists(id_user_1: str, id_user_2: str):
    conn = sqlite3.connect(path_database)
    c = conn.cursor()
    c.execute("SELECT id_chat FROM chat WHERE (id_user_first = ? AND id_user_second = ?) OR (id_user_first = ? AND id_user_second = ?)", (id_user_1, id_user_2, id_user_2, id_user_1))
    result = c.fetchone()
    conn.close()
    if result is not None:
        return [True, result[0]]
    else:
        return [False]

def checkUserInChat(id_user: str, id_chat: str):
    conn = sqlite3.connect(path_database)
    c = conn.cursor()
    
    # Controlla se l'utente è presente come id_user_first in una chat
    c.execute("SELECT * FROM chat WHERE (id_user_first=? OR id_user_second=?) AND id_chat = ?", (id_user, id_user, id_chat))
    result = c.fetchone()
    if result:
        conn.close()
        return True
    
    conn.close()
    return False

def getChats(id_user: str):
    conn = sqlite3.connect(path_database)
    c = conn.cursor()
    c.execute("""SELECT c.id_chat, 
                            CASE WHEN c.id_user_first = ? THEN u2.username ELSE u1.username END AS username, 
                            CASE WHEN c.id_user_first = ? THEN up2.profile_pic ELSE up1.profile_pic END AS profile_pic
                     FROM chat c
                     JOIN auth u1 ON c.id_user_first = u1.id_user
                     JOIN auth u2 ON c.id_user_second = u2.id_user
                     JOIN users up1 ON u1.id_user = up1.id_user
                     JOIN users up2 ON u2.id_user = up2.id_user
                     WHERE c.id_user_first = ? OR c.id_user_second = ?
                     ORDER BY c.last_update DESC""", (id_user, id_user, id_user, id_user))
    results = c.fetchall()
    chats = []
    for row in results:
        chat = {'id_chat': row[0], 'username': row[1], 'id_user': get_id_user_from_username(row[1]), 'profile_pic': row[2]}
        chats.append(chat)
    conn.close()
    return chats

def getMessages(id_chat: str):
    conn = sqlite3.connect(path_database)
    c = conn.cursor()
    c.execute("""SELECT m.id_message, m.id_chat, m.id_user, m.content, m.creation_date, a.username
                 FROM messages m
                 JOIN auth a ON m.id_user = a.id_user
                 WHERE m.id_chat = ?""", (id_chat,))
    messages = []
    for row in c.fetchall():
        message = {
            'id_message': row[0],
            'id_chat': row[1],
            'id_user': row[2],
            'content': row[3],
            'creation_date': row[4],
            'username': row[5]
        }
        messages.append(message)
    conn.close()
    return messages

def storeMessage(message: messageOBJ):
    id_message = createID('msg')
    try:
        query = "INSERT INTO messages (id_message, id_chat, id_user, content, creation_date) VALUES (?,?,?,?,?)"
        data = (id_message, message.id_chat, message.id_user_sender, message.content, message.creation_date)
        c = sqlite3.connect(path_database)
        c.execute(query, data)
        c.commit()
        c.close()
        return True
    except:
        return True
    
#assistance
def createTicket(id_ticket: str, id_user: str,  ticketOBJ: NewTicketSchema):
    today = datetime.now()
    try:
        query = "INSERT INTO tickets (id_ticket, id_user, category, content, subject, creation_date) VALUES (?,?,?,?,?,?)"
        data = (id_ticket, id_user, ticketOBJ.category, ticketOBJ.content, ticketOBJ.subject, today)
        c = sqlite3.connect(path_database)
        c.execute(query, data)
        c.commit()
        c.close()
        return True
    except:
        return True

#home
def getRecentPost():
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()
    query = '''
        SELECT auth.username, users.fullname, users.profile_pic, post.id_post, post.title, post.content, post.creation_date
        FROM post
        INNER JOIN auth ON post.id_user = auth.id_user
        INNER JOIN users ON post.id_user = users.id_user
        WHERE post.public_flag = 1 AND users.privacy_account = 0
        ORDER BY post.creation_date DESC
        LIMIT 20
    '''
    cursor.execute(query)
    recent_posts = []
    for row in cursor.fetchall():
        username, fullname, profile_pic, id_post, title, content, creation_date = row
        post = {
            'id_post': id_post,
            'creation_date': creation_date,
            'profile_pic': profile_pic,
            'username': username,
            'title': title,
            'content': content,
            'fullname': fullname
        }
        recent_posts.append(post)

    cursor.close()
    conn.close()
    return recent_posts

def getprofilePic(id_user: str):
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()
    cursor.execute("SELECT profile_pic FROM users WHERE id_user = ?", (id_user,))
    profile_pic = cursor.fetchone()
    if profile_pic:
        return profile_pic[0]
    return None

def getPostbyFollower(id_user: str):
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()
    query = '''
        SELECT auth.username, users.fullname, users.profile_pic, post.id_post, post.title, post.content, post.creation_date
        FROM post
        INNER JOIN auth ON post.id_user = auth.id_user
        INNER JOIN users ON post.id_user = users.id_user
        INNER JOIN follows ON post.id_user = follows.id_recipient
        WHERE follows.id_sender = ? AND follows.state = 2 AND post.public_flag = 1
        ORDER BY post.creation_date DESC
        LIMIT 20
    '''
    user_posts = []
    for row in cursor.execute(query, (id_user,)).fetchall():
        username, fullname, profile_pic, id_post, title, content, creation_date = row
        post = {
            'id_post': id_post, 
            'creation_date': creation_date,
            'profile_pic': profile_pic,
            'username': username,
            'title': title,
            'content': content,
            'fullname': fullname
        }
        user_posts.append(post)

    cursor.close()
    conn.close()

    return user_posts

# Functions
def get_id_user_from_username(username: str):
    c = sqlite3.connect(path_database)
    user = c.execute("SELECT id_user FROM auth WHERE username=?",
        (username,)).fetchone()
    c.close()
    if not user:
        return None
    return user[0]


def get_id_user_from_post(id_post: str):
    c = sqlite3.connect(path_database)
    id_user = c.execute(
        "SELECT id_user FROM post WHERE id_post=?", (id_post,)).fetchone()
    c.close()
    if not id_user:
        return None
    return id_user[0]

def get_email_from_id_user(id_user: str):
    c = sqlite3.connect(path_database)
    id_user = c.execute(
        "SELECT email FROM auth WHERE id_user=?", (id_user,)).fetchone()
    c.close()
    if not id_user:
        return None
    return id_user[0]

def get_privacy(id_user: str):
    query = """
            SELECT privacy_account
            FROM users
            WHERE id_user = ?
        """
    c = sqlite3.connect(path_database)
    privacy = c.execute(query, (id_user,)).fetchone()
    c.close()
    if privacy != None:
        return bool(privacy[0])
    else:
        return [False, "error"]
    
def blockUser(id_user: str):
    c = sqlite3.connect(path_database)
    query = "UPDATE users SET state = 3 WHERE id_user =?"
    c.execute(query, (id_user,))
    c.commit()
    c.close()

def getFollowers(id_user: str):
    c = sqlite3.connect(path_database)
    db_lock = Lock()
    db_lock.acquire()
    query = '''
        SELECT auth.username, users.profile_pic, users.fullname
        FROM follows
        INNER JOIN auth ON follows.id_sender = auth.id_user
        INNER JOIN users ON follows.id_sender = users.id_user
        WHERE follows.id_recipient = ? AND follows.state = 2 
    '''
    followers = []
    try:
        for row in c.execute(query, (id_user,)).fetchall():
            username, profile_pic, fullname = row
            post = {
                'profile_pic': profile_pic,
                'username': username,
                'fullname': fullname
            }
            followers.append(post)
        c.close()
        c.close()
        return followers
    finally:
        db_lock.release()

def getFollowed(id_user: str):
    c = sqlite3.connect(path_database)
    query = '''
        SELECT auth.username, users.profile_pic, users.fullname
        FROM follows
        INNER JOIN auth ON follows.id_recipient = auth.id_user
        INNER JOIN users ON follows.id_recipient = users.id_user
        WHERE follows.id_sender = ? AND follows.state = 2 
    '''
    followed = []
    for row in c.execute(query, (id_user,)).fetchall():
        username, profile_pic, fullname = row
        post = {
            'profile_pic': profile_pic,
            'username': username,
            'fullname': fullname
        }
        followed.append(post)

    c.close()
    c.close()
    return followed

def getRequests(id_user: str):
    c = sqlite3.connect(path_database)
    query = '''
        SELECT auth.username, users.profile_pic, users.fullname
        FROM follows
        INNER JOIN auth ON follows.id_recipient = auth.id_user
        INNER JOIN users ON follows.id_recipient = users.id_user
        WHERE follows.id_sender = ? AND follows.state = 1
    '''
    requests = []
    for row in c.execute(query, (id_user,)).fetchall():
        username, profile_pic, fullname = row
        post = {
            'profile_pic': profile_pic,
            'username': username,
            'fullname': fullname
        }
        requests.append(post)

    c.close()
    c.close()
    return requests

def resetPW(email: str, password: str):
    try:
        c = sqlite3.connect(path_database)
        c.execute("UPDATE auth SET password=? WHERE email=?", (getHashedPassword(password=password), email))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        return False


def deleteAccount(id_user: str):
    try:
        c = sqlite3.connect(path_database)
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM auth WHERE id_user = ?", (id_user,))
        c.commit()
        c.close()
        return True
    except sqlite3.Error as error:
        print(error)
        return False

def checkUsernameAndIDUser(username: str, id_user: str):
    conn = sqlite3.connect(path_database)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM auth WHERE id_user = ?", (id_user,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is not None and result[0] == username:
        return True
    else:
        return False



#security
def getHashedPassword(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def verify_password(password: str, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

