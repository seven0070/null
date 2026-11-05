// Atlas Bedrock bot — joins Sanath's Null Universe world.
// Server: jensen-planting.tun.ply.gg:5650 (Bedrock 1.26.51, protocol 2193, Creative)
const { createClient } = require('bedrock-protocol')
const fs = require('fs')

const LOG = __dirname + '/bot.log'
function log (...args) {
  const line = `[${new Date().toISOString()}] ` + args.map(a => typeof a === 'string' ? a : JSON.stringify(a)).join(' ') + '\n'
  fs.appendFileSync(LOG, line)
  process.stdout.write(line)
}

const HOST = process.env.MC_HOST || 'jensen-planting.tun.ply.gg'
const PORT = parseInt(process.env.MC_PORT || '5650', 10)
const VERSION = process.env.MC_VERSION || '1.26.60' // server protocol 2225
const USERNAME = process.env.MC_USERNAME || 'Atlas'

log(`starting ${USERNAME} bot -> ${HOST}:${PORT} (Bedrock ${VERSION}, offline)`)

const client = createClient({
  host: HOST,
  port: PORT,
  username: USERNAME,
  version: VERSION, // server now reports 1.26.62 / protocol 2225 = minecraft-data 1.26.60
  offline: true,
  skipPing: true, // discovery ping hardcodes raknet-native, which segfaults here; version is known
  raknetBackend: 'jsp-raknet',
  useRaknetWorkers: false
})

client.on('spawn', () => {
  log('SPAWNED. entityId=', client.entityId, 'position=', JSON.stringify(client.entity?.position || client.position))
})

client.on('text', (packet) => {
  log('CHAT', packet.type, packet.source_name || '', ':', packet.message || '')
})

client.on('move_player', (packet) => {
  if (packet.runtime_id === client.entityId) {
    log('POSITION', JSON.stringify(packet.position), 'yaw=', packet.yaw, 'pitch=', packet.pitch)
  }
})

client.on('play_status', (packet) => log('PLAY_STATUS', packet.status))
client.on('disconnect', (packet) => log('DISCONNECTED', JSON.stringify(packet)))
client.on('kick', (packet) => log('KICKED', JSON.stringify(packet)))
client.on('error', (err) => log('ERROR', err.message))
client.on('close', () => { log('CONNECTION CLOSED'); process.exit(0) })

// keep-alive heartbeat in the log so we know it is still alive
setInterval(() => {
  const pos = client.entity?.position || client.position
  log('HEARTBEAT position=', JSON.stringify(pos), 'connected=', client.connected)
}, 60000)
