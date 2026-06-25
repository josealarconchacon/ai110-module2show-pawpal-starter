# temporary "testing ground" to verify logic works in the terminal.

# importing the classes from pawpal_system.py
from datetime import date
from pawpal_system import Pet, Task, Owner, Schedule

# --- Owner ---
owner = Owner(
    name="Alex Rivera",
    available_minutes_per_day=90,
    preferences={"preferred_time_of_day": "morning"},
)

# --- Pets ---
pet1 = Pet(
    name="Luna",
    species="Dog",
    breed="Golden Retriever",
    age=3,
    special_needs=["scare of thunderstorms", "scare of cars honk"],
)

pet2 = Pet(
    name="Mochi",
    species="Cat",
    breed="Scottish Fold",
    age=5,
    special_needs=[],
)

# --- Tasks ---
task1 = Task(
    name="Morning Walk",
    category="Exercise",
    duration_minutes=30,
    priority="high",
    frequency="daily",
    preferred_time_of_day="morning",
    completed=False
)

task2 = Task(
    name="Feeding",
    category="Nutrition",
    duration_minutes=10,
    priority="medium",
    frequency="daily",
    preferred_time_of_day="morning",
    completed=False
)

task3 = Task(
    name="Grooming",
    category="Hygiene",
    duration_minutes=20,
    priority="low",
    frequency="daily",          
    preferred_time_of_day="afternoon",
    completed=False
)

# --- Luna's schedule: Walk + Feeding ---
schedule_luna = Schedule(schedule_date=date.today(), owner=owner, pet=pet1)
schedule_luna.generate(tasks=[task1, task2], available_minutes=owner.available_minutes_per_day)

# --- Mochi's schedule: Feeding + Grooming ---
schedule_mochi = Schedule(schedule_date=date.today(), owner=owner, pet=pet2)
schedule_mochi.generate(tasks=[task2, task3], available_minutes=owner.available_minutes_per_day)

print("=== Today's Schedule ===")
print(schedule_luna.get_summary())
print()
print(schedule_luna.get_skipped_summary())
print()
print(schedule_mochi.get_summary())
print()
print(schedule_mochi.get_skipped_summary())

