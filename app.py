import os

from itertools import combinations
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from datetime import timedelta, timezone
from datetime import datetime 
from models import Service, Ticket, TicketMember, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # moves into an environment variable later
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

PH_TIME = timezone(timedelta(hours=8))  # Philippine time has no daylight saving

@app.template_filter("waited")
def waited(value):
    """Minutes since a database time, e.g. '12 min'."""
    if not value:
        return ""
    minutes = int((datetime.now(timezone.utc) - value).total_seconds() // 60)
    return f"{minutes} min"

@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Oct 31, 04:53 PM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""

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

COURTS = [1, 2, 3]

GAME_SIZE = 4

def count_names(text):
    """Number of non-empty comma-separated names in the partner field."""
    return len([n for n in text.split(",") if n.strip()])


def players_of(t):
    return t.players

def courts_in_use():
    """Return {court_number: [tickets]} for courts with a game in progress."""
    stmt = (db.select(Ticket)
            .where(Ticket.status == "called", Ticket.court.is_not(None))
            .order_by(Ticket.id))
    used = {}
    for t in db.session.scalars(stmt):
        used.setdefault(t.court, []).append(t)
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
    """Find waiting tickets that add up to exactly `needed` players.
    Among the possible sets, choose the one with the earliest tickets,
    so nobody is split and passed-over tickets are tried first next time.
    Returns a list of tickets, or None if it cannot be filled yet."""
    waiting = db.session.scalars(
        db.select(Ticket).filter_by(status="waiting")
        .order_by(Ticket.created_at, Ticket.id).limit(12)).all()
    best = None
    for size in range(1, len(waiting) + 1):
        for combo in combinations(waiting, size):
            if sum(players_of(t) for t in combo) == needed:
                key = sorted(t.id for t in combo)
                if best is None or key < best[0]:
                    best = (key, list(combo))
    return best[1] if best else None

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

def all_services():
    return db.session.scalars(db.select(Service).order_by(Service.id)).all()

def people_ahead(t):
    """Count tickets still waiting for the same service that joined before t."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.service_id == t.service_id,
                   Ticket.status == "waiting",
                   Ticket.created_at < t.created_at))
    return db.session.scalar(stmt)

def games_played(user_id):
    """Count the person's served tickets. Computed, never stored."""
    stmt = (db.select(func.count())
            .select_from(Ticket)
            .where(Ticket.user_id == user_id, Ticket.status == "served"))
    return db.session.scalar(stmt)

def active_services():
    stmt = db.select(Service).filter_by(active=True).order_by(Service.id)
    return db.session.scalars(stmt).all()


@app.get("/join")
def join_form():
    return render_template("join.html", services=active_services(),
                           form={}, errors={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    partner = form.get("partner", "").strip()
    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name or len(name) > 80:
        errors["name"] = "Enter your name (up to 80 characters)."
    if "@" not in email or len(email) > 120:
        errors["email"] = "Enter a valid email address."
    if service is None or not service.active:
        errors["service_id"] = "Choose a service."

    members = []
    if service is not None and service.active:
        if service.id == 3:
            partner = ""
        else:
            members = [n.strip() for n in partner.split(",") if n.strip()]
            if service.id == 1 and len(members) != 1:
                errors["partner"] = ("This option is for 2 players. Enter exactly 1 name, "
                                     "or choose 'looking for a partner' if you are alone.")
            elif service.id == 2 and len(members) != 3:
                errors["partner"] = "A group of 4 needs exactly 3 other names, separated by commas."
            elif any(len(n) > 80 for n in members):
                errors["partner"] = "Each name can have up to 80 characters."

    user = None
    if "email" not in errors:
        user = db.session.scalar(db.select(User).filter_by(email=email))
        if user is not None:
            active = db.session.scalar(
                db.select(Ticket)
                .filter_by(user_id=user.id)
                .where(Ticket.status.in_(["waiting", "called"])))
            if active is not None:
                errors["email"] = (f"You already have ticket #{active.id}. "
                                   "Leave it first if you want to join again.")

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=active_services(),
                               form=form, errors=errors), 400

    if user is None:
        user = User(name=name, email=email)
    ticket = Ticket(user=user, service=service,
                    members=[TicketMember(name=n) for n in members])
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("You already have an active ticket, or something went wrong saving. "
              "Please check My place or try again.", "danger")
        return render_template("join.html", services=active_services(),
                               form=form, errors={}), 409

    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return render_template("ticket.html", ticket=t, service=t.service,
                           ahead=people_ahead(t))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    return {"status": t.status, "ahead": people_ahead(t), "court": t.court}

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if t.status in ("waiting", "called"):
        t.status = "left"  # soft delete: the row stays for reports
        t.court = None     # the court CHECK only allows a court while called
        db.session.commit()
    flash("You left the queue.", "info")
    return redirect(url_for("index"))

@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)  # hard delete: the row is gone for good
    db.session.commit()
    flash(f"Ticket #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard"))

