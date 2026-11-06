# Archive — the Minecraft era

These files are **no longer part of the Null Universe build**. They are kept
here for the record, not for running.

On 2026-11-06 Sanath asked to remove or replace the Minecraft dependence
and tune the project to run the Null Universe on its own. The replacement
is `../standalone/` — the same world, the same Atlas chat agent, the same
manifestation vocabulary, with zero Minecraft in it.

What used to live here:

- `pumpkin-null-universe/` — the Null Universe hosted inside a Pumpkin
  (Rust Minecraft) server: RCON-driven monoliths (deepslate bricks),
  K_n graphs (sea lanterns + end rods), void anchor (crying obsidian),
  nullify (fill air). Needed a Pumpkin binary and a running server.
- `bedrock-bot/` — Atlas as a Bedrock multiplayer bot (bedrock-protocol):
  joined the live server at `jensen-planting.tun.ply.gg:5650` and answered
  in Minecraft's own chat bar, creating via in-game commands (needed
  `/op Atlas`). Included the in-world chat agent (`chat.js`, 17/17 checks)
  whose command vocabulary lives on in `../standalone/atlas.py`.

Why they were retired: the world depended on a free playit.gg server that
kept going down, on Minecraft binaries, and on UDP that the build machine
blocks — the Null Universe itself never needed any of that. The void is
the game now, not a Minecraft world.
