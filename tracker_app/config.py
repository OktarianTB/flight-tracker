import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    API_KEY = os.environ.get("google_maps_api_key")