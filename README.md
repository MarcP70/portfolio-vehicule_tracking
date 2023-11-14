# Vehicle Tracking
Vehicule Tracking is an application serves as a comprehensive solution for
efficiently managing and monitoring the technical maintenance of vehicles.
In the dynamic world of transportation, ensuring the reliability and safety of
your vehicles is crucial. This project aims to streamline the tracking and
recording of various maintenance aspects, providing users with an organized and
proactive approach to fleet maintenance.

## Installation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Starting MongoDb services for datastorage
sudo service mongod start

## Starting application
source venv/bin/activate
export FLASK_APP=api.app
export FLASK_ENV=development
flask run

## Stoping application
Ctrl+C
deactivate
