"""Reads a folder of notes in the shared shape (see note-shape.md). Used by both scripts; never writes a note."""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

SKIP_DIRS = {'brief-history', '.git', '.obsidian', '.claude', 'node_modules'}
SKIP_FILES = {'INDEX.md', 'brief.md', 'README.md'}
_LINK = re.compile(r'\[\[([^\]|#\n]+)(?:[#|][^\]\n]*)?\]\]')


def _value(raw: str):
    raw = re.sub(r'\s+#.*$', '', raw).strip()
    if raw.startswith('[') and raw.endswith(']'):
        return [_value(part) for part in raw[1:-1].split(',') if part.strip()]
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in '"\'':
        return raw[1:-1]
    if re.fullmatch(r'-?\d+', raw):
        return int(raw)
    if raw.lower() in ('', 'null', '~', 'none'):
        return None
    return raw


def frontmatter(text: str) -> tuple[dict, str]:
    """The note's fields and its body. A note with no frontmatter has no fields."""
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---', 3)
    if end == -1:
        return {}, text
    fields, key = {}, None
    for line in text[3:end].splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        item = re.match(r'\s+-\s+(.*)', line)
        if item and key:
            if not isinstance(fields.get(key), list):
                fields[key] = []
            fields[key].append(_value(item.group(1)))
            continue
        pair = re.match(r'([A-Za-z_][\w-]*)\s*:\s*(.*)', line)
        if pair:
            key = pair.group(1)
            fields[key] = _value(pair.group(2))
    return fields, text[end + 4:].lstrip('\n')


def _date(value) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def _key(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def load(folder: Path) -> list[dict]:
    """Every note under the folder, with its links resolved to other notes where they can be."""
    notes = []
    for path in sorted(folder.rglob('*.md')):
        rel = path.relative_to(folder)
        if path.name in SKIP_FILES or SKIP_DIRS & set(rel.parts[:-1]):
            continue
        fields, body = frontmatter(path.read_text(encoding='utf-8', errors='replace'))
        importance = fields.get('importance')
        superseded = fields.get('superseded_by')
        notes.append({
            'path': rel.as_posix(),
            'stem': path.stem,
            'title': str(fields.get('title') or path.stem),
            'date': _date(fields.get('date')),
            'type': str(fields.get('type') or 'note'),
            'summary': str(fields.get('summary') or ''),
            'importance': importance if isinstance(importance, int) else None,
            'tags': [str(t) for t in fields.get('tags') or [] if t] if isinstance(fields.get('tags'), list) else [],
            'refs': fields.get('refs') if isinstance(fields.get('refs'), int) else 0,
            'last_ref': _date(fields.get('last_ref')),
            'confidence': fields.get('confidence'),
            'superseded_by': str(superseded) if superseded else None,
            'archived': 'archive' in rel.parts[:-1],
            'raw_links': _LINK.findall(body) + _LINK.findall(str(superseded or '')),
            'missing': [f for f in ('title', 'date', 'type', 'summary', 'importance') if fields.get(f) in (None, '')],
        })
    by_name = {}
    for i, note in enumerate(notes):
        by_name.setdefault(_key(note['stem']), i)
        by_name.setdefault(_key(note['title']), i)
    for i, note in enumerate(notes):
        note['links'] = sorted({by_name[_key(l)] for l in note['raw_links'] if _key(l) in by_name} - {i})
        replaced = _LINK.findall(note['superseded_by'] or '')
        note['replaced_by'] = by_name.get(_key(replaced[0])) if replaced else None
        note['inbound'] = 0
    for note in notes:
        for j in note['links']:
            notes[j]['inbound'] += 1
    return notes
