# Atlas Bedrock Bot — Null Universe multiplayer

A bot that joins Sanath's Null Universe Bedrock world as a multiplayer player
(`Atlas`) and stays in the world, logging spawn, position, and chat.

Server: `jensen-planting.tun.ply.gg:5650` (Bedrock, Creative)
Default version: `1.26.60` (protocol 2225 — matches the server as of 2026-11-05;
the server's advertised version has already moved once, 1.26.51 → 1.26.62,
so check the live protocol if the bot fails to connect).

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

## Notes

- `offline: true` — no Xbox Live login; the server must allow offline players.
- Uses the pure-JS `jsp-raknet` backend with `skipPing: true`: the library's
  server-discovery ping hardcodes the native `raknet-native` backend, which
  crashes on hosts without a working native build.
- Logs go to `bot.log` (plus a heartbeat line every 60 s with the bot's position).
- `bot.js` currently only joins, stands, and watches. Tell Atlas what it
  should do in-world (follow, build, chat, run the pumpkin_agent routines)
  and it will be added here.
