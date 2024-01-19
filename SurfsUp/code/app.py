# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy import desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station

Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
most_recent = session.query(Measurement.date).order_by(desc(Measurement.date)).first()

most_recent

latest_date = most_recent[0]

str(latest_date)

latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')

latest_date = latest_date.strftime('%Y-%m-%d')

latest_date 

year_before = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)

active_stations = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(desc(func.count(Measurement.tobs)))

most_active = active_stations[0]

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
#static route
@app.route("/")

def homepage():
    return (f"Cowabunga dude! Surfs up, or is it? Find out here!<br/>"
     f"Here's your available routes:<br/>"
        
        f"/api/v1.0/precipitation<br/>"
        
        f"/api/v1.0/stations<br/>"
        
        f"/api/v1.0/tobs<br/>"
        
        f"/api/v1.0/<start><br/>"
        
        f"/api/v1.0/<start>/<end><br/>")

@app.route("/api/v1.0/precipitaton")

def precipitation():
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_before).order_by(Measurement.date).all()
    
    precip_dict = list(np.ravel(precipitation_data))

    return(jsonify(precip_dict))

@app.route("/api/v1.0/stations")

def stations():
    stations_list = session.query(Station.station, Station.name).all()

    stations_dict = list(np.ravel(stations_list))

    return(jsonify(stations_dict))

@app.route("/api/v1.0/tobs")

def tobs():

    tobs_data = session.query(Measurement.tobs, Measurement.date).filter(Measurement.date >= year_before).filter(Measurement.station == most_active[0]).order_by(Measurement.date).order_by(Measurement.date).all()

    tobs_dict = list(np.ravel(tobs_data))

    return(jsonify(tobs_dict))


@app.route("/api/v1.0/<start>")

def startrange(date):
    ranged_query = session.query(Measurement.date,func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= date).all()
    
    ranged_dict = list(np.ravel(ranged_query))

    return(jsonify(ranged_dict))

@app.route("/api/v1.0/<start>/<end>")

def betweendates(date_start, date_end):
    inbetween_query = session.query(Measurement.date,func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= date_start).filter(Measurement.date <=date_end).all()
    
    inbetween_dict = list(np.ravel(inbetween_query))
    
    return(jsonify(inbetween_dict))





if __name__ == '__main__':
    app.run(debug=True) 
    