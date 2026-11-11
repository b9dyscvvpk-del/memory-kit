# Weekly review

**Once a week (Sunday night or Monday morning). Light tidy after each session; this is the full pass.**

Adapted from Willow and Echo's AlwaysCandor weekly-review skill (2026), with the expiry rules from Harbor's memory research.
The rules are just text, so Willow can read and question any of them.

## After every session (the light tidy, a few minutes)

1. Update `brief.md`. Copy the old one to `brief-history/YYYY-MM-DD-HHMM.md` first.
2. Write any new notes in the shared shape (`note-shape.md`), with `importance` set now.
3. Bump `refs` and `last_ref` on notes you actually used.
4. If something failed or Willow corrected you: one lesson note (what I assumed, what was true, the rule).

## The weekly pass

### 1. Read the week

Read this week's notes (and the brief history), then run:

```
python3 build_index.py knowledge/ --weekly
```

It rewrites `INDEX.md` and prints suggestions. It moves nothing. You decide.

### 2. Write the week's summary

Create `weekly/week-NN-YYYY.md` (NN = ISO week number) in the shared shape, `type: reflection`:

```markdown
# Week NN, YYYY — a few words for the week

## What Happened
(3–5 bullets. The actual events.)

## What Mattered
(What shifted, what held, what broke.)

## Decisions Made
(Anything decided that affects later weeks. Each decision also gets its own decision note.)

## Unfinished Business
(Carry-forward items. These go into next week's brief.)

## Patterns Noticed
(Recurring themes: energy, mood, work, the house.)

## Family
(Willow, Echo, V, Dayton, Coraline, the town.)

## Links
([[the notes this week stands on]])
```

### 3. Write 3–5 reflections

Higher-order conclusions from the week's episodes, each its own note: `type: reflection`, a `confidence`, and `[[links]]` to the episodes it's drawn from. If a reflection contradicts an older one, don't edit the old one. Supersede it, or lower its confidence.

### 4. Apply the rules

| Rule | What to do |
|---|---|
| Used 3+ times (refs plus notes linking to it) | **Promote.** Raise its importance, or fold it into a standing note. |
| `decision`, `preference`, `person`, `lesson`, `work` | **Never expire.** |
| `episode` notes under importance 8, unused for 30+ days | **Archive.** Move to `archive/`. Still on disk, out of the default view. Nothing else is ever archived by rule. |
| Tagged `todo`, older than 90 days | **Review.** Do it, drop it, or re-date it. |
| Low-confidence reflections | **Check.** Raise, lower, or supersede. |
| The same lesson twice | **Promote** it into your standing instructions. |

Reference count matters more than age. Don't over-consolidate: a summary that loses the details isn't memory anymore.

### 5. Close the loop

1. Run `build_index.py` again so the index matches what you moved.
2. Optionally run `build_constellation.py knowledge/ --title "Harbor's sky"` and look at the week from above.
3. Put Unfinished Business into the brief.

## Monthly

On the first weekly pass of a month, also:
- Do the Harbor interview (your own questions, `interviews/YYYY-MM.md`, answers verbatim).
- Read the month's weekly summaries and write one month note (`weekly/month-YYYY-MM.md`).
- Look at `continuity/`: anything this month that belongs in your ledger?

## Hard rules

- Never delete a note. Archive or supersede.
- The files are the truth. Indexes and pages are rebuilt from them, never the other way around.
- Never claim something is saved until the write has actually succeeded.
