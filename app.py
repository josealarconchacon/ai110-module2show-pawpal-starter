import re
import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes_per_day = st.number_input(
    "Available minutes per day", min_value=15, max_value=600, value=90
)
st.session_state["owner"] = Owner(
    name=owner_name,
    available_minutes_per_day=available_minutes_per_day,
    preferences={},
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    st.session_state["pet"] = Pet(
        name=pet_name,
        species=species,
        breed="Unknown",
        age=0,
        special_needs=[],
    )
    st.success(f"Pet saved: {pet_name} ({species})")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    scheduled_time = st.text_input("Scheduled time", value="", placeholder="e.g. 08:00")

if st.button("Add task"):
    if not task_title or not task_title.strip():
        st.error("Task title cannot be empty.")
    elif not scheduled_time:
        st.error("Scheduled time cannot be empty. Please enter a time in HH:MM format.")
    elif not re.fullmatch(r"\d{2}:\d{2}", scheduled_time):
        st.error("Scheduled time must be in HH:MM format, e.g. 08:00")
    else:
        st.session_state.tasks.append(
            Task(
                name=task_title,
                duration_minutes=int(duration),
                priority=priority,
                scheduled_time=scheduled_time,
                category="General",
                frequency="daily",
                preferred_time_of_day="morning",
            )
        )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "name": task.name,
                "scheduled_time": task.scheduled_time,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
            }
            for task in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    if not (st.session_state.get("owner") and st.session_state.get("pet") and st.session_state.tasks):
        st.warning("Add an owner, a pet, and at least one task before generating a schedule.")
    else:
        schedule = Schedule(
            schedule_date=date.today(),
            owner=st.session_state["owner"],
            pet=st.session_state["pet"],
        )
        schedule.generate(
            tasks=st.session_state.tasks,
            available_minutes=st.session_state["owner"].available_minutes_per_day,
        )
        st.session_state["schedule"] = schedule
        st.success(schedule.get_summary())
        if schedule.skipped_tasks:
            st.warning(schedule.get_skipped_summary())

        st.subheader("📅 Sorted by Time")
        sorted_tasks = schedule.sort_by_time()
        st.table([{"name": task.name, "scheduled_time": task.scheduled_time} for _, task in sorted_tasks])

        st.subheader("⚠️ Conflict Warnings")
        warnings = schedule.detect_conflicts()
        if warnings:
            for warning in warnings:
                st.error(warning)
        else:
            st.success("No scheduling conflicts detected.")

        st.subheader("🔍 Filter by Status")
        status_filter = st.radio("Filter by status", ["All", "Completed", "Incomplete"], index=0)
        if status_filter == "All":
            filtered = schedule.filter_tasks(completed=None)
        elif status_filter == "Completed":
            filtered = schedule.filter_tasks(completed=True)
        else:
            filtered = schedule.filter_tasks(completed=False)
        st.table([{"name": t.name, "scheduled_time": t.scheduled_time} for t in filtered])
