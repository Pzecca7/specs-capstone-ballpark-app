from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import ReviewForm, LoginForm, CreateAccountForm, RatingForm
from model import db, Review, User, Ballpark, Rating, BucketList, connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def home():

    create_account_form = CreateAccountForm()

    return render_template("homepage.html", create_account_form = create_account_form )

@app.route("/create-account", methods=["POST"])
def create_account():

    print("apples")
    create_account_form = CreateAccountForm()
    
    if create_account_form.validate_on_submit():
        username = create_account_form.username.data
        email = create_account_form.email.data
        password = create_account_form.password.data
        favorite_team = create_account_form.favorite_team.data

        user = crud.get_by_username(username)
        if user:
            flash("Cannot create an account with that username. Try again.")
        else:
            user = crud.create_user(username, email, password, favorite_team)
            db.session.add(user)
            db.session.commit()
            flash("Account created! Please log in.")
        
        return redirect("/login")



@app.route("/login",  methods=["GET","POST"])
def login():
 
    login_form = LoginForm()

    if login_form.validate_on_submit():
        print("here")
        username = login_form.username.data
        password = login_form.password.data

        user = crud.get_by_username(username)

        if not user or user.password != password:
            flash("Invalid username or password")
            return redirect('/login')
        
        session["username"] = user.username
        flash("logged in")
        return redirect("/ballparks")
    
    return render_template("login.html", login_form=login_form)

@app.route("/logout")
def logout():
    del session["username"]
    flash("Logged out")
    return redirect("/login")

@app.route("/ballparks")
def all_ballparks():

    ballparks = crud.get_ballparks()

    return render_template("ballparks.html", ballparks=ballparks)

@app.route("/review")
def review():

    review_form = ReviewForm()
    review_form.update_ballparks(Ballpark.query.all())

    return render_template("review.html", review_form=review_form)

@app.route("/add-review", methods=["POST"])
def add_review():

    if 'username' not in session:
        return redirect("/login")
    
    user = crud.get_by_username(session["username"])
    user_id = user.user_id

    review_form = ReviewForm()
    review_form.update_ballparks(Ballpark.query.all())

    print(review_form.validate())
    print(review_form.is_submitted())
    print(review_form.errors)
    if review_form.validate_on_submit():
        visit_date = review_form.visit_date.data
        seat_location = review_form.seat_location.data
        description = review_form.description.data
        seat_view = review_form.seat_view.data
        favorite_food_tried = review_form.favorite_food_tried.data
        ballpark_id = review_form.ballpark_selection.data
        new_review = crud.create_review(visit_date, seat_location, description, seat_view, favorite_food_tried, user_id, ballpark_id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(("/ballparks"))
    else:
        return "not validated"

@app.route("/ballparks/<ballpark_id>/reviews")
def ballpark_reviews():

    return render_template("ballpark-reviews.html")

@app.route("/rate")
def rate():

    rating_form = RatingForm()
    rating_form.update_ballparks(Ballpark.query.all())

    return render_template("rate.html", rating_form=rating_form)

@app.route("/create-rating")
def create_rating():

    if 'username' not in session:
        return redirect("/login")
    
    user = crud.get_by_username(session["username"])

    rating_form = RatingForm()
    rating_form.update_ballparks(Ballpark.query.all())



    return redirect ("/ballparks")

@app.route("/ballparks/<ballpark_id>/ratings")
def ballpark_ratings():

    return render_template("ballpark-ratings.html")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
