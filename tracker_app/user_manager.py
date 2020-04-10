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
    sql = f"INSERT INTO users (email, username) VALUES ('{email}', '{name}')"
    cursor.execute(sql)
    my_db.commit()
    print("User created with email:", email)


def get_user_data(email):
    cursor = my_db.cursor()
    cursor.execute(f"SELECT * FROM users WHERE email='{email}'")
    result = cursor.fetchall()[0]
    return {"email": result[0], "name": result[1], "date": result[2], "color": result[3]}


def change_name(email, name):
    cursor = my_db.cursor()
    sql = f"UPDATE users SET username='{name}' WHERE email='{email}'"
    cursor.execute(sql)
    my_db.commit()
    print("User with email:", email, "has updated his name to", name)



