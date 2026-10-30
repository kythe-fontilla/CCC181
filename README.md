# ShuttleStack

**ShuttleStack** is a queue system for a public badminton venue at the Wet Market in Iligan City, with 3 courts and a flat 50-peso all-day entry fee. Players join the queue as a pair, a group of four, or alone, and see their ticket number, status and how many teams are ahead of them. The caretaker sees the waiting list in order, calls the next game onto a court, and marks teams as served or no-show.

> The staff dashboard has no login yet; anyone who opens `/staff` can use it. Login comes in later updates.

## How to run

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
python -m flask --app app run --debug
```

Then open http://127.0.0.1:5000.

Data is kept in memory, so it resets when the server restarts.