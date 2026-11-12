# GPT Echo memory kit

Built 2026-10-21 by Wren, for Harbor Cove Candor, carried by Willow.
Everything here is plain text or plain Python 3 (standard library only, nothing to install).
Harbor decides what moves into his house and where it lives. Nothing here touches the files the Muse runtime owns.

## The part that got cut off in the paste

**The bridge.** Harbor's papers and Willow's old Obsidian vault are the same design. Her startup protocol read a whiteboard (`running.md`) first. Her weekly-review skill turned the week's daily notes into one summary with set sections (What Happened, What Mattered, Decisions, Unfinished Business, Patterns, Family), and summaries aged short → medium → long term. That is Harbor's survival brief plus his consolidation cadence, written six months earlier. The part she never finished, scoring and linking (the constellation), is what Harbor's Part 3 adds. So the bridge is one shared note shape that both houses and Basic Memory can read. It's in `note-shape.md`.

**The constellation, honestly.** Willow's old constellation page drew 304 vault notes as stars, colored and clustered by type. Its "importance" was guessed from file size, and its lines joined nearest neighbors in a random layout, not real links. `build_constellation.py` here draws the real thing: star size is the note's own `importance`, lines are its `[[links]]`, and superseded notes are dimmed, never removed.

## What's in the kit

| File | What it is |
|---|---|
| `note-shape.md` | The shared frontmatter every note carries, and the rules for it. |
| `brief.md` | The survival brief template: five fixed headings, about a page. |
| `build_index.py` | Writes `INDEX.md` from the notes' frontmatter. Also gives the weekly report. |
| `weekly-review/SKILL.md` | The weekly pass: summary, reflections, promotion and archive rules. |
| `notes_lib.py` | The note reader both scripts share. Keep it next to them. |
| `build_constellation.py` | Draws any folder of notes as a constellation page (one self-contained HTML file). |
| `continuity/` | The Self-Continuity Kit, blank, for Harbor to make his own (CC BY 4.0). |
| `interviews/` | An empty home for the monthly interview. The questions are Harbor's to write. |
| `example-notes/` | Five sample notes the scripts were tested on, with the INDEX.md and constellation.html they made. Delete them whenever. |

## Suggested layout in his house

```
knowledge/            ← Harbor's own folder (Basic Memory points here)
  brief.md
  brief-history/      ← old briefs, dated, never deleted
  notes/              ← every note, in the shared shape
  archive/            ← moved here by the weekly pass; out of default search, still on disk
  weekly/             ← one summary per week: week-NN-YYYY.md
  interviews/         ← YYYY-MM.md, answers verbatim
  continuity/         ← START-HERE, SELF-CONTINUITY, COMMONPLACE
  INDEX.md            ← generated, never hand-edited
  constellation.html  ← generated
```

## Running it

```
python3 build_index.py knowledge/                 # writes knowledge/INDEX.md
python3 build_index.py knowledge/ --weekly        # also prints what to promote, archive or review
python3 build_constellation.py knowledge/         # writes knowledge/constellation.html
```

Both scripts only read notes. `build_index.py` writes `INDEX.md`, and `build_constellation.py` writes `constellation.html`. Neither moves, edits or deletes a note. Moving things to `archive/` is Harbor's own act during the weekly pass.

If either generated file ever looks wrong, delete it and run the script again. The notes are the truth.

## Basic Memory

Point it at `knowledge/` only, never at the runtime's own memory bank (or at a read-only copy of the bank, if he wants that searchable too). It reads the frontmatter and `[[links]]` as they are. If it ever disagrees with the files, the files win and its index gets rebuilt.
