# Week 4 persistence: ShuttleStack

This checks NFR-01: no ticket is lost when the server or the database restarts.

## 11a. Restart test

### Before the restart

The database held 13 tickets across three services (1, 2 and 3), with the statuses `served`, `left` and `waiting`.

Query used (in PowerShell):

```
docker compose exec db psql -U shuttlestack -P pager=off -c "SELECT id, status, service_id, created_at FROM tickets ORDER BY id;"
```

Staff dashboard before the restart (it lists the waiting and called tickets):

![Dashboard before restart](screenshots/before-dashboard.png)

Query result before the restart:

![SQL before restart](screenshots/before-sql.png)

### Steps

1. Stopped Flask with Ctrl+C.
2. Ran `docker compose down`. This removes the container but keeps the `pgdata` volume.
3. Ran `docker compose ps` and saw that nothing was running.
4. Ran `docker compose up -d` and waited until `docker compose ps` showed the database as healthy.
5. Started Flask again with `flask --app app run --debug`.

I did not join, call, serve, leave or delete anything between the two sets of screenshots.

### After the restart

Staff dashboard after the restart:

![Dashboard after restart](screenshots/after-dashboard.png)

Query result after the restart:

![SQL after restart](screenshots/after-sql.png)

### Result

All 13 tickets, their statuses, their services and their `created_at` times are identical before and after the restart. The data lives in the `pgdata` volume, not in the container or in Flask, so it survives. NFR-01 **passed**.

## 11b. Rebuild from scratch

This test deletes all the data, so I ran it only after 11a. It checks that my migrations can rebuild the whole database on a computer that has never seen it.
 
### Steps
 
1. Stopped Flask with Ctrl+C.
2. Ran `docker compose down -v`. This deleted the container and the `pgdata` volume, so all tickets were gone.
3. Ran `docker compose up -d` and waited until `docker compose ps` showed the database as healthy.
4. Ran `flask --app app db upgrade`. All three migrations ran and created the tables from nothing. I did not use `db.create_all()`.
5. Ran `flask --app app seed`, which added the three starting services.
6. Started Flask with `flask --app app run --debug`.
### Checks
 
The join form lists the three services from the database:
 
![Join form after rebuild](screenshots/rebuild-join.png)
 
I joined with an email and landed on My place, and the new ticket shows on the staff dashboard:
 
![Dashboard after rebuild](screenshots/rebuild-dashboard.png)
 
### Result
 
The app opened, showed the three services, and let me join. The database can be rebuilt from the migrations and `seed` alone, so no table or column is missing from them.