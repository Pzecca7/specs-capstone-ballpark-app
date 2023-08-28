from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    favorite_team = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"

class Ballpark(db.Model):

    __tablename__ = "ballparks"

    ballpark_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ballpark_name = db.Column(db.String)
    home_team = db.Column(db.String)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String)
    year_opened = db.Column(db.Integer)
    surface = db.Column(db.String)
    roof_type = db.Column(db.String)
    ballpark_image = db.Column(db.String)
    ballpark_dimensions = db.Column(db.String)
    team_logo = db.Column(db.String)

    def __repr__(self):
        return f"<Ballpark ballpark_id={self.ballpark_id} ballpark_name={self.ballpark_name}>"

class Feature(db.Model):

    __tablename__ = "features"

    feature_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    unique_feature = db.Column(db.String)
    ballpark_id = db.Column(db.Integer, db.ForeignKey("ballparks.ballpark_id"))

    ballpark = db.relationship("Ballpark", backref="feature")

    def __repr__(self):
        return f"<Feature feature_id={self.feature_id} unique_feature={self.unique_feature}>"

class BucketList(db.Model):

    __tablename__ = "bucket_lists"

    bucket_list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    feature_id = db.Column(db.Integer, db.ForeignKey("features.feature_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    completed = db.Column(db.Boolean)

    user = db.relationship("User", backref="bucket_list")
    feature = db.relationship("Feature", backref="bucket_list")

    def __repr__(self):
        return f"<Bucket-List bucket_list_id={self.bucket_list_id} feature_id={self.feature_id}>"

class Review(db.Model):

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    visit_date = db.Column(db.DateTime)
    seat_location = db.Column(db.String)
    description = db.Column(db.Text)
    seat_view = db.Column(db.String)
    favorite_food_tried = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    ballpark_id = db.Column(db.Integer, db.ForeignKey("ballparks.ballpark_id"))

    user = db.relationship("User", backref="reviews")
    ballpark = db.relationship("Ballpark", backref="reviews")

    def __repr__(self):
        return f"<Review review_id={self.review_id} visit_date={self.visit_date}>"

class Rating(db.Model): 

    __tablename__ = "ratings"

    ratings_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    atmosphere_score = db.Column(db.Integer)
    accessibility_score = db.Column(db.Integer)
    concessions_score = db.Column(db.Integer)
    aesthetics_score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    ballpark_id = db.Column(db.Integer, db.ForeignKey("ballparks.ballpark_id"))

    user = db.relationship("User", backref="ratings")
    ballpark = db.relationship("Ballpark", backref="ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.feature_id} atmosphere_score={self.atmosphere_scrore} accessibility_score={self.accessibility_score} concessions_score={self.concessions_score}>  asethetics_score={self.aesthetics_score}"


def connect_to_db(flask_app, echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)