# Project Name
Vehicle Tracking

# Introduction
Vehicule Tracking is an application serves as a comprehensive solution for
efficiently managing and monitoring the technical maintenance of vehicles.
In the dynamic world of transportation, ensuring the reliability and safety of
your vehicles is crucial. This project aims to streamline the tracking and
recording of various maintenance aspects, providing users with an organized and
proactive approach to fleet maintenance.

## Deployed site
Not deployed at all

## Blog of the project
[Read about the project on Medium](https://medium.com/@marcpourias/vehicle-tracking-225f16c23782)

## Author
Marc Pourias - [LinkedIn](https://www.linkedin.com/in/marc-pourias/)

# Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Starting MongoDb services for datastorage
```bash
sudo service mongod start
```

## Starting application
```bash
source venv/bin/activate
export FLASK_APP=api.app
export FLASK_ENV=development
flask run
```

## Stoping application
```bash
Ctrl+C
deactivate
```

# Usage
Register and login you
Update your informations
Create your vehicles with registration number
Create your trackings of vehicles
Update trackings
Delete trackings/vehicles/account

# Contribution

# Related projects
None for the moments

# Licensing
No licensing necessary
