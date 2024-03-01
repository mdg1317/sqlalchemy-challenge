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

# Store latest date and starting date for use in multiple routes
latest_date = session.query(Measurement).order_by(Measurement.date.desc()).first().date
latest_date_dt = dt.datetime.strptime(latest_date, "%Y-%m-%d")
starting_date = (latest_date_dt - dt.timedelta(days=365)).strftime("%Y-%m-%d")

# Home page
@app.route("/")
def home():
    # Print message to console
    print("Server received request for 'Home' page...")

    # Return all available routes
    return (
        f"127.0.0.1:5000/api/v1.0/precipitation<br/>"
        f"127.0.0.1:5000/api/v1.0/stations<br/>"
        f"127.0.0.1:5000/api/v1.0/tobs<br/>"
        f"127.0.0.1:5000/api/v1.0/start<br/>"
        f"127.0.0.1:5000/api/v1.0/start/end<br/>"
    )


# Precipitation analysis page
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Print message to console
    print("Server received request for 'Precipitation' page...")

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
    # Print message to console
    print("Server received request for 'Stations' page...")

    # Query all station data
    stations_query = session.query(Station).distinct().all()

    # Put the queried data into a dictionary
    station_dict = []
    for q in stations_query:
        station_dict.append({"station": q.station, "name": q.name, "latitude": q.latitude, "longitude": q.longitude, "elevation": q.elevation})
    
    # Return the JSONified dictionary
    return jsonify(station_dict)


# TOBS analysis page
@app.route("/api/v1.0/tobs")
def tobs():
    # Print message to console
    print("Server received request for 'TOBS' page...")

    # Get the most active station
    most_active_station = session.query(Measurement.station)\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc()).all()[0][0]
    
    # Query all temperature data over last 12 months
    temp_query = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= starting_date).all()
    
    # Put the queried data into a dictionary
    temp_dict = {}
    for x in range(len(temp_query)):
        temp_dict[temp_query[x][0]] = temp_query[x][1]

    # Return the JSONified dictionary
    return jsonify(temp_dict)


# Start route
@app.route("/api/v1.0/<start>")
def start(start):
    # Print message to console
    print("Server received request for 'Start' page...")

    # Query all temperatures starting from specified date
    temp_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .group_by(Measurement.date)\
        .filter(Measurement.date >= start).all()
    
    # Put the queried data into a dictionary
    temp_list = []
    for x in range(len(temp_query)):
        temp_dict = {}
        temp_dict["date"] = temp_query[x][0]
        temp_dict["min"] = temp_query[x][1]
        temp_dict["avg"] = temp_query[x][2]
        temp_dict["max"] = temp_query[x][3]
        temp_list.append(temp_dict)

    # Return the JSONified dictionary
    return jsonify(temp_list)


# Start/end routes
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Print message to console
    print("Server received request for 'Start/End' page...")

    # Query all temperatures starting from specified date
    temp_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .group_by(Measurement.date)\
        .filter((Measurement.date >= start) & (Measurement.date <= end)).all()
    
    # Put the queried data into a dictionary
    temp_list = []
    for x in range(len(temp_query)):
        temp_dict = {}
        temp_dict["date"] = temp_query[x][0]
        temp_dict["min"] = temp_query[x][1]
        temp_dict["avg"] = temp_query[x][2]
        temp_dict["max"] = temp_query[x][3]
        temp_list.append(temp_dict)

    # Return the JSONified dictionary
    return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug=True)