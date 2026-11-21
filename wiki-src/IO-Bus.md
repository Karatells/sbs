# I/O Bus

Moves items between a **neighbouring inventory** and the network automatically.

| Property | Value |
|---|---|
| Base cycle | every 10 ticks (`max(2, 10 - 2 × speed_cards)`) |
| Items per cycle | `64 × (1 + speed_cards)` (64 up to 320) |
| Filter slots | 9 (ghost slots) |
| Upgrade slots | 4 (Speed Cards) |
| Idle drain | 2 FE/t |

## Modes (toggle with the button)

### Import
Pulls items from the neighbouring inventory into the network. Supports an **Allow / Deny** toggle:
- **Allow (Whitelist)**: only listed items are imported (empty filter = imports everything).
- **Deny (Blacklist)**: imports everything *except* the listed items.

### Export
Keeps the listed items stocked in the neighbouring inventory. The **count in a filter slot is the amount to keep**. Left-click sets the stack count, right-click adds 1. The bus tops up from the network when the inventory has less than that.

## Speed Cards & Redstone Control

- **Speed Cards (up to 4)**: each card reduces the cycle interval by 2 ticks (10 → 8 → 6 → 4 → 2 ticks) and adds +64 items per cycle (64 → 128 → 192 → 256 → 320 items/cycle). Cards drop when the block is broken.
- **Redstone control**: click the `RS` button to cycle between **RS: Always**, **RS: High** (active only with a redstone signal), and **RS: Low** (active only without a redstone signal).

## Notes
- The bus works on **every adjacent inventory** (not other network devices).
- Automatically pauses when the network enters **Eco Mode** (Controller energy `< 10%`).
- For fluids, use the [Fluid I/O Bus](Storage#fluid-storage).
- For connecting an external inventory directly as storage without moving items, use the [Storage Bus](Storage#storage-bus).
- For logic that goes beyond filters (thresholds, conditions, auto-crafting), see the [Scripting addon](Scripting-Overview).
