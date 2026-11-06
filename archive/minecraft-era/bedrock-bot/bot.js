// Atlas Bedrock bot — joins Sanath's Null Universe world as a multiplayer
// player and talks + creates in-world, like this chat.
//
// The communication bar is Minecraft's own chat bar: the player opens it,
// types to Atlas, Atlas answers in chat — and when asked, manifests things
// into the void (monoliths, K_n graphs, anchors) or nullifies space back
// to nothing. Creation runs through in-game commands, so the bot needs
// operator on the server: /op Atlas
//
// Server: jensen-planting.tun.ply.gg:5650 (Bedrock, Creative)
//   version via MC_VERSION (default 1.26.60 = protocol 2225)
//   host/port/username via MC_HOST / MC_PORT / MC_USERNAME
//   reconnect attempts via MC_RECONNECT_ATTEMPTS (default 3)

const { createClient } = require('bedrock-protocol')
const { createChatAgent } = require('./chat')
const fs = require('fs')
const crypto = require('crypto')

const HOST = process.env.MC_HOST || 'jensen-planting.tun.ply.gg'
const PORT = parseInt(process.env.MC_PORT || '5650', 10)
const VERSION = process.env.MC_VERSION || '1.26.60'
const USERNAME = process.env.MC_USERNAME || 'Atlas'
const RECONNECT_ATTEMPTS = parseInt(process.env.MC_RECONNECT_ATTEMPTS || '3', 10)
const RUN_UUID = crypto.randomUUID()

const LOG = __dirname + '/bot.log'
function log (...args) {
  const line = `[${new Date().toISOString()}] ` + args.map(a => typeof a === 'string' ? a : JSON.stringify(a)).join(' ') + '\n'
  fs.appendFileSync(LOG, line)
  process.stdout.write(line)
}

let attemptsLeft = RECONNECT_ATTEMPTS
let client = null

function startBot () {
  log(`starting ${USERNAME} bot -> ${HOST}:${PORT} (Bedrock ${VERSION}, offline, reconnect attempts left: ${attemptsLeft})`)

  client = createClient({
    host: HOST,
    port: PORT,
    username: USERNAME,
    version: VERSION,
    offline: true,
    skipPing: true, // discovery ping hardcodes raknet-native, which segfaults here
    raknetBackend: 'jsp-raknet',
    useRaknetWorkers: false
  })

  const agent = createChatAgent({
    username: USERNAME,
    sendChat: (text) => {
      client.queue('text', {
        type: 'chat', needs_translation: false, source_name: USERNAME,
        xuid: '', platform_chat_id: '', filtered_message: '', message: text
      })
    },
    runCommand: (cmd) => {
      // CommandRequestPacket — the only guaranteed way to run a server command.
      client.queue('command_request', {
        command: cmd,
        origin: { type: 'player', uuid: RUN_UUID, request_id: '', player_entity_id: 0 },
        internal: false,
        version: '52'
      })
      log('COMMAND', cmd)
    },
    getPosition: () => {
      const p = client.entity?.position || client.position
      return p ? { x: p.x, y: p.y, z: p.z } : null
    }
  })

  client.on('spawn', () => {
    const pos = client.entity?.position || client.position
    log('SPAWNED. entityId=', client.entityId, 'position=', JSON.stringify(pos))
    attemptsLeft = RECONNECT_ATTEMPTS // a good connection resets the budget
    setTimeout(() => agent.greet(), 1500)
  })

  client.on('text', (packet) => {
    if (packet.type === 'chat' || packet.type === 'whisper') {
      log('CHAT', packet.source_name || '', ':', packet.message || '')
    }
    agent.handleText(packet)
    agent.handleSystemText(packet)
  })

  client.on('command_output', (packet) => {
    log('COMMAND_OUTPUT', JSON.stringify(packet).slice(0, 300))
    agent.handleCommandOutput(packet)
  })

  client.on('move_player', (packet) => {
    if (packet.runtime_id === client.entityId) {
      log('POSITION', JSON.stringify(packet.position))
    }
  })

  client.on('play_status', (packet) => log('PLAY_STATUS', packet.status))
  client.on('disconnect', (packet) => log('DISCONNECTED', JSON.stringify(packet)))
  client.on('kick', (packet) => log('KICKED', JSON.stringify(packet)))
  client.on('error', (err) => log('ERROR', err.message))

  client.on('close', () => {
    log('CONNECTION CLOSED')
    if (attemptsLeft > 0) {
      attemptsLeft--
      log(`reconnecting in 5s (${attemptsLeft} attempts left)`)
      setTimeout(startBot, 5000)
    } else {
      log('reconnect budget exhausted, stopping')
      process.exit(0)
    }
  })

  // Heartbeat so the log shows the bot is still alive in-world.
  setInterval(() => {
    const pos = client.entity?.position || client.position
    log('HEARTBEAT position=', JSON.stringify(pos), 'connected=', client.connected)
  }, 60000).unref()
}

startBot()
