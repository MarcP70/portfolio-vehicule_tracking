from flask import request, render_template, session, jsonify, redirect, url_for
from api.models.tracking_models import (
    Tracking,
    TrackingCreationError,
    TrackingDeletionError
)
from api.app import app, login_required


@app.route('/vehicle/<vehicle_id>/list_trackings/')
@login_required
def list_trackings(vehicle_id):
    """
    Retrieves all tracking entries for a given vehicle ID and returns a
        rendered HTML template with the tracking entries.

    Args:
        vehicle_id (str): The ID of the vehicle for which to retrieve
            entries.

    Returns:
        If the retrieval is successful, the function returns a rendered HTML
            template with the tracking entries.
        If there is an error during the retrieval, the function returns a JSON
            response with an error message.
    """
    tracking = Tracking()
    try:
        vehicle_trackings = tracking.read_by_vehicle(vehicle_id)
        return render_template('list_trackings.html',
                               vehicle_trackings=vehicle_trackings)
    except TrackingDeletionError as e:
        return jsonify({"error": str(e)}), 404


@app.route('/tracking/<tracking_id>/show_tracking/')
@login_required
def show_tracking(tracking_id):
    """
    Retrieves a specific tracking entry based on the provided tracking ID.

    Args:
        tracking_id (str): The ID of the tracking entry to retrieve.

    Returns:
        If the tracking entry is found, it returns a rendered template with
            the tracking data.
        If the tracking entry is not found, it returns a JSON response with an
            error message indicating that the tracking entry was not found.
        If there is an error during the retrieval of the tracking entry, it
            returns a JSON response with the error message.
    """
    tracking = Tracking()
    try:
        tracking_data = tracking.read(tracking_id)
        if tracking_data:
            return render_template('show_tracking.html',
                                   trackingData=tracking_data)
        else:
            return jsonify({"error": "Suivi introuvable"}), 404
    except TrackingDeletionError as e:
        return jsonify({"error": str(e)}), 500


@app.route('/vehicle/<vehicle_id>/create_tracking', methods=['POST'])
@login_required
def create_new_tracking(vehicle_id):
    """
    Creates a new tracking entry for a vehicle using the Tracking class.

    Args:
        vehicle_id (str): The ID of the vehicle.

    Returns:
        tuple: A tuple containing the created tracking entry as JSON and a
            status code.

    Raises:
        TrackingCreationError: If there is an error during the creation of the
            tracking entry.
    """
    try:
        tracking = Tracking()
        new_tracking = tracking.create(
            vehicle_id,
            date=request.form.get('date'),
            mileage=request.form.get('mileage'),
            tire_front_left=request.form.get('tireFrontLeft'),
            tire_front_right=request.form.get('tireFrontRight'),
            ref_tires_front=request.form.get('refTiresFront'),
            tire_rear_left=request.form.get('tireRearLeft'),
            tire_rear_right=request.form.get('tireRearRight'),
            ref_tires_rear=request.form.get('refTiresRear'),
            brake_pads_front=request.form.get('brakePadsFront'),
            ref_brake_pads_front=request.form.get('refBrakePadsFront'),
            brake_pads_rear=request.form.get('brakePadsRear'),
            ref_brake_pads_rear=request.form.get('refBrakePadsRear'),
            brake_disks_front=request.form.get('brakeDisksFront'),
            ref_brake_disks_front=request.form.get('refBrakeDisksFront'),
            brake_disks_rear=request.form.get('brakeDisksRear'),
            ref_brake_disks_rear=request.form.get('refBrakeDisksRear'),
            oil_change=request.form.get('oilChange'),
            ref_oil_change=request.form.get('refOilChange'),
            oil_filter=request.form.get('oilFilter'),
            ref_oil_filter=request.form.get('refOilFilter'),
            air_filter=request.form.get('airFilter'),
            ref_air_filter=request.form.get('refAirFilter'),
            fuel_filter=request.form.get('fuelFilter'),
            ref_fuel_filter=request.form.get('refFuelFilter'),
            cabin_filter=request.form.get('cabinFilter'),
            ref_cabin_filter=request.form.get('refCabinFilter'),
        )
        return jsonify(new_tracking), 201
    except TrackingCreationError as e:
        return jsonify({"error": str(e)}), 409


@app.route('/delete_tracking', methods=['POST'])
@login_required
def delete_trackings():
    """
    Deletes a specific tracking entry.

    :return: JSON response with success message if deletion is successful,
        or error message if there is an error.
    :rtype: flask.Response
    """
    try:
        tracking_id = request.form.get('tracking_id')
        tracking = Tracking()
        tracking.delete(tracking_id)
        return jsonify({"message": "Suivi supprimé avec succès"}), 200
    except TrackingDeletionError as e:
        return jsonify({"error": str(e)}), 404


@app.route('/tracking/<tracking_id>/update_tracking', methods=['POST'])
@login_required
def update_tracking(tracking_id):
    """
    Update a specific tracking entry in a vehicle tracking system.

    Args:
        tracking_id (str): The ID of the tracking entry to be updated.

    Returns:
        If the update is successful, a JSON response with a success message.
        If there is an error during the update, a JSON response with an
            error message.
    """
    try:
        tracking = Tracking()
        tracking.update(
            tracking_id,
            date=request.form.get('date'),
            mileage=request.form.get('mileage'),
            tire_front_left=request.form.get('tireFrontLeft'),
            tire_front_right=request.form.get('tireFrontRight'),
            ref_tires_front=request.form.get('refTiresFront'),
            tire_rear_left=request.form.get('tireRearLeft'),
            tire_rear_right=request.form.get('tireRearRight'),
            ref_tires_rear=request.form.get('refTiresRear'),
            brake_pads_front=request.form.get('brakePadsFront'),
            ref_brake_pads_front=request.form.get('refBrakePadsFront'),
            brake_pads_rear=request.form.get('brakePadsRear'),
            ref_brake_pads_rear=request.form.get('refBrakePadsRear'),
            brake_disks_front=request.form.get('brakeDisksFront'),
            ref_brake_disks_front=request.form.get('refBrakeDisksFront'),
            brake_disks_rear=request.form.get('brakeDisksRear'),
            ref_brake_disks_rear=request.form.get('refBrakeDisksRear'),
            oil_change=request.form.get('oilChange'),
            ref_oil_change=request.form.get('refOilChange'),
            oil_filter=request.form.get('oilFilter'),
            ref_oil_filter=request.form.get('refOilFilter'),
            air_filter=request.form.get('airFilter'),
            ref_air_filter=request.form.get('refAirFilter'),
            fuel_filter=request.form.get('fuelFilter'),
            ref_fuel_filter=request.form.get('refFuelFilter'),
            cabin_filter=request.form.get('cabinFilter'),
            ref_cabin_filter=request.form.get('refCabinFilter'),
        )
        return jsonify({"message": "Suivi mis à jour avec succès"}), 200
    except (TrackingCreationError, TrackingDeletionError) as e:
        return jsonify({"error": str(e)}), 409
