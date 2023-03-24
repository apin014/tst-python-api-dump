from flask import Blueprint, render_template, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from .models import TemperatureAnomaly
import dotenv

dotenv.load_dotenv('..\.env')

main = Blueprint('main', __name__)

""" @main.route('/')
def index():
    return render_template('index.html') """

@main.route('/')
def index():
    return 'The API is running!'

@main.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    username = get_jwt_identity()
    return jsonify({'hello': 'from {}'.format(username)}), 200

@main.route('/api/data/all', methods=['GET'])
@jwt_required()
def data_all():
    data = TemperatureAnomaly.query.all()
    if not data:
        return jsonify({'status':'resource not found', 'msg':'there is no available data'}), 404
    
    resp = []
    for row in data:
        temperature_anomaly_data = {}
        temperature_anomaly_data['entity'] = row.entity
        temperature_anomaly_data['year'] = row.year
        temperature_anomaly_data['median_anomaly_from_1961_1990_avg'] = row.median_anomaly_from_1961_1990_avg
        temperature_anomaly_data['upper_bound_95percent_CI'] = row.upper_bound_95percent_CI
        temperature_anomaly_data['lower_bound_95percent_CI'] = row.lower_bound_95percent_CI
        
        resp.append(temperature_anomaly_data)
    
    return jsonify({'results':resp}), 200
    