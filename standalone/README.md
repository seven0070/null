# Null Universe — Standalone

The Null Universe, running on its own. **No Minecraft.** No Pumpkin server,
no Bedrock server, no free playit tunnel to keep alive, no `/op`, no UDP.
The world is a web page you open in your browser, and the chat bar inside
it is the communication bar: talk to Atlas, Atlas answers and creates.

## Run it

```bash
python3 server.py        # macOS / Linux
```

or double-click `start.bat` on Windows. Then open **http://localhost:8765**.

That's it. Python 3, standard library only — nothing to install.

## What you get

- **The world** (`static/index.html`): a live top-down view of the void —
  gold diamond = void anchor, grey blocks = monoliths, blue nodes + lines =
  K_n graphs, dashed circles = fields, pulsing white dot = Atlas.
  HUD shows tick, status, entropy, mass, energy, entity counts.
- **The Chronicle**: every manifestation, nullification, pause and birth,
  logged with its tick.
- **The chat bar**: talk to Atlas exactly like you talk to Atlas here.
  Atlas answers in the chat and creates in the void.

## Talking to Atlas

```
atlas help                          — what I can do
atlas status                        — live numbers of the void
atlas anchor                        — set the void anchor at (0, 0, 0)
atlas manifest monolith [w h d]     — raise a monolith (default 3x6x3)
atlas manifest graph 5              — materialize a complete graph K5
atlas manifest field                — raise an entropy-dampening field
atlas materialize <name>            — birth a new native Null Entity
atlas nullify [name]                — cleanse matter back to nothing
atlas pause / atlas resume          — stop and restart time
```

## How it works

| File | What it is |
|---|---|
| `world.py` | The universe engine: genesis T=0 zero state, Null Entity metabolism, manifestation engine (PhysicalConstruct / DiscreteMathGraph / FieldEmitter), nullify, tick + entropy, persistence. A runnable port of `../null-universe/scripts/harness.py` and `src/core`. |
| `atlas.py` | The chat agent. Pure logic, same command vocabulary as the old Minecraft chat bar — re-pointed at this world instead of a Minecraft server. |
| `server.py` | Stdlib-only HTTP server: serves the world page, `GET /api/state`, `POST /api/chat`. Ticks the universe once a second, persists to `universe-state.json` so the void remembers what was manifested. |
| `static/index.html` | The world itself: canvas view + HUD + Chronicle + chat bar. No dependencies, vanilla JS. |

The reference engine in `../null-universe/` (Rust: Bevy ECS + Rapier) is
unchanged — it is the design authority; this standalone runtime is the one
that actually runs anywhere, today.

## What changed (2026-11-06)

The Minecraft dependence was removed. The old Minecraft variants live in
`../archive/minecraft-era/` (Pumpkin-hosted world + Bedrock bot) for the
record — they are no longer part of the build, and nothing in `standalone/`
imports, calls, or needs Minecraft in any form.
