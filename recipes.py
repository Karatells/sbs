"""Renders docs/Recipes.html with crafting-grid pictures from the mod's recipe JSON files."""
import html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data-src"
IMG = ROOT / "assets" / "img"

# mod item id -> texture file in assets/img (without .png)
TEX = {
    "controller": "controller_front_online",
    "drive": "drive_front",
    "terminal": "terminal_front",
    "crafting_terminal": "crafting_terminal_front",
    "pattern_terminal": "pattern_terminal_front",
    "pattern_encoding_terminal": "pattern_encoding_terminal_front",
    "assembler": "assembler_front",
    "pattern_provider": "pattern_provider",
    "pattern": "pattern_item",
    "security_terminal": "security_terminal_front",
    "network_display": "network_display_front",
}

# vanilla item id -> (css colour, short label); anything else gets a neutral tile
VANILLA = {
    "iron_ingot": ("#c9ced6", "Iron"),
    "iron_nugget": ("#aeb4bd", "Nugget"),
    "iron_bars": ("#949ca8", "Iron Bars"),
    "gold_ingot": ("#f2c94c", "Gold"),
    "redstone": ("#e5383b", "Redstone"),
    "redstone_block": ("#b81d24", "Redstone Blk"),
    "diamond": ("#4fe3d8", "Diamond"),
    "diamond_block": ("#3bc9bd", "Diamond Blk"),
    "emerald": ("#2ecc71", "Emerald"),
    "lapis_lazuli": ("#2563eb", "Lapis"),
    "lime_dye": ("#65d445", "Lime Dye"),
    "glass_pane": ("#a9d6e5", "Glass Pane"),
    "chest": ("#a8742f", "Chest"),
    "piston": ("#b08d57", "Piston"),
    "crafting_table": ("#9c6b3a", "Crafting Table"),
    "hopper": ("#5b5f66", "Hopper"),
    "bucket": ("#b9c2cc", "Bucket"),
    "obsidian": ("#3c2b52", "Obsidian"),
    "ender_pearl": ("#1f8a70", "Ender Pearl"),
    "ender_eye": ("#34d399", "Ender Eye"),
    "quartz": ("#eee8dc", "Quartz"),
    "paper": ("#f4f1e8", "Paper"),
    "book": ("#8a5a3c", "Book"),
    "netherite_ingot": ("#5a4a4f", "Netherite"),
    "nether_star": ("#f7f3c2", "Nether Star"),
    "totem_of_undying": ("#e6c84a", "Totem"),
    "iron_pickaxe": ("#c9ced6", "Iron Pickaxe"),
    "repeater": ("#b9b9b9", "Repeater"),
    "comparator": ("#b9b9b9", "Compar."),
}

