from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Pet:
    """Pet class with its profile information and special care requirements"""
    name: str
    species: str
    breed: str
    age: int
    special_needs: List = field(default_factory=list)

    def get_care_profile(self) -> dict:
        """Returns a dictionary summarizing the pet's profile, including species, breed, age, and special needs"""
        return {
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "special_needs": self.special_needs,
        }

    def has_special_needs(self) -> bool:
        """Returns True if the pet has any special needs, False otherwise"""
        return len(self.special_needs) > 0


@dataclass
class Task:
    """Represents a single care task (feeding, grooming) that can be scheduled for a pet"""
    name: str
    category: str
    duration_minutes: int
    priority: str  # "low", "medium", or "high"
    frequency: str
    preferred_time_of_day: str
    completed: bool = False

    def mark_complete(self):
        """Sets the task's completed status to True"""
        self.completed = True

    def is_due_today(self) -> bool:
        """Returns True if this task should be performed today based on its frequency"""
        today = date.today()
        freq = self.frequency.lower()
        if freq == "daily":
            return True
        elif freq == "weekly":
            return today.weekday() == 0  # Mondays
        elif freq == "bi-weekly":
            week_number = today.isocalendar()[1]
            return today.weekday() == 0 and week_number % 2 == 0
        elif freq == "monthly":
            return today.day == 1
        return True

    def get_priority_value(self) -> int:
        """Returns a numeric value for priority, used for sorting (low=3, medium=2, high=1)"""
        return {"high": 1, "medium": 2, "low": 3}.get(self.priority.lower(), 2)

    def get_display_label(self) -> str:
        """Returns a label for the task, combining name, category, and duration."""
        return f"{self.name} [{self.category}] — {self.duration_minutes} min [priority: {self.priority}]"


class Owner:
    """Pet owner with their daily availability and a list of care tasks they manage"""
    def __init__(self, name: str, available_minutes_per_day: int, preferences: dict):
        self.name = name
        self.available_minutes_per_day = available_minutes_per_day
        self.preferences = preferences
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        """Adds a Task to the owner's managed task list"""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Removes a Task from the owner's managed task list"""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Returns the full list of Tasks currently managed by this owner"""
        return self.tasks

    def set_availability(self, minutes: int):
        """Updates the owner's available time per day in minutes"""
        self.available_minutes_per_day = minutes


class Schedule:
    """Builds and holds a daily care schedule for a specific owner and pet"""
    def __init__(self, date: date, owner: Owner, pet: Pet):
        self.date = date
        self.owner = owner
        self.pet = pet
        self.slots: List = []
        self.total_minutes_used: int = 0
        self.skipped_tasks: List[Task] = []

    def generate(self, tasks: List[Task], available_minutes: int):
        """Populates slots by fitting tasks into the available time budget in priority order"""
        due_tasks = [t for t in tasks if t.is_due_today()]
        sorted_tasks = sorted(due_tasks, key=lambda t: t.get_priority_value())

        current_minute = 0
        time_remaining = available_minutes

        for task in sorted_tasks:
            if self.fits_in_budget(task, time_remaining):
                self.add_slot(current_minute, task)
                current_minute += task.duration_minutes
                time_remaining -= task.duration_minutes
            else:
                self.skipped_tasks.append(task)

    def add_slot(self, start_time: int, task: Task):
        """Appends a (start_time, task) entry to the schedule's slot list and updates total_minutes_used"""
        self.slots.append((start_time, task))
        self.total_minutes_used += task.duration_minutes

    def fits_in_budget(self, task: Task, time_remaining: int) -> bool:
        """Returns True if the task's duration fits within the remaining available minutes"""
        return task.duration_minutes <= time_remaining

    def is_full(self) -> bool:
        """Returns True if no available minutes remain for additional tasks"""
        return self.total_minutes_used >= self.owner.available_minutes_per_day

    def get_summary(self) -> str:
        """Returns a formatted string listing all scheduled slots and total minutes used"""
        if not self.slots:
            return "No tasks scheduled."
        lines = [f"Schedule for {self.pet.name} on {self.date} (Owner: {self.owner.name}):"]
        base_hour, base_minute = 8, 0
        for offset_minutes, task in self.slots:
            total = base_hour * 60 + base_minute + offset_minutes
            h, m = divmod(total, 60)
            lines.append(f"  {h:02d}:{m:02d} — {task.get_display_label()}")
        lines.append(f"Total time used: {self.total_minutes_used} min")
        return "\n".join(lines)

    def get_skipped_summary(self) -> str:
        """Returns a formatted string listing all tasks that were skipped due to time constraints"""
        if not self.skipped_tasks:
            return "No tasks skipped."
        lines = ["Skipped tasks (insufficient time):"]
        for task in self.skipped_tasks:
            lines.append(f"  - {task.get_display_label()}")
        return "\n".join(lines)
