// Offline test for the chat agent — no server needed.
// Feeds fake chat packets into chat.js and checks the replies/commands.
const { createChatAgent } = require('./chat')

let passed = 0
let failed = 0
function check (name, cond, extra) {
  if (cond) { passed++; console.log('PASS', name) }
  else { failed++; console.log('FAIL', name, extra || '') }
}

function makeAgent (position) {
  const chats = []
  const commands = []
  const agent = createChatAgent({
    username: 'Atlas',
    sendChat: (t) => chats.push(t),
    runCommand: (c) => commands.push(c),
    getPosition: () => position || { x: 10.4, y: 64, z: -3.7 }
  })
  return { agent, chats, commands }
}

function chat (agent, from, message, type) {
  agent.handleText({ type: type || 'chat', source_name: from, message })
}

// 1. help
{
  const { agent, chats } = makeAgent()
  chat(agent, 'Sanath', 'atlas help')
  check('help answers with command list', chats.length === 1 && chats[0].includes('manifest monolith') && chats[0].includes('atlas help'))
}

// 2. bare help without prefix
{
  const { agent, chats } = makeAgent()
  chat(agent, 'Sanath', 'help')
  check('bare help works', chats.length === 1 && chats[0].includes('manifest'))
}

// 3. status reports floored position
{
  const { agent, chats } = makeAgent()
  chat(agent, 'Sanath', 'atlas status')
  check('status reports position', chats.length === 1 && chats[0].includes('(10, 64, -4)') && chats[0].includes('0 entities'))
}

// 4. monolith default 3x6x3
{
  const { agent, chats, commands } = makeAgent()
  chat(agent, 'Sanath', 'atlas manifest monolith')
  check('monolith runs one /fill', commands.length === 1 && commands[0] === '/fill ~-1 ~ ~-1 ~1 ~5 ~1 minecraft:deepslate_bricks', JSON.stringify(commands))
  check('monolith announces', chats.length === 1 && chats[0].includes('3x6x3'))
}

// 5. graph K5: 5 nodes + 10 edges = 15 setblocks, sea lanterns + end rods
{
  const { agent, chats, commands } = makeAgent()
  chat(agent, 'Sanath', 'atlas manifest graph 5')
  const lanterns = commands.filter(c => c.includes('sea_lantern')).length
  const rods = commands.filter(c => c.includes('end_rod')).length
  check('graph K5 has 5 lantern nodes', lanterns === 5, `got ${lanterns}`)
  check('graph K5 has 10 end-rod edges', rods === 10, `got ${rods}`)
  check('graph announces K5', chats.length === 1 && chats[0].includes('K5') && chats[0].includes('10 end-rod'))
}

// 6. anchor
{
  const { agent, commands } = makeAgent()
  chat(agent, 'Sanath', 'atlas anchor')
  check('anchor sets crying obsidian below', commands.length === 1 && commands[0] === '/setblock ~ ~-1 ~ minecraft:crying_obsidian')
}

// 7. nullify
{
  const { agent, commands } = makeAgent()
  chat(agent, 'Sanath', 'atlas nullify')
  check('nullify fills air', commands.length === 1 && commands[0].includes('minecraft:air'))
}

// 8. come here teleports bot to speaker
{
  const { agent, commands } = makeAgent()
  chat(agent, 'Sanath', 'atlas come here')
  check('come here teleports Atlas to speaker', commands.length === 1 && commands[0] === '/tp Atlas Sanath', JSON.stringify(commands))
}

// 9. greeting + fallback
{
  const { agent, chats } = makeAgent()
  chat(agent, 'Sanath', 'hello')
  check('greeting answers', chats.length === 1 && chats[0].startsWith('Hey Sanath'))
  chat(agent, 'Sanath', 'atlas what is the meaning of life')
  check('unknown addressed message falls back to help pointer', chats.length === 2 && chats[1].includes('atlas help'))
}

// 10. ignores own messages, system text, and slash commands
{
  const { agent, chats, commands } = makeAgent()
  chat(agent, 'Atlas', 'atlas help')
  chat(agent, 'Sanath', '/fill ~ ~ ~ ~ ~ ~ minecraft:stone')
  agent.handleText({ type: 'system', source_name: '', message: 'atlas help' })
  check('ignores own messages, slash input and system text', chats.length === 0 && commands.length === 0)
}

// 11. failed command output -> op hint (once)
{
  const { agent, chats, commands } = makeAgent()
  chat(agent, 'Sanath', 'atlas manifest monolith')
  agent.handleCommandOutput({ success: false })
  check('failed command explains /op needed', chats.some(c => c.includes('/op Atlas')), JSON.stringify(chats))
  const n = chats.length
  agent.handleCommandOutput({ success: false })
  check('op hint not spammed', chats.length === n)
}

// 12. the produced commands actually serialize as real Bedrock packets
{
  const { createSerializer } = require('bedrock-protocol/src/transforms/serializer')
  const s = createSerializer('1.26.60')
  const { agent, commands } = makeAgent()
  chat(agent, 'Sanath', 'atlas manifest monolith')
  chat(agent, 'Sanath', 'atlas manifest graph 5')
  let ok = true
  for (const cmd of commands) {
    try {
      s.createPacketBuffer({ name: 'command_request', params: { command: cmd, origin: { type: 'player', uuid: '00000000-0000-0000-0000-000000000000', request_id: '', player_entity_id: 0 }, internal: false, version: '52' } })
    } catch (e) { ok = false; console.log('serialize failed for', cmd, e.message) }
  }
  check(`all ${commands.length} produced commands serialize as command_request packets`, ok)
}

console.log(`\n${passed} passed, ${failed} failed`)
process.exit(failed ? 1 : 0)
