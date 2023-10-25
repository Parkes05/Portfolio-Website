from flask_wtf import FlaskForm
from wtforms import StringField, URLField, PasswordField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

class InputForm(FlaskForm):
    table = StringField(label='Table', validators=[DataRequired()])
    title = StringField(label='Title', validators=[DataRequired()])
    description = TextAreaField(label='Description', validators=[DataRequired()])
    img_url = URLField(label='Image_url', validators=[DataRequired()])
    github_url = URLField(label='Github_url', validators=[DataRequired()])
    submit = SubmitField(label='Submit')