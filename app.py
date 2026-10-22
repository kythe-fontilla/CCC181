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


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    partner = form.get("partner", "").strip()

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."
    elif service_id in (1, 2) and not partner:
        errors["partner"] = "Enter the name of the player or players you are playing with."
    elif service_id == 2 and len([p for p in partner.split(",") if p.strip()]) != 3:
        errors["partner"] = "For a group of 4, list the other 3 players, separated by commas."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    if service_id == 3:
        partner = ""
    TICKETS.append({"number": number, "name": name, "email": email, "partner": partner,
                    "service_id": service_id, "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
    flash("You left the queue.", "info")
    return redirect(url_for("index"))

@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"