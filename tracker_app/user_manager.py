import mysql.connector
from tracker_app.config import Config

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=Config.DATABASE_PW,
    database="travel_tracker")


def check_if_user_exists(email):
    cursor = my_db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE email='{email}'")
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True


def create_user(email, name):
    cursor = my_db.cursor()
    data = (email, name)
    sql = f"INSERT INTO users (email, username) VALUES (%s, %s)"
    cursor.execute(sql, data)
    my_db.commit()
    print("User created with email:", email)


def get_user_data(email):
    cursor = my_db.cursor()
    data = (email, )
    sql = f"SELECT * FROM users WHERE email=%s"
    cursor.execute(sql, data)
    result = cursor.fetchall()[0]
    return {"email": result[0], "name": result[1], "date": result[2], "color": result[3]}


def change_name(email, name):
    cursor = my_db.cursor()
    data = (name, email)
    sql = f"UPDATE users SET username=%s WHERE email=%s"
    cursor.execute(sql, data)
    my_db.commit()



