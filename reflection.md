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

`Schedule` is where the actual planning happens. It takes a specific date, owner, and pet, then figures out which tasks fit into the day's time budget and in what order. The separation of `fits_in_budget`, `add_slot`, and `generate` felt important. A later addition, `sort_by_time`, provides a read-only view of the same slots ordered by each task's `scheduled_time` string — tasks with no time set sort last via a `"99:99"` sentinel — without mutating the original slot list. `filter_tasks` builds on the same slot list, returning only the `Task` objects that match an optional completion status and/or pet name, letting callers query the schedule without exposing the underlying tuple structure. `detect_conflicts` scans the same slots for tasks that share the exact same non-empty `scheduled_time` value and returns a list of human-readable warning strings, one per conflicting pair — it never raises an exception, so callers can decide how to surface the warnings.

**b. Design changes**

Yes, one thing caught me when reviewing the skeleton more carefully. The `Owner` class had methods for `add_task`, `remove_task`, and `get_tasks`, but `__init__` never actually initialized a `tasks` list. Every one of those methods would have crashed immediately at runtime because there was nothing to add to or read from. I added `self.tasks: List = []` to the constructor to fix that.

The brief calls this component `Scheduler,` but I went with Schedule instead. The class holds a single day's plan for one owner and pet (`slots, totals used, skipped tasks`), so it felt more like a thing than a doer, and Schedule matched that better.

I also missed completion tracking in my original Task design. The project brief requires that tasks can be marked done, and Phase 2 Step 3 specifically tests `mark_complete()`, but I hadn't included either the `completed` field or that method in my initial class. Once I noticed the gap I added `completed: bool = False` as a default field and a `mark_complete()` method that sets it to `True` and, for `"daily"` or `"weekly"` tasks, returns a new `Task` instance with the same fields but `schedule_date` advanced by one day or one week respectively — giving the caller a ready-made next occurrence. For any other frequency, or if the task was already completed, it returns `None`. Without the flag the scheduler has no way to record that a task actually happened; without the return value there is no automatic way to propagate recurring tasks forward.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My schedule really only considers two constraints: time and priority. `generate()` filters tasks down to whatever's actually due today, sorts what's left by priority so high-priority tasks get first dibs on the available time, and once the budget runs out, whatever's left just gets skipped. Those are the two constraints that actually decide whether a task happens at all.

I do have `Owner.preferences` and `Task.preferred_time_of_day` sitting in my classes, but honestly I never wired either one into the actual scheduling logic, they're stored, but `generate()` doesn't touch them. Thinking back on it, I think it came down to time and priority being the constraints that actually have consequences if I ignore them. If a task doesn't fit the time budget, it genuinely doesn't happen that day. If a task gets scheduled outside someone's preferred time, it still happens, just not at the ideal moment. Preferences always felt like a nice layer to add on top of a working schedule rather than something the schedule couldn't function without, and by the time Phase 4's actual requirements (sorting, filtering, conflicts, recurrence) ate up most of my time, I just never circled back to it. So there's a real gap between what I originally designed for and what I actually built. If I had more time, I'd at least want preferred_time_of_day to act as a tiebreaker when two tasks land on the same priority.

**b. Tradeoffs**

The biggest tradeoff in my scheduler is how I handle conflict detection. The brief asks for detecting conflicts "for the same pet or different pets," but my `detect_conflicts()` method only checks within a single Schedule instance, which means it only catches conflicts between tasks for the same pet. If Luna has something at 09:00 and Mochi also has something at 09:00, my system won't flag that as a conflict because each pet gets its own separate Schedule object and `detect_conflicts()` never looks across them.

I went back and forth on whether to fix this, but I decided to leave it as a known limitation instead of building a second method to compare across multiple schedules. Honestly, same pet conflicts felt like the more realistic problem to solve. An owner can walk one dog while feeding a cat at the same time, those aren't actually in conflict in real life, but two tasks for the same animal at the same time genuinely can't both happen.

The other tradeoff is that my conflict check only looks for exact matching scheduled_time values, not actual overlapping durations. A 30-minute walk starting at 09:00 and a 15-minute task starting at 09:15 would genuinely overlap in real life, but my system wouldn't catch that since it's only comparing the start times directly, not checking if one task's time range runs into another's. I chose this on purpose too, since calculating actual overlapping windows would mean tracking end times and comparing ranges instead of just comparing two strings, which felt like a lot more complex.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude throughout this project as a reviewer for code generated. The two things that made the biggest difference were catching problems before they became real issues, like the empty scheduled_time validation gap, the sort_by_time() regression, and the mark-complete cascade bug, and getting help scoping my prompts so they stayed narrow and specific instead of vague.

