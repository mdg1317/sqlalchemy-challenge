# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"127.0.0.1:5000/api/v1.0/precipitation<br/>"
        f"127.0.0.1:5000/api/v1.0/stations<br/>"
        f"127.0.0.1:5000/api/v1.0/start<br/>"
        f"127.0.0.1:5000/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    return "Precipitation"

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    return "Stations"

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