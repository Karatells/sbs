# World & Materials

Version **1.3.0** introduces dedicated world generation and crafting materials that anchor Simple Byte Storage's progression: **Bytite Ore** in the Overworld and the **Silicon Rift** features.

## Bytite Ore

| Property | Value |
|---|---|
| Blocks | `bytite_ore` (stone), `deepslate_bytite_ore` (deepslate) |
| Generation | Overworld (`#minecraft:is_overworld`), `Y = -48` to `+48` (trapezoid distribution, peaking around `Y = 0`) |
| Vein size / frequency | Up to 7 blocks per vein, 9 attempts per chunk |
| Mining requirement | Iron Pickaxe or higher (`needs_iron_tool`) |
| Drop | 1× **Raw Bytite (`raw_bytite`)** (affected by Fortune; Silk Touch drops the ore block) |

Smelt **Raw Bytite** (or ore blocks) in a **Furnace** (10 s, 0.7 XP) or **Blast Furnace** (5 s, 0.7 XP) to obtain **Bytite Ingots (`bytite_ingot`)**. Nine ingots craft a decorative **Block of Bytite (`bytite_block`)** and back.

**Bytite Ingots** are the core structural metal of the mod, used in Cables, Drives, Terminals, Controllers, Buses, and Storage Cells.

## Silicon Rift & Surface Resources

The mod defines the **Silicon Rift (`silicon_rift`)** biome and adds its three resource features across Overworld biomes so every world can obtain them:

| World Block | Spawns | Tool / Light | Drop / Product | Used for |
|---|---|---|---|---|
| **Silicate Crust** (`silicate_crust`) | Stone patches (size 18, `Y = 40..90`, 1/4 chunk chance) | Pickaxe | **Silicon Dust** (`silicon_dust`) → crafted into **Logic Wafer** (`logic_wafer`) | Network Controller, Crafting Co-Processor, Speed / Void / Lock / Wireless cards, Scripting blocks |
| **Quantum Quartz Cluster** (`quantum_cluster`) | Surface (`WORLD_SURFACE_WG`, 1/6 chunk chance) | Iron Pickaxe · Light 7 | **Quantum Quartz** (`quantum_quartz`) | High-tier cells (`16k`–`1M`, Fluid `16k`–`64k`), Quantum Relay, Entangled Crystal, Wireless Terminal, Recipe Library |
| **Circuit Bloom** (`circuit_bloom`) | Surface (`WORLD_SURFACE_WG`, 1/8 chunk chance) | Instabreak · Light 9 | **Circuit Bloom** → crafted into 2× **Cyan Phosphor** (`cyan_phosphor`) | Screen-bearing blocks (Terminals, Network Display, Security Terminal, Network Analyzer) |

## Progression Overview

1. **Early game:** Mine **Bytite Ore** (`Y = -48..+48`) with an Iron Pickaxe and smelt **Bytite Ingots**.
2. **First network:** Craft Cables, a Drive, `1k`/`4k` Byte Storage Cells, and a basic Terminal.
3. **Explore for Rift materials:** Gather **Silicate Crust** (Silicon Dust → Logic Wafer), **Quantum Quartz Clusters**, and **Circuit Blooms** (Cyan Phosphor).
4. **Advanced network & autocrafting:** Build high-capacity `16k`–`1M` cells, Fluid Byte Cells, Assemblers, Crafting Co-Processors, Pattern Buses, Wireless Terminals, and Quantum Relays.

See [Recipes](Recipes#world-materials) for all smelting, blasting, and material crafting grids.

## Advancements

Simple Byte Storage includes 5 built-in advancements that guide you through progression:

| Advancement | Requirement |
|---|---|
| **Simple Byte Storage** | Root advancement |
| **First Byte** | Craft a `1k` Byte Storage Cell |
| **Virtual Pool** | Craft a Drive and a Terminal |
| **Factory Online** | Craft an Assembler or a Pattern Bus |
| **One Megabyte** | Craft a `1M` Byte Storage Cell |