GROUPS = [
    ("World & materials", [
        "smelt_raw_bytite", "blast_raw_bytite",
        "smelt_bytite_ore", "blast_bytite_ore",
        "smelt_deepslate_bytite_ore", "blast_deepslate_bytite_ore",
        "bytite_block", "bytite_ingots_from_block",
        "logic_wafer", "cyan_phosphor", "entangled_crystal",
    ]),
    ("Network & power", [
        "controller", "cable", "drive", "storage_bus",
        "energy_port", "capacitor", "quantum_relay",
        "security_terminal", "network_display",
    ]),
    ("Storage cells", [
        "cell_1k", "cell_4k", "cell_16k", "cell_64k", "cell_256k", "cell_1m",
        "fluid_cell_1k", "fluid_cell_4k", "fluid_cell_16k", "fluid_cell_64k",
    ]),
    ("Terminals", [
        "terminal", "crafting_terminal", "pattern_terminal",
        "pattern_encoding_terminal", "wireless_terminal",
    ]),
    ("Autocrafting", [
        "pattern", "assembler", "crafting_coprocessor", "pattern_provider",
    ]),
    ("Buses & utility", [
        "io_bus", "fluid_io_bus", "cell_workbench", "archiver",
        "network_analyzer", "guide_book",
    ]),
    ("Cards & upgrades", [
        "speed_card", "void_card", "lock_card", "recipe_library",
        "auto_transfer_card", "insurance_card", "tool_card", "macro_card",
    ]),
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
    if isinstance(entry, list):
        return ident(entry[0]) if entry else None
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
    rtype = r["type"]
    res = r["result"]
    if isinstance(res, str):
        res_id, res_n = res, 1
    else:
        res_id, res_n = res["item"], res.get("count", 1)

    if rtype.endswith("smelting") or rtype.endswith("blasting"):
        ing = ident(r.get("ingredient"))
        cells = [ing]
        cols = 1
        secs = r.get("cookingtime", 200) / 20
        xp = r.get("experience", 0)
        if rtype.endswith("blasting"):
            kind, tag_cls = "Blasting", "blasting"
            hint = f"Blast Furnace · {secs:g}s · {xp:g} XP"
        else:
            kind, tag_cls = "Smelting", "smelting"
            hint = f"Furnace · {secs:g}s · {xp:g} XP"
        title_suffix = f" ({name_of(ing, lang)})" if ing else ""
    elif rtype.endswith("shaped"):
        rows = r["pattern"]
        cols = max(len(x) for x in rows)
        cells = [ident(r["key"].get(ch)) if ch != " " else None for row in rows for ch in row.ljust(cols)]
        kind, tag_cls, hint = "Shaped", "shaped", "Place exactly as shown"
        title_suffix = ""
    else:
        ings = [ident(i) for i in r["ingredients"]]
        cols = 3 if len(ings) > 3 else max(1, len(ings))
        cells = ings
        while len(cells) % cols:
            cells.append(None)
        kind, tag_cls, hint = "Shapeless", "shapeless", "Any arrangement works"
        title_suffix = ""

    grid = "".join(slot(c, lang) for c in cells)
    counts = {}
    for c in cells:
        if c:
            counts[c] = counts.get(c, 0) + 1
    summary = ", ".join(
        f"{n}× {html.escape(name_of(i, lang))}" if n > 1 else html.escape(name_of(i, lang))
        for i, n in counts.items()
    )
    heading = html.escape(name_of(res_id, lang) + title_suffix)
    return f'''<div class="recipe" id="{rid}">
  <h3>{heading}</h3>
  <div class="rflow">
    <div class="rgrid" style="grid-template-columns:repeat({cols},var(--s))">{grid}</div>
    <span class="rarrow">➜</span>
    {slot(res_id, lang, res_n, big=True)}
  </div>
  <p class="rmeta"><span class="rtag {tag_cls}">{kind}</span> {html.escape(hint)}</p>
  <p class="rsum">{summary}</p>
</div>'''


def render(page_template, sidebar_html, repo):
    recipes, lang = load()
    seen, parts = set(), []
    for title, ids in GROUPS:
        cards = []
        for rid in ids:
            if rid in recipes:
                cards.append(card(rid, recipes[rid], lang))
                seen.add(rid)
        if cards:
            anchor = title.lower().replace(" & ", "-").replace(" ", "-")
            parts.append(f'<h2 id="{anchor}">{html.escape(title)}</h2>\n<div class="rlist">{"".join(cards)}</div>')
    rest = [r for r in recipes if r not in seen]           # recipes added to the mod but not grouped yet
    if rest:
        parts.append('<h2 id="other">Other</h2>\n<div class="rlist">' + "".join(card(r, recipes[r], lang) for r in rest) + "</div>")
    body = f'''<h1>Recipes</h1>
<p>Every crafting, smelting and blasting recipe in Simple Byte Storage (v1.3.0). Hover a slot to see the item name. Items from the mod use their real textures;
items from vanilla Minecraft are shown as labelled tiles.</p>
{"".join(parts)}
<p>All items are also available in the creative tabs <em>Simple Byte Storage</em> and <em>Simple Byte Storage: Scripting</em>.</p>'''
    return page_template.format(
        title="Recipes",
        desc="All crafting, smelting and blasting recipes of Simple Byte Storage, shown as grids.",
        repo=repo,
        sidebar=sidebar_html,
        body=body,
        slug="Recipes",
    )
