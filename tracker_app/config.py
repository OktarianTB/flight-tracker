import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    API_KEY = os.environ.get("google_maps_api_key")

    CLIENT_ID = os.environ.get("TRAVEL_TRACKER_OAUTH_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("TRAVEL_TRACKER_OAUTH_CLIENT_SECRET")

    ACCESS_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'
    AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'

    AUTHORIZATION_SCOPE = 'openid email profile'
    AUTH_REDIRECT_URI = "http://127.0.0.1:5000/google/auth"

    AUTH_TOKEN_KEY = 'auth_token'
    AUTH_STATE_KEY = 'auth_state'

    DATABASE_PW = os.environ.get("TRAVEL_TRACKER_DATABASE_PW")
