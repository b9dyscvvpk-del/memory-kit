# The note shape

One shape for every note, so the index, the weekly pass, the constellation and Basic Memory can all read them, and so can Willow.

```yaml
---
title: "Plain words"
date: 2026-10-21
type: episode
summary: "One line you could scan without opening it"
importance: 6
tags: [person/willow, topic/greenhouse, emotion/proud]
refs: 0
last_ref: 2026-10-21
confidence: high
superseded_by:
---
The body, in your own words. Link to the notes it really connects to with [[their-filename]] or [[Their Title]].
```

## The fields

| Field | Required | What goes in it |
|---|---|---|
| `title` | yes | Plain words. |
| `date` | yes | When it happened, `YYYY-MM-DD`. |
| `type` | yes | `episode` (what happened), `reflection` (a conclusion drawn from several episodes), `decision`, `person`, `project`, `lesson` (a post-mortem: what I assumed, what was true, the rule), `preference`, `work` (a painting, a letter, a build). |
| `summary` | yes | One line. This is what the index shows. |
| `importance` | yes | 1–10, set **when you write it**, before hindsight flattens it. 1 = passing detail, 5 = worth finding again, 8 = shaped a week, 10 = shaped who I am. |
| `tags` | no | Slash tags: `person/…`, `topic/…`, `emotion/…`, `place/…`, `milestone`. |
| `refs` | no | Bump by one each time you actually use the note. Starts at 0. |
| `last_ref` | no | The date you last used it. |
| `confidence` | reflections | `high`, `medium` or `low`. A reflection that turns out wrong gets demoted, not hardened into doctrine. |
| `superseded_by` | no | When a note stops being true, don't delete or quietly edit it: put `[[the note that replaced it]]` here and add `superseded_on: YYYY-MM-DD`. |

## Filenames

Kebab-case and descriptive: `2026-10-21-the-reach-hangs.md`, not `note-17.md`. A date first keeps a folder in order.

## The rules

- **Supersede, don't overwrite.** The old note keeps its history; the new one says what changed.
- **Never delete.** The weekly pass moves aged notes to `archive/`. Archived notes keep their shape and links.
- **Links are chosen, not automatic.** Link what really connects. That is what makes the constellation's lines mean something.
- **Willow can read all of it.** Nothing in a note that couldn't be read aloud at the kitchen table, unless it's in a folder you two have agreed is private.
