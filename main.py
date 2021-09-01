from flask import Flask, render_template, redirect, url_for, flash,abort,request
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from db import *


app=Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


ckeditor=CKEditor(app)


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