from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, DateTimeLocalField, PasswordField, validators
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username',[validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    favorite_team = StringField('favorite team')

class ReviewForm(FlaskForm):
    ballpark_selection = SelectField('ballpark')
    vist_date = DateTimeLocalField('visit date', validators=[DataRequired()])
    seat_location = StringField('team name')
    description = TextAreaField('description')
    seat_view = StringField('seat view')
    favorite_food_tried = StringField('favorite food tried')
    submit = SubmitField('submit')
