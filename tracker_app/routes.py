import flask
from flask import Blueprint, render_template, redirect, url_for, flash, make_response, request
from tracker_app.config import Config
import functools
from authlib.integrations.requests_client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
from tracker_app.user_manager import check_if_user_exists, create_user, get_user_data, change_name
from tracker_app.forms import UpdateUserSettings, NewLocation
from tracker_app.location_manager import get_address_from_coordinates, add_location_to_db, get_locations_from_db, \
    extract_coordinates_from_data


tracker = Blueprint("tracker", __name__)


@tracker.route("/", methods=["GET", "POST"])
def home():
    if is_logged_in():
        user_info = get_user_info()
        if check_if_user_exists(user_info['email']) is False:
            create_user(user_info['email'], user_info['given_name'])

        data = get_locations_from_db(user_info['email'])
        coordinates = extract_coordinates_from_data(data)
        return render_template("home.html", title="Home", api_key=Config.API_KEY, coordinates=coordinates,
                               name=user_info['given_name'], email=user_info['email'], logged_in=True)

    flash("You need to login!", "info")
    return render_template("home.html", title="Home", logged_in=False)


@tracker.route("/settings", methods=["GET", "POST"])
def settings():
    if is_logged_in():
        user_info = get_user_info()
        if check_if_user_exists(user_info['email']):
            data = get_user_data(user_info['email'])

            form = UpdateUserSettings()
            form.username.data = data["name"]
            if form.validate_on_submit():
                if form.username.raw_data[0] != data["name"]:
                    change_name(data["email"], form.username.raw_data[0])
                else:
                    flash("You haven't made any changes to your settings.", "info")
                return redirect(url_for("tracker.settings"))

            return render_template("settings.html", title="Settings", logged_in=True, form=form,
                                   email=data["email"], name=data["name"], color=data["color"])

    flash("Unable to access settings without being logged in!", "danger")
    return redirect(url_for("tracker.home"))


@tracker.route("/locations", methods=["GET", "POST"])
def locations():
    if is_logged_in():
        user_info = get_user_info()

        if check_if_user_exists(user_info['email']):
            data = get_locations_from_db(user_info['email'])
            number_of_locations = len(data)
            return render_template("locations.html", title="Locations", logged_in=True,
                                   number_of_locations=number_of_locations, data=data)

    flash("Unable to access the location page without being logged in!", "danger")
    return redirect(url_for("tracker.home"))


@tracker.route("/locations/add", methods=["GET", "POST"])
def add_location():
    if is_logged_in():
        user_info = get_user_info()

        if check_if_user_exists(user_info['email']):
            return render_template("add_location.html", title="Add Location", logged_in=True, api_key=Config.API_KEY)

    flash("Unable to access the location page without being logged in!", "danger")
    return redirect(url_for("tracker.home"))


@tracker.route("/locations/confirm/<lat>/<lng>", methods=["GET", "POST"])
def confirm_add_location(lat, lng):
    if is_logged_in():
        user_info = get_user_info()
        if check_if_user_exists(user_info['email']):
            form = NewLocation()
            address = get_address_from_coordinates(lat, lng)
            if form.validate_on_submit():
                add_location_to_db(user_info['email'], form.name.data, address, form.description.data, lat, lng)
                return redirect(url_for("tracker.locations"))
            return render_template("confirm_location.html", title="Confirm Location", logged_in=True,
                                   address=address, form=form)

    flash("Unable to access the location page without being logged in!", "danger")
    return redirect(url_for("tracker.home"))


def is_logged_in():
    return True if Config.AUTH_TOKEN_KEY in flask.session else False


def build_credentials():
    if not is_logged_in():
        raise Exception('User must be logged in')

    oauth2_tokens = flask.session[Config.AUTH_TOKEN_KEY]

    return google.oauth2.credentials.Credentials(
        oauth2_tokens['access_token'],
        refresh_token=oauth2_tokens['refresh_token'],
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        token_uri=Config.ACCESS_TOKEN_URI)


def get_user_info():
    credentials = build_credentials()

    oauth2_client = googleapiclient.discovery.build(
                        'oauth2', 'v2',
                        credentials=credentials)

    return oauth2_client.userinfo().get().execute()


def no_cache(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return functools.update_wrapper(no_cache_impl, view)


@tracker.route('/google/login')
@no_cache
def login():
    session = OAuth2Session(Config.CLIENT_ID, Config.CLIENT_SECRET,
                            scope=Config.AUTHORIZATION_SCOPE,
                            redirect_uri=Config.AUTH_REDIRECT_URI)

    uri, state = session.create_authorization_url(Config.AUTHORIZATION_URL)

    flask.session[Config.AUTH_STATE_KEY] = state
    flask.session.permanent = True

    return redirect(uri, code=302)


@tracker.route('/google/auth')
@no_cache
def google_auth_redirect():
    req_state = request.args.get('state', default=None, type=None)

    if req_state != flask.session[Config.AUTH_STATE_KEY]:
        response = make_response('Invalid state parameter', 401)
        return response

    session = OAuth2Session(Config.CLIENT_ID, Config.CLIENT_SECRET,
                            scope=Config.AUTHORIZATION_SCOPE,
                            state=flask.session[Config.AUTH_STATE_KEY],
                            redirect_uri=Config.AUTH_REDIRECT_URI)

    oauth2_tokens = session.fetch_access_token(
        Config.ACCESS_TOKEN_URI,
        authorization_response=flask.request.url)

    flask.session[Config.AUTH_TOKEN_KEY] = oauth2_tokens

    return redirect(url_for("tracker.home"), code=302)


@tracker.route('/google/logout')
@no_cache
def logout():
    flask.session.pop(Config.AUTH_TOKEN_KEY, None)
    flask.session.pop(Config.AUTH_STATE_KEY, None)

    return redirect(url_for("tracker.home"), code=302)

