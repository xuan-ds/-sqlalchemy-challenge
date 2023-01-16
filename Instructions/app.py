import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func

from flask import Flask, jsonify
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Climate App<br/>"
        f"<br/>"
        f"Here are the availlable routes:<br/> "
        f"<br/>"
        f"Precipitation Analysis:<br/>" 
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Station List: <br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Analysis:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"The min/avg/max temperature for a specified start or start-end date:<br/>"
        f"/api/v1.0/<start>*StartDate<br/>"
        f"/api/v1.0/<start>*StartDate/<end>*EndDate<br/>"
        f"<br/>"
        f"*Enter a date in YYYYMMDD formate, numbers only.<br/>"
        f"(Due to the data limitation, enter the date between 20100101 to 20170823.)<br/> "
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session from Python to the DB
    session = Session(engine)

    # Query Measurement
    result_date = dt.date(2017,8,23)-dt.timedelta(days=365)

    result_prcp = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= result_date).all()  
    session.close()

    # Create a dictionary
    precipitation_dict = {date:prcp for date, prcp in result_prcp}

    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create session from Python to the DB
    session = Session(engine)

    # Query Measurement
    station_query = session.query(Station.station,Station.name).all()
    
    session.close()

    # Create a dictionary
    station_dict = {station:name for station, name in station_query}

    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session from Python to the DB
    session = Session(engine)

    # Query Measurement
    USC00519281_tobs_date = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.station == "USC00519281").\
                filter(Measurement.date >= dt.date(2016,8,23)).all()

    session.close()

    # Create a dictionary
    tobs_dict = {date:prcp for date, prcp in USC00519281_tobs_date}

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start_only(start):
    # Query Measurement
    session = Session(engine)
    tobs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    session.close()

    #Create a list
    tobs_list = list(np.ravel(tobs))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start, end):

    # Query Measurement
    session = Session(engine)

    tobs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()
                
    session.close()

    #Create a list
    tobs_list = list(np.ravel(tobs))

    return jsonify(tobs_list)


if __name__ == '__main__':
    app.run(debug=True)