@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    stmt = (db.select(Ticket)
            .where(Ticket.status.in_(["waiting", "called"]))
            .order_by(Ticket.created_at, Ticket.id))
    if service_id:
        stmt = stmt.where(Ticket.service_id == service_id)
    queue = db.session.scalars(stmt).all()

    used = courts_in_use()
    waiting = db.session.scalars(
        db.select(Ticket).filter_by(status="waiting")).all()
    return render_template(
        "staff.html",
        queue=queue,
        services=all_services(),
        selected=service_id,
        courts=COURTS,
        in_use=used,
        all_courts_full=first_free_court() is None and short_court() is None,
        short=short_court(),
        court_counts={c: court_players(g) for c, g in used.items()},
        waiting_players=sum(players_of(t) for t in waiting),
        games={t.user_id: games_played(t.user_id) for t in queue},
    )

STAFF_ACTIONS = ("serve", "no-show")


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    if action not in STAFF_ACTIONS:
        abort(404)
    t = db.get_or_404(Ticket, ticket_id)

    if action == "serve":
        if t.status != "called":
            flash(f"Ticket #{ticket_id} must be called before it can be served.", "warning")
            return redirect(url_for("staff_dashboard"))
        court = t.court
        game = db.session.scalars(
            db.select(Ticket).filter_by(status="called", court=court)).all()
        for x in game:
            x.status = "served"
            x.court = None
        db.session.commit()
        numbers = ", ".join(f"#{x.id}" for x in game)
        flash(f"Court {court} finished: {numbers} marked served.", "info")
    else:  # no-show
        if t.status not in ("waiting", "called"):
            flash(f"Ticket #{ticket_id} is already {t.status}.", "warning")
            return redirect(url_for("staff_dashboard"))
        t.status = "no-show"
        t.court = None
        db.session.commit()
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
        message = f"Court {court} filled: called"
    else:
        court = first_free_court()
        if court is None:
            flash("All 3 courts are in use. Serve a game first.", "warning")
            return redirect(url_for("staff_dashboard"))
        group = pick_next_game()
        if group is None:
            flash("Not enough players yet to fill a game of 4.", "warning")
            return redirect(url_for("staff_dashboard"))
        message = f"Court {court}: called"

    for t in group:
        t.status = "called"
        t.court = court
        t.called_at = func.now()  # the database fills in the time
    db.session.commit()
    numbers = ", ".join(f"#{t.id}" for t in group)
    flash(f"{message} {numbers}.", "info")
    return redirect(url_for("staff_dashboard"))

@app.get("/staff/services")
def services_list():
    return render_template("services.html", services=all_services())

@app.post("/staff/services")
def service_create():
    name = request.form.get("name", "").strip()
    if not name or len(name) > 60:
        flash("Enter a service name (up to 60 characters).", "danger")
        return redirect(url_for("services_list"))
    db.session.add(Service(name=name))
    try:
        db.session.commit()
        flash(f"Service “{name}” added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{name}” already exists.", "danger")
    return redirect(url_for("services_list"))

@app.post("/staff/services/<int:service_id>/edit")
def service_edit(service_id):
    s = db.get_or_404(Service, service_id)
    name = request.form.get("name", "").strip()
    if not name or len(name) > 60:
        flash("Enter a service name (up to 60 characters).", "danger")
        return redirect(url_for("services_list"))
    s.name = name
    s.active = request.form.get("active") == "on"  # unticked boxes are not sent
    try:
        db.session.commit()
        flash(f"Service “{name}” updated.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"A service named “{name}” already exists.", "danger")
    return redirect(url_for("services_list"))

@app.post("/staff/services/<int:service_id>/delete")
def service_delete(service_id):
    s = db.get_or_404(Service, service_id)
    if s.tickets:
        flash(f"“{s.name}” has tickets, so it cannot be deleted. Switch it off instead.", "danger")
        return redirect(url_for("services_list"))
    name = s.name
    db.session.delete(s)
    db.session.commit()
    flash(f"Service “{name}” deleted.", "warning")
    return redirect(url_for("services_list"))