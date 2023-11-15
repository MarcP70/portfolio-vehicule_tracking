from flask import request, render_template, session, jsonify
from api.models.vehicle_models import (
    Vehicle,
    VehicleCreationError,
    VehicleDeletionError,
)
from api.app import app, login_required
import requests


@app.route("/dashboard/")
@login_required
def dashboard():
    """
    Retrieves the vehicles belonging to a user from a database and renders a
        template with the retrieved vehicles.

    Returns:
        The rendered template with the retrieved vehicles.
    """
    user_id = session["user"]["_id"]
    vehicle = Vehicle()
    user_vehicles = vehicle.read(user_id)
    return render_template("dashboard.html", user_vehicles=user_vehicles)


@app.route("/create_vehicle/", methods=["GET", "POST"])
@login_required
def create_vehicle():
    """
    Creates a new vehicle object and calls its create method with the provided
        form data.

    Returns a JSON response with the created vehicle details and status
        code 201 if the creation is successful.
    Returns a JSON response with an error message and status code 409
        if there is an error during the creation.
    """
    if request.method == "POST":
        user_id = session["user"]["_id"]
        try:
            vehicle = Vehicle()
            new_vehicle = vehicle.create(
                user_id,
                request.form.get("registrationNumber"),
                request.form.get("brand"),
                request.form.get("model"),
                request.form.get("description"),
                request.form.get("firstRegistrationDate"),
                request.form.get("energy"),
                request.form.get("gearbox"),
                request.form.get("typeMine"),
                request.form.get("vin"),
            )
            return jsonify(new_vehicle), 201
        except VehicleCreationError as e:
            return jsonify({"error": str(e)}), 409
    else:
        return render_template("create_vehicle.html")


@app.route("/vehicle/<vehicle_id>/create_tracking/")
@login_required
def create_tracking_form(vehicle_id):
    """
    Create a tracking form for a specific vehicle.

    Args:
        vehicle_id (str): The ID of the vehicle for which the tracking form
            needs to be created.

    Returns:
        tuple: A tuple containing the tracking form data and status code.

    Raises:
        VehicleDeletionError: If there is an error during the deletion of the
            vehicle.
    """
    vehicle = Vehicle()
    try:
        vehicle_data = vehicle.read(
            session["user"]["_id"], vehicle_id=vehicle_id
        )
        if not vehicle_data:
            return "Véhicule introuvable", 404
        return render_template("create_tracking.html", vehicle=vehicle_data)
    except VehicleDeletionError as e:
        raise VehicleDeletionError(str(e))


@app.route("/delete_vehicle/", methods=["POST"])
@login_required
def delete_vehicle():
    """
    Deletes a vehicle from the database based on the provided vehicle ID.

    :return: A JSON response with a success message and status code 200
                if the deletion is successful.
             A JSON response with an error message and status code 404
                if there is an error during deletion.
    """
    vehicle_id = request.form.get("vehicle_id")
    vehicle = Vehicle()
    try:
        delete_message = vehicle.delete(vehicle_id)
        return jsonify(delete_message), 200
    except VehicleDeletionError as e:
        return jsonify({"error": str(e)}), 404


@app.route("/search_api_registrationNumber", methods=["POST"])
@login_required
def search_api_registrationNumber():
    """
    Retrieves information about a vehicle based on its registration number.

    Args:
        None

    Returns:
        If the vehicle information is found:
            JSON response containing the vehicle brand, model, description,
                first registration date, energy type, gearbox type, type mine,
                    and VIN with a status code of 200.
        If the vehicle information is not found:
            Error JSON response with a status code of 500 indicating that the
                vehicle was not found.
        If the registration number is missing:
            Error JSON response with a status code of 500 indicating that the
                registration number is missing.
    """

    registrationNumber = request.form["registrationNumber"]
    if registrationNumber:
        token = "TokenDemoRapidapi"

        url = "https://api-plaque-immatriculation-siv.p.rapidapi.com/get-vehicule-info"
        querystring = {
            "token": token,
            "host_name": "https://apiplaqueimmatriculation.com",
            "immatriculation": registrationNumber,
        }

        headers = {
            "X-RapidAPI-Key": "",
            "X-RapidAPI-Host": "api-plaque-immatriculation-siv.p.rapidapi.com",
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if "data" in data and "marque" in data["data"]:
            brand = data["data"]["marque"]
            model = data["data"]["modele"]
            description = data["data"]["sra_commercial"]
            firstRegistrationDate = data["data"]["date1erCir_fr"]
            energy = data["data"]["energieNGC"]
            gearbox = data["data"]["boite_vitesse"]
            typeMine = data["data"]["type_mine"]
            vin = data["data"]["vin"]

            return (
                jsonify(
                    {
                        "brand": brand,
                        "model": model,
                        "description": description,
                        "firstRegistrationDate": firstRegistrationDate,
                        "energy": energy,
                        "gearbox": gearbox,
                        "typeMine": typeMine,
                        "vin": vin,
                    }
                ),
                200,
            )

        else:
            return jsonify({"error": "Ce véhicule n'a pas été trouvé"}), 500
    else:
        return jsonify({"error": "Numéro d'immatriculation manquant"}), 500
