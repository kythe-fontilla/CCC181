# Week 1 Proposal: ShuttleStack

## Setting
A public badminton venue in Wet Market, Iligan City with 3 courts and a 50-peso flat entry fee that
covers play for the whole day. There is no written queue; players wait for
a court by asking the teams currently playing.

## Users
- **Player waiting:** comes with a partner or team, or alone and looks for
  one. Warms up, scrolls their phone, or leaves to eat while waiting. Uses
  mobile data because there is no Wi-Fi.
- **Caretaker (collects the entry fee, decides who plays next):** tracks
  the waiting teams from memory and settles turn disputes.

## Services (types of queue entry)
1. Doubles: with a partner (a pair, open to playing against others)
2. Doubles: full group of 4 (2 vs 2 among themselves)
3. Doubles: looking for a partner / open to playing with others

## Functional requirements
| ID | Requirement | Priority |
| --- | --- | --- |
| FR-01 | A player can join the queue as a team or alone and get a ticket | Must |
| FR-02 | A player can see their ticket number, status and how many teams are ahead | Must |
| FR-03 | The caretaker can view the waiting list in order and call, serve or mark no-show | Must |
| FR-04 | A player can leave the queue | Should |
| FR-05 | The caretaker can assign a called ticket to a court (1 to 3) and see which courts are in use (star) | Should |
| FR-06 | The caretaker can see how many games each waiting team has played and how long they have waited (star) | Should |

## Observation notes (date, time, place: <fill in>)
- No list. Players ask the playing team "naay musunod sa inyoha?" (observation)
- 4 to 8 people wait at the same court; doubles fills up fast (observation)
- A 21-point game should take 20 to 30 minutes, but runs to 40 because
  nobody tracks the score (observation)
- Arguments: people claiming spots, games going past 21, skipped turns (observation)
- Waiting players warm up, scroll phones, leave the area, or watch (observation)
- Tracking is "just memory" (observation)

## Interview notes
**Player (interview)**
- "i want to have a tangible place where i could see the queue and the current status of the ones playing in court."
- "since naa koy pag ka-introvert, maulaw kog approach sa player to ask if naay musunod na sa ilaha mudula."
- "wi-fi is not available here i use mobile data"

**Caretaker (interview)**
- "if i see that they are waiting for a long time. but if daghan ang tao and wala ko kabalo who wants to play, ginapabay-an nalang nako kinsay musunod."
- "katong naay mas gamay na dula akong padulaon una"
- "just memory or estimate lang"
- "if i could keep tabs kinsang players ang naa sa court, pila na ilang nadula na games, how long na sila gahulat para mudula..."