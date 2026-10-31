## Jerald, the player

> "i want to have a tangible place where i could see the queue and the current status of the ones playing in court." *(interview)*

| | |
| --- | --- |
| **Photo or sketch** | 🏸 Icon: shuttlecock emoji |
| **Age, role and background** | 24, a working adult who goes to the court after work |
| **Goals** | Get a turn without having to ask the playing teams "naay musunod sa inyoha?" *(interview)*. See the queue and the current status of those playing *(interview)*. Find a partner if he arrives alone *(interview)*. |
| **Frustrations** | There is no clear list of who is next, so he talks to the current players and, if all 3 courts are full, asks the other courts *(interview)*. He can't see the score, so he doesn't know when a game will finish *(interview)*. He is shy to approach players ("maulaw kog approach") *(interview)*. |
| **Devices and context** | Mobile phone, on mobile data because there is no Wi-Fi at the court *(interview)*. Does warm-ups while waiting and sometimes leaves the court to eat *(interview)*. |
| **Tech comfort** | Medium. He uses his phone and mobile data every day, but he has only ever queued by asking people, never with an app. |
| **Accessibility needs** | Slow or limited mobile data, so pages must be light *(interview)*. Often away from the court area (warming up, eating), so the status must be readable at a glance on a phone. |

### Scenario

Jerald arrives at the court after work and finds all 3 courts full. He and his playing partner don't want to walk up to the players and ask who is next, because Jerald is shy about approaching people. He opens ShuttleStack on his phone, joins "Doubles: with a partner", types his partner's name under "Who are you playing with?", and gets ticket #7. His place says 3 teams are ahead, so he warms up and then goes to eat. While he eats, the status changes to "Called" in large letters, so he walks back to the court knowing it is really his turn. After the game he doesn't need to argue about whose turn it was, and he can leave the queue or join again.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Join the queue as a pair, a group of four, or alone | Join | FR-01 |
| Check ticket number, status and how many teams are ahead | My place | FR-02 |
| Leave the queue | My place | FR-04 |

### What this means for my interface

1. Because he warms up or leaves the court to eat, the status must be written in words, shown big, and update by itself without refreshing.
2. Because there is no Wi-Fi and he uses mobile data, pages must be light, with no large images.
3. Because he is shy to approach other players, joining and checking his place must work without talking to anyone.
4. Because he comes as a team or alone, the join form must ask "Who are you playing with?" so one form works for all three services.

## Swishy, the caretaker

> "just memory or estimate lang" *(interview)*

| | |
| --- | --- |
| **Photo or sketch** | 🪙 Icon: coin emoji|
| **Age, role and background** | 20, collects the 50 pesos at the venue and decides who plays next *(interview)* |
| **Goals** | Make sure the team that has waited longest or played fewer games goes next *(interview)*. Know who is on the court and how many games each team has played *(interview)*. Know whether a team came together or is also open to playing with others *(interview)*. |
| **Frustrations** | She keeps track of who is waiting by "just memory or estimate lang" *(interview)*. When many people are waiting and she doesn't know who wants to play, she leaves it to chance: "ginapabay-an nalang nako kinsay musunod" *(interview)*. Some players can't play or wait too long because it isn't clear who is next *(interview)*. When two teams both say it's their turn, she has to ask how many games each has played *(interview)*. |
| **Devices and context** | Mobile phone, and sometimes a computer. She uses the dashboard at the counter while collecting the 50 pesos and answering players who come up to her, so she can only look at it in short moments. |
| **Tech comfort** | Medium. She is used to a phone and sometimes a computer, but she has no tool for the queue today, so the dashboard must not need explaining. |
| **Accessibility needs** | Hands often busy with money, and she is standing or moving around the counter, so buttons must be large and easy to tap. The venue has no Wi-Fi *(interview)*, so the page must load on mobile data. Outdoor light can make the screen hard to read, so status and numbers need strong contrast. |

### Scenario

It is a busy evening and all 3 courts are in use. Swishy is collecting the 50 pesos from a new arrival when two teams both tell her it is their turn. Before, she would have tried to remember who came first and guessed. Now she opens the ShuttleStack dashboard on her phone. The waiting list is in order, and each row shows the ticket number and who came with whom. She sees that one team's ticket is earlier, so she taps "Call" on it, assigns it to the court that has just freed up, and tells the other team they are next. She goes back to collecting money without having to remember anyone.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| See the waiting list in order and call, serve or mark a no-show | Staff dashboard | FR-03 |
| Assign a called ticket to a court (1 to 3) and see which courts are in use and which ticket is on each | Staff dashboard | FR-05 |

### What this means for my interface

1. Because she now tracks the queue by memory, the dashboard must show the whole waiting list in order, so she doesn't have to remember anyone.
2. Because she picks the team that has waited longest, the waiting list must be in join order with the ticket number clearly visible, so a dispute between two teams can be settled by looking at which ticket came first.
3. Because she wants to know who is on the court, the dashboard must show which of the 3 courts are in use and by which ticket.
4. Because some teams are open to playing with others and some want to stay as a team, each row must show who came with whom, using the "Who are you playing with?" field.
5. Because her hands are often busy with money, call, serve and no-show must each take one large tap.