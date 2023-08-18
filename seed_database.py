import os
import csv
from random import choice, randint
from datetime import datetime
from pprint import pprint

import crud
import model 
import server

os.system("dropdb ballpark-app")
os.system("createdb ballpark-app")

model.connect_to_db(server.app)

with server.app.app_context():
    model.db.create_all()

    with open('data/mlb-ballparks.csv') as f:
        ballpark_data = csv.DictReader(f)
    

        ballparks_in_db = []
        for ballpark in ballpark_data:

            
            ballpark_name, home_team, capacity, location, year_opened, surface, roof_type, ballpark_image, ballpark_dimensions, team_logo = (
                ballpark["ballpark_name"],
                ballpark["home_team"],
                ballpark["capacity"],
                ballpark["location"],
                ballpark["year_opened"],
                ballpark["surface"],
                ballpark["roof_type"],
                ballpark["ballpark_image"],
                ballpark["ballpark_dimensions"],
                ballpark["team_logo"]
            )

            db_ballpark = crud.create_ballpark(ballpark_name, home_team, capacity, location, year_opened, surface, roof_type, ballpark_image, ballpark_dimensions, team_logo)
            ballparks_in_db.append(db_ballpark)

    model.db.session.add_all(ballparks_in_db)
    model.db.session.commit()

    with open('data/unique-features.csv') as f:
        feature_data = csv.DictReader(f)

        features_in_db = []
        for feature in feature_data:

            unique_feature, ballpark= (
                feature["unique_feature"],
                feature["ballpark"]
            )

        db_feature = crud.create_feature(unique_feature, ballpark)
        features_in_db.append(db_feature)


