# import necessary libraries
import numpy as np
import pandas as pd

#geo library
from geo import getGeo

#distance library
from distance import closestBuddies

#sqlalchemy library
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#mysql library
import pymysql
pymysql.install_as_MySQLdb()

#flask library
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy

connection_string ="mysql://baff6e90fa899d:cc8fb5c8@us-cdbr-iron-east-05.cleardb.net/heroku_69314c212045914"
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Fitness(db.Model):
    __tablename__ = 'fitness'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    name = db.Column(db.String(64))
    dateofbirth = db.Column(db.String(64))
    address = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    martialstatus = db.Column(db.String(64))
    level = db.Column(db.String(64))
    sports = db.Column(db.String(64))
    sportsBrands = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    country = db.Column(db.String(64))

    def __repr__(self):
        return '<Fitness %r>' % (self.name)


# @app.before_first_request
# def setup():
#     Recreate database each time for demo
#     db.drop_all()
#     db.create_all()


@app.route("/")
def home():


    # buddy1 = Fitness(email="asela.d82@gmail.com", \
    #                 name="asela dassanayake", \
    #                 dateofbirth="08-15-1982", \
    #                 address="26/2d,Sri Dharmapala Mawatha,Mount Lavinia,Sri Lanka",\
    #                 gender="Male",\
    #                 martialstatus="Single",\
    #                 level="Expert",\
    #                 sports="Tennis",\
    #                 sportsBrands="Nike",\
    #                 lat = 6.8443913,\
    #                 lng = 79.8635164,\
    #                 country = "Sri Lanka")

    # buddy2 = Fitness(email="bobby.t@gmail.com", \
    #                 name="Bobby Taylor", \
    #                 dateofbirth="03-19-1982", \
    #                 address="saint louis,usa",\
    #                 gender="Male",\
    #                 martialstatus="Married",\
    #                 level="Advanced",\
    #                 sports="Swimming",\
    #                 sportsBrands="Speedo",\
    #                 lat = 38.6270025,\
    #                 lng = -90.19940419999999,\
    #                 country = "USA")

    # buddy3 = Fitness(email="john.madeo@gmail.com", \
    #                 name="jean madeo", \
    #                 dateofbirth="01-25-1980", \
    #                 address="paris,france",\
    #                 gender="Male",\
    #                 martialstatus="Married with Children",\
    #                 level="Beginner",\
    #                 sports="Walking",\
    #                 sportsBrands="Puma",\
    #                 lat = 48.856614,\
    #                 lng = 2.3522219,\
    #                 country = "France")

    # buddy4 = Fitness(email="wendy.w@gmail.com", \
    #                 name="wendy walsh", \
    #                 dateofbirth="07-20-1985", \
    #                 address="doha,qatar",\
    #                 gender="Female",\
    #                 martialstatus="Single",\
    #                 level="Advanced",\
    #                 sports="Swimming",\
    #                 sportsBrands="Nike",\
    #                 lat = 25.2854473,\
    #                 lng = 51.53103979999999,\
    #                 country = "Qatar")


    # db.session.add(buddy1)
    # db.session.add(buddy2)
    # db.session.add(buddy3)
    # db.session.add(buddy4)
    # db.session.commit()

    return render_template("index.html")

# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        email = request.form["exampleInputEmail"]
        name = request.form["exampleInputName"]
        dateofbirth = request.form["exampleInputDateofBirth"]
        address = request.form["exampleInputAddress"]
        gender = request.form["optionsRadiosGender"]
        martialstatus = request.form["optionsRadiosMarital"]
        level = request.form["optionsRadiosLevel"]
        sports = request.form["sports"]
        sportsBrands = request.form["sportsBrands"]

        # google geolocate
        geoAddress = getGeo(address)
        lat = geoAddress['lat']
        lng = geoAddress['lng']
        country = geoAddress['country']

        print(email,name,dateofbirth,address,gender,martialstatus,level,sports,sportsBrands,lat,lng,country)

        buddy = Fitness(email=email, \
                        name=name, \
                        dateofbirth=dateofbirth, \
                        address=address,\
                        gender=gender,\
                        martialstatus=martialstatus,\
                        level=level,\
                        sports=sports,\
                        sportsBrands=sportsBrands,\
                        lat = lat,\
                        lng = lng,\
                        country = country)
        db.session.add(buddy)
        db.session.commit()

        return redirect(url_for('home'), code=302)

    return render_template("index.html")

@app.route("/api/data")
def data():
    results = db.session.query(Fitness.id, Fitness.dateofbirth, Fitness.gender,
                                Fitness.martialstatus,Fitness.level,Fitness.sports,Fitness.sportsBrands,
                                Fitness.country).all()

    buddies = []
    for result in results:
        buddies.append({
            "id": result[0],
            "date of birth": result[1],
            "gender": result[2],
            "martial status": result[3],
            "level": result[4],
            "sports": result[5],
            "sports brands": result[6],
            "country": result[7]
        })
    return jsonify(buddies) 


@app.route("/api/data/dashboard")
def plotting():

    sel = [Fitness.sports, func.count(Fitness.sports)]
    results = db.session.query(*sel).group_by(Fitness.sports).all()
    df = pd.DataFrame(results, columns=['sports', 'buddies'])
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/data/dashboard/map")
def plotting_map():

    results = db.session.query(Fitness.lat,Fitness.lng).all()

    locations = []
    for result in results:
        locations.append({
            "lat": result[0],
            "lng": result[1]
        })
    return jsonify(locations) 


@app.route("/api/data/dashboard/pie")
def plotting_pie():

    sel = [Fitness.sportsBrands, func.count(Fitness.id)]
    results = db.session.query(*sel).group_by(Fitness.sportsBrands).all()
    df = pd.DataFrame(results, columns=['sportsBrands', 'Frequency'])
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/data/dashboard/barH")
def plotting_barH():

    sel = [Fitness.gender, func.count(Fitness.id)]
    results = db.session.query(*sel).group_by(Fitness.gender).all()
    df = pd.DataFrame(results, columns=['Gender', 'Frequency'])
    return jsonify(df.to_dict(orient="records"))

@app.route("/distance")
def distance():
    df = closestBuddies()
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run()
