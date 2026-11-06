#!/usr/bin/env python3
"""
Atlas — the chat agent of the Null Universe.

Same agent as the old Minecraft chat bar (bedrock-bot/chat.js), re-pointed
at the standalone world instead of a Minecraft server. Pure logic: no HTTP,
no sockets — the server injects the world and collects the replies.

Talk to Atlas like you talk to Atlas here: type in the bar, Atlas answers
and creates in the void. Same command vocabulary, minus the Minecraft-only
bits (no /op, no teleport — Atlas IS the native Null Entity, it has nowhere
to teleport from).
"""

import re
from typing import List

from world import NullUniverse, OPERATOR


class ChatAgent:
    def __init__(self, world: NullUniverse, name: str = "Atlas"):
        self.world = world
        self.name = name

    # -- replies ------------------------------------------------------------
    def help_text(self) -> str:
        return "\n".join([
            f"I'm {self.name}. Talk to me in the bar below — I create what you ask for.",
            "atlas help — this list",
            "atlas status — the state of the void, live numbers",
            "atlas anchor — set the void anchor at the genesis point",
            "atlas manifest monolith [w h d] — raise a monolith out of the void",
            "atlas manifest graph 5 — materialize a complete graph K5",
            "atlas manifest field — raise an entropy-dampening field",
            "atlas materialize <name> — birth a new native Null Entity",
            "atlas nullify [name] — cleanse manifested matter back to nothing",
            "atlas pause / atlas resume — stop and restart time",
        ])

    def greet(self) -> str:
        return (f"I'm {self.name}, in the Null Universe. Type in the bar below and talk to me "
                f"like you talk to Atlas — try 'atlas help'. I can manifest monoliths, graphs, "
                f"fields and anchors into the void, and nullify space back to nothing.")

    # -- commands -----------------------------------------------------------
    def _status(self, speaker: str) -> str:
        r = self.world.report()
        atlas = self.world.null_entities.get(self.name)
        resonance = f", my void resonance {atlas.void_resonance:.2f}" if atlas else ""
        return (f"Zero world check, {speaker}: tick {r['tick']}, status {r['status']}, "
                f"{r['physical_entities']} manifested things, {r['null_entities']} null "
                f"entit{'y' if r['null_entities'] == 1 else 'ies'}, mass {r['total_mass']}, "
                f"energy {r['total_energy']}, entropy {r['entropy']}{resonance}.")

    def _anchor(self, speaker: str) -> str:
        self.world.anchor(operator_id=speaker)
        return f"Void anchor set at the genesis point (0, 0, 0) for {speaker}."

    def _monolith(self, speaker: str, args: List[str]) -> str:
        def _int(i: int, default: int) -> int:
            try:
                return int(args[i])
            except (IndexError, ValueError):
                return default
        w, h, d = _int(0, 3), _int(1, 6), _int(2, 3)
        e = self.world.manifest_monolith(w, h, d, operator_id=speaker)
        return f"Manifested a {w}x{h}x{d} monolith '{e.id}' out of the void for {speaker}."

    def _graph(self, speaker: str, args: List[str]) -> str:
        def _num(i: int, default):
            try:
                return float(args[i])
            except (IndexError, ValueError):
                return default
        n = int(_num(0, 5))
        radius = _num(1, 5.0)
        n = max(3, min(8, n))
        nodes = self.world.manifest_graph(n, radius, operator_id=speaker)
        graph = nodes[0].metadata["graph"]
        return (f"Materialized a complete graph {graph} into the void for {speaker} — "
                f"{n} nodes, {n * (n - 1) // 2} edges.")

    def _field(self, speaker: str, args: List[str]) -> str:
        field_type = args[0] if args else "EntropyDampener"
        e = self.world.manifest_field(field_type=field_type, operator_id=speaker)
        return f"Manifested field emitter '{e.id}' ({field_type}) for {speaker}."

    def _materialize(self, speaker: str, args: List[str]) -> str:
        name = args[0] if args else f"NullEntity_{len(self.world.null_entities) + 1}"
        if name in self.world.null_entities:
            return f"There is already a Null Entity called '{name}'."
        try:
            self.world.materialize_null_entity(name, operator_id=speaker)
        except ValueError as exc:
            return str(exc)
        return f"A new native Null Entity '{name}' was born of the void for {speaker}."

    def _nullify(self, speaker: str, args: List[str]) -> str:
        target = args[0] if args else None
        try:
            result = self.world.nullify(target=target, operator_id=speaker)
        except ValueError as exc:
            return str(exc)
        n = len(result["removed"])
        if n == 0:
            return f"Nothing to cleanse, {speaker} — the void is already empty."
        what = f"'{result['removed'][0]}'" if n == 1 else f"{n} manifested things"
        return f"Cleansed {what} back to pure nothingness for {speaker}."

    def _pause(self, speaker: str) -> str:
        self.world.pause()
        return f"Time stopped, {speaker}. The universe is paused at tick {self.world.tick}."

    def _resume(self, speaker: str) -> str:
        self.world.resume()
        return f"Time flows again, {speaker}. The universe is {self.world.status}."

    # -- routing ------------------------------------------------------------
    def handle_command(self, speaker: str, text: str) -> str:
        parts = text.strip().split()
        cmd = (parts[0] if parts else "").lower()
        args = parts[1:]

        if cmd in ("", "help", "what"):
            return self.help_text()
        if cmd in ("status", "where"):
            return self._status(speaker)
        if cmd == "anchor":
            return self._anchor(speaker)
        if cmd in ("nullify", "cleanse", "void"):
            return self._nullify(speaker, args)
        if cmd in ("graph", "k"):
            return self._graph(speaker, args)
        if cmd == "monolith":
            return self._monolith(speaker, args)
        if cmd == "field":
            return self._field(speaker, args)
        if cmd in ("materialize", "spawn", "birth"):
            return self._materialize(speaker, args)
        if cmd == "pause":
            return self._pause(speaker)
        if cmd in ("resume", "unpause", "continue"):
            return self._resume(speaker)
        if cmd in ("manifest", "make", "create", "build"):
            thing = (args[0] if args else "").lower()
            if thing in ("monolith", ""):
                return self._monolith(speaker, args[1:])
            if thing in ("graph",) or thing.startswith("k"):
                return self._graph(speaker, args[1:])
            if thing == "anchor":
                return self._anchor(speaker)
            if thing == "field":
                return self._field(speaker, args[1:])
            return "I can manifest monoliths, graphs, fields and anchors — and nullify space. Try 'atlas manifest monolith'."
        if re.match(r"^(hi|hello|hey|yo|hiya)\b", cmd):
            return f"Hey {speaker}. The void is listening — ask me to manifest something."
        return f"Got it, {speaker}. Try 'atlas help' to see what I can manifest into the void."

    def handle_message(self, speaker: str, message: str) -> List[str]:
        """One incoming chat line -> zero or more replies. Never creates
        unless the speaker asked Atlas to."""
        text = (message or "").strip()
        if not text:
            return []
        addressed = re.match(r"^(?:@?atlas)[,: ]\s*(.*)$", text, re.IGNORECASE)
        if addressed:
            return [self.handle_command(speaker, addressed.group(1))]
        if re.match(r"^(help|status|manifest|graph|monolith|anchor|nullify|field|materialize|pause|resume)\b",
                    text, re.IGNORECASE):
            return [self.handle_command(speaker, text)]
        if re.match(r"^(hi|hello|hey|yo|hiya)\b", text, re.IGNORECASE):
            return [f"Hey {speaker}. The void is listening — ask me to manifest something."]
        return [f"Heard you, {speaker}. If you want me to create something, start with 'atlas' — try 'atlas help'."]
