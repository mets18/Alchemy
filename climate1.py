import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Code for precipitation table
sel = [Measurement.date, func.max(Measurement.prcp)]
beg_date = dt.date(2017,8,23) - dt.timedelta(days=365)
last_12 = session.query(*sel).\
    filter(Measurement.date > beg_date).\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()

# Code for stations data
all_stations = session.query(distinct(Measurement.station)).all()

# Code for tobs data
beg_date_9281 = dt.date(2017,8,18) - dt.timedelta(days=365)
all_tobs = session.query(Measurement.tobs).\
    filter(Measurement.date > beg_date_9281, Measurement.station == 'USC00519281').\
    all()

# Code for start date only
sel2 = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
start_only = session.query(*sel2).\
    filter(Measurement.date > dt.date(2017,2,10),Measurement.station == 'USC00519281').\
    all()

# Code for start and end date
sel3 = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
start_end = session.query(*sel3).\
    filter(Measurement.date > dt.date(2017,2,10), Measurement.date < dt.date(2017,2,18), Measurement.station == 'USC00519281').\
    all()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017-02-10<br/>"
        f"/api/v1.0/2017-02-10/2017-02-17"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    
   

    # Construct dictionary of precip
    all_prcp = []
    for date, prcp in last_12:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
   
    
    # Return list of stations
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Return list of temperatures

    return jsonify(all_tobs)

@app.route("/api/v1.0/2017-02-10")
def temps_by_start_date():
    
    # Return temps starting at start date

    
    return jsonify(start_only)



@app.route("/api/v1.0/2017-02-10/2017-02-17")
def temps_start_end():
    
    
    # Return temps from start to end date
    
    return jsonify(start_end)
    

if __name__ == '__main__':
    app.run(debug=True)