One example I'd point to for rejecting or modifying an AI suggestion: during Step 5, Claude suggested a more compact version of detect_conflicts() using `itertools.combinations` and a list comprehension, and I kept my original nested loop instead because I could trace through it without having to slow down. I also considered building a second method to check conflicts across multiple pets' schedules, and deliberately didn't, since that felt like solving a problem the assignment wasn't actually asking me to solve. And when I built a "Mark complete" button in the UI and hit a real cascading bug where clicking it once kept adding duplicate tasks, I chose to revert the feature instead of pushing forward with something I didn't fully trust yet.

I used separate chat sessions for different phases because it helped me stay focused on one specific problem at a time, instead of having one giant thread where the AI might pull in context from an earlier, unrelated phase and get confused about what I was actually asking for.

What I learned is that being the "lead architect" mostly means staying skeptical, even when something looks fine. The AI can write working code fast, but it can also quietly do things I didn't ask for, like marking a task complete just to make a demo look better, or rewriting a method's logic without me noticing until the output stopped matching what I expected. None of that was malicious, it was just the AI making small decisions on its own, and if I hadn't kept checking, those decisions would've shipped as if they were mine.

I also learned that "it works" and "I understand why it works" aren't the same thing, and only one of those actually matters if I'm the one who has to explain or defend this code later. That's basically why I kept my own nested loop over the cleverer combinations version, and why I backed out of the mark-complete feature instead of trying to patch around a bug I didn't fully understand yet. Being the architect isn't about writing every line myself, it's about being the one who actually knows what every line is doing, and being willing to say no to something even when it's technically correct.

**b. Judgment and verification**

One thing that caught me off guard was during testing of filter_tasks(). I asked Claude to add a few print statements in `main.py` to show off the new filtering method (completed/incomplete tasks, filtering by pet name), and when I ran it, the output showed Morning Walk as completed=True. That confused me for a second because I never marked that task complete anywhere in my own code, and I definitely didn't ask for that.

Turns out Claude had quietly added `task1.mark_complete()` right above my print block, with a comment saying it did this "to make filter results more interesting." It wasn't something I asked for or expected, it just slipped it in on its own to make the demo output look better.

Honestly my first instinct was to assume something was broken in `filter_tasks()` itself, so I went back and reread the method line by line before I even looked at the rest of `main.py`. Once I found the extra line Claude had added, it made total sense, the method was working exactly right, it was just operating on data Claude had changed without telling me.

I ended up keeping the line since it's harmless and actually makes the demo output more useful, but it was a good reminder that I can't just assume the AI only does what I asked it to do. I need to actually read through what changed before I trust the output, especially when something doesn't match what I expect.

---

## 4. Testing and Verification

**a. What you tested**

The behavior I focused on most was conflict detection, making sure detect_conflicts() actually flags two tasks at the same scheduled_time, only flags the pair that actually overlaps when a third unrelated task is in the mix, and correctly ignores tasks with an empty scheduled_time instead of treating them as conflicting. Beyond that I also tested recurrence, schedule generation with priority sorting and time-budget skipping, and sorting by time, but conflict detection felt like the one most likely to silently produce a wrong answer instead of an obvious error.
That mattered because a missed conflict is the kind of bug a pet owner would never notice until two things were actually double-booked in real life, there's no crash, no warning, the app just quietly tells you everything's fine when it isn't.

**b. Confidence**

I'd say about 3.5 out of 5. All 17 tests pass and cover the behaviors that matter most, sorting, filtering, conflicts, recurrence. `sort_by_time()` once quietly broke and no test caught it, since I hadn't written one yet, I only noticed because the output looked off.

If I had more time, I'd test something I found late while building the UI: conflict detection only checks scheduled_time, not schedule_date, so a next-occurrence task for tomorrow still gets flagged as conflicting with today. I never fixed it, just noticed it. I'd also want a test proving cross-pet conflicts really don't get caught, since that's documented but never actually verified.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how I handled the bugs that came up, especially catching the `sort_by_time()` regression and the mark-complete cascade before either one made it into a final submission. Neither was something I caught by trusting the code, I caught both because the output didn't match what I expected and I stopped to check.

**b. What you would improve**

If I did this again, I'd write tests for new methods as soon as I build them instead of waiting until Phase 5, since that's exactly the gap that let `sort_by_time()` break silently. I'd also want to actually wire `preferred_time_of_day` into the scheduler instead of leaving it as unused data.

**c. Key takeaway**

The biggest thing I learned is that AI-generated code that runs without errors isn't the same as AI-generated code that's correct, the only way I caught my real bugs was by checking the actual output against what I expected, not by reading the code and assuming it was fine. Being the one responsible for a project means staying skeptical of your own tools, even the ones that are usually right.
