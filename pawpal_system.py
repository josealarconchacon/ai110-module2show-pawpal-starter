from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Pet:
    """Pet class with its profile information and special care requirements."""
    name: str
    species: str
    breed: str
    age: int
    special_needs: List = field(default_factory=list)

    def get_care_profile(self) -> dict:
        """Returns a dictionary summarizing the pet's profile, including species, breed, age, and special needs."""
        pass

    def has_special_needs(self) -> bool:
        """Returns True if the pet has any special needs, False otherwise."""
        pass


@dataclass
class Task:
    """Represents a single care task (feeding, grooming) that can be scheduled for a pet."""
    name: str
    category: str
    duration_minutes: int
    priority: int
    frequency: str
    preferred_time_of_day: str

    def is_due_today(self) -> bool:
        """Returns True if this task should be performed today based on its frequency."""
        pass

    def get_priority_value(self) -> int:
        """Returns the numeric priority of this task, used for sorting when building a schedule."""
        pass

    def get_display_label(self) -> str:
        """Returns a label for the task, combining name, category, and duration."""
        pass


class Owner:
    """Pet owner with their daily availability and a list of care tasks they manage."""
    def __init__(self, name: str, available_minutes_per_day: int, preferences: dict):
        self.name = name
        self.available_minutes_per_day = available_minutes_per_day
        self.preferences = preferences
        self.tasks: List = []

    def add_task(self, task):
        """Adds a Task to the owner's managed task list."""
        pass

    def remove_task(self, task):
        """Removes a Task from the owner's managed task list."""
        pass

    def get_tasks(self) -> List:
        """Returns the full list of Tasks currently managed by this owner."""
        pass

    def set_availability(self, minutes):
        """Updates the owner's available time per day in minutes."""
        pass


class Schedule:
    """Builds and holds a daily care schedule for a specific owner and pet."""
    def __init__(self, date: date, owner: Owner, pet: Pet):
        self.date = date
        self.owner = owner
        self.pet = pet
        self.slots: List = []
        self.total_minutes_used: int = 0
        self.skipped_tasks: List = []

    def generate(self, tasks, available_minutes):
        """Populates slots by fitting tasks into the available time budget in priority order."""
        pass

    def add_slot(self, start_time, task):
        """Appends a (start_time, task) entry to the schedule's slot list and updates total_minutes_used."""
        pass

    def fits_in_budget(self, task, time_remaining) -> bool:
        """Returns True if the task's duration fits within the remaining available minutes."""
        pass

    def is_full(self) -> bool:
        """Returns True if no available minutes remain for additional tasks."""
        pass

    def get_summary(self) -> str:
        """Returns a formatted string listing all scheduled slots and total minutes used."""
        pass

    def get_skipped_summary(self) -> str:
        """Returns a formatted string listing all tasks that were skipped due to time constraints."""
        pass
