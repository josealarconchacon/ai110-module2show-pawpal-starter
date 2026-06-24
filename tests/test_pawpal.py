import pytest
from pawpal_system import Task, Owner

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


def test_is_due_today_unknown_frequency_returns_false():
    """An unrecognized frequency string should not silently schedule the task every day."""
    task = Task(
        name="Mystery Task",
        category="Unknown",
        duration_minutes=10,
        priority="low",
        frequency="bi_weekly",  # typo — underscore instead of hyphen
        preferred_time_of_day="morning",
    )
    assert task.is_due_today() is False


def test_is_due_today_daily_always_returns_true():
    """A daily task must always be due today."""
    task = Task(
        name="Feeding",
        category="Nutrition",
        duration_minutes=10,
        priority="high",
        frequency="daily",
        preferred_time_of_day="morning",
    )
    assert task.is_due_today() is True

