# Week 3 Usability Test: ShuttleStack

## 10a. Test with a real user

**Tester:** Tester A, a casual badminton player who matches the persona **Jerald** (the player). No full name is recorded here.
**Device:** laptop (Chrome), running the app locally.
**Method:** I gave three tasks one at a time, did not help, and asked him to think aloud.
**Date:** October 25, 2026

*Screen and voice were recorded with the tester's permission. The recording is not included in this repository.*

### Tasks

1. "You just arrived. Get in line to play."
2. "How many teams are ahead of you? What is your ticket number?"
3. "Pretend you are the caretaker. Call the next team and mark it as served."

### Results

| Task | Finished? | Time | Notes |
|---|---|---|---|
| 1. Join the queue | Yes | About 20 seconds | Filled in the join form without help. *(observation)* |
| 2. Find the ticket number and teams ahead | Yes | Split second | Found both right away on My place. *(observation)* |
| 3. Call a team and mark it served (staff role) | Yes | Under 20 seconds once on the dashboard | He took a while to find the dashboard. I had not prepared a separate tab for staff, so he had to find the "Staff" link in the top navigation. That was a gap in my test setup. *(observation)* |

All three tasks took about 2 minutes in total.

### Where he hesitated and what surprised me

- **Finding the staff dashboard.** He had a hard time locating it because I had not opened it in its own tab for him. It was only in the navigation at the top. *(observation)*
- **The Call next game button.** This was not part of the task. The dashboard said "Players waiting: 5" next to the button, so he tried to press it to start a game on another court. The button refused, even though two waiting tickets (#2 and #4) could have filled a free court together. *(observation)*
- **Singles.** He said that in his experience there are times when a court is not filled, and players could play singles. He suggested that the caretaker could assign a singles match if the players want it. *(interview)*

### Persona rules: what held up and what did not

| Rule (from personas.md) | Result | Evidence from the test |
|---|---|---|
| Jerald: status in words, shown big, and updates by itself | Partly tested | He found his ticket number and position in a split second. Auto-updating was not observed during the test. |
| Jerald: pages must be light, with no large images, because of mobile data | Not tested | Tested on a laptop, so mobile data and page weight were not checked. |
| Jerald: joining and checking his place must work without talking to anyone | Held up | He joined and checked his place on his own, with no help. |
| Jerald: one form must work for all three services ("Who are you playing with?") | Held up | He completed the join form in about 20 seconds with no help. |
| Swishy: call, serve and no-show must each take one large tap | Held up | As the staff role, he called a team and marked it served in under 20 seconds. |
| Swishy: waiting list in order, ticket numbers visible, and courts in use shown | Not tested directly | The tester matches Jerald and only role-played staff for Task 3. |

**Where the design did not hold up:** none of my rules covered a free court sitting idle while players who could play together were waiting. This is the problem I fixed in 10b.

**Setup note:** the delay finding the staff dashboard came from my test setup. In the next test I will have the staff page ready in its own tab.

## 10b. One improvement

### Problem

A free court stayed idle while players who could fill it were waiting. The queue always built a game starting from the longest-waiting ticket. If that ticket could not be part of a full game of 4, nothing was called, even though other waiting tickets could make 4 players together. In my test data, Court 1 was full, Courts 2 and 3 were free, and tickets #2 (a pair) and #4 (a pair) were waiting but could not be called, because ticket #3 (a solo) sat between them and the game could not be completed around it. The dashboard said "Players waiting: 5", which made the Call next game button look usable when it was not. *(observation from the test)*

### Fix

I changed `pick_next_game()` in `app.py`. It now checks the combinations of waiting tickets and picks the set that adds up to exactly 4 players and contains the earliest ticket numbers. Tickets that are passed over keep their numbers and are tried first again next time, so nobody loses their place. Backfilling a short court uses the same function.

**Trade-off:** this loosens strict join order. A complete game can now be called ahead of an earlier ticket that is still waiting for more players. I accepted this because a free court with four ready players waiting was a worse result than the small unfairness to the passed-over ticket.

### Before and after

**Before:** Court 1 is full, Courts 2 and 3 are free, and tickets #2 and #4 cannot be called.

![Before: court idle](screenshots/before-court-idle.png)

**After:** Call next game puts tickets #2 and #4 together on Court 2.

![After: ready game called](screenshots/after-court-idle.png)

## Not built this week

The tester suggested that if few players are waiting, players who joined without a partner or team could play singles, and the staff could assign a singles match if the players want it. I did not build this. It is covered in the Reflection of my report.