import requests
from flask import redirect, url_for, flash
import mysql.connector
from tracker_app.config import Config

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=Config.DATABASE_PW,
    database="travel_tracker")


def get_address_from_coordinates(lat, lng):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    r = requests.get(url + f"latlng={lat},{lng}&key=" + Config.API_KEY)
    data = r.json()
    if r.status_code == 200:
        return data['results'][0]['formatted_address']
    flash("Unable to access that specific location.", "danger")
    return redirect(url_for("tracker.home"))


def add_location_to_db(email, name, address, description, lat, lng):
    cursor = my_db.cursor()
    if len(description) == 0:
        sql = f"INSERT INTO locations (user_email, name, address, lat, lng) VALUES ('{email}', '{name}', " \
              f"'{address[:250]}', '{lat}', '{lng}')"
    else:
        sql = f"INSERT INTO locations (user_email, name, address, description, lat, lng) VALUES ('{email}', '{name}', '{address[:250]}', " \
              f"'{description}', '{lat}', '{lng}')"
    cursor.execute(sql)
    my_db.commit()


def get_locations_from_db(email):
    cursor = my_db.cursor()
    cursor.execute(f"SELECT * FROM locations WHERE user_email='{email}'")
    result = cursor.fetchall()
    return result
