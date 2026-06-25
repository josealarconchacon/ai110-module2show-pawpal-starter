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
Schedule for Luna on 2026-06-23 (Owner: Alex Rivera):
  08:00 — Morning Walk [Exercise] — 30 min [priority: high]
  08:30 — Feeding [Nutrition] — 10 min [priority: medium]
Total time used: 40 min

No tasks skipped.

Schedule for Mochi on 2026-06-23 (Owner: Alex Rivera):
  08:00 — Feeding [Nutrition] — 10 min [priority: medium]
  08:10 — Grooming [Hygiene] — 20 min [priority: low]
Total time used: 30 min

No tasks skipped.
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
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature           | Method(s)                     | Notes                                                                                                                                                                                                                              |
| ----------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Task sorting      | `Schedule.sort_by_time()`     | Returns a new list of slots sorted by `scheduled_time`, doesn't mutate `self.slots`. Tasks with no `scheduled_time` sort last.                                                                                                     |
| Filtering         | `Schedule.filter_tasks()`     | Filters by completed status and/or `pet_name`, combined with AND logic.                                                                                                                                                            |
| Conflict handling | `Schedule.detect_conflicts()` | Flags tasks with the exact same `scheduled_time` within one pet's schedule. Returns warning strings instead of raising errors. Only checks within a single pet's schedule, not across pets — does not check overlapping durations. |
| Recurring tasks   | `Task.mark_complete()`        | When a `"daily"` or `"weekly"` task is completed for the first time, returns a new `Task` instance scheduled one day/week later. Returns `None` for other frequencies or duplicate completions.                                    |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
