# Storage

## Drive

A **Drive** holds up to **10 storage cells** (both item Byte Storage Cells and Fluid Byte Cells). The contents of all item cells in all drives are merged into one virtual item pool for the whole network.

### Drive settings

- **Priority** — when inserting, higher-priority drives are filled first (and extraction drains lower-priority drives first). Hold Shift while changing it to step by ±10.
- **Whitelist** (9 filter slots) — only items in the list are accepted. **Empty = accepts everything.**
- **Upgrade slot** (1 slot) — accepts a **Void Overflow Card** or a **Lock Card** (see below).

Combine priority and whitelist to sort items into dedicated drives (for example, a whitelisted drive for ores with a high priority).

## Byte Storage Cells

| Cell | Capacity (bytes = items) | Crystal colour | Idle drain |
|---|---|---|---|
| `1k` | 1,024 | Green | 1 FE/t |
| `4k` | 4,096 | Blue | 2 FE/t |
| `16k` | 16,384 | Purple | 3 FE/t |
| `64k` | 65,536 | Orange | 4 FE/t |
| `256k` | 262,144 | Cyan | 6 FE/t |
| `1M` | 1,048,576 | Red | 8 FE/t |

**1 item = 1 byte**, regardless of the item type or stack size. A stack of 64 cobblestone costs 64 bytes, and so does 64 different single items.

Cell upgrades are crafted by combining the lower tier with extra materials — see [Recipes](Recipes#storage-cells).

## Cells as Assembler buffers

Any item Byte Storage Cell can also be used as the buffer of an [Assembler](Assembler).

## Cell Workbench & Drive Upgrade Cards

- **Cell Workbench (`cell_workbench`)**: insert a Byte Storage Cell and configure up to **9 filter slots** in **Allow** (whitelist) or **Deny** (blacklist) mode, plus a **Clear** button. The filter is written directly into the cell's NBT (`CellFilter` / `CellBlacklist`), so it travels with the cell across drives.
- **Void Overflow Card (`void_card`)**: insert into a Drive's upgrade slot; when the drive is full, excess incoming items matching its filter are destroyed instead of backing up farms or buses.
- **Lock Card (`lock_card`)**: insert into a Drive's upgrade slot to make the drive **read-only** (allows extraction, blocks new insertions — handy before migrating or retiring a drive).

## Storage Bus

The **Storage Bus (`storage_bus`)** connects adjacent external inventories (chests, barrels, mod drawers) directly to the virtual network pool without copying their contents into storage cells.
- Supports **Priority** (`-999` to `+999`, Shift = ±10).
- Supports a **9-slot filter** in **Allow** (whitelist) or **Deny** (blacklist) mode (empty = all items).
- Costs **2 FE/t** idle energy.

## Byte Archiver & Data Blobs

The **Byte Archiver (`archiver`)** automatically compresses large bulk stacks in your network to save bytes:
- Every second, if any stackable, non-NBT item (`maxStackSize >= 16`) exceeds **4,096** items in stock (at least `4,096 + 64`), the Archiver compresses **64 items into 1 Data Blob (`data_blob`)** — a **64:1** byte reduction.
- Each compression costs **160 FE** from the Controller.
- Idle drain is **10 FE/t** while active (1 FE/t when paused in its GUI). Pauses automatically in **Eco Mode (`<10%`)**.
- Right-click a **Data Blob** in your hand to unpack it back into 64 items.

## Fluid Storage

Simple Byte Storage extends its type-unlimited model to fluids: **1,000 mB = 1 byte**, with **no limit on fluid types**.

| Fluid Cell | Capacity (mB) | Equivalent bytes |
|---|---|---|
| `1k` Fluid Byte Cell | 1,024,000 mB | 1,024 |
| `4k` Fluid Byte Cell | 4,096,000 mB | 4,096 |
| `16k` Fluid Byte Cell | 16,384,000 mB | 16,384 |
| `64k` Fluid Byte Cell | 65,536,000 mB | 65,536 |

- Insert Fluid Byte Cells directly into any **Drive**.
- Use a **Fluid I/O Bus (`fluid_io_bus`)** next to tanks, pipes, or fluid machines to **Import** or **Export** up to **1,000 mB every 10 ticks** (2 FE/t idle; pauses in Eco Mode).
