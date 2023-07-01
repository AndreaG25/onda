import sqlite3

def create_database():
    conn = sqlite3.connect('cleardbcopy.db')
    c = conn.cursor()

    # Creazione delle tabelle
    c.execute('''CREATE TABLE Auth (
                    id_user TEXT PRIMARY KEY,
                    username TEXT,
                    email TEXT,
                    password TEXT
                )''')

    c.execute('''CREATE TABLE Users (
                    id_user TEXT PRIMARY KEY,
                    state INT,
                    fullname TEXT,
                    born_date TEXT,
                    profile_pic TEXT,
                    description TEXT,
                    privacy_account BOOL,
                    registration_date TEXT,
                    FOREIGN KEY (id_user) REFERENCES Auth (id_user) ON DELETE CASCADE
                )''')

    c.execute('''CREATE TABLE Posts (
                    id_post TEXT PRIMARY KEY,
                    id_user TEXT,
                    title TEXT,
                    content TEXT,
                    creation_date TEXT,
                    comment_flag BOOL,
                    public_flag BOOL,
                    FOREIGN KEY (id_user) REFERENCES Auth (id_user) ON DELETE CASCADE
                )''')

    c.execute('''CREATE TABLE Follows (
                    id_follow TEXT PRIMARY KEY,
                    id_sender TEXT,
                    id_recipient TEXT,
                    state INT,
                    creation_date TEXT,
                    FOREIGN KEY (id_sender) REFERENCES Auth (id_user) ON DELETE CASCADE,
                    FOREIGN KEY (id_recipient) REFERENCES Auth (id_user) ON DELETE CASCADE
                )''')

    c.execute('''CREATE TABLE Comments (
                    id_comment TEXT PRIMARY KEY,
                    id_user TEXT,
                    id_post TEXT,
                    content TEXT,
                    reference_comment TEXT,
                    creation_date TEXT,
                    FOREIGN KEY (id_user) REFERENCES Auth (id_user) ON DELETE CASCADE,
                    FOREIGN KEY (id_post) REFERENCES Posts (id_post) ON DELETE CASCADE,
                    FOREIGN KEY (reference_comment) REFERENCES Comments (id_comment) ON DELETE CASCADE
                )''')

    c.execute('''CREATE TABLE Like (
                    id_like TEXT PRIMARY KEY,
                    id_user TEXT,
                    id_post TEXT,
                    creation_date TEXT,
                    FOREIGN KEY (id_user) REFERENCES Auth (id_user) ON DELETE CASCADE,
                    FOREIGN KEY (id_post) REFERENCES Posts (id_post) ON DELETE CASCADE
                )''')

    c.execute('''CREATE TABLE Chat (
                    id_chat TEXT PRIMARY KEY,
                    id_user_first TEXT,
                    id_user_second TEXT,
                    last_update TEXT,
                    FOREIGN KEY (id_user_first) REFERENCES Auth (id_user) ON DELETE CASCADE,
                    FOREIGN KEY (id_user_second) REFERENCES Auth (id_user) ON DELETE CASCADE
                )''')

    c.execute('''CREATE TABLE Messages (
                    id_message TEXT PRIMARY KEY,
                    id_chat TEXT,
                    id_user TEXT,
                    content TEXT,
                    creation_date TEXT,
                    FOREIGN KEY (id_chat) REFERENCES Chat (id_chat) ON DELETE CASCADE,
                    FOREIGN KEY (id_user) REFERENCES Auth (id_user) ON DELETE CASCADE
                )''')

    c.execute('''CREATE TABLE Tickets (
                    id_ticket TEXT PRIMARY KEY,
                    id_user TEXT,
                    category INT,
                    content TEXT,
                    creation_date TEXT,
                    answer BOOL,
                    subject TEXT,
                    FOREIGN KEY (id_user) REFERENCES Auth (id_user) ON DELETE CASCADE
                )''')

    c.execute('''CREATE TABLE Admin (
                    id_admin TEXT PRIMARY KEY,
                    username TEXT,
                    password TEXT
                )''')

    # Creazione del trigger sulla tabella Auth
    c.execute('''CREATE TRIGGER IF NOT EXISTS auth_insert_trigger 
                    AFTER INSERT ON Auth
                    BEGIN
                        INSERT INTO Log (table_name, action, timestamp)
                    SELECT 'Auth', 'INSERT', DATETIME('now');
                    END;
                ''')
    # Creazione della tabella Log
    c.execute('''CREATE TABLE Log (
                    id INTEGER PRIMARY KEY,
                    table_name TEXT,
                    action TEXT,
                    timestamp TEXT
                )''')
    
    conn.commit()
    conn.close()

create_database()