from flask import Flask, render_template, redirect, url_for, flash,abort,request
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from db import *
from authlib.integrations.flask_client import OAuth

app=Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

ckeditor=CKEditor(app)

oauths = OAuth(app)
google = oauths.register(
    name = 'google',
    client_id = "175887749203-gdtkc1h93svnal7gspl415t24ggfd5be.apps.googleusercontent.com",
    client_secret = "90KgzC26EfXluVqju8LJkRrA",
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)


# login_manager=LoginManager()
# login_manager.init_app(app)
#
# @login_manager.user_loader()
# def load_user(user_id):
#     return User.query.get(str(user_id))

@app.route('/',methods=["GET","POST"])
def start():

    return "working "



if __name__ == "__main__":
    app.run(debug=True)