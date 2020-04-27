import requests
from flask import flash
import mysql.connector
from tracker_app.config import Config
from time import sleep

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=Config.DATABASE_PW,
    database="travel_tracker")


def get_country_from_coordinates(lat, lng):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    r = requests.get(url + f"latlng={lat},{lng}&key=" + Config.API_KEY)
    data = r.json()

    if r.status_code == 200:
        try:
            for component in data["results"][0]["address_components"]:
                if "country" in component["types"]:
                    return component["long_name"]
        except IndexError:
            pass

    flash("Unable to access that specific location.", "danger")
    return None


def get_location_from_coordinates(lat, lng):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    r = requests.get(url + f"latlng={lat},{lng}&key=" + Config.API_KEY)
    data = r.json()

    if r.status_code == 200:
        try:
            if "airport" in data["results"][0]["address_components"][0]["types"]:
                location = data["results"][0]["address_components"][0]["long_name"]
            elif data["results"][1]["address_components"][0]["types"]:
                location = data["results"][1]["address_components"][0]["long_name"]
            else:
                return None
            return location[:250]
        except IndexError:
            pass

    return None


def add_location_to_db(email, name, country, description, lat, lng, pin_color):
    cursor = my_db.cursor()
    if len(description) == 0:
        data = (email, name, country[:200], lat, lng, pin_color)
        sql = f"INSERT INTO locations (user_email, name, country, lat, lng, color) VALUES (%s, %s, " \
              f"%s, %s, %s, %s)"
        cursor.execute(sql, data)
    else:
        data = (email, name, country[:200], description[:200], lat, lng, pin_color)
        sql = f"INSERT INTO locations (user_email, name, country, description, lat, lng, color) VALUES (%s, %s, " \
              f"%s, %s, %s, %s, %s)"
        cursor.execute(sql, data)
    my_db.commit()


def add_flight_to_db(email, flight_name, start_name, start_lat, start_lng, end_name, end_lat, end_lng):
    cursor = my_db.cursor()
    data = (email, flight_name, start_name, start_lat, start_lng, end_name, end_lat, end_lng)
    sql = f"INSERT INTO flights (user_email, flight_name, start_name, start_lat, start_lng, end_name, end_lat, " \
          f"end_lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, data)
    my_db.commit()


def get_locations_from_db(email):
    cursor = my_db.cursor()
    data = (email, )
    sql = f"SELECT * FROM locations WHERE user_email=%s"
    cursor.execute(sql, data)
    result = cursor.fetchall()
    return result


def get_flights_from_db(email):
    cursor = my_db.cursor()
    data = (email, )
    sql = f"SELECT * FROM flights WHERE user_email=%s"
    cursor.execute(sql, data)
    result = cursor.fetchall()
    return result


def get_flight_coordinates(email):
    flight_info = []
    flights = get_flights_from_db(email)
    for flight in flights:
        flight_info.append([flight[2], float(flight[4]), float(flight[5]), float(flight[7]), float(flight[8])])
    return flight_info


def get_location_coordinates(email):
    data = get_locations_from_db(email)
    coordinates = []
    for location in data:
        coordinates.append([float(location[5]), float(location[6]), location[7], location[2]])
    return coordinates


def delete_location_from_db(location_id):
    cursor = my_db.cursor()
    data = (location_id, )
    sql = f"DELETE FROM locations WHERE id=%s"
    cursor.execute(sql, data)
    my_db.commit()


def delete_flight_from_db(flight_id):
    cursor = my_db.cursor()
    data = (flight_id, )
    sql = f"DELETE FROM flights WHERE id=%s"
    cursor.execute(sql, data)
    my_db.commit()


def check_location_id_belongs_to_user(email, location_id):
    cursor = my_db.cursor()
    data = (email, location_id)
    sql = f"SELECT * FROM locations WHERE user_email=%s AND id=%s"
    cursor.execute(sql, data)
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True


def check_flight_id_belongs_to_user(email, flight_id):
    cursor = my_db.cursor()
    data = (email, flight_id)
    sql = f"SELECT * FROM flights WHERE user_email=%s AND id=%s"
    cursor.execute(sql, data)
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True
