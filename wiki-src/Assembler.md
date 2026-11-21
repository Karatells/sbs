# Assembler

Executes crafting-table patterns for the network.

## How it works

1. Insert any **storage cell** into the Assembler as its **buffer**.
2. On an order, the Assembler copies the needed ingredients from the network into the buffer.
3. It crafts, then returns the result (and any leftovers, such as buckets) to the network.

All blocks must be connected to an online controller.

## Speed Cards & Crafting Co-Processors

The Assembler has **4 upgrade slots** for **Speed Cards**, and benefits from **Crafting Co-Processors (`crafting_coprocessor`)** connected anywhere on the network (up to 8 co-processors counted; each co-processor costs 8 FE/t idle):

```
ticks per craft = max(4, 40 / (1 + speed_cards + min(8, coprocessors)))
```

| Speed Cards (0 Co-Processors) | Ticks per craft |
|---|---|
| 0 | 40 |
| 1 | 20 |
| 2 | 13 |
| 3 | 10 |
| 4 | 8 |
| 4 + 5 Co-Processors (or 9 total) | **4 (maximum speed)** |

## Queue

Each Assembler holds up to **9,999** pending crafts. When several Assemblers are available, new crafts are spread by the lowest current load.

## Status messages

When it is waiting, the GUI says why:

- No buffer card
- Not enough resources in the network
- Buffer cell busy or too small
- Network offline
- Network full (cannot return results)

If an order can't be routed, the Pattern Terminal tells you: *no Assembler* or *no memory card in the Assembler*.
