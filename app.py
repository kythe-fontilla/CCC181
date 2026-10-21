from flask import Flask, render_template

app = Flask(__name__)

APP_NAME = "ShuttleStack"

SERVICES = [
    {"id": 1, "name": "Doubles: with a partner"},
    {"id": 2, "name": "Doubles: group of 4"},
    {"id": 3, "name": "Doubles: looking for a partner"},
]

# Each ticket: number, name, email, partner, service_id, status
# partner: the other players with you (empty if you are looking for a partner)
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Ana", "email": "ana@g.msuiit.edu.ph", "partner": "Ben", "service_id": 1, "status": "waiting"},
    {"number": 2, "name": "Carlo", "email": "carlo@g.msuiit.edu.ph", "partner": "", "service_id": 3, "status": "waiting"},
    {"number": 3, "name": "Dana", "email": "dana@g.msuiit.edu.ph", "partner": "Eli, Fe, Gio", "service_id": 2, "status": "waiting"},
]

@app.route("/")
def index():
    return f"<h1>{APP_NAME}</h1><p>Badminton court queue</p>"