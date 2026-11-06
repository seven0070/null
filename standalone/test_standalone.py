#!/usr/bin/env python3
"""Offline checks for the standalone Null Universe (no server, no Minecraft).

Run:  python3 test_standalone.py
Exit code 0 = all checks pass.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from world import NullUniverse, STATUS_PRIMORDIAL_VOID, STATUS_ACTIVE, STATUS_PAUSED, STATUS_FROZEN
from atlas import ChatAgent

PASSED = 0
FAILED = 0


def check(name, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  PASS  {name}")
    else:
        FAILED += 1
        print(f"  FAIL  {name}  {detail}")


def fresh():
    u = NullUniverse()
    u.spawn_null_entity("Atlas")
    return u


print("== world: genesis ==")
u = NullUniverse()
check("genesis tick 0", u.tick == 0)
check("genesis entropy 0", u.entropy == 0.0)
check("genesis mass 0", u.total_mass() == 0.0)
check("genesis energy 0", u.total_energy() == 0.0)
check("genesis 0 physical entities", len(u.physical_entities) == 0)
check("genesis 0 null entities", len(u.null_entities) == 0)
check("genesis status PrimordialVoid", u.status == STATUS_PRIMORDIAL_VOID)

print("== world: atlas spawn ==")
u = fresh()
check("atlas spawned", "Atlas" in u.null_entities)
check("spawn activates universe", u.status == STATUS_ACTIVE)

print("== world: anchor ==")
u = fresh()
a = u.anchor()
check("anchor id", a.id == "Void_Anchor")
check("anchor at genesis point", (a.position.x, a.position.y, a.position.z) == (0.0, 0.0, 0.0))
check("anchor mass 0", a.mass == 0.0)
u.anchor()
check("anchor idempotent", len(u.physical_entities) == 1)

print("== world: monolith ==")
u = fresh()
m = u.manifest_monolith()
check("monolith default id", m.id == "Monolith_1")
check("monolith default dims", (m.metadata["width"], m.metadata["height"], m.metadata["depth"]) == (3, 6, 3))
check("monolith mass 100", m.mass == 100.0)
check("monolith at (0,0,5)", (m.position.x, m.position.z) == (0.0, 5.0))
check("total mass 100 after monolith", u.total_mass() == 100.0)
m2 = u.manifest_monolith(5, 9, 5)
check("monolith custom dims", (m2.metadata["width"], m2.metadata["height"], m2.metadata["depth"]) == (5, 9, 5))

print("== world: graph ==")
u = fresh()
nodes = u.manifest_graph(5)
check("K5 has 5 nodes", len(nodes) == 5)
check("K5 has 10 edges", len(u.edges) == 10)
check("K5 node ids", nodes[0].id.startswith("K1_5_Node_"))
check("K5 mass +5", u.total_mass() == 5.0)
u2 = fresh()
u2.manifest_graph(1)
check("graph n clamps to min 3", len(u2.physical_entities) == 3 and len(u2.edges) == 3)
u2.manifest_graph(99)
check("graph n clamps to max 8", len([e for e in u2.physical_entities.values() if e.entity_type == "math_node"]) == 11)

print("== world: field + materialize ==")
u = fresh()
f = u.manifest_field()
check("field emitter", f.entity_type == "field_emitter" and f.radius == 15.0)
ne = u.materialize_null_entity("Nova")
check("materialized null entity", "Nova" in u.null_entities)
check("materialized at radius 6", abs((ne.position.x ** 2 + ne.position.z ** 2) ** 0.5 - 6.0) < 0.01)

print("== world: nullify ==")
u = fresh()
u.anchor()
u.manifest_monolith()
u.manifest_graph(4)
n_before = len(u.physical_entities)
r = u.nullify(target="Monolith_1")
check("nullify target removes 1", r["removed"] == ["Monolith_1"] and "Monolith_1" not in u.physical_entities)
check("nullify target keeps graph", len(u.edges) == 6)
r = u.nullify()
check("nullify all leaves anchor only", set(u.physical_entities) == {"Void_Anchor"})
check("nullify all clears edges", len(u.edges) == 0)
check("nullify all mass back to 0", u.total_mass() == 0.0)
try:
    u.nullify(target="Void_Anchor")
    check("nullify anchor refused", False, "no error raised")
except ValueError:
    check("nullify anchor refused", True)
try:
    u.nullify(target="Nope")
    check("nullify missing refused", False, "no error raised")
except ValueError:
    check("nullify missing refused", True)

print("== world: time ==")
u = fresh()
u.manifest_monolith()
u.pause()
check("pause status", u.status == STATUS_PAUSED)
t = u.tick
u.step()
check("paused tick frozen", u.tick == t)
u.resume()
check("resume status", u.status == STATUS_ACTIVE)
u.step()
check("resumed tick advances", u.tick == t + 1)
u.freeze()
check("freeze status", u.status == STATUS_FROZEN)
t = u.tick
u.step()
check("frozen tick frozen", u.tick == t)
u2 = fresh()
for _ in range(50):
    u2.step()
check("entropy never negative", u2.entropy >= 0.0)

print("== world: persistence ==")
u = fresh()
u.anchor()
u.manifest_monolith()
u.manifest_graph(5)
u.step()
with tempfile.TemporaryDirectory() as d:
    path = os.path.join(d, "state.json")
    u.save(path)
    v = NullUniverse.load(path)
check("persist tick", v.tick == u.tick)
check("persist entities", len(v.physical_entities) == len(u.physical_entities))
check("persist edges", len(v.edges) == len(u.edges))
check("persist chronicle", len(v.chronicle) == len(u.chronicle))
check("persist status", v.status == u.status)

print("== atlas: commands ==")
u = fresh()
agent = ChatAgent(u)
check("help lists commands", all(k in agent.help_text() for k in
                                 ["atlas status", "atlas anchor", "atlas manifest monolith",
                                  "atlas manifest graph", "atlas nullify", "atlas pause"]))
check("greet mentions chat bar", "chat" in agent.greet().lower() or "bar" in agent.greet().lower())

replies = agent.handle_message("Sanath", "atlas manifest monolith")
check("chat monolith creates", "Monolith_1" in u.physical_entities and "monolith" in replies[0].lower())
replies = agent.handle_message("Sanath", "atlas manifest graph 5")
check("chat graph creates K5", len(u.edges) == 10 and "K" in replies[0])
replies = agent.handle_message("Sanath", "atlas status")
check("chat status reports live numbers", "tick" in replies[0] and "mass 105" in replies[0])
replies = agent.handle_message("Sanath", "atlas anchor")
check("chat anchor", "Void_Anchor" in u.physical_entities)
replies = agent.handle_message("Sanath", "atlas materialize Nova")
check("chat materialize", "Nova" in u.null_entities)
replies = agent.handle_message("Sanath", "atlas nullify")
check("chat nullify cleanses", len(u.physical_entities) == 1 and "nothingness" in replies[0])
replies = agent.handle_message("Sanath", "atlas pause")
check("chat pause", u.status == STATUS_PAUSED)
replies = agent.handle_message("Sanath", "atlas resume")
check("chat resume", u.status == STATUS_ACTIVE)
replies = agent.handle_message("Sanath", "atlas frobnicate")
check("chat unknown points to help", "atlas help" in replies[0])
replies = agent.handle_message("Sanath", "hello")
check("chat greeting, no creation", "Hey" in replies[0] and len(u.physical_entities) == 1)
replies = agent.handle_message("Sanath", "nice void")
check("chat plain talk, no creation", "Heard you" in replies[0] and len(u.physical_entities) == 1)
replies = agent.handle_message("Sanath", "manifest graph 3")
check("chat bare manifest works", len(u.edges) == 3)
replies = agent.handle_message("Sanath", "")
check("chat empty message ignored", replies == [])

print(f"\n{PASSED} passed, {FAILED} failed")
sys.exit(1 if FAILED else 0)
