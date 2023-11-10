from flask import request, render_template, session, jsonify
from api.models.vehicle_models import Vehicle, VehicleCreationError, VehicleDeletionError
from api.app import app, login_required
import requests

@app.route('/dashboard/')
@login_required
def dashboard():
    user_id = session['user']['_id']
    vehicle = Vehicle()
    user_vehicles = vehicle.read(user_id)
    return render_template('dashboard.html', user_vehicles=user_vehicles)

@app.route('/create_vehicle/', methods=['GET', 'POST'])
@login_required
def create_vehicle():
    if request.method == 'POST':
        user_id = session['user']['_id']
        try:
            vehicle = Vehicle()
            new_vehicle = vehicle.create(
                user_id,
                request.form.get('registrationNumber'),
                request.form.get('brand'),
                request.form.get('model'),
                request.form.get('description'),
                request.form.get('firstRegistrationDate'),
                request.form.get('energy'),
                request.form.get('gearbox'),
                request.form.get('typeMine'),
                request.form.get('vin')
            )
            return jsonify(new_vehicle), 201
        except VehicleCreationError as e:
            return jsonify({"error": str(e)}), 409
    else:
        return render_template('create_vehicle.html')

@app.route('/vehicle/<vehicle_id>/create_tracking/')
@login_required
def create_tracking_form(vehicle_id):
    vehicle = Vehicle()
    try:
        vehicle_data = vehicle.read(session['user']['_id'], vehicle_id=vehicle_id)
        if not vehicle_data:
            return "Véhicule introuvable", 404
        return render_template('create_tracking.html', vehicle=vehicle_data)
    except VehicleDeletionError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_vehicle/', methods=['POST'])
@login_required
def delete_vehicle():
    vehicle_id = request.form.get('vehicle_id')
    vehicle = Vehicle()
    try:
        delete_message = vehicle.delete(vehicle_id)
        return jsonify(delete_message), 200
    except VehicleDeletionError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/search_api_registrationNumber', methods=['POST'])
@login_required
def search_api_registrationNumber():
    registrationNumber = request.form['registrationNumber']
    if registrationNumber:

        token = "TokenDemoRapidapi"

        url = \
    "https://api-plaque-immatriculation-siv.p.rapidapi.com/get-vehicule-info"
        querystring = {
            "token": token,
            "host_name": "https://apiplaqueimmatriculation.com",
            "immatriculation": registrationNumber,
        }

        headers = {
            "X-RapidAPI-Key":
            "bd0dfd9713msh7e14a295c8d45bcp12956ajsndab3a5183800",
            "X-RapidAPI-Host": "api-plaque-immatriculation-siv.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if 'data' in data and 'marque' in data['data']:
            brand = data['data']['marque']
            model = data['data']['modele']
            description = data['data']['sra_commercial']
            firstRegistrationDate = data['data']['date1erCir_fr']
            energy = data['data']['energieNGC']
            gearbox = data['data']['boite_vitesse']
            typeMine = data['data']['type_mine']
            vin = data['data']['vin']

            return jsonify({'brand': brand,
                            'model': model,
                            'description': description,
                            'firstRegistrationDate': firstRegistrationDate,
                            'energy': energy,
                            'gearbox': gearbox,
                            'typeMine': typeMine,
                            'vin': vin
                            }), 200

        else:

            return jsonify({"error": "Ce véhicule n'a pas été trouvé"}), 500
    else:

        return jsonify({"error": "Numéro d'immatriculation manquant"}), 500
