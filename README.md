# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
=== Today's Schedule ===
Schedule for Luna on 2026-06-25 (Owner: Alex Rivera):
  08:00 — Morning Walk [Exercise] — 30 min [priority: high]
  08:30 — Feeding [Nutrition] — 10 min [priority: medium]
Total time used: 40 min

No tasks skipped.

Schedule for Mochi on 2026-06-25 (Owner: Alex Rivera):
  08:00 — Feeding [Nutrition] — 10 min [priority: medium]
  08:10 — Grooming [Hygiene] — 20 min [priority: low]
Total time used: 30 min

No tasks skipped.

=== Sorted by Time ===
Feeding: 08:00
Morning Walk: 14:00

=== filter_tasks: incomplete tasks on Luna's schedule ===
  Feeding (completed=False)

=== filter_tasks: completed tasks on Luna's schedule ===
  Morning Walk (completed=True)

=== filter_tasks: tasks for pet 'Luna' ===
  Morning Walk
  Feeding

=== filter_tasks: tasks for pet 'Mochi' (should be empty on Luna's schedule) ===
  []

=== Recurring Task: mark_complete() on Feeding ===
  Feeding | schedule_date: 2026-06-25 (completed=True)
  Feeding | schedule_date: 2026-06-26 (next occurrence)

=== Conflict Detection ===
  Conflict: 'Medication' and 'Dental Cleaning' both scheduled at 09:00
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
=============================== test session starts ===============================
platform darwin -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/**********/Desktop/CodePath/ai110-module2show-pawpal-starter
configfile: pytest.ini
plugins: anyio-4.14.0, cov-7.1.0
collected 17 items

tests/test_pawpal.py .................                                      [100%]

=============================== 17 passed in 0.04s ================================
```

The 17 tests cover the core scheduling behaviors built into PawPal+, marking tasks as complete and verifying that daily/weekly recurring tasks correctly generate a next occurrence. They also validate schedule generation, making sure high-priority tasks are placed first and that tasks exceeding the available time budget get skipped. Beyond that, the suite checks that `sort_by_time()` returns slots in the right order, that `filter_tasks()` correctly narrows results by completion status or pet name, and that `detect_conflicts()` catches two tasks assigned to the same time slot.

Confidence Level: ⭐⭐⭐½ (3.5/5)

I'm fairly confident in this system, all 17 tests pass and they actually cover the behaviors that matter most, sorting, filtering, conflict detection, and recurrence. But I'm not giving it a full 5 stars because I know firsthand that passing tests don't catch everything. For example, earlier in this project, sort_by_time() quietly got changed to sort by the wrong field, and none of my tests caught it since I hadn't written tests for that method yet at the time, I only caught it because I happened to look closely at the terminal output and it didn't match what I expected. That experience made me trust my test suite more, but also made me realize that a green checkmark only means what I actually wrote tests for, not that the whole system is bulletproof.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature           | Method(s)                     | Notes                                                                                                                                                                                                                             |
| ----------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task sorting      | `Schedule.sort_by_time()`     | Returns a new list of slots sorted by `scheduled_time`, doesn't mutate `self.slots`. Tasks with no `scheduled_time` sort last.                                                                                                    |
| Filtering         | `Schedule.filter_tasks()`     | Filters by completed status and/or `pet_name`, combined with AND logic.                                                                                                                                                           |
| Conflict handling | `Schedule.detect_conflicts()` | Flags tasks with the exact same `scheduled_time` within one pet's schedule. Returns warning strings instead of raising errors. Only checks within a single pet's schedule, not across pets, does not check overlapping durations. |
| Recurring tasks   | `Task.mark_complete()`        | When a `"daily"` or `"weekly"` task is completed for the first time, returns a new `Task` instance scheduled one day/week later. Returns `None` for other frequencies or duplicate completions.                                   |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
