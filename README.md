# Simple Byte Storage — website

Static site (GitHub Pages) for the [Simple Byte Storage](https://github.com/Karatells/ByteStorage) Minecraft mod.

- `index.html` — landing page (RU/EN switch), hand-written
- `docs/*.html` — documentation, generated from the mod's wiki Markdown
- `assets/` — shared CSS and the mod's textures
- `wiki-src/` — snapshot of `docs/wiki` from the mod repository
- `recipes.py` — draws `docs/Recipes.html` (crafting grids) from the mod's recipe JSON
- `data-src/` — snapshot of the mod's recipe JSON and language files
- `build.py` — regenerates `docs/` (`pip install markdown`)

## Update the docs
```bash
python3 build.py /path/to/ByteStorage   # copies fresh wiki + recipes from the mod repo, rebuilds docs/
```

## Publish
Repository Settings → Pages → Deploy from a branch → `main` / `(root)`.

## Recipe icons
Items from the mod use their real textures. Vanilla items are drawn as labelled colour tiles.
To use real vanilla icons, drop PNGs named after the item id (e.g. `iron_ingot.png`) into `assets/img/mc/` and rebuild; they are picked up automatically.
