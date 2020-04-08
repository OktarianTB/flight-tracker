from flask import Blueprint, render_template, redirect, url_for, flash
from tracker_app import bcrypt
from tracker_app.config import Config


tracker = Blueprint("tracker", __name__)


@tracker.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html", title="Home", api_key=Config.API_KEY)


