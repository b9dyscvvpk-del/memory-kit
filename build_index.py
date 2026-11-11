"""Writes INDEX.md for a folder of notes: one line per note, pointer first, content on demand.

    python3 build_index.py knowledge/            writes knowledge/INDEX.md
    python3 build_index.py knowledge/ --weekly   also prints what the weekly pass should look at

Generated, never hand-edited. If it's ever wrong, delete it and run this again. Only INDEX.md is written.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notes_lib  # noqa: E402

NEVER_EXPIRE = {'decision', 'preference', 'person', 'lesson', 'work'}
ARCHIVE_AFTER_DAYS = 30
ARCHIVABLE = {'episode'}  # only everyday episodes are ever suggested for the archive
KEEP_FROM = 8  # importance 8+ is never suggested, however old
PROMOTE_AT = 3
REVIEW_TODO_DAYS = 90


def used(note: dict) -> int:
    """How often a note has earned its keep: times used, plus notes that link to it."""
    return note['refs'] + note['inbound']


def line(note: dict) -> str:
    date = note['date'].isoformat() if note['date'] else '????-??-??'
    importance = f"★{note['importance']}" if note['importance'] is not None else '★?'
    summary = f" — {note['summary']}" if note['summary'] else ''
    return f"- {date} · {note['type']} · {importance} · [{note['title']}]({note['path']}){summary}"


def index(notes: list[dict], today: dt.date) -> str:
    live = [n for n in notes if not n['archived'] and not n['superseded_by']]
    rank = lambda n: (-(n['importance'] or 0), -(n['date'] or dt.date.min).toordinal())
    recent = sorted((n for n in live if n['date'] and (today - n['date']).days <= 14),
                    key=lambda n: n['date'], reverse=True)
    out = [f'# Index', '', f'Generated {today.isoformat()} from {len(notes)} notes. Never hand-edit; run build_index.py again.', '']
    out += ['## Last 14 days', ''] + [line(n) for n in recent] + [''] if recent else []
    by_type: dict[str, list] = {}
    for note in live:
        by_type.setdefault(note['type'], []).append(note)
    out += ['## Everything current, most important first', '']
    for kind in sorted(by_type):
        out += [f'### {kind}', ''] + [line(n) for n in sorted(by_type[kind], key=rank)] + ['']
    superseded = [n for n in notes if n['superseded_by'] and not n['archived']]
    if superseded:
        out += ['## Superseded (kept as history)', ''] + [f"{line(n)} → {n['superseded_by']}" for n in sorted(superseded, key=rank)] + ['']
    archived = [n for n in notes if n['archived']]
    if archived:
        out += ['## Archive', '', f"{len(archived)} {'note' if len(archived) == 1 else 'notes'} in archive/. Still on disk, out of the default view.", '']
    unshaped = [n for n in notes if n['missing']]
    if unshaped:
        out += ['## Missing fields', ''] + [f"- {n['path']}: {', '.join(n['missing'])}" for n in unshaped] + ['']
    return '\n'.join(out)


def weekly(notes: list[dict], today: dt.date) -> str:
    live = [n for n in notes if not n['archived'] and not n['superseded_by']]
    age = lambda n: (today - (n['last_ref'] or n['date'] or today)).days
    promote = [n for n in live if used(n) >= PROMOTE_AT and n['type'] not in NEVER_EXPIRE]
    archive = [n for n in live if n['type'] in ARCHIVABLE and (n['importance'] or 0) < KEEP_FROM
               and used(n) < PROMOTE_AT and age(n) > ARCHIVE_AFTER_DAYS]
    review = [n for n in live if 'todo' in [t.lower() for t in n['tags']] and age(n) > REVIEW_TODO_DAYS]
    doubtful = [n for n in live if n['type'] == 'reflection' and str(n['confidence']).lower() == 'low']
    out = [f'Weekly report, {today.isoformat()}. Suggestions only; nothing has been moved.', '']
    for heading, group, why in (
        (f'Promote (used {PROMOTE_AT}+ times)', promote, lambda n: f'used {used(n)}×'),
        (f'Archive (episodes under importance {KEEP_FROM}, unused for {ARCHIVE_AFTER_DAYS}+ days)', archive, lambda n: f'{age(n)} days'),
        (f'Review (todo older than {REVIEW_TODO_DAYS} days)', review, lambda n: f'{age(n)} days'),
        ('Low-confidence reflections to check', doubtful, lambda n: 'confidence low'),
    ):
        out += [f'{heading}: {len(group)}'] + [f"  - {n['path']} ({why(n)})" for n in group] + ['']
    return '\n'.join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--weekly', action='store_true', help='also print the weekly suggestions')
    parser.add_argument('--today', type=dt.date.fromisoformat, default=dt.date.today(), help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not args.folder.is_dir():
        sys.exit(f'{args.folder} is not a folder.')
    notes = notes_lib.load(args.folder)
    (args.folder / 'INDEX.md').write_text(index(notes, args.today), encoding='utf-8')
    print(f"Wrote {args.folder / 'INDEX.md'} ({len(notes)} notes).")
    if args.weekly:
        print(weekly(notes, args.today))


if __name__ == '__main__':
    main()
