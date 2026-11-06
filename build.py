#!/usr/bin/env python3
"""Build the documentation pages (docs/*.html) from the Markdown wiki in wiki-src/.

Usage:
    python3 build.py                          # uses ./wiki-src and ./data-src
    python3 build.py /path/to/ByteStorage     # refresh wiki + recipes from the mod repo first

Needs the `markdown` package (pip install markdown). The landing page (index.html)
is hand-written and is not touched by this script.
"""
import html, re, shutil, sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "wiki-src"
OUT = ROOT / "docs"
REPO = "https://github.com/Karatells/ByteStorage"

sys.path.insert(0, str(ROOT))
import recipes  # noqa: E402  (local module; path added explicitly so `python3 -I` works)

if len(sys.argv) > 1:
    arg = Path(sys.argv[1])
    wiki = arg / "docs" / "wiki" if (arg / "docs" / "wiki").is_dir() else arg   # mod repo root or wiki dir
    for f in wiki.glob("*.md"):
        shutil.copy(f, SRC / f.name)
    if wiki != arg:                                                            # refresh recipe data from the mod repo
        pairs = [(arg / "src/main/resources/data/simple_bytestorage/recipes", ROOT / "data-src/recipes"),
                 (arg / "scripting/src/main/resources/data/simple_bytestorage_scripting/recipes", ROOT / "data-src/recipes-scripting")]
        for src, dst in pairs:
            if src.is_dir():
                shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst)
        for src, dst in [(arg / "src/main/resources/assets/simple_bytestorage/lang/en_us.json", "en_us.json"),
                         (arg / "scripting/src/main/resources/assets/simple_bytestorage_scripting/lang/en_us.json", "scripting_en_us.json")]:
            if src.is_file():
                shutil.copy(src, ROOT / "data-src/lang" / dst)

# ---- sidebar from the wiki's own _Sidebar.md -------------------------------
groups, cur = [], None
for line in (SRC / "_Sidebar.md").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    m = re.fullmatch(r"\*\*\[(.+?)\]\((.+?)\)\*\*", line)          # **[Home](Home)**
    if m:
        groups.append((None, [(m.group(1), m.group(2))]))
        continue
    m = re.fullmatch(r"\*\*(.+?)\*\*", line)                        # **Group**
    if m:
        cur = (m.group(1), [])
        groups.append(cur)
        continue
    m = re.fullmatch(r"- \[(.+?)\]\((.+?)\)", line)                 # - [Title](Slug)
    if m and cur:
        cur[1].append((m.group(1), m.group(2)))

slugs = {p.stem for p in SRC.glob("*.md") if not p.stem.startswith("_")}
titles = {s: t for _, items in groups for t, s in items}

PAGE = """<!doctype html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Simple Byte Storage</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="../assets/favicon.png">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="../index.html"><img class="brandlogo" src="../assets/logo-256.png" alt="" width="32" height="32"> Simple Byte Storage</a>
    <nav class="links">
      <a href="../index.html">Home</a>
      <a href="Home.html">Documentation</a>
      <a href="{repo}/releases/latest">Download</a>
      <a href="{repo}">GitHub</a>
    </nav>
  </div>
</header>
<div class="wrap doc">
  <aside class="side" id="side">{sidebar}</aside>
  <main class="prose">
    <button class="lang menu-btn" id="menuBtn">☰ Pages</button>
    {body}
    <hr>
    <p class="docnote">Found a mistake? This page is generated from
    <a href="{repo}/blob/main/docs/wiki/{slug}.md">docs/wiki/{slug}.md</a> in the mod repository.</p>
  </main>
</div>
<footer><div class="wrap"><div>Simple Byte Storage · MIT · <a href="{repo}">github.com/Karatells/ByteStorage</a></div>
<div>Not an official Minecraft product. Not approved by or associated with Mojang or Microsoft.</div></div></footer>
<script src="../assets/vendor/highlight.min.js" defer></script>
<script>
document.getElementById('menuBtn').addEventListener('click',function(){{document.getElementById('side').classList.toggle('open')}});
</script>
</body>
</html>
"""

def sidebar(current):
    out = []
    for name, items in groups:
        if name:
            out.append(f"<h4>{html.escape(name)}</h4>")
        for title, slug in items:
            cls = ' class="cur"' if slug == current else ""
            out.append(f'<a{cls} href="{slug}.html">{html.escape(title)}</a>')
    return "\n".join(out)

def fix_links(body):
    def sub(m):
        slug, frag = m.group(1), m.group(2) or ""
        return f'href="{slug}.html{frag}"' if slug in slugs else m.group(0)
    return re.sub(r'href="([A-Za-z0-9_-]+)(#[^"]*)?"', sub, body)

OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.html"):
    old.unlink()

for slug in sorted(slugs):
    if slug == "Recipes":        # generated from the mod's recipe JSON, with crafting-grid pictures
        (OUT / "Recipes.html").write_text(recipes.render(PAGE, sidebar(slug), REPO), encoding="utf-8")
        continue
    text = (SRC / f"{slug}.md").read_text(encoding="utf-8")
    # GitHub accepts 2-3 space nested lists; Python-Markdown needs 4
    src = re.sub(r"^( {2,3})(?=([-*]|\d+\.) )", "    ", text, flags=re.M)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"],
                           extension_configs={"toc": {"permalink": "#", "permalink_class": "anchor"}})
    body = fix_links(md.convert(src))
    first = re.search(r"^# (.+)$", text, re.M)
    title = first.group(1).strip() if first else titles.get(slug, slug)
    para = re.search(r"^(?!#|\||-|\*|\d|```|\s*$)(.+)$", text, re.M)
    desc = re.sub(r"[*`\[\]]", "", para.group(1))[:160] if para else title
    (OUT / f"{slug}.html").write_text(
        PAGE.format(title=html.escape(title), desc=html.escape(desc, quote=True), repo=REPO,
                    sidebar=sidebar(slug), body=body, slug=slug),
        encoding="utf-8")
print(f"built {len(slugs)} pages into {OUT}")
