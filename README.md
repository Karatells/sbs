# Simple Byte Storage — website

Static site (GitHub Pages) for the [Simple Byte Storage](https://github.com/Karatells/ByteStorage) Minecraft mod.

- `index.html` — landing page (RU/EN switch), hand-written
- `docs/*.html` — documentation, generated from the mod's wiki Markdown
- `assets/` — shared CSS and the mod's textures
- `wiki-src/` — snapshot of `docs/wiki` from the mod repository
- `build.py` — regenerates `docs/` (`pip install markdown`)

## Update the docs
```bash
python3 build.py /path/to/ByteStorage/docs/wiki   # copies fresh .md files, rebuilds docs/
```

## Publish
Repository Settings → Pages → Deploy from a branch → `main` / `(root)`.
