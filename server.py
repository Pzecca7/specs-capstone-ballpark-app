from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import ReviewForm, LoginForm, CreateAccountForm, RatingForm, FeatureForm
from model import db, Review, User, Ballpark, Rating, BucketList, Feature, connect_to_db
from datetime import datetime
from pprint import pprint
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

@app.route("/ballparks/<ballpark_id>/features")
def features(ballpark_id):

    ballpark = crud.get_ballpark_by_id(ballpark_id)
    feature_form = FeatureForm()
    feature_form.update_features(Ballpark.query.get(ballpark_id).feature)
    

    return render_template("features.html", feature_form=feature_form, ballpark_id=ballpark_id, ballpark=ballpark)

@app.route("/create-bucket-list/<ballpark_id>", methods=["POST"])
def create_bucket_list(ballpark_id):

    if 'username' not in session:
        flash("You must be logged in to create your bucket list.")
        return redirect("/login")
    
    user = crud.get_by_username(session["username"])
    user_id = user.user_id

    feature_form = FeatureForm()
    feature_form.update_features(Ballpark.query.get(ballpark_id).feature)

    if feature_form.validate_on_submit():
        feature_id = feature_form.feature_selection.data
        completed = False
        bucket_list_item = crud.create_bucket_list(feature_id, user_id, completed)
        db.session.add(bucket_list_item)
        db.session.commit()
        return redirect(("/bucket-list/"))
    else:
        return redirect(("/home"))

@app.route("/bucket-list/")
def bucket_list():

    if 'username' not in session:
        flash("You must be logged in to see your bucket list.")
        return redirect("/login")

    user = crud.get_by_username(session["username"])  

    return render_template("bucket-list.html", user=user)

@app.route("/update-bucketlist/<bucket_list_id>")
def update_bucket_list(bucket_list_id):

    bucket_list_item = BucketList.query.get(bucket_list_id) 

    bucket_list_item.completed = True
    db.session.add(bucket_list_item)
    db.session.commit()

    return redirect("/bucket-list/")

@app.route("/review")
def review():

    review_form = ReviewForm()
    review_form.update_ballparks(Ballpark.query.all())

    return render_template("review.html", review_form=review_form)

@app.route("/add-review", methods=["POST"])
def add_review():

    if 'username' not in session:
        flash("You must be logged in to review your seats")
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
        return redirect(("/home"))

@app.route("/ballparks/<ballpark_id>/reviews")
def ballpark_reviews(ballpark_id):

    ballpark = crud.get_ballpark_by_id(ballpark_id)

    

    return render_template("ballpark-reviews.html", ballpark=ballpark)

@app.route("/rate")
def rate():

    rating_form = RatingForm()
    rating_form.update_ballparks(Ballpark.query.all())

    return render_template("rate.html", rating_form=rating_form)

@app.route("/create-rating", methods=["POST"])
def create_rating():

    if 'username' not in session:
        flash("You must be logged in to rate a ballpark")
        return redirect("/login")
    
    user = crud.get_by_username(session["username"])
    user_id = user.user_id

    rating_form = RatingForm()
    rating_form.update_ballparks(Ballpark.query.all())
    
    if rating_form.validate_on_submit():
        atmosphere_score = rating_form.atmosphere_score.data
        accessibility_score = rating_form.accessibility_score.data
        concessions_score = rating_form.concessions_score.data
        aesthetics_score = rating_form.aesthetics_score.data
        ballpark_id = rating_form.ballpark_selection.data
        rating = crud.create_rating(int(atmosphere_score), int(accessibility_score), int(concessions_score), int(aesthetics_score),user_id, ballpark_id)
        db.session.add(rating)
        db.session.commit()
        return redirect(("/ballparks"))
    else:
        return redirect(("/home"))

@app.route("/ballparks/<ballpark_id>/ratings")
def ballpark_ratings(ballpark_id):

    ballpark = crud.get_ballpark_by_id(ballpark_id)
    total_score = 0


    ballpark_ratings = []

    for rating in ballpark.ratings:

        total_score = rating.atmosphere_score + rating.concessions_score + rating.accessibility_score + rating.aesthetics_score

        rating.total_score = total_score

        ballpark_ratings.append(rating)


    return render_template("ballpark-ratings.html", ballpark=ballpark, ballpark_ratings=ballpark_ratings)

@app.route("/user-profile")
def profile():

    user = crud.get_by_username(session["username"])
    total_score = 0  

    for rating in user.ratings:

        total_score = rating.atmosphere_score + rating.concessions_score + rating.accessibility_score + rating.aesthetics_score

        rating.total_score = total_score


    return render_template("profile.html", user=user, total_score=total_score)

@app.route("/look-up-user/<user_id>")
def look_up_user(user_id):

    user = crud.get_user_by_id(user_id)
    total_score = 0  

    for rating in user.ratings:

        total_score = rating.atmosphere_score + rating.concessions_score + rating.accessibility_score + rating.aesthetics_score

        rating.total_score = total_score

    return render_template("user.html", user=user, total_score=total_score)

# @app.route("/delete-rating/<ratings_id>")
# def delete_rating(ratings_id):

#     ratings_to_delete = crud.get_ratings_by_id(ratings_id)
#     db.session.delete(ratings_to_delete)
#     db.session.commit()

#     return redirect("/ballparks")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
