"""Renders docs/Recipes.html with crafting-grid pictures from the mod's recipe JSON files."""
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data-src"
IMG = ROOT / "assets" / "img"

# mod item id -> texture file in assets/img (without .png)
TEX = {
    "controller": "controller_front_online", "drive": "drive_front", "terminal": "terminal_front",
    "crafting_terminal": "crafting_terminal_front", "pattern_terminal": "pattern_terminal_front",
    "pattern_encoding_terminal": "pattern_encoding_terminal_front", "assembler": "assembler_front",
    "pattern_provider": "pattern_provider", "pattern": "pattern_item",
}
# vanilla item id -> (css colour, short label); anything else gets a neutral tile
VANILLA = {
    "iron_ingot": ("#c9ced6", "Iron"), "iron_nugget": ("#aeb4bd", "Nugget"), "gold_ingot": ("#f2c94c", "Gold"),
    "redstone": ("#e5383b", "Redstone"), "diamond": ("#4fe3d8", "Diamond"), "diamond_block": ("#3bc9bd", "Diamond Blk"),
    "emerald": ("#2ecc71", "Emerald"), "glass_pane": ("#a9d6e5", "Glass Pane"), "chest": ("#a8742f", "Chest"),
    "piston": ("#b08d57", "Piston"), "crafting_table": ("#9c6b3a", "Crafting Table"), "hopper": ("#5b5f66", "Hopper"),
    "ender_pearl": ("#1f8a70", "Ender Pearl"), "quartz": ("#eee8dc", "Quartz"), "paper": ("#f4f1e8", "Paper"),
    "book": ("#8a5a3c", "Book"), "netherite_ingot": ("#5a4a4f", "Netherite"), "nether_star": ("#f7f3c2", "Nether Star"),
    "totem_of_undying": ("#e6c84a", "Totem"), "iron_pickaxe": ("#c9ced6", "Iron Pickaxe"),
    "repeater": ("#b9b9b9", "Repeater"), "comparator": ("#b9b9b9", "Compar."),
}
GROUPS = [
    ("Network", ["controller", "cable", "drive", "energy_port"]),
    ("Storage cells", ["cell_1k", "cell_4k", "cell_16k", "cell_64k"]),
    ("Terminals", ["terminal", "crafting_terminal", "pattern_terminal", "pattern_encoding_terminal", "wireless_terminal"]),
    ("Cards and upgrades", ["speed_card", "recipe_library", "auto_transfer_card", "insurance_card", "tool_card", "macro_card"]),
    ("Autocrafting", ["pattern", "assembler", "pattern_provider"]),
    ("Utility", ["io_bus", "guide_book"]),
    ("Scripting addon", ["logic_bus", "logic_terminal"]),
]

def load():
    recipes, lang = {}, {}
    for folder in ("recipes", "recipes-scripting"):
        for f in sorted((DATA / folder).glob("*.json")):
            r = json.loads(f.read_text(encoding="utf-8"))
            recipes[f.stem] = r
    for name in ("en_us.json", "scripting_en_us.json"):
        lang.update(json.loads((DATA / "lang" / name).read_text(encoding="utf-8")))
    return recipes, lang

def pretty(item_id):
    return item_id.split(":")[1].replace("_", " ").title()

def ident(entry):
    """JSON ingredient/result -> namespaced id (None for an empty slot)."""
    if not entry:
        return None
    return entry.get("item") or ("#" + entry["tag"])

def name_of(item_id, lang):
    ns, path = item_id.split(":", 1)
    for kind in ("item", "block"):
        v = lang.get(f"{kind}.{ns}.{path}")
        if v:
            return v
    return pretty(item_id)

def slot(item_id, lang, count=1, big=False):
    cls = "slot big" if big else "slot"
    if item_id is None:
        return f'<span class="{cls} empty"></span>'
    ns, path = item_id.split(":", 1)
    title = html.escape(name_of(item_id, lang))
    badge = f'<b class="cnt">{count}</b>' if count > 1 else ""
    if ns.startswith("simple_bytestorage"):
        tex = TEX.get(path, path)
        if (IMG / f"{tex}.png").exists():
            return f'<span class="{cls}" title="{title}"><img class="px" src="../assets/img/{tex}.png" alt="{title}">{badge}</span>'
    mc = IMG / "mc" / f"{path}.png"          # optional drop-in vanilla icon
    if ns == "minecraft" and mc.exists():
        return f'<span class="{cls}" title="{title}"><img class="px" src="../assets/img/mc/{path}.png" alt="{title}">{badge}</span>'
    color, label = VANILLA.get(path, ("#8b98a9", pretty(item_id)))
    return (f'<span class="{cls} van" title="{title}"><i style="background:{color}"></i>'
            f'<em>{html.escape(label)}</em>{badge}</span>')

def card(rid, r, lang):
    res = r["result"]
    res_id, res_n = res["item"], res.get("count", 1)
    if r["type"].endswith("shaped"):
        rows = r["pattern"]
        cols = max(len(x) for x in rows)
        cells = [ident(r["key"].get(ch)) if ch != " " else None for row in rows for ch in row.ljust(cols)]
        kind, hint = "Shaped", "Place exactly as shown"
    else:
        ings = [ident(i) for i in r["ingredients"]]
        cols = 3 if len(ings) > 3 else len(ings)
        cells = ings
        while len(cells) % cols:
            cells.append(None)
        kind, hint = "Shapeless", "Any arrangement works"
    grid = "".join(slot(c, lang) for c in cells)
    # ingredient summary (text, for accessibility and quick reading)
    counts = {}
    for c in cells:
        if c:
            counts[c] = counts.get(c, 0) + 1
    summary = ", ".join(f"{n}× {html.escape(name_of(i, lang))}" if n > 1 else html.escape(name_of(i, lang))
                        for i, n in counts.items())
    return f'''<div class="recipe" id="{rid}">
  <h3>{html.escape(name_of(res_id, lang))}</h3>
  <div class="rflow">
    <div class="rgrid" style="grid-template-columns:repeat({cols},var(--s))">{grid}</div>
    <span class="rarrow">➜</span>
    {slot(res_id, lang, res_n, big=True)}
  </div>
  <p class="rmeta"><span class="rtag {kind.lower()}">{kind}</span> {hint}</p>
  <p class="rsum">{summary}</p>
</div>'''

def render(page_template, sidebar_html, repo):
    recipes, lang = load()
    seen, parts = set(), []
    for title, ids in GROUPS:
        cards = []
        for rid in ids:
            if rid in recipes:
                cards.append(card(rid, recipes[rid], lang)); seen.add(rid)
        if cards:
            parts.append(f'<h2 id="{title.lower().replace(" ", "-")}">{html.escape(title)}</h2>\n<div class="rlist">{"".join(cards)}</div>')
    rest = [r for r in recipes if r not in seen]           # recipes added to the mod but not grouped yet
    if rest:
        parts.append('<h2 id="other">Other</h2>\n<div class="rlist">' + "".join(card(r, recipes[r], lang) for r in rest) + "</div>")
    body = f'''<h1>Recipes</h1>
<p>Every crafting recipe in Simple Byte Storage. Hover a slot to see the item name. Items from the mod use their real textures;
items from vanilla Minecraft are shown as labelled tiles.</p>
{"".join(parts)}
<p>All items are also available in the creative tabs <em>Simple Byte Storage</em> and <em>Simple Byte Storage: Scripting</em>.</p>'''
    return page_template.format(title="Recipes", desc="All crafting recipes of Simple Byte Storage, shown as crafting grids.",
                                repo=repo, sidebar=sidebar_html, body=body, slug="Recipes")
