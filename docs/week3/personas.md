# clInIcT Personas

## Ding Dong, the person waiting

> "Wa ko kabalo aha ko na mulinya. Ga tindog ra ko sa gilid" 

| | |
| --- | --- |
| **Photo or sketch** | 🧑‍💻 *(icon, not a real person)* |
| **Age, role and background** | 20, 3rd-year Computer Science student at MSU-IIT who often has back-to-back classes *(interview)* |
| **Goals** | 1. Get a drug test for his OJT medical clearance. 2. Fill up the clinic form without losing his turn. 3. Get back to class on time. |
| **Frustrations** | 1. The clinic is cramped and there is no visible waiting line *(observation)*. 2. He does not know which line he is supposed to follow *(interview)*. 3. He cannot leave the room, because he might miss his turn. |
| **Devices and context** | Uses his own cellphone on campus, sometimes while still in class or walking between buildings *(interview)* |
| **Tech comfort** | High. He is a Computer Science student and installs and tries new apps easily. |
| **Accessibility needs** | Old phone with a small, low-resolution screen and slow mobile data *(interview)*. Needs light pages with no large images. |

### Scenario

Ding Dong has a free hour between his Data Structures and Networks classes, and he needs a drug test for his OJT clearance. He walks to the campus clinic and finds the waiting area packed, with no sign of who is first. Instead of squeezing inside, he opens clInIcT on his old phone, picks "OJT & Athletic Medical Clearances", types his name, email and ID number, and taps "Get a ticket". His ticket number appears in large text with "3 people ahead of you". He sits in the corridor and fills up the clinic form on his lap. Ten minutes later his phone shows "Called", so he walks in and is served without having asked anyone how long the wait is.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Join the queue for a clearance or other clinic service | Join | FR-01 |
| Check my ticket number and how many people are ahead | My place | FR-02 |
| See right away when I am called | My place | FR-02 |
| Leave the queue if I have to go back to class | My place | FR-02 |

### What this means for my interface

1. Because Ding Dong checks his phone between classes and cannot tell where he stands in the crowded clinic, his ticket number and "people ahead" must be the biggest thing on My place.
2. Because his old phone uses slow mobile data, the pages must load fast and work without large images.
3. Because he may be called while still in class or in the corridor, the status must update by itself without him refreshing.
4. Because he does not know which line he is in, the Join form must ask him to choose a service and show his service name on My place.

---

## Maria Antonnete, the staff member

> "Naay estudyante sa akong atubangan and naa pud 5 sa uibang area. I can't accomodate them all."

| | |
| --- | --- |
| **Photo or sketch** | 👩‍⚕️ *(icon, not a real person)* |
| **Age, role and background** | 32, clinic nurse who also handles the front desk during busy hours *(interview)* |
| **Goals** | 1. Call patients in the correct order for each service. 2. Keep track of who is waiting, called, served or a no-show. 3. Keep the clinic less crowded and calm. |
| **Frustrations** | 1. Patients keep asking how many people are ahead of them. 2. The crowd blocks the counter because there is no clear line *(observation)*. 3. She cannot tell quickly which service each person is waiting for. |
| **Devices and context** | Shared clinic desktop or laptop at the counter, while attending to a patient and answering questions at the same time |
| **Tech comfort** | Medium. She is comfortable with basic computer and clinic record systems, but she is a nurse, not an IT person, so she needs clear buttons and no technical steps. |
| **Accessibility needs** | One hand is often busy with a patient or paperwork. She is interrupted often, so she needs big, clearly labeled buttons that are hard to press by mistake, and text readable from a short distance on a shared screen. |

### Scenario

It is 10:30 in the morning and the clinic is at its busiest, with a nurse at the counter and patients waiting for consultations, medical certificates and clearances. Maria Antonnete finishes with a patient, and with one hand still holding a form she opens the clInIcT staff dashboard on the shared computer. The list shows who is waiting, in order, with each person's service. She taps "Call next", the first patient's phone changes to "Called", and she greets them at the counter. When she is done she taps "Serve". If someone does not show up after being called, she marks "No-show" and moves on to the next person without a single shouted name.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| See the waiting list in order | Staff dashboard | FR-03 |
| Filter the list by service | Staff dashboard | FR-03 |
| Call the next patient | Staff dashboard | FR-03 |
| Mark a patient as served | Staff dashboard | FR-03 |
| Mark a patient as a no-show | Staff dashboard | FR-03 |

### What this means for my interface

1. Because Maria often has one hand busy with a patient, "Call next" must be the largest and easiest button to reach, at the top of the dashboard.
2. Because she cannot tell at a glance which service each person needs, the table must show the service name in every row and offer a service filter.
3. Because she is interrupted constantly and could press the wrong button, Serve and No-show must look different and be labeled with the ticket number.
4. Because she shares the computer and has a medium tech comfort, the dashboard must need no setup and use plain words like "Call next" and "No-show".