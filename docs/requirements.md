# ShuttleStack requirements

**Setting:** Public badminton venue in Wet Market, Iligan City, with 3 courts and a flat 50-peso all-day entry fee.
**People who wait:** Players, such as Jerald (see docs/week3/personas.md).
**People who serve:** The caretaker, Swishy (see docs/week3/personas.md).

**Problem statement:** A player who arrives when the courts are full needs a way to see who is next and when it is his turn without asking the playing teams, because there is no written list, turns are claimed verbally, and he is shy to approach other players. The caretaker needs a way to see the waiting teams in order and to fill each court with a complete game of 4, because she now tracks teams by memory, settles turn disputes by guessing, and a court can sit idle while players who could play together are still waiting.

## Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A player can join the queue as a pair, a group of four, or alone and get a ticket. | Must | **Yes** | Built (Week 3) |
| FR-02 | A player can see their ticket number, status and how many teams are ahead. | Must | **Yes** | Built (Week 3) |
| FR-03 | The caretaker can view the waiting list in order and call, serve or mark no-show. | Must | **Yes** | Built (Week 3) |
| FR-04 | A player can leave the queue. | Should | **Yes** | Built (Week 3) |
| FR-05 ★ | The caretaker sees which courts are in use and which ticket is on each. | Must | **Yes** | Built (Week 3) |
| FR-06 ★ | The caretaker can see how many games each waiting team has played and how long they have waited. | Should | **Yes** | Later |
| FR-07 ★ | The caretaker can call the next game: the system picks waiting tickets in join order that add up to exactly 4 players, never splitting a team, and assigns them to a free court. | Must | **Yes** | Built (Week 3) |
| FR-08 | The caretaker can filter the waiting list by service. | Should | No | Built (Week 3) |
| FR-09 | The caretaker can add, rename and switch off a service, and cannot delete a service that has tickets. | Must | **Yes** | This week |
| FR-10 | The caretaker can delete a ticket that was created by mistake. | Should | **Yes** | This week |
| FR-11 ★ | A player who joins can mark that they are open to a singles game, and the caretaker can choose to start a singles game (2 players) on a free court when few players are at the venue. | Could | **Yes** | This week (partly) |
| FR-12 | A player cannot join again while they already have a ticket that is waiting or called. | Must | **Yes** | This week |

## Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | No ticket is lost when the server or the database restarts. | Reliability | Must |
| NFR-02 | Two players can never get the same ticket number, even if they join at the same moment. | Data integrity | Must |
| NFR-03 | My place loads in under 2 seconds on mobile data. | Performance | Should |
| NFR-04 | Every screen scores 90 or higher in the Lighthouse accessibility check. | Accessibility | Must |
| NFR-05 | No password or secret key is stored in the repository. | Security | Must |
| NFR-06 | A court is never assigned a game of more than 4 players, and a team is never split across two courts. | Data integrity | Must |

## MVP

**MVP:** FR-01, FR-02, FR-03, FR-05, FR-07, FR-09, FR-12, NFR-01, NFR-02, NFR-04, NFR-05, NFR-06.

This is the smallest version that still solves the problem: a player can join and see their place without asking anyone, the caretaker can see the waiting list and which courts are in use, she can call a full game of 4 onto a free court, and tickets survive a restart. Leaving the queue, filtering, deleting mistaken tickets, wait-time reports and singles games are useful, but the queue still works without them.

## Out of scope

- **Player accounts and login:** players join with a name and email only. Staff login is planned for Week 11, so I will not build player accounts this semester.
- **Score tracking and game timers:** I observed that games run to 40 minutes because nobody tracks the score *(observation)*, but the queue works without it, and it would need a live scoring screen that I will not build this semester.
- **Payment of the 50-peso entry fee:** the caretaker collects it by hand today, and the queue does not depend on it.
- **Verifying who a player is:** FR-12 only stops the same email from holding two active tickets. Players join with a name and email that are not verified, so someone can still join again with a different email or name, or after being listed as another player's partner. The caretaker is the final check, because she sees who came with whom and can mark a no-show or delete a ticket. Accounts and login are planned for another week.

## Feedback from a real person

| Who (role only, no full name) | What they said | What I changed |
| --- | --- | --- |
| Player | Missing: "since the venue na ginaconsider diri is ang wet market, I think enough na man ang mga lists for a queueing app." Not important or wrong: "it's not wrong but i why is 'She can see how many games each waiting team has played and how long they have waited' to be built later? I think this is also important para ma ensure na fair ang dula/waiting." Top three: seeing your ticket number, status and teams ahead; joining as a pair, a group of 4, or alone; the caretaker seeing the whole waiting list in order and calling, finishing or marking no-show. | Raised FR-06 from Later to **This week** and kept it a Should, because he said it keeps play and waiting fair. Everything else stays as it is: he found nothing missing, and his top three (FR-02, FR-01, FR-03) are all already Must and in the MVP. |   

