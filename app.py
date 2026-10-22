from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable

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


@app.context_processor
def inject_app_name():
    # Makes {{ app_name }} available in every template
    return {"app_name": APP_NAME}


@app.route("/")
def index():
    return render_template("index.html")


# Placeholders so the navbar links work. Part 5 and Part 7 replace these.
@app.route("/join")
def join_form():
    return "Join form coming soon"


@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"