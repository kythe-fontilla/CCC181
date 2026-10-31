import os

from itertools import combinations
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Service, Ticket, TicketMember, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # moves into an environment variable later
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [
        "Doubles: with a partner",
        "Doubles: group of 4",
        "Doubles: looking for a partner",
    ]
    for name in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name))
    db.session.commit()
    print("Services are ready.")

APP_NAME = "ShuttleStack"

SERVICES = [
    {"id": 1, "name": "Doubles: with a partner"},
    {"id": 2, "name": "Doubles: group of 4"},
    {"id": 3, "name": "Doubles: looking for a partner"},
]

COURTS = [1, 2, 3]

GAME_SIZE = 4

def count_names(text):
    """Number of non-empty comma-separated names in the partner field."""
    return len([n for n in text.split(",") if n.strip()])


def players_of(t):
    return t["players"]

# Each ticket: number, name, email, partner, service_id, status
# partner: the other players with you (empty if you are looking for a partner)
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Dana", "email": "dana@g.msuiit.edu.ph", "partner": "Eli, Fe, Gio", "service_id": 2, "status": "waiting", "court": None, "players": 4},
    {"number": 2, "name": "Ana", "email": "ana@g.msuiit.edu.ph", "partner": "Ben", "service_id": 1, "status": "waiting", "court": None, "players": 2},
    {"number": 3, "name": "Carlo", "email": "carlo@g.msuiit.edu.ph", "service_id": 3, "status": "waiting", "court": None, "players": 1},
]

def courts_in_use():
    """Return {court_number: [tickets]} for courts with a game in progress."""
    used = {}
    for t in TICKETS:
        if t["status"] == "called" and t["court"] is not None:
            used.setdefault(t["court"], []).append(t)
    return used


def court_players(game):
    return sum(players_of(t) for t in game)


def short_court():
    """Return (court_number, gap) for the first court with fewer than 4 players, else None."""
    for c, game in sorted(courts_in_use().items()):
        gap = GAME_SIZE - court_players(game)
        if gap > 0:
            return c, gap
    return None


def pick_next_game(needed=GAME_SIZE):
    """Find a set of waiting tickets that adds up to exactly `needed` players.
    Among all possible sets, choose the one with the earliest ticket numbers,
    so the longest-waiting teams play first and nobody is split.
    Returns the list of tickets, or None if no set adds up."""
    waiting = sorted((t for t in TICKETS if t["status"] == "waiting"),
                     key=lambda t: t["number"])
    best, best_key = None, None
    for size in range(1, needed + 1):
        for combo in combinations(waiting, size):
            if sum(players_of(t) for t in combo) == needed:
                key = [t["number"] for t in combo]
                if best_key is None or key < best_key:
                    best, best_key = combo, key
    return list(best) if best else None

def first_free_court():
    used = courts_in_use()
    for c in COURTS:
        if c not in used:
            return c
    return None

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

    if service_id == 1:
        if count_names(partner) != 1:
            errors["partner"] = ("This option is for 2 players. Enter exactly 1 name, "
                                 "or choose 'looking for a partner' if you are alone.")
    elif service_id == 2:
        if count_names(partner) != 3:
            errors["partner"] = "A group of 4 needs exactly 3 other names, separated by commas."
    elif service_id == 3:
        partner = ""

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form,
                               errors=errors), 400

    # Tidy the commas: "Eli,Fe ,Gio" is saved as "Eli, Fe, Gio"
    partner = ", ".join(n.strip() for n in partner.split(",") if n.strip())
    players = 1 + count_names(partner)

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({
        "number": number,
        "name": name,
        "email": email,
        "partner": partner,
        "service_id": service_id,
        "status": "waiting",
        "court": None,
        "players": players,
    })
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

@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = sum(1 for x in TICKETS
                if x["service_id"] == t["service_id"]
                and x["status"] == "waiting"
                and x["number"] < t["number"])
    return {"status": t["status"], "ahead": ahead, "court": t["court"]}

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
    t["court"] = None
    flash("You left the queue.", "info")
    return redirect(url_for("index"))

@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
    queue.sort(key=lambda t: t["number"])
    names = {s["id"]: s["name"] for s in SERVICES}
    return render_template(
        "staff.html",
        queue=queue,
        services=SERVICES,
        names=names,
        selected=service_id,
        courts=COURTS,
        in_use=courts_in_use(),
        all_courts_full=first_free_court() is None and short_court() is None,
        short=short_court(),
        court_counts={c: court_players(g) for c, g in courts_in_use().items()},
        waiting_players=sum(players_of(t) for t in TICKETS if t["status"] == "waiting"),
    )

@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None or action not in ("serve", "no-show"):
        abort(404)

    if action == "serve":
        if t["status"] != "called":
            flash(f"Ticket #{ticket_id} must be called before it can be served.", "warning")
            return redirect(url_for("staff_dashboard"))
        court = t["court"]
        game = [x for x in TICKETS if x["status"] == "called" and x["court"] == court]
        for x in game:
            x["status"] = "served"
            x["court"] = None
        numbers = ", ".join(f"#{x['number']}" for x in game)
        flash(f"Court {court} finished: {numbers} marked served.", "info")
    else:  # no-show
        if t["status"] not in ("waiting", "called"):
            flash(f"Ticket #{ticket_id} is already {t['status']}.", "warning")
            return redirect(url_for("staff_dashboard"))
        t["status"] = "no-show"
        t["court"] = None
        flash(f"Ticket #{ticket_id} marked no-show.", "info")

    return redirect(url_for("staff_dashboard"))

@app.post("/staff/call-next")
def call_next():
    short = short_court()
    if short:
        court, gap = short
        group = pick_next_game(gap)
        if group is None:
            flash(f"Court {court} needs {gap} more player(s), but no waiting ticket fits yet.", "warning")
            return redirect(url_for("staff_dashboard"))
        for t in group:
            t["status"] = "called"
            t["court"] = court
        numbers = ", ".join(f"#{t['number']}" for t in group)
        flash(f"Court {court} filled: called {numbers}.", "info")
        return redirect(url_for("staff_dashboard"))

    court = first_free_court()
    if court is None:
        flash("All 3 courts are in use. Serve a game first.", "warning")
        return redirect(url_for("staff_dashboard"))
    group = pick_next_game()
    if group is None:
        flash("Not enough players yet to fill a game of 4.", "warning")
        return redirect(url_for("staff_dashboard"))
    for t in group:
        t["status"] = "called"
        t["court"] = court
    numbers = ", ".join(f"#{t['number']}" for t in group)
    flash(f"Court {court}: called {numbers}.", "info")
    return redirect(url_for("staff_dashboard"))