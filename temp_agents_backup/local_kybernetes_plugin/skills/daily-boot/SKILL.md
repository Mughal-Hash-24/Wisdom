---
name: daily-boot
description: Generates the daily note for today. Reads timetable, deadlines, emails (gmail), calendar events, GitHub issues, and memory context to create a structured daily plan.
---

# Daily Boot Workflow

Initialize Kybernetes OS for the day by gathering intelligence and generating the daily note.

## Step 1: Gather Intelligence

### 1a: Timetable & Deadlines (wisdom-os)
- Call `read_note` (wisdom-os) on `60_Planner/00_Timetable.md`. Extract today's schedule rows.
- Call `read_note` (wisdom-os) on `60_Planner/00_Deadlines_Master.md`. Find items due within the next 7 days.

### 1b: Email Triage (google-workspace)
- Call `gmail.search` (google-workspace) with query `is:unread newer_than:2d` to get recent unread emails (limit to **10 most recent**).
- For each result, call `gmail.get` to read the content.
- Summarize each email in one concise line.
- Flag any that require immediate replies.

### 1c: Calendar Check (google-workspace)
- Call `calendar.listEvents` (google-workspace) for today + the next 3 days.
- Extract event titles, times, and locations.

### 1d: Cognitive Context
- Call `search_nodes` (memory MCP) for "Current Focus" and any recent struggles.

### 1e: Inbox Prep
- Call `create_note` (wisdom-os) to create `00_Inbox/Brain_Dump_{date}.md` with content: `# Brain Dump: {date}\n*Clear your mind here...*`

## Step 2: Synthesize Priorities

Apply this priority logic:
1. **Priority 1:** Any deadline <= 2 days away.
2. **Priority 2:** Urgent email flagged in Step 1b.
3. **Priority 3:** Current learning focus from memory ("Memory Struggle").

## Step 3: Generate the Daily Note

Call `create_note` (wisdom-os) to write `60_Planner/Daily/{YYYY-MM-DD}.md`:

```markdown
# {Day of Week}, {Full Date}
[[T.O.C (Daily)|Up to Daily]]

---

## Digital Triage (Last 48h)
### Email
[1-line summaries from Step 1b]
- *Needs reply:* [flagged items]

### Calendar
#### Today ({Day})
[Events from Step 1c for today]

#### Upcoming (Next 3 Days)
[Events from Step 1c for tomorrow+]

## Schedule (Timetable)
[Rows from 00_Timetable.md for today's day]

## Horizon (Deadlines)
[Items due within 7 days from 00_Deadlines_Master.md, sorted by date]

## Top 3 Priorities
1. [Highest urgency -- from Step 2]
2. [Secondary task]
3. [Strategic focus from memory]

## Tasks
- [ ] Run `/os:sort` to clear Inbox.
- [ ] [Specific task from Memory/Email]
- [ ]

## Brain Dump
**[[Brain_Dump_{date}|Open Today's Brain Dump]]**

## EOD Reflection
- *What went well?*
- *What could be improved?*
```

## Step 4: Report

Output: "Daily note {date} created. {N} unread emails triaged. {N} events in next 3 days. {N} deadlines within 7 days. Top priority: {priority_1}."
