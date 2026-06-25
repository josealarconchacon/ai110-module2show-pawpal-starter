# PawPal+ Project Reflection

## 1. System Design

PawPal+ is built around three core user actions:

1. **Register a pet** — the owner creates a pet profile, capturing the animal's name, species, breed, age, and any special care needs.
2. **Assign care tasks** — the owner adds tasks (feeding, grooming, medication, etc.) to their task list, each described by its duration, priority, frequency, and preferred time of day.
3. **Generate a daily schedule** — the system takes the owner's available time and the pet's tasks, filters to what is due today, and produces an ordered plan that fits within the time budget.

**a. Initial design**

I ended up with four classes: `Pet`, `Task`, `Owner`, and `Schedule`. Each one handles a pretty distinct piece of the problem.

`Pet` is just a profile, it holds the animal's name, species, breed, age, and any special needs. Its two methods (`get_care_profile` and `has_special_needs`) exist mostly so other parts of the system can ask questions about the pet without digging into its raw fields. I wanted Pet to be passive; it doesn't do anything on its own, it just describes the animal.

`Task` represents a single care item, like feeding or grooming. It carries the information I need to schedule it, how long it takes, how urgent it is, how often it happens, and what time of day works best. The `is_due_today` method felt necessary early on because not every task runs every day, so the scheduler needs a way to filter before it even starts building the plan. `get_priority_value` and `get_display_label` are utility methods that keep the scheduling and display logic from leaking into Task's data.

`Owner` will stores how much time the owner has available each day and their preferences, and it acts as the container for the task list. Tasks are managed through the owner rather than floating loose. That felt right because in real life, the owner is the one deciding what needs to get done.

`Schedule` is where the actual planning happens. It takes a specific date, owner, and pet, then figures out which tasks fit into the day's time budget and in what order. The separation of `fits_in_budget`, `add_slot`, and `generate` felt important. A later addition, `sort_by_time`, provides a read-only view of the same slots ordered by each task's `scheduled_time` string — tasks with no time set sort last via a `"99:99"` sentinel — without mutating the original slot list. `filter_tasks` builds on the same slot list, returning only the `Task` objects that match an optional completion status and/or pet name, letting callers query the schedule without exposing the underlying tuple structure.

**b. Design changes**

Yes, one thing caught me when reviewing the skeleton more carefully. The `Owner` class had methods for `add_task`, `remove_task`, and `get_tasks`, but `__init__` never actually initialized a `tasks` list. Every one of those methods would have crashed immediately at runtime because there was nothing to add to or read from. I added `self.tasks: List = []` to the constructor to fix that.

The brief calls this component `Scheduler,` but I went with Schedule instead. The class holds a single day's plan for one owner and pet (`slots, totals used, skipped tasks`), so it felt more like a thing than a doer, and Schedule matched that better.

I also missed completion tracking in my original Task design. The project brief requires that tasks can be marked done, and Phase 2 Step 3 specifically tests `mark_complete()`, but I hadn't included either the `completed` field or that method in my initial class. Once I noticed the gap I added `completed: bool = False` as a default field and a `mark_complete()` method that flips it to `True`. It's a small addition but without it the scheduler has no way to record that a task actually happened, only that it was planned.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

One thing that caught me off guard was during testing of filter_tasks(). I asked Claude to add a few print statements in main.py to show off the new filtering method (completed/incomplete tasks, filtering by pet name), and when I ran it, the output showed Morning Walk as completed=True. That confused me for a second because I never marked that task complete anywhere in my own code, and I definitely didn't ask for that.

Turns out Claude had quietly added task1.mark_complete() right above my print block, with a comment saying it did this "to make filter results more interesting." It wasn't something I asked for or expected, it just slipped it in on its own to make the demo output look better.

Honestly my first instinct was to assume something was broken in filter_tasks() itself, so I went back and reread the method line by line before I even looked at the rest of main.py. Once I found the extra line Claude had added, it made total sense, the method was working exactly right, it was just operating on data Claude had changed without telling me.

I ended up keeping the line since it's harmless and actually makes the demo output more useful, but it was a good reminder that I can't just assume the AI only does what I asked it to do. I need to actually read through what changed before I trust the output, especially when something doesn't match what I expect.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
