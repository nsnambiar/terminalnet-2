from flask import Flask, render_template, redirect, url_for, flash,abort,request
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from db import *
from forms import *
from authlib.integrations.flask_client import OAuth
from datetime import *
from sqlalchemy import desc
import base64
import os

app=Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['HEROKU_POSTGRESQL_COPPER_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Bootstrap(app)
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


login_manager=LoginManager()
login_manager.init_app(app)

# @app.template_filter('b64encode')
def b64encode(data):
    return base64.b64encode(data).decode()
app.jinja_env.filters['b64encode'] = b64encode


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/',methods=["GET","POST"])
def start():
    db.create_all()
    return redirect(url_for('view',page=0))


@app.route('/Page:<int:page>',methods=['GET'])
def view(page):
    per_page = 5
    posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page,per_page,error_out=False)
    issues = IssueBlogPost.query.order_by(desc(IssueBlogPost.id)).all()
    return render_template("index.html", all_post=posts, currentuser=current_user, issue_post=issues)




@app.route("/Registration",methods=["GET","POST"])
def registration():
    Reg_form = RegisterForm()
    img=0
    if Reg_form.validate_on_submit():
        new_user = User(email=Reg_form.email.data, name=Reg_form.name.data,img=img)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("start"))
    return render_template("registration.html", form=Reg_form, current_user=current_user)




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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('view', page=1))

@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    if current_user.is_authenticated:
        form = CreatePostForm()
        if form.validate_on_submit():
            pic = request.files['image']
            # if not pic:
            #     return 'No pic uploaded!', 400
            mimetype = pic.mimetype
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                body=form.body.data,
                img=pic.read(),
                filetype=mimetype,
                author=current_user,
                date=date.today().strftime("%b,%d,%Y"),
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("start"))
    else:
        flash("You need to login to Add New Post.")
        return redirect(url_for("login"))
    return render_template("addpost.html", form=form)


@app.route("/upload-issue",methods=["GET","POST"])
def issue():
    if current_user.is_authenticated:
        issueform = CreateissueForm()
        if issueform.validate_on_submit():
            pic = request.files['image']
            # if not pic:
            #     return 'No pic uploaded!', 400
            new_post = IssueBlogPost(
                title=issueform.title.data,
                body=issueform.body.data,
                img=pic.read(),
                author=current_user,
                date=date.today().strftime("%b %d, %Y"),
            )
            db.session.add(new_post)
            db.session.commit()
    else:
            flash("You need to login to Raise issue.")
            return redirect(url_for("login"))

    return render_template("addissue.html",currentuser=current_user,issueform=issueform)

@app.route("/issue:<post_id>", methods=["GET", "POST"])
def issues(post_id):
    comment = CommentForm()
    issuepost = IssueBlogPost.query.get(post_id)
    if comment.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        new_comment = IssueComment(
            text=comment.comment_text.data,
            comment_author=current_user,
            parent_post=issuepost
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("blog-posst.html",all_post=issuepost,comment=comment)

@app.route("/<post_id>", methods=["GET","POST"])
def show_blog(post_id):
    comment = CommentForm()
    request_post = BlogPost.query.get(post_id)
    if comment.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=comment.comment_text.data,
            comment_author=current_user,
            parent_post=request_post

        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("blog-posst.html",all_post=request_post,comment=comment)



@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        print(search)
        search_query = BlogPost.query.filter(BlogPost.title.contains(search.title())).all()
        issues = IssueBlogPost.query.order_by(desc(IssueBlogPost.id)).all()
        print(search_query)
        return render_template("index.html", all_post=search_query, issue_post=issues)


@app.route('/login/google')
def google_login():
    google = oauths.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize')
def google_authorize():
    google = oauths.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    usersemail=User.query.filter_by(email=resp['email']).first()
    if not usersemail:
        new_user = User(email=resp['email'], name=resp['given_name'],img=resp['picture'])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("start"))
    else:
        login_user(usersemail)
        return redirect(url_for("start"))


if __name__ == "__main__":
    app.run(debug=True)