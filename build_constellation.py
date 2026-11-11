"""Draws a folder of notes as a constellation: one self-contained HTML page, no internet needed.

    python3 build_constellation.py knowledge/                  writes knowledge/constellation.html
    python3 build_constellation.py knowledge/ --title "Harbor's sky" --out sky.html

Star size is the note's own importance. Lines are its real [[links]]. Superseded notes are dimmed,
with a dashed line to what replaced them. Archived notes are left out unless --archive is given.
Only the HTML file is written; the notes are only read.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notes_lib  # noqa: E402

COLORS = {
    'episode': '#7ac4c4', 'reflection': '#b07aeb', 'decision': '#f0c040', 'person': '#e8789a',
    'project': '#5a9cf5', 'lesson': '#ef6c40', 'preference': '#d4a070', 'work': '#50c878',
}

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
  html,body{margin:0;height:100%;background:#0b0d17;color:#e6e6f0;font:14px/1.4 system-ui,sans-serif;overflow:hidden}
  canvas{display:block;width:100vw;height:100vh;cursor:grab}
  #head{position:fixed;top:12px;left:16px;pointer-events:none}
  #head h1{margin:0;font-size:18px;font-weight:600}
  #head p{margin:2px 0 0;opacity:.6;font-size:12px}
  #legend{position:fixed;bottom:12px;left:16px;font-size:12px;opacity:.85}
  #legend span{display:inline-block;margin-right:10px;cursor:pointer}
  #legend span.off{opacity:.3}
  #legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:4px}
  #card{position:fixed;top:12px;right:16px;max-width:320px;background:#161a2bee;border:1px solid #2a3050;
        border-radius:10px;padding:12px 14px;display:none}
  #card h2{margin:0 0 4px;font-size:15px}
  #card .meta{opacity:.65;font-size:12px;margin-bottom:6px}
  #card .path{opacity:.45;font-size:11px;margin-top:8px;word-break:break-all}
  #search{position:fixed;top:12px;left:50%;transform:translateX(-50%);background:#161a2b;color:inherit;
          border:1px solid #2a3050;border-radius:8px;padding:6px 10px;width:min(260px,50vw)}
</style></head><body>
<canvas id="sky"></canvas>
<div id="head"><h1>__TITLE__</h1><p>__COUNT__</p></div>
<input id="search" placeholder="find a star…" autocomplete="off">
<div id="legend"></div><div id="card"></div>
<script>
const NOTES = __DATA__;
const COLORS = __COLORS__;
const sky = document.getElementById('sky'), ctx = sky.getContext('2d');
const card = document.getElementById('card'), search = document.getElementById('search');
let W, H, dpr, cam = {x: 0, y: 0, k: 1}, hover = null, pinned = null, hidden = new Set(), query = '';
const color = t => COLORS[t] || '#9aa3b5';
const radius = n => 2.5 + (n.importance == null ? 3 : n.importance) * 0.9;
NOTES.forEach((n, i) => { const a = i * 2.399963, r = 40 * Math.sqrt(i + 1);
  n.x = Math.cos(a) * r; n.y = Math.sin(a) * r; n.vx = 0; n.vy = 0; n.phase = Math.random() * 6.28; });
const edges = [];
NOTES.forEach((n, i) => n.links.forEach(j => edges.push([i, j, false])));
NOTES.forEach((n, i) => { if (n.replaced_by != null) edges.push([i, n.replaced_by, true]); });
function resize() { dpr = window.devicePixelRatio || 1; W = innerWidth; H = innerHeight;
  sky.width = W * dpr; sky.height = H * dpr; }
addEventListener('resize', resize); resize();
function settle(steps) {
  for (let s = 0; s < steps; s++) {
    for (let i = 0; i < NOTES.length; i++) for (let j = i + 1; j < NOTES.length; j++) {
      const a = NOTES[i], b = NOTES[j], dx = a.x - b.x, dy = a.y - b.y, d2 = dx * dx + dy * dy + 0.01;
      if (d2 > 90000) continue;
      const f = 900 / d2; a.vx += dx * f; a.vy += dy * f; b.vx -= dx * f; b.vy -= dy * f; }
    edges.forEach(([i, j]) => { const a = NOTES[i], b = NOTES[j], dx = b.x - a.x, dy = b.y - a.y;
      const d = Math.sqrt(dx * dx + dy * dy) || 1, f = (d - 70) * 0.01;
      a.vx += dx / d * f; a.vy += dy / d * f; b.vx -= dx / d * f; b.vy -= dy / d * f; });
    NOTES.forEach(n => { n.vx -= n.x * 0.002; n.vy -= n.y * 0.002; n.x += n.vx; n.y += n.vy; n.vx *= 0.6; n.vy *= 0.6; });
  }
}
settle(300);
function visible(n) { return !hidden.has(n.type); }
function lit(n) { return !query || (n.title + ' ' + n.summary + ' ' + n.tags.join(' ')).toLowerCase().includes(query); }
function screen(n) { return [W / 2 + (n.x + cam.x) * cam.k, H / 2 + (n.y + cam.y) * cam.k]; }
function draw(t) {
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
  const focus = pinned ?? hover, near = new Set();
  if (focus != null) edges.forEach(([i, j]) => { if (i === focus) near.add(j); if (j === focus) near.add(i); });
  edges.forEach(([i, j, dashed]) => { const a = NOTES[i], b = NOTES[j]; if (!visible(a) || !visible(b)) return;
    const [x1, y1] = screen(a), [x2, y2] = screen(b), on = focus === i || focus === j;
    ctx.strokeStyle = on ? 'rgba(255,255,255,.7)' : 'rgba(160,170,210,.18)'; ctx.lineWidth = on ? 1.4 : 0.8;
    ctx.setLineDash(dashed ? [4, 4] : []); ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); });
  ctx.setLineDash([]);
  NOTES.forEach((n, i) => { if (!visible(n)) return;
    const [x, y] = screen(n), r = radius(n) * Math.sqrt(cam.k), glow = 0.85 + 0.15 * Math.sin(t / 900 + n.phase);
    let alpha = n.superseded ? 0.28 : glow;
    if (!lit(n)) alpha *= 0.15; else if (focus != null && i !== focus && !near.has(i)) alpha *= 0.35;
    ctx.globalAlpha = alpha * 0.25; ctx.fillStyle = color(n.type);
    ctx.beginPath(); ctx.arc(x, y, r * 2.4, 0, 6.29); ctx.fill();
    ctx.globalAlpha = alpha; ctx.beginPath(); ctx.arc(x, y, r, 0, 6.29); ctx.fill();
    if (i === focus || (query && lit(n)) || (n.importance >= 8 && cam.k > 0.6)) {
      ctx.globalAlpha = Math.min(1, alpha + 0.2); ctx.fillStyle = '#e6e6f0'; ctx.font = '12px system-ui';
      ctx.fillText(n.title, x + r + 4, y + 4); }
  });
  ctx.globalAlpha = 1; requestAnimationFrame(draw);
}
requestAnimationFrame(draw);
function at(px, py) { let best = null, bd = 1e9;
  NOTES.forEach((n, i) => { if (!visible(n)) return; const [x, y] = screen(n), d = Math.hypot(x - px, y - py);
    if (d < radius(n) * Math.sqrt(cam.k) + 6 && d < bd) { bd = d; best = i; } }); return best; }
function show(i) { if (i == null) { card.style.display = 'none'; return; } const n = NOTES[i];
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  card.innerHTML = `<h2>${esc(n.title)}</h2><div class="meta">${esc(n.type)} · ${esc(n.date || 'no date')} · importance ${n.importance ?? '?'}`
    + `${n.superseded ? ' · superseded' : ''}</div><div>${esc(n.summary)}</div>`
    + (n.tags.length ? `<div class="meta" style="margin-top:6px">${n.tags.map(esc).join(' · ')}</div>` : '')
    + `<div class="path">${esc(n.path)}</div>`; card.style.display = 'block'; }
let drag = null;
sky.addEventListener('pointerdown', e => { drag = {x: e.clientX, y: e.clientY, cx: cam.x, cy: cam.y, moved: false}; });
addEventListener('pointerup', e => { if (drag && !drag.moved) { pinned = at(e.clientX, e.clientY); show(pinned ?? hover); } drag = null; });
sky.addEventListener('pointermove', e => {
  if (drag) { const dx = e.clientX - drag.x, dy = e.clientY - drag.y; if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true;
    cam.x = drag.cx + dx / cam.k; cam.y = drag.cy + dy / cam.k; return; }
  hover = at(e.clientX, e.clientY); if (pinned == null) show(hover); });
sky.addEventListener('wheel', e => { e.preventDefault(); cam.k = Math.min(4, Math.max(0.2, cam.k * (e.deltaY < 0 ? 1.1 : 0.9))); }, {passive: false});
search.addEventListener('input', () => { query = search.value.trim().toLowerCase(); });
const legend = document.getElementById('legend');
[...new Set(NOTES.map(n => n.type))].sort().forEach(t => { const s = document.createElement('span');
  s.innerHTML = `<i style="background:${color(t)}"></i>${t}`;
  s.onclick = () => { hidden.has(t) ? hidden.delete(t) : hidden.add(t); s.classList.toggle('off'); }; legend.appendChild(s); });
</script></body></html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--title', default='Constellation')
    parser.add_argument('--out', type=Path, help='where to write the page (default: <folder>/constellation.html)')
    parser.add_argument('--archive', action='store_true', help='include archived notes too')
    args = parser.parse_args()
    if not args.folder.is_dir():
        sys.exit(f'{args.folder} is not a folder.')
    everything = notes_lib.load(args.folder)
    kept = [i for i, n in enumerate(everything) if args.archive or not n['archived']]
    new_index = {old: new for new, old in enumerate(kept)}
    data = []
    for old in kept:
        n = everything[old]
        data.append({
            'title': n['title'], 'type': n['type'], 'summary': n['summary'], 'tags': n['tags'],
            'date': n['date'].isoformat() if n['date'] else None, 'importance': n['importance'],
            'superseded': bool(n['superseded_by']), 'path': n['path'],
            'links': [new_index[j] for j in n['links'] if j in new_index],
            'replaced_by': new_index.get(n['replaced_by']),
        })
    page = (PAGE.replace('__TITLE__', html.escape(args.title))
            .replace('__COUNT__', f'{len(data)} notes · size = importance · lines = links · drag, scroll, click')
            .replace('__COLORS__', json.dumps(COLORS))
            .replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/')))
    out = args.out or args.folder / 'constellation.html'
    out.write_text(page, encoding='utf-8')
    print(f'Wrote {out} ({len(data)} stars, {sum(len(d["links"]) for d in data)} links).')


if __name__ == '__main__':
    main()
