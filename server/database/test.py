import sqlite3
import bcrypt
path_database = "C:/Users/Andrea/Desktop/pf3/database/database.db"

def getHashedPassword(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


conn = sqlite3.connect(path_database)
conn.execute("INSERT INTO Admin (id_admin, username, password) VALUES (?,?,?)", ("id_admin_test", "admin", getHashedPassword(password="admin")))
conn.commit()
conn.close()


