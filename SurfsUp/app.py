# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home page
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"127.0.0.1:5000/api/v1.0/precipitation<br/>"
        f"127.0.0.1:5000/api/v1.0/stations<br/>"
        f"127.0.0.1:5000/api/v1.0/start<br/>"
        f"127.0.0.1:5000/api/v1.0/start/end<br/>"
    )


# Precipitation analysis page
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Print message to console
    print("Server received request for 'Precipitation' page...")

    # Get latest date and calculate date 12 months before
    latest_date = session.query(Measurement).order_by(Measurement.date.desc()).first().date
    latest_date_dt = dt.datetime.strptime(latest_date, "%Y-%m-%d")
    starting_date = (latest_date_dt - dt.timedelta(days=365)).strftime("%Y-%m-%d")

    # Query all precipitation data with the last year
    prcp_query = session.query(Measurement.date, Measurement.prcp)\
        .order_by(Measurement.date)\
        .filter(Measurement.date >= starting_date)\
        .all()

    # Put the queried data into a dictionary
    prcp_dict = {}
    for x in range(len(prcp_query)):
        prcp_dict[prcp_query[x][0]] = prcp_query[x][1]

    # Return the JSONified dictionary
    return jsonify(prcp_dict)


# Station analysis page
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")

    stations_query = session.query(Station).distinct().all()

    station_dict = []
    for q in stations_query:
        station_dict.append({"station": q.station, "name": q.name, "latitude": q.latitude, "longitude": q.longitude, "elevation": q.elevation})
    
    return jsonify(station_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    print("Server received request for 'Start' page...")
    return "Start"

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print("Server received request for 'Start/End' page...")
    return "Start/End"

if __name__ == "__main__":
    app.run(debug=True)