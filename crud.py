from model import db, User, Ballpark, Feature, BucketList, Review, Rating

def create_user(username, email, password, favorite_team):
    """Create and return a new user."""

    user = User(username=username, email=email, password=password, favorite_team=favorite_team)

    return user

def get_by_username(username):

    user = User.query.filter(User.username == username).first()

    return user

def create_ballpark(ballpark_name, home_team, capacity, location, year_opened, surface ,roof_type, ballpark_image, ballpark_dimensions, team_logo ):

    ballpark = Ballpark(ballpark_name=ballpark_name, home_team=home_team, capacity=capacity, location=location, year_opened=year_opened, surface=surface, roof_type=roof_type, ballpark_image=ballpark_image, ballpark_dimensions=ballpark_dimensions, team_logo=team_logo)

    return ballpark

def get_ballparks():
    
    return Ballpark.query.all()

def create_feature(unique_feature, ballpark_id):
    
    feature = Feature(unique_feature=unique_feature, ballpark_id=ballpark_id)

    return feature

def create_bucket_list(feature, ballpark, completed):

    bucket_list = BucketList(feature=feature, ballpark=ballpark, completed=completed)

    return bucket_list

def create_review(visit_date, seat_location, description, seat_view, favorite_food_tried, user_id, ballpark_id):

    review = Review(visit_date=visit_date, seat_location=seat_location, description=description, seat_view=seat_view, favorite_food_tried=favorite_food_tried, user_id=user_id, ballpark_id=ballpark_id)

    return review

def create_rating(atmosphere_score, acessibility_score, concessions_score, aesthetics_score):

    rating = Rating(atmosphere_score=atmosphere_score, acessibility_score=acessibility_score, concessions_score=concessions_score, aesthetics_score=aesthetics_score)

    return rating

