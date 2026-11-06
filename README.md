# Null Universe

A world that starts as nothing — tick 0, 0 mass, 0 energy, 0 entropy,
0 entities, status `PrimordialVoid` — and only becomes something when
you (or Atlas) manifest it into being.

**No Minecraft.** The Null Universe runs on its own now. The old
Minecraft variants are archived under `archive/minecraft-era/` for the
record; nothing in the active build imports, calls, or needs Minecraft.

Source of truth: https://github.com/seven0070/null

## Run it (the game)

```bash
cd standalone
python3 server.py        # then open http://localhost:8765
```

Or double-click `standalone/start.bat` on Windows. Python 3 only,
standard library — nothing to install, no server to start elsewhere,
no account, no `/op`.

What opens is the world itself: a live view of the void, the Chronicle,
and a chat bar at the bottom. Talk to Atlas in the bar — Atlas answers
and creates, the same way you talk to Atlas here:

```
atlas help
atlas status
atlas anchor
atlas manifest monolith [w h d]
atlas manifest graph 5
atlas manifest field
atlas materialize <name>
atlas nullify [name]
atlas pause / atlas resume
```

See `standalone/README.md` for the full tour.

## What's in this repo

| Path | What it is |
|---|---|
| `standalone/` | **The runnable Null Universe.** Python world engine (`world.py`), Atlas chat agent (`atlas.py`), stdlib web server (`server.py`), the world page (`static/index.html`), tests (`test_standalone.py`, 62 checks). |
| `null-universe/` | The reference engine (Rust: Bevy ECS + Rapier 3D physics, JSON-RPC/Unix-socket IPC). The design authority; needs a Rust toolchain to build. The standalone runtime is the runnable port of its genesis state, Null Entity metabolism, and manifestation engine. |
| `archive/minecraft-era/` | Retired 2026-11-06: the Pumpkin-hosted variant and the Bedrock bot. Preserved, not part of the build. |
