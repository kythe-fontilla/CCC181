# ShuttleStack

**ShuttleStack** is a queue system for a public badminton venue in Wet Market, Iligan City, with 3 courts and a flat 50-peso entry fee. Players join the queue as a pair, a group of four, or alone, and see their ticket, status and how many teams are ahead. The caretaker sees the waiting list in order, calls a full game of 4 onto a free court, and marks games served or no-shows.

Requirements: see [docs/requirements.md](docs/requirements.md).

**Note:** the staff pages (`/staff` and `/staff/services`) have no login yet. Anyone who opens them can use them.

## How to run it

You need Python 3.11 or newer, Git and Docker.

1. Clone the repository and open a terminal in its folder.
2. Create and activate a virtual environment, then install the packages:

   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1        # Windows PowerShell
   source .venv/bin/activate         # macOS/Linux
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and replace `change-me` with your own password, in both lines:

   ```
   copy .env.example .env            # Windows
   cp .env.example .env              # macOS/Linux
   ```

4. Start PostgreSQL and wait until `docker compose ps` says **healthy**:

   ```
   docker compose up -d
   docker compose ps
   ```

5. Create the tables, add the starting services, and run the app:

   ```
   flask --app app db upgrade
   flask --app app seed
   flask --app app run --debug
   ```

6. Open http://127.0.0.1:5000.

Stop the database with `docker compose down`. Your data stays in the Docker volume. Do not use `docker compose down -v` unless you want to delete all the data.