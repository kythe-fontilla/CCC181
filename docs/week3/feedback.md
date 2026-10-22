# Week 3 self-review: ShuttleStack wireframes

Reviewed against the personas in `personas.md` (Jerald, the player, and Swishy, the caretaker), looking at both the phone and the laptop frame of each screen.

## Screen 1: Join (Jerald, FR-01)

**Works well:** The form is short (name, email, service, who he is playing with, one button) and the button is the last, full-width element. This follows Jerald's rule 3: he is shy to approach other players, so joining must work without talking to anyone. The same form also works for all three services, which follows rule 4. On both phone and laptop, he can tell within 5 seconds what to do, because the heading says "Join the queue" and the button says "Get a ticket".

**Problem:** The "Who are you playing with?" field depends on one small hint ("Leave empty if no partner"). A first-time player does not know what to type for "Doubles: full group of four" (three names? separated how?) or for "Doubles: with a partner". This breaks *recognition rather than recall* and invites bad input (*error prevention*), because the player has to guess the format.

**Change:** Make the hint depend on the service: "Type your partner's name. For a group of four, list the other three. Leave empty if you are looking for a partner." I am keeping the wireframe as drawn, because it already shows the field and a hint line. I will write the improved hint text into `join.html` in Part 5, and validate on the server that a group of four has three names.

## Screen 2: My place (Jerald, FR-02, FR-04)

**Works well:** The ticket number (#7) is the biggest element, and the status ("Waiting") is large and written in words, not only color. The position sentence ("3 teams ahead of you") and the "You're next!" note sit right below. This follows Jerald's rule 1: he warms up or leaves the court to eat, so he must be able to read his status at a glance on a phone. The note "Updates by itself every 10 seconds" shows he does not need to refresh. "Leave the queue" is quiet in style, placed at the bottom away from the main information, and its note says it asks "Are you sure you want to leave?" before acting, so an accidental tap cannot cost him his turn. The phone version shows the most important thing first.

**Problem:** The page says it updates every 10 seconds, but it does not show *when* it last updated or what happens if the update fails. Jerald uses mobile data (rule 2), which can be slow or drop. If a refresh fails, he could keep seeing "Waiting" while he has really been called, and walk back late or miss his turn. This is a *visibility of system status* problem.

**Change:** Add a small line under the status, "Last updated 12:04:30", and show "Can't refresh, check your connection" when a refresh fails. I am keeping the rest of the wireframe as drawn, because the layout already puts the number and status first. I will build the line and the failure message into the JavaScript in Part 8, where the page fetches the status every 10 seconds.

## Screen 3: Staff dashboard (Swishy, FR-03, FR-05)

**Works well:** "Call Next" is a large button at the top, so Swishy's most frequent action is the easiest to reach (rule 5, hands busy with money). The waiting list is in ticket order, so a dispute between two teams can be settled by looking at which ticket came first (rule 2). Each card shows who came with whom (rule 4), the status is in words, and the court strip shows which of the 3 courts are in use and by which ticket (rule 3). On the phone, the cards are stacked one per row, so the buttons stay large enough to tap.

**Problem:** The frames show that a ticket is on a court ("Called (Court 3)"), but they have no control to pick which court a called ticket goes to. FR-05 is only half shown, and Swishy would have to remember or guess which court is free, which is the *recognition rather than recall* problem she has today. Also, the Serve button appears on a Waiting card, even though only a called ticket can be served.

**Change:** When Swishy taps Call, show a court choice (1 to 3) that lists only the free courts. Disable Serve on cards that are not Called. I am keeping the wireframes as drawn for now, because the court strip and the "Called (Court 3)" status already show the result of FR-05. I will build the court choice and the disabled Serve button in Part 7. The laptop frame uses cards like the phone frame. In Part 7 I will build it as a table, using `table-responsive`, as the assignment asks.

## Summary of design rules

| Persona rule | Followed by | Broken or incomplete |
|---|---|---|
| Jerald 1: status in words, big, updates itself | My place | Does not show when it last updated or if it failed |
| Jerald 3: join without talking to anyone | Join | None |
| Jerald 4: one form for all three services | Join | Hint is unclear for group of four |
| Swishy 3: see which courts are in use | Staff dashboard | No way to choose the court (FR-05) |
| Swishy 5: one large tap per action | Staff dashboard | Serve shown on cards that cannot be served |