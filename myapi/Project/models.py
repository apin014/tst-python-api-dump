from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    
class TemperatureAnomaly(db.Model): # model yang akan dimanfaatkan dalam core API
    entity = db.Column(db.String(20), primary_key=True, nullable=False)
    year = db.Column(db.Integer, primary_key=True, nullable=False)
    median_anomaly_from_1961_1990_avg = db.Column(db.Float(4), nullable=True)
    upper_bound_95percent_CI = db.Column(db.Float(4), nullable=True)
    lower_bound_95percent_CI = db.Column(db.Float(4), nullable=True)