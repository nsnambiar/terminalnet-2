from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, validators,FileField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField


class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    image = FileField('Upload Image')
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CreateissueForm(FlaskForm):
    title = StringField("Issue Title", validators=[DataRequired()])
    body = CKEditorField("Issue Body", validators=[DataRequired()])
    image = FileField('Upload Image')
    submit = SubmitField("Submit Issue")


class Login(FlaskForm):
    name=StringField("Name", validators=[DataRequired(),validators.Regexp(r'^[\w.@+-]+$')])
    email = StringField('Email',validators=[DataRequired()])
    submit=SubmitField("Login")


class RegisterForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!.")


class CommentForm(FlaskForm):
    comment_text = TextAreaField( "",validators=[DataRequired()])
    submit = SubmitField("Submit Comment")













