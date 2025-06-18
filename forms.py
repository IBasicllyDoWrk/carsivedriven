from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=4, max=25),
        Regexp("^[A-Za-z0-9_]+$", message="Username must contain only letters, numbers, or underscores")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match")
    ])
    name = StringField("Name", validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    age = IntegerField("Age", validators=[
        DataRequired(),
        NumberRange(min=10, max=120, message="Enter a valid age between 10 and 120")
    ])
    location = StringField("Location", validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class CarForm(FlaskForm):
    make = StringField("Make", validators=[
        DataRequired(),
        Length(max=30),
        Regexp("^[A-Za-z ]+$", message="Make should contain only letters and spaces")
    ])
    model = StringField("Model", validators=[
        DataRequired(),
        Length(max=30),
        Regexp("^[A-Za-z0-9 -]+$", message="Model can include letters, numbers, spaces and hyphens")
    ])
    model_year = StringField("Model Year", validators=[
        DataRequired(),
        Regexp("^(19|20)\d{2}$", message="Enter a valid 4-digit year between 1900–2099")
    ])
    engine = StringField("Engine", validators=[DataRequired(), Length(max=50)])
    transmission = StringField("Transmission", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Add Car")

class ProfileUpdateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=100)])
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=1, max=120)])
    location = StringField("Location", validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField("Update")
