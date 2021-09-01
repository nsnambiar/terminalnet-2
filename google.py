from flask_oauthlib.client import OAuth
from main import app,request,db
oauth=OAuth(app)
import os


google = oauth.register(
    name = 'google',
    client_id = os.environ['GOOGLE_CLIENT_ID'],
    client_secret = os.environ['GOOGLE_CLIENT_SECRET'],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)
