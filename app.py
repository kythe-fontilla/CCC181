from flask import Flask, abort, render_template

app = Flask(__name__)

APP_NAME = "clInIcT"


@app.context_processor
def inject_app_name():
    # Makes {{ app_name }} available in every template
    return {"app_name": APP_NAME}


SERVICES = [
    {"id": 1, "name": "Medical Consultation"},
    {"id": 2, "name": "Medical Certificates & Excuse Slips"},
    {"id": 3, "name": "First Aid & Wound Dressing"},
    {"id": 4, "name": "Dental Check-Up & Cleaning"},
    {"id": 5, "name": "OJT & Athletic Medical Clearances"},
]

# Each ticket: number, name, email, id_number, service_id, status
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Ana", "email": "ana@g.msuiit.edu.ph", "id_number": "2023-0001", "service_id": 1, "status": "waiting"},
    {"number": 2, "name": "Ben", "email": "ben@g.msuiit.edu.ph", "id_number": "2022-0456", "service_id": 2, "status": "waiting"},
    {"number": 3, "name": "Carla", "email": "carla@g.msuiit.edu.ph", "id_number": "2024-0789", "service_id": 1, "status": "waiting"},
]


@app.route("/")
def index():
    return render_template("index.html", tickets=TICKETS)


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    return render_template("ticket.html", ticket=t)


@app.route("/hello")
def hello():
    return "Hello, CCC181!"