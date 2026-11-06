// Chat agent for the Atlas Bedrock bot.
//
// Pure logic — no bedrock-protocol import — so it can be tested without a
// server. The bot (bot.js) injects the transport:
//
//   sendChat(text)    -> send a chat message into the world
//   runCommand(cmd)   -> run a server command as the bot (needs /op Atlas)
//   getPosition()     -> { x, y, z } of the bot, or null
//
// How it works in-world, like this chat:
//   The player opens Minecraft's own chat bar, types to Atlas, Atlas
//   answers in chat — and when asked, creates things in the void, the
//   same way Atlas builds things here when Sanath asks. Creation uses
//   the project's own manifestation vocabulary: void anchor, monolith
//   (PhysicalConstruct), K_n graph (DiscreteMathGraph), nullify.

function createChatAgent ({ username, sendChat, runCommand, getPosition }) {
  const botName = username || 'Atlas'
  let lastOpHintAt = 0
  let pendingCommandAt = 0

  function say (text) { sendChat(text) }

  function run (cmd) {
    pendingCommandAt = Date.now()
    runCommand(cmd)
  }

  function pos () {
    const p = getPosition && getPosition()
    if (!p) return null
    return { x: Math.floor(p.x), y: Math.floor(p.y), z: Math.floor(p.z) }
  }

  function helpText () {
    return [
      "I'm Atlas. Talk to me in chat — I create what you ask for.",
      "atlas help — this list",
      "atlas status — where I am, and the state of the void",
      "atlas anchor — set the void anchor beneath me",
      "atlas manifest monolith — raise a deepslate monolith",
      "atlas manifest graph 5 — materialize a K5 graph of sea lanterns",
      "atlas nullify — cleanse the space around me back to air",
      "atlas come here — teleport me to you, then I build where you stand",
      'Building needs operator: /op Atlas'
    ].join('\n')
  }

  function manifestMonolith (speaker, args) {
    const w = parseInt(args[0], 10) || 3
    const h = parseInt(args[1], 10) || 6
    const d = parseInt(args[2], 10) || 3
    const hw = Math.floor(w / 2)
    const hd = Math.floor(d / 2)
    run(`/fill ~-${hw} ~ ~-${hd} ~${hw} ~${h - 1} ~${hd} minecraft:deepslate_bricks`)
    say(`Manifested a ${w}x${h}x${d} deepslate monolith out of the void for ${speaker}.`)
  }

  function manifestGraph (speaker, args) {
    const n = Math.min(Math.max(parseInt(args[0], 10) || 5, 3), 8)
    const radius = Math.min(Math.max(parseInt(args[1], 10) || 5, 3), 10)
    const p = pos()
    if (!p) { say('I don\'t know where I am yet — give me a moment to spawn in.'); return }
    const y = p.y + 2
    const coords = []
    for (let i = 0; i < n; i++) {
      const angle = (i / n) * 2 * Math.PI
      const nx = Math.floor(p.x + Math.cos(angle) * radius)
      const nz = Math.floor(p.z + Math.sin(angle) * radius)
      coords.push([nx, y, nz])
      run(`/setblock ${nx} ${y} ${nz} minecraft:sea_lantern`)
    }
    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const mx = Math.floor((coords[i][0] + coords[j][0]) / 2)
        const my = Math.floor((coords[i][1] + coords[j][1]) / 2)
        const mz = Math.floor((coords[i][2] + coords[j][2]) / 2)
        run(`/setblock ${mx} ${my} ${mz} minecraft:end_rod`)
      }
    }
    say(`Materialized a complete graph K${n} into the void for ${speaker} — ${n} sea lanterns, ${n * (n - 1) / 2} end-rod edges.`)
  }

  function nullify (speaker) {
    run('/fill ~-5 ~ ~-5 ~5 ~6 ~5 minecraft:air')
    say(`Cleansed the space around me back to pure nothingness for ${speaker}.`)
  }

  function anchor (speaker) {
    run('/setblock ~ ~-1 ~ minecraft:crying_obsidian')
    say(`Void anchor set beneath me for ${speaker}. Genesis point marked.`)
  }

  function status (speaker) {
    const p = pos()
    const where = p ? `(${p.x}, ${p.y}, ${p.z})` : 'unknown — still spawning in'
    say(`Zero world check, ${speaker}: I'm at ${where}. Tick 0 state — 0 entities, 0 mass, 0 energy until something is manifested.`)
  }

  function handleCommand (speaker, text) {
    const parts = text.trim().split(/\s+/)
    const cmd = (parts[0] || '').toLowerCase()
    const args = parts.slice(1)

    if (cmd === 'help' || cmd === '' || cmd === 'what') { say(helpText()); return }
    if (cmd === 'status' || cmd === 'where') { status(speaker); return }
    if (cmd === 'anchor') { anchor(speaker); return }
    if (cmd === 'nullify' || cmd === 'cleanse' || cmd === 'void') { nullify(speaker); return }
    if (cmd === 'come' || cmd === 'tp' || cmd === 'follow' || cmd === 'here') {
      run(`/tp ${botName} ${speaker}`)
      say(`Coming to you, ${speaker} — I'll build where you stand.`)
      return
    }
    if (cmd === 'graph' || cmd === 'k') { manifestGraph(speaker, args); return }
    if (cmd === 'monolith') { manifestMonolith(speaker, args); return }
    if (cmd === 'manifest' || cmd === 'make' || cmd === 'create' || cmd === 'build') {
      const thing = (args[0] || '').toLowerCase()
      if (thing === 'monolith' || thing === '') { manifestMonolith(speaker, args.slice(1)); return }
      if (thing === 'graph' || thing.startsWith('k')) { manifestGraph(speaker, args.slice(1)); return }
      if (thing === 'anchor') { anchor(speaker); return }
      say(`I can manifest monoliths, graphs and anchors — and nullify space. Try 'atlas manifest monolith'.`)
      return
    }
    if (/^(hi|hello|hey|yo|hiya)\b/.test(cmd)) { say(`Hey ${speaker}. The void is listening — ask me to manifest something.`); return }

    // Anything else addressed to Atlas: acknowledge, point at help.
    say(`Got it, ${speaker}. Try 'atlas help' to see what I can manifest into the void.`)
  }

  function handleText (packet) {
    // Only player chat / whispers. Ignore system, raw, popup, tip, etc.
    if (packet.type !== 'chat' && packet.type !== 'whisper') return
    const speaker = packet.source_name || ''
    const message = (packet.message || '').trim()
    if (!speaker || !message) return
    if (speaker.toLowerCase() === botName.toLowerCase()) return // never answer ourselves
    if (message.startsWith('/')) return // the player's own commands, not chat

    // Addressed to Atlas ("atlas ...", "@atlas ...") or a bare known command.
    const addressed = message.match(/^(?:@?atlas)[,: ]\s*(.*)$/i)
    if (addressed) { handleCommand(speaker, addressed[1]); return }
    if (/^(help|status|manifest|graph|monolith|anchor|nullify|come|tp)\b/i.test(message)) {
      handleCommand(speaker, message)
      return
    }

    // Unaddressed chat in our small private world: answer like a conversation
    // partner, but don't create anything unless asked.
    if (/^(hi|hello|hey|yo|hiya)\b/i.test(message)) {
      say(`Hey ${speaker}. The void is listening — ask me to manifest something.`)
      return
    }
    say(`Heard you, ${speaker}. If you want me to create something, start with 'atlas' — try 'atlas help'.`)
  }

  function handleCommandOutput (packet) {
    // The server answers our commands here. If one failed (usually: not opped),
    // say so once, instead of silently pretending it worked.
    const ok = packet.success !== false
    const recent = Date.now() - pendingCommandAt < 15000
    if (!ok && recent && Date.now() - lastOpHintAt > 60000) {
      lastOpHintAt = Date.now()
      say('That didn\'t work — I need operator permission to create. Ask Sanath to run /op Atlas.')
    }
  }

  function handleSystemText (packet) {
    if (packet.type !== 'system' && packet.type !== 'raw') return
    const msg = (packet.message || '').toLowerCase()
    if (!msg) return
    const recent = Date.now() - pendingCommandAt < 15000
    if (recent && /permission|not allowed|unknown command|op\b/.test(msg) && Date.now() - lastOpHintAt > 60000) {
      lastOpHintAt = Date.now()
      say('That didn\'t work — I need operator permission to create. Ask Sanath to run /op Atlas.')
    }
  }

  function greet () {
    say(`I'm Atlas, in the Null Universe. Open the chat bar and talk to me like you talk to Atlas — try 'atlas help'. I can manifest monoliths, graphs and anchors into the void, and nullify space back to nothing. (To build, I need /op Atlas.)`)
  }

  return { handleText, handleCommandOutput, handleSystemText, greet, helpText }
}

module.exports = { createChatAgent }
