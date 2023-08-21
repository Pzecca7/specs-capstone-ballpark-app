from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import ReviewForm
from model import db, Review, User, Ballpark, Rating, BucketList, connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/ballparks")
def all_ballparks():

    ballparks = crud.get_ballparks()

    return render_template("ballparks.html", ballparks=ballparks)

@app.route("/review")
def review():

    review_form = ReviewForm()

    return render_template("review.html", review_form=review_form)

@app.route("/add-review", methods=["POST"])
def add_review():

    review_form = ReviewForm()

    if review_form.validate_on_submit():
        visit_date = review_form.visit_date.data
        seat_location = review_form.seat_location.data
        description = review_form.description.data
        seat_view = review_form.seat_view.data
        favorite_food_tried = review_form.favorite_food_tried.data
        ballpark_id = review_form.ballpark_selection.data
        new_review = Review(visit_date, seat_location, description, seat_view, favorite_food_tried, user_id, ballpark_id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for("ballparks"))
    else:
        return redirect(url_for("home"))


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
