# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I ended up with four classes: `Pet`, `Task`, `Owner`, and `Schedule`. Each one handles a pretty distinct piece of the problem.

`Pet` is just a profile, it holds the animal's name, species, breed, age, and any special needs. Its two methods (`get_care_profile` and `has_special_needs`) exist mostly so other parts of the system can ask questions about the pet without digging into its raw fields. I wanted Pet to be passive; it doesn't do anything on its own, it just describes the animal.

`Task` represents a single care item, like feeding or grooming. It carries the information I need to schedule it, how long it takes, how urgent it is, how often it happens, and what time of day works best. The `is_due_today` method felt necessary early on because not every task runs every day, so the scheduler needs a way to filter before it even starts building the plan. `get_priority_value` and `get_display_label` are utility methods that keep the scheduling and display logic from leaking into Task's data.

`Owner` will stores how much time the owner has available each day and their preferences, and it acts as the container for the task list. Tasks are managed through the owner rather than floating loose. That felt right because in real life, the owner is the one deciding what needs to get done.

`Schedule` is where the actual planning happens. It takes a specific date, owner, and pet, then figures out which tasks fit into the day's time budget and in what order. The separation of `fits_in_budget`, `add_slot`, and `generate` felt important. I didn't want generate to be one giant method that did everything at once. Breaking it up made the logic easier to reason about step by step.

**b. Design changes**

Yes, one thing caught me when reviewing the skeleton more carefully. The `Owner` class had methods for `add_task`, `remove_task`, and `get_tasks`, but `__init__` never actually initialized a `tasks` list. Every one of those methods would have crashed immediately at runtime because there was nothing to add to or read from. I added `self.tasks: List = []` to the constructor to fix that.

The brief calls this component `Scheduler,` but I went with Schedule instead. The class holds a single day's plan for one owner and pet (`slots, totals used, skipped tasks`), so it felt more like a thing than a doer, and Schedule matched that better.

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

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
