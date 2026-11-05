# Week 4 validation: ShuttleStack

The same rules are checked in three layers. The browser is for users (fast feedback), Flask is for security (the real gatekeeper), and PostgreSQL is for integrity (the last line of defense).

## 10a. Browser layer

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Name is required and at most 80 characters (`users.name` is `varchar(80)`) | Browser | Pasted 100 characters into the name field on `/join` | Typing stopped at 80 characters. `required` and `maxlength="80"` are set on the input. |
| Email is required, is an email, and is at most 120 characters (`users.email` is `varchar(120)`) | Browser | Checked the input attributes on `/join` | `required`, `type="email"` and `maxlength="120"` are set. |
| Partner names have a loose upper limit | Browser | Checked the input attributes on `/join` | `maxlength="250"`. This is not one column: each name becomes a `ticket_members.name` row of `varchar(80)`, which Flask checks one name at a time. |

The browser rules only help honest users. `novalidate` is on the form so that the server's own error messages show, and anyone can skip every attribute above. Section 10b proves it.

## 10b. Flask layer (skipping the form with curl)

Command shape, using `curl.exe` in PowerShell:

```
curl.exe -i -X POST http://127.0.0.1:5000/join -d "name=..." -d "email=..." -d "service_id=..."
```

I counted the rows in `tickets` before the tests (`SELECT count(*) FROM tickets;`) and again after.

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| Name, email and service are all checked | Flask | `name=` (empty), `email=not-an-email`, `service_id=999` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| Name is at most 80 characters | Flask | Name of 200 `a` characters, `service_id=3` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| A group of 4 needs exactly 3 other names | Flask | `service_id=2` with `partner=OnlyOne` | `HTTP/1.1 400 BAD REQUEST`, nothing saved |
| A switched-off service cannot be joined | Flask | Switched off "Doubles: looking for a partner" in Manage services, then posted `service_id=3` | `HTTP/1.1 400 BAD REQUEST`, nothing saved. The service was switched back on afterwards. |

The ticket count was the same after the tests as before them.

**A mistake I made while testing.** My first run of the switched-off-service test returned `302 FOUND` and created ticket #9. The cause was my test, not the code: I had unticked **Active** but had not clicked **Save**, so the service was still active. I deleted ticket #9 with the dashboard's Delete button (which also tested the hard delete) and repeated the test correctly.

## 10c. Database layer (skipping Flask with psql)

Every bad statement was typed directly into `docker compose exec db psql -U shuttlestack`.

| Rule | Layer | How I tested it | What happened |
| --- | --- | --- | --- |
| FOREIGN KEY: a ticket needs an existing service | Database | `INSERT INTO tickets (user_id, service_id, status) VALUES (17, 999, 'served');` | `ERROR: insert or update on table "tickets" violates foreign key constraint "tickets_service_id_fkey"` / `DETAIL: Key (service_id)=(999) is not present in table "services".` |
| CHECK: only the five allowed statuses | Database | `UPDATE tickets SET status = 'lost' WHERE id = 1;` | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_status"` |
| CHECK: a court only while the ticket is called | Database | `UPDATE tickets SET court = 2 ...` on a `served` ticket | `ERROR: new row for relation "tickets" violates check constraint "ck_tickets_court"` |
| UNIQUE: one account per email | Database | `INSERT INTO users (name, email) VALUES ('Copy', '<an email already in users>');` | `ERROR: duplicate key value violates unique constraint "users_email_key"` / `DETAIL: Key (email)=(...) already exists.` |
| NOT NULL: a user needs a name | Database | `INSERT INTO users (email) VALUES ('nonull@test.com');` | `ERROR: null value in column "name" of relation "users" violates not-null constraint` |
| RESTRICT: a service with tickets cannot be deleted | Database | `DELETE FROM services WHERE id = 1;` | `ERROR: update or delete on table "services" violates foreign key constraint "tickets_service_id_fkey" on table "tickets"` / `DETAIL: Key (id)=(1) is still referenced from table "tickets".` |
| Partial unique index: at most one active ticket per user (FR-12) | Database | `INSERT INTO tickets (user_id, service_id, status) VALUES (1, 1, 'waiting');` for a user who already has an active ticket | `ERROR: duplicate key value violates unique constraint "uq_tickets_one_active_per_user"` / `DETAIL: Key (user_id)=(1) already exists.` |
| Defaults: the database fills in status and time | Database | `INSERT INTO tickets (user_id, service_id) VALUES (<user with no active ticket>, 1) RETURNING id, status, created_at;` | The row was accepted with `status = waiting` and `created_at` set by PostgreSQL (ticket 15). I deleted the test row afterwards. |

**Mistakes I made while testing.**

- My first foreign key test failed on the partial unique index instead, because user 1 already had an active ticket and PostgreSQL checked that index first. I repeated it with a user who has no active ticket and with `status = 'served'`, which the partial index does not cover.
- My first UNIQUE test accidentally succeeded, because I left the placeholder text `REAL_EMAIL_HERE` as the email. That inserted a junk user, which I deleted. I then repeated the test with a real email, and it failed as expected.

## 10d. No SQL in f-strings

```
git grep -nE "f[\"'].*(SELECT|INSERT|UPDATE|DELETE)" -- "*.py"
```

Result: the command printed nothing, so no SQL is built from strings. All queries use SQLAlchemy (`db.select(...)`, `db.session.get(...)`), which sends values separately from the SQL.

## Most useful PostgreSQL error

`duplicate key value violates unique constraint "uq_tickets_one_active_per_user"`. It showed up on its own while I was testing something else, which proved that the FR-12 rule (one active ticket per player) is enforced by the database and not only by `join()` in Flask. Even if a bug skipped the Flask check, PostgreSQL would still refuse the second active ticket.