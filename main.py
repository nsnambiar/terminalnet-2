from flask import Flask, render_template, redirect, url_for, flash,abort,request
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from db import *
from forms import *
from authlib.integrations.flask_client import OAuth
import os

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
    # db.create_all()
    # return redirect(url_for('view',page=1))

    return "working "


@app.route('/Page<int:page>',methods=['GET'])
def view(page):
    per_page = 5
    posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page,per_page,error_out=False)
    issues = IssueBlogPost.query.order_by(desc(IssueBlogPost.id)).all()
    return render_template("index.html", all_post=posts, currentuser=current_user, issue_post=issues)




@app.route('/login',methods=["GET","POST"])
def login():
    form=Login()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        checking = User.query.filter_by(email=email).first()
        if not checking:
            flash('Username or Email incorrect, please try again.')
            return redirect(url_for('login'))
        elif checking.name != name:
            flash('Username or Email incorrect, please try again.')
        else:
            login_user(checking)
            return redirect(url_for('start'))
    return render_template("login.html",form=form)



if __name__ == "__main__":
    app.run(debug=True)