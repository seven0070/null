# Atlas Bedrock Bot — Null Universe multiplayer

A bot that joins Sanath's Null Universe Bedrock world as a multiplayer player
(`Atlas`) and stays in the world, logging spawn, position, and chat.

Server: `jensen-planting.tun.ply.gg:5650` (Bedrock, Creative)
Default version: `1.26.60` (protocol 2225 — matches the server as of 2026-11-05;
the server's advertised version has already moved once, 1.26.51 → 1.26.62,
so check the live protocol if the bot fails to connect).

## Talking to Atlas in-world — the communication bar

The communication bar is Minecraft's own chat bar. Open it (tap the chat
button / press T), type to Atlas, and Atlas answers in chat — and when asked,
creates things in the void, just like talking to Atlas here.

When Atlas spawns in, it greets the world and tells everyone how to reach it.
Try:

```
atlas help                    — what Atlas can do
atlas status                  — where Atlas is, and the state of the void
atlas anchor                  — set the void anchor (crying obsidian) beneath Atlas
atlas manifest monolith       — raise a 3x6x3 deepslate monolith
atlas manifest graph 5        — materialize a K5 graph: 5 sea lanterns, 10 end-rod edges
atlas nullify                 — cleanse the space around Atlas back to air
atlas come here               — teleport Atlas to you, then it builds where you stand
```

Creation runs through in-game commands, so Atlas needs operator on the
server: `/op Atlas`. If a creation fails, Atlas says so in chat instead of
pretending it worked.

Plain chat works too: say hi and Atlas answers; anything it doesn't
understand gets pointed at `atlas help`. It never answers its own messages.

## Run

Needs Node 20+ on a machine with normal internet (outbound UDP must work —
this bot cannot run on the Muse VM, which blocks all outbound UDP).

```bash
npm install
node bot.js
```

## Configure

```bash
MC_HOST=jensen-planting.tun.ply.gg MC_PORT=5650 MC_VERSION=1.26.60 MC_USERNAME=Atlas node bot.js
```

`MC_RECONNECT_ATTEMPTS` (default 3) bounds reconnects after a drop; a good
connection resets the budget.

## Files

- `bot.js` — connects, spawns, wires chat + commands to the world
- `chat.js` — the chat agent: understands messages, answers, and builds the
  manifestation commands (no Minecraft connection needed to test it)
- `test-chat.js` — offline tests for the chat agent: `node test-chat.js`
  (17 checks: help, status, monolith, K5 graph, anchor, nullify, teleport,
  greetings, op-failure hint, and real packet serialization of every
  command the agent produces)

## Notes

- `offline: true` — no Xbox Live login; the server must allow offline players.
- Uses the pure-JS `jsp-raknet` backend with `skipPing: true`: the library's
  server-discovery ping hardcodes the native `raknet-native` backend, which
  crashes on hosts without a working native build.
- Logs go to `bot.log` (plus a heartbeat line every 60 s with the bot's position).
- The manifestation vocabulary mirrors the sim's own blueprints
  (`PhysicalConstruct`, `DiscreteMathGraph`) and the Pumpkin agent's
  routines (anchor, monolith, K_n graph, nullify).
