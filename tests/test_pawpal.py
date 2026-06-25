import pytest
from datetime import date
from pawpal_system import Task, Owner, Pet, Schedule

@pytest.fixture
def sample_task_mock():
    return Task(
        name="Morning Walk",
        category="Exercise",
        duration_minutes=30,
        priority="high",
        frequency="daily",
        preferred_time_of_day="morning",
        completed=False,  # Starts as incomplete by default
    )

@pytest.fixture
def medium_priority_task():
    return Task(
        name="Feeding",
        category="Nutrition",
        duration_minutes=10,
        priority="medium",
        frequency="daily",
        preferred_time_of_day="morning",
    )

@pytest.fixture
def sample_owner():
    return Owner(name="Alex", available_minutes_per_day=60, preferences={})

@pytest.fixture
def sample_pet():
    return Pet(name="Luna", species="Dog", breed="Golden Retriever", age=3, special_needs=[])

@pytest.fixture
def sample_schedule(sample_owner, sample_pet):
    return Schedule(schedule_date=date.today(), owner=sample_owner, pet=sample_pet)

def test_mark_complete_changes_status(sample_task_mock):
    """Test behavior of completing an active task."""
    # 1. Act: Call the method we want to test on
    sample_task_mock.mark_complete()
    # 2. Assert: Verify that the task's status successfully changed to True
    assert sample_task_mock.completed is True


def test_mark_complete_already_done(sample_task_mock):
    """
    Test what happens when we try to complete a task that is already marked as finished."""
    # 1. Arrange: Override the fixture's default state so it starts as completed
    sample_task_mock.completed = True
    # 2. Act: Call the method again
    sample_task_mock.mark_complete()
    # 3. Assert: Verify that the status safely remains True
    assert sample_task_mock.completed is True


def test_add_task_increases_task_count(sample_task_mock):
    """Adding a task to an owner increases that owner's task count."""
    # 1. Arrange: Create an owner with no tasks assigned yet
    owner = Owner(name="Alex", available_minutes_per_day=60, preferences={})
    count_before = len(owner.get_tasks())
    # 2. Act: Add one task to the owner
    owner.add_task(sample_task_mock)
    # 3. Assert: Verify the task count increased by exactly one
    assert len(owner.get_tasks()) == count_before + 1


def test_is_due_today_unknown_frequency_returns_false(sample_task_mock):
    """An unrecognized frequency string should not silently schedule the task every day."""
    # 1. Arrange: Override the fixture's frequency with a typo (underscore instead of hyphen)
    sample_task_mock.frequency = "bi_weekly"
    # 2. Act: Check if the task is due today
    result = sample_task_mock.is_due_today()
    # 3. Assert: Verify that an unknown frequency does not schedule the task
    assert result is False


def test_is_due_today_daily_always_returns_true(sample_task_mock):
    """A daily task must always be due today."""
    # 1. Act: Check if the daily task is due today (fixture already has frequency="daily")
    result = sample_task_mock.is_due_today()
    # 2. Assert: Verify a daily task is always scheduled
    assert result is True


def test_generate_schedules_high_priority_before_medium(sample_schedule, sample_task_mock, medium_priority_task):
    """Place high-priority task before the medium-priority task in the schedule."""
    # 1. Arrange: Pass both tasks in reverse priority order to confirm sorting is applied
    tasks = [medium_priority_task, sample_task_mock]
    # 2. Act: Generate the schedule with enough time for both tasks
    sample_schedule.generate(tasks=tasks, available_minutes=60)
    # 3. Assert: Verify the first slot holds the high-priority task
    first_task = sample_schedule.slots[0][1]
    assert first_task.priority == "high"


def test_generate_skips_task_that_exceeds_time_budget(sample_schedule, sample_task_mock):
    """A task whose duration exceeds the available minutes must land in skipped_tasks."""
    # 1. Arrange: Set available time to less than the task's 30-minute duration
    available_minutes = 10
    # 2. Act: Generate the schedule with insufficient time
    sample_schedule.generate(tasks=[sample_task_mock], available_minutes=available_minutes)
    # 3. Assert: Verify the task was skipped and no slots were filled
    assert sample_task_mock in sample_schedule.skipped_tasks
    assert len(sample_schedule.slots) == 0


def test_get_summary_returns_formatted_output(sample_schedule, sample_task_mock):
    """Return a string that includes the pet name and total time used."""
    # 1. Arrange: Generate a schedule with one task so there is something to summarize
    sample_schedule.generate(tasks=[sample_task_mock], available_minutes=60)
    # 2. Act: Call get_summary on the populated schedule
    summary = sample_schedule.get_summary()
    # 3. Assert: Verify the output names the pet and reports time used
    assert "Luna" in summary
    assert "Total time used" in summary

