from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, DateField, PasswordField, validators
from wtforms.validators import DataRequired, Length

class CreateAccountForm(FlaskForm):
     username = StringField('username', [validators.InputRequired()])
     email = StringField('email', [validators.InputRequired()])
     password = PasswordField('password', [validators.InputRequired()])
     favorite_team = StringField('favorite team')
     submit = SubmitField('submit')
    

class LoginForm(FlaskForm):
    username = StringField('username',[validators.InputRequired()])
    password = PasswordField('password', [validators.InputRequired()])
    submit = SubmitField('submit')

class ReviewForm(FlaskForm):
    ballpark_selection = SelectField('Ballpark: ')
    visit_date = DateField('Visit Date: ')
    seat_location = StringField('Seat Location: ')
    description = TextAreaField('Description: ')
    seat_view = StringField('Seat View: ')
    favorite_food_tried = StringField('Favorite Food Tried: ')
    submit = SubmitField('Submit: ')

    def update_ballparks(self, ballparks):
        self.ballpark_selection.choices = [ (ballpark.ballpark_id, ballpark.ballpark_name) for ballpark in ballparks ]

class RatingForm(FlaskForm):
    ballpark_selection = SelectField("Ballpark")
    atmosphere_score = SelectField("Atmosphere", choices="012345")
    accessibility_score = SelectField("Accessibility", choices="012345")
    concessions_score = SelectField("Concessions", choices="012345")
    aesthetics_score = SelectField("Aesthetics", choices="012345")
    submit = SubmitField("Submit")


    def update_ballparks(self, ballparks):
        self.ballpark_selection.choices = [ (ballpark.ballpark_id, ballpark.ballpark_name) for ballpark in ballparks ]

class FeatureForm(FlaskForm):
    feature_selection = SelectField("Must Do's")
    submit = SubmitField("Submit")
    
    def update_features(self, features):
        self.feature_selection.choices = [ (feature.feature_id, feature.unique_feature) for feature in features ]