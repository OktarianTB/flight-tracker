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
