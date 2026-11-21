# Simple Byte Storage

**Simple Byte Storage** is a storage and autocrafting mod for **Minecraft 1.20.1 (Forge 47.2+)**.

Its core idea is simple: **1 item = 1 byte**. There is no limit on the number of *different* item types in your network, only on the total number of items (bytes) your storage cells can hold. The same rule extends to fluids (**1,000 mB = 1 byte**, unlimited fluid types).

An optional addon, **Simple Byte Storage: Scripting**, adds a Logic Bus and a Logic Terminal with a full JavaScript code editor to automate inventories, autocrafting, redstone, persistent storage, and Network Displays.

## Contents

**Getting started**
- [Downloads](Downloads) — releases, requirements, installation, version history
- [Getting Started](Getting-Started) — your first network in five minutes
- [World & Materials](Worldgen) — Bytite Ore, Silicon Rift resources, progression, advancements
- [Recipes](Recipes) — every crafting, smelting, and blasting recipe

**Core mod**
- [Network and Power](Network-and-Power) — controller, cables, Energy Interface, Capacitor, Eco Mode, Quantum Relay, Security Terminal, Network Analyzer, Network Display
- [Storage](Storage) — drives, 1k–1M cells, Fluid Byte Cells, Cell Workbench, Void/Lock cards, Storage Bus, Byte Archiver
- [Terminals](Terminals) — Terminal, Crafting Terminal, search syntax, saved searches, tooltips, Max button
- [Network Controller GUI](Network-Controller) — 7 tabs (Overview, Storage, Crafting, Recipes, Stock, Journal, Graphs)
- [Wireless Terminal](Wireless-Terminal) — binding, charging, Auto-Transfer, Insurance, Tool, Macro cards
- [Autocrafting](Autocrafting) — patterns, encoding, ordering, sub-craft tree, resource reservation, Crafting Co-Processor
- [Assembler](Assembler) — crafting-table patterns, Speed Cards, Crafting Co-Processors
- [Pattern Bus](Pattern-Bus) — machine crafts, learning mode, Blocking Mode, stuck detection
- [I/O Bus](IO-Bus) — item import/export, Speed Cards, Allow/Deny filter, redstone control
- [JEI Integration](JEI-Integration)
- [Guide Book](Guide-Book) — the in-game manual

**Scripting addon**
- [Scripting Overview](Scripting-Overview) — Logic Bus, Logic Terminal, code editor, identifiers
- [Scripting API](Scripting-API) — `net`, `stock`, `recipes`, `journal`, `store`, `redstone`, `display`, events
- [Scripting Examples](Scripting-Examples)
- [Scripting Administration](Scripting-Administration) — config, security model, limits

**Other**
- [Troubleshooting](Troubleshooting)
- [Building from Source](Building-from-Source)

## Quick facts

| | |
|---|---|
| Current version | **1.3.0** |
| Minecraft / Loader | 1.20.1 / Forge 47.2.0+ |
| Mod id | `simple_bytestorage` |
| Addon mod id | `simple_bytestorage_scripting` (optional) |
| Storage model | 1 item = 1 byte (1,000 mB = 1 byte for fluids), unlimited types |
| Languages | English, Russian, Ukrainian |
| Optional integrations | JEI |
