# Pattern Bus

Runs **processing** patterns: crafts that happen in a machine such as a furnace, smoker, or any mod machine that exposes an item handler.

## Setup

1. Place the Pattern Bus **touching the machine** and connect it to the network.
2. Put encoded **processing** patterns (made in the [Encoding Terminal](Autocrafting#pattern-encoding-terminal)) into its **9 slots**, or record one with [Learning Mode](Autocrafting#learning-mode-pattern-bus).
3. Order the craft from the [Pattern Terminal](Autocrafting#pattern-terminal) or any Terminal.

## What it does

For each craft the bus takes the inputs from the network, pushes them into the adjacent machine, and later extracts the expected outputs from **any side** of the machine and sends them to the network.

### Blocking Mode
Toggle **Block: ON / OFF** in the Pattern Bus GUI. When enabled, the bus will **not** push the next craft's ingredients while the adjacent machine still contains non-output items — essential for machines that mix recipes if multiple sets of ingredients are inserted at once.

### Powering the machine
The bus also **charges** adjacent machines that have an energy buffer (electric furnace, crusher, ...) with the network's energy (up to 1,000 FE/t, only as much as the machine accepts). The network always keeps a reserve for its own consumption, so machines cannot black it out. To power a machine that has no Pattern Bus next to it, use the [Energy Interface](Network-and-Power#energy-interface).

### Stuck detection
If a Pattern Bus waits for ingredients for more than **30 seconds**, or finds no adjacent machine willing to accept inputs for more than **60 seconds**, it logs a **Stuck** entry in the Controller's Journal, sends a chat warning to Wireless Terminal holders, and triggers `onAlert(e)` in scripts.

| Property | Value |
|---|---|
| Pattern slots | 9 |
| Cycle | every 10 ticks |
| Pushes per cycle | 16 |
| Jobs in flight | up to 256 (in practice limited by what the machine accepts) |
| Queue size | 1,024 crafts |

If several buses hold the same pattern, orders are balanced to the one with the least pending crafts.

## Tips

- The machine must expose an item handler (inventory capability) on the face that touches the bus.
- **Mind the face.** Many machines expose different slots on different faces. A vanilla furnace takes input from the **top**, outputs from the bottom, and accepts only fuel from the sides, so put the Pattern Bus on top of a furnace.
- Make sure the machine is able to receive all inputs; a full machine slows the queue.
- The queue and its state are visible in the bus's GUI and in the Pattern Terminal's Queue tab.
