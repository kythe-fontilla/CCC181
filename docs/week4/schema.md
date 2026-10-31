# ShuttleStack schema

## 2a. Nouns in the requirements

| Req ID | Requirement | Nouns | Table or column? |
| --- | --- | --- | --- |
| FR-01 | A **player** can join the **queue** as a **pair**, a **group of four**, or alone and get a **ticket**. | player, queue, ticket, pair, group of four | users, *(not a table)*, tickets, services (the three entry types), tickets.players |
| FR-02 | A player can see their **ticket number**, **status** and how many teams are **ahead**. | ticket number, status, ahead | tickets.id, tickets.status, *(computed)* |
| FR-03 | The **caretaker** can view the **waiting list** in order and **call**, **serve** or mark **no-show**. | caretaker, waiting list, call, serve, no-show | users (role staff), *(not a table: query of tickets with status waiting, ordered by created_at)*, tickets.status values called, served, no-show |
| FR-04 | A player can **leave** the queue. | leave | tickets.status value left *(soft delete, no new table)* |
| FR-05 | The caretaker sees which **courts** are in use and which **ticket** is on each. | court, ticket | tickets.court (integer 1 to 3, empty when not on a court); *not a table, because a court has no data of its own* |
| FR-06 | The caretaker can see how many **games** each waiting **team** has **played** and how long they have **waited**. | games played, team, wait time | *(computed)*: count of the person's tickets with status served, and now() minus tickets.created_at; nothing stored |
| FR-07 | The caretaker can call the next **game**: the system picks waiting tickets in join order that add up to exactly 4 **players**, never splitting a team, and assigns them to a free court. | game, players, join order, free court | tickets.players (integer 1, 2 or 4), tickets.created_at, tickets.court; *a game is not a table, it is the set of called tickets sharing one court* |
| FR-09 | The caretaker can add, rename and switch off a **service**, and cannot delete a service that has tickets. | service, name, active | services, services.name, services.active |
| FR-10 | The caretaker can delete a **ticket** that was created by **mistake**. | ticket, mistake | *(hard delete of a tickets row, no new column)* |
| FR-11 | A player who joins can mark that they are **open to a singles game**, and the caretaker can choose to start a singles game (2 players) on a free court when few players are at the venue. | open to singles, singles game | tickets.open_to_singles (boolean, default false) |

**Two rules applied:**

- **The queue is not a table.** It is all tickets with status `waiting`, ordered by `created_at`.
- **Store facts, not results.** Position in line, games played and wait time are computed when needed, never stored.

**Open question for 2b:** `partner` currently holds names such as "Eli, Fe, Gio" in one cell. That is a list in one cell, which the 1NF check in 2e will flag. We'll decide there whether to keep it as text or split it out.