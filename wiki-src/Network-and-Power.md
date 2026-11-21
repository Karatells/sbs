# Network and Power

## Network Controller

The controller coordinates the network and supplies its power.

| Property | Value |
|---|---|
| Energy buffer | 100,000 FE |
| Max receive | 2,000 FE/t |
| Own consumption | 10 FE/t |

### Grid states

| State | Meaning |
|---|---|
| `ONLINE` | Network active, power stable. The controller face shows a bright cyan core. |
| `OFFLINE` | Not enough power. Devices stop working. |
| `CONFLICT` | More than one controller in the same connected network. Remove one. |

## Idle energy consumption

Every device draws a small amount of FE per tick from the network.

| Device | FE/t |
|---|---|
| Network Controller | 10 |
| Terminal | 2 |
| Crafting Terminal | 3 |
| Pattern Terminal | 1 |
| Pattern Encoding Terminal | 2 |
| Assembler | 3 |
| Crafting Co-Processor | 8 |
| Pattern Bus | 2 |
| I/O Bus | 2 |
| Fluid I/O Bus | 2 |
| Storage Bus | 2 |
| Drive | 2 + per-cell cost (`1k`: 1, `4k`: 2, `16k`: 3, `64k`: 4, `256k`: 6, `1M`: 8) |
| Energy Interface | 1 |
| Capacitor | 1 |
| Byte Archiver | 10 while active, 1 when paused (+160 FE per 64:1 compression) |
| Quantum Relay | 50 while linked, 5 when unlinked |
| Security Terminal | 4 |
| Network Display | 2 |
| Cable | 0 |
| Logic Bus *(addon)* | 4 while running, 1 otherwise |
| Logic Terminal *(addon)* | 2 |

## Cable

Cables carry the network over distance and cost no energy. Crafting 1 recipe gives 4 cables. Devices that touch each other connect without a cable.

## Re-scan timing

The network uses event-driven topology updates (`topologyDirty`) with a background safety scan every **100 ticks** (5 seconds). The scan only traverses loaded chunks so it never force-loads distant areas.

## Energy Interface
A network block with no GUI. Connect it to the network with cables and place it **next to a machine with an energy buffer**; every few ticks it charges the neighbouring machines with energy from the Controller's buffer (up to 1,000 FE/t per interface, only what the machine accepts). Network blocks next to it are not charged. It costs 1 FE/t of idle energy. The Controller always keeps a reserve (about 40 ticks of the network's own consumption, at least 500 FE) so that powering machines cannot turn the network offline. The Pattern Bus charges its own adjacent machines the same way.

## Capacitor
A network block that stores up to **500,000 FE** as a reserve for the network. Connect it with cables, like any network block. Every 5 ticks it works with the Controller's buffer:
- when the Controller is **below 50%** full, the Capacitor tops it up to 60% (up to 4,000 FE/t);
- when the Controller is **above 90%** full, the Capacitor takes the surplus down to 85%, so incoming energy is not wasted.

It also accepts energy directly from generators placed next to it (up to 2,000 FE/t) but never gives energy to anything except the Controller. Right-click it to see how much it holds. The stored energy is saved with the block. It costs 1 FE/t of idle energy. Several Capacitors work independently and add up.

## Eco Mode
When the Controller's energy buffer drops **below 10%** (10,000 FE), the network enters **Eco Mode**: **I/O Buses**, **Fluid I/O Buses**, and **Byte Archivers** pause automatically while Terminals remain usable so you can still access your items and restore power.

## Quantum Relay & Entangled Crystal
Connect remote bases or different dimensions (Overworld, Nether, End) into a single network without laying cables:
1. Hold **2 or more Entangled Crystals (`entangled_crystal`)** and **Shift + Right-Click** to pair them with a shared Link ID (UUID).
2. Place **Quantum Relays (`quantum_relay`)** at each location and insert one paired crystal into each relay's GUI.
3. Linked relays bridge both segments as one unified network during topology scans (50 FE/t idle per linked relay, 5 FE/t when unlinked). Both relay chunks must be loaded.

## Security Terminal
Place a **Security Terminal (`security_terminal`)** anywhere on your network to protect terminal access on multiplayer servers:
- The player who places the block is recorded as the **Owner** (server operators with permission level 2+ also retain access).
- Open its GUI to toggle between **Access: Locked** (owner & operators only) and **Access: Public**.
- Costs 4 FE/t idle energy.

## Network Analyzer
The **Network Analyzer (`network_analyzer`)** is a handheld diagnostic tool. Right-click any network block to print a live summary in chat:
- Grid state (`ONLINE` / `OFFLINE` / `CONFLICT`)
- Total connected nodes
- Clicked node's idle drain and total network drain (FE/t)
- Stored / max energy (FE)
- Used / total storage capacity (bytes)

## Network Display
The **Network Display (`network_display`)** is a network monitor block with **6 text lines** (up to 128 characters per line) controlled by scripts via `display.set(line, text)` and `display.clear()`. Right-click it to view the lines in a clean GUI. Costs 2 FE/t idle energy.
