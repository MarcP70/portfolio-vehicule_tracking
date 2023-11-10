from flask import request, render_template, session, jsonify, redirect, url_for
from api.models.tracking_models import Tracking, TrackingCreationError, TrackingDeletionError
from api.app import app, login_required

# Liste les suivis pour un véhicule spécifique
@app.route('/vehicle/<vehicle_id>/list_trackings/')
@login_required
def list_trackings(vehicle_id):
    tracking = Tracking()
    try:
        vehicle_trackings = tracking.read_by_vehicle(vehicle_id)
        return render_template('list_trackings.html', vehicle_trackings=vehicle_trackings)
    except TrackingDeletionError as e:
        return jsonify({"error": str(e)}), 404

# Affiche un suivi spécifique
@app.route('/tracking/<tracking_id>/show_tracking/')
@login_required
def show_tracking(tracking_id):
    tracking = Tracking()
    try:
        tracking_data = tracking.read(tracking_id)
        if tracking_data:
            return render_template('show_tracking.html', trackingData=tracking_data)
        else:
            return jsonify({"error": "Suivi introuvable"}), 404
    except TrackingDeletionError as e:
        return jsonify({"error": str(e)}), 500

# Crée un nouveau suivi
@app.route('/vehicle/<vehicle_id>/create_tracking', methods=['POST'])
@login_required
def create_new_tracking(vehicle_id):
    try:
        tracking = Tracking()
        new_tracking = tracking.create(
            vehicle_id,
            date = request.form.get('date'),
            mileage = request.form.get('mileage'),
            tire_front_left = request.form.get('tireFrontLeft'),
            tire_front_right = request.form.get('tireFrontRight'),
            ref_tires_front = request.form.get('refTiresFront'),
            tire_rear_left = request.form.get('tireRearLeft'),
            tire_rear_right = request.form.get('tireRearRight'),
            ref_tires_rear = request.form.get('refTiresRear'),

            brake_pads_front = request.form.get('brakePadsFront'),
            ref_brake_pads_front = request.form.get('refBrakePadsFront'),
            brake_pads_rear = request.form.get('brakePadsRear'),
            ref_brake_pads_rear = request.form.get('refBrakePadsRear'),

            brake_disks_front = request.form.get('brakeDisksFront'),
            ref_brake_disks_front = request.form.get('refBrakeDisksFront'),
            brake_disks_rear = request.form.get('brakeDisksRear'),
            ref_brake_disks_rear = request.form.get('refBrakeDisksRear'),

            oil_change = request.form.get('oilChange'),
            ref_oil_change = request.form.get('refOilChange'),

            oil_filter = request.form.get('oilFilter'),
            ref_oil_filter = request.form.get('refOilFilter'),

            air_filter = request.form.get('airFilter'),
            ref_air_filter = request.form.get('refAirFilter'),

            fuel_filter = request.form.get('fuelFilter'),
            ref_fuel_filter = request.form.get('refFuelFilter'),

            cabin_filter = request.form.get('cabinFilter'),
            ref_cabin_filter = request.form.get('refCabinFilter'),
        )
        return jsonify(new_tracking), 201
    except TrackingCreationError as e:
        return jsonify({"error": str(e)}), 409

# Supprime un suivi
@app.route('/delete_tracking', methods=['POST'])
@login_required
def delete_trackings():
    try:
        tracking_id = request.form.get('tracking_id')
        tracking = Tracking()
        tracking.delete(tracking_id)
        return jsonify({"message": "Suivi supprimé avec succès"}), 200
    except TrackingDeletionError as e:
        return jsonify({"error": str(e)}), 404

# Met à jour un suivi
@app.route('/tracking/<tracking_id>/update_tracking', methods=['POST'])
@login_required
def update_tracking(tracking_id):
    try:
        tracking = Tracking()
        tracking.update(
            tracking_id,
            date = request.form.get('date'),
            mileage = request.form.get('mileage'),
            tire_front_left = request.form.get('tireFrontLeft'),
            tire_front_right = request.form.get('tireFrontRight'),
            ref_tires_front = request.form.get('refTiresFront'),
            tire_rear_left = request.form.get('tireRearLeft'),
            tire_rear_right = request.form.get('tireRearRight'),
            ref_tires_rear = request.form.get('refTiresRear'),

            brake_pads_front = request.form.get('brakePadsFront'),
            ref_brake_pads_front = request.form.get('refBrakePadsFront'),
            brake_pads_rear = request.form.get('brakePadsRear'),
            ref_brake_pads_rear = request.form.get('refBrakePadsRear'),

            brake_disks_front = request.form.get('brakeDisksFront'),
            ref_brake_disks_front = request.form.get('refBrakeDisksFront'),
            brake_disks_rear = request.form.get('brakeDisksRear'),
            ref_brake_disks_rear = request.form.get('refBrakeDisksRear'),

            oil_change = request.form.get('oilChange'),
            ref_oil_change = request.form.get('refOilChange'),

            oil_filter = request.form.get('oilFilter'),
            ref_oil_filter = request.form.get('refOilFilter'),

            air_filter = request.form.get('airFilter'),
            ref_air_filter = request.form.get('refAirFilter'),

            fuel_filter = request.form.get('fuelFilter'),
            ref_fuel_filter = request.form.get('refFuelFilter'),

            cabin_filter = request.form.get('cabinFilter'),
            ref_cabin_filter = request.form.get('refCabinFilter'),
        )
        return jsonify({"message": "Suivi mis à jour avec succès"}), 200
    except (TrackingCreationError, TrackingDeletionError) as e:
        return jsonify({"error": str(e)}), 409
