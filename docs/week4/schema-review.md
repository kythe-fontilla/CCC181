# Schema self-review

## Entry 1: Bad data (question 4)

**Works well:** `tickets.status` has a CHECK limited to five values, and the foreign keys use RESTRICT, so a ticket can never point to a missing person or service, and a mistyped status like "lost" is rejected by the database.

**Problem:** `court` and `status` can disagree. Nothing stops a ticket from being `waiting` with `court = 2`, or `served` with a court still set. The court strip on the dashboard (FR-05) reads `court`, so a wrong value would show a court as busy when it is not.

**Change:** add `CHECK (court IS NULL OR (court BETWEEN 1 AND 3 AND status = 'called'))` to `tickets`. The ERD does not change, because it does not show CHECK rules. I updated the `court` row in the 2c table in `schema.md`, and `models.py` will carry the constraint. The "never more than 4 players on one court" rule (NFR-06) stays in Flask, because the database cannot add up members across rows with a simple CHECK.

## Entry 2: Coverage (question 1)

**Works well:** every requirement marked *Stores data = Yes* maps to a table or column. FR-12 needs no new column, because it queries `users.email` and `tickets.status`.

**Problem:** `users.role` is not read by any code this week. The staff pages are open to everyone, so nothing checks the role, and a column no requirement needs breaks the rule that every column is there for a reason.

**Change:** keep it. FR-03 and FR-09 name the caretaker as a different kind of user from a player, and `role` is the field that records that difference. It has a CHECK limited to `visitor` and `staff`, so it cannot hold a wrong value.

## Entry 3: Facts, not results (question 3)

**Works well:** position in line, wait time and number of players are computed, not stored. Moving `players` and `partner` into `ticket_members` removed a stored copy that could drift out of sync.

**Problem:** FR-06 (games played) is computed by counting a person's `served` tickets, but only the ticket owner is a `users` row. Listed members are plain names, so their games are not counted.

**Change:** keep the schema. "Games played" means the games the ticket owner has served, which stands for the team. I will state this limit in the report. Linking members to users would need verified accounts, which are out of scope. 