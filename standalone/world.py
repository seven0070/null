#!/usr/bin/env python3
"""
Null Universe — standalone world engine.

No Minecraft. No Pumpkin. No Bedrock. No server to start elsewhere.
This is the runnable Null Universe: the same genesis state, Null Entity
metabolism, and manifestation engine as the reference Rust engine
(null-universe/src/core + scripts/harness.py), running on plain Python.

Genesis (T=0): tick 0, entropy 0.0, mass 0.0, energy 0.0, 0 entities,
status PrimordialVoid. Everything that exists afterwards is manifested
into the void by an operator (you) or by Atlas, the native Null Entity,
acting on your command — the same vocabulary as the old Minecraft
routines, now in native coordinates:

  anchor            -> void anchor at the genesis point (0, 0, 0)
  monolith w h d    -> PhysicalConstruct cuboid (was: deepslate bricks)
  graph K_n         -> DiscreteMathGraph, N nodes + N(N-1)/2 edges
                       (was: sea lanterns + end rods)
  nullify           -> cleanse manifested matter back to nothingness
                       (was: fill air)
  materialize name  -> spawn a native Null Entity (MaterializeNullEntity)
  pause / resume    -> UniverseStatus Paused <-> ActiveSimulation
"""

import json
import math
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any

# Universe-level states — same enum as src/core/genesis.rs
STATUS_PRIMORDIAL_VOID = "PrimordialVoid"
STATUS_ACTIVE = "ActiveSimulation"
STATUS_PAUSED = "Paused"
STATUS_FROZEN = "Frozen"

OPERATOR = "Prime_Architect_User"


def _round3(v: float) -> float:
    return round(float(v), 3)


@dataclass
class Vec3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def to_dict(self) -> dict:
        return {"x": _round3(self.x), "y": _round3(self.y), "z": _round3(self.z)}

    @classmethod
    def from_dict(cls, d: dict) -> "Vec3":
        return cls(float(d.get("x", 0.0)), float(d.get("y", 0.0)), float(d.get("z", 0.0)))

    def distance_to(self, other: "Vec3") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)


@dataclass
class PhysicalEntity:
    id: str
    entity_type: str  # anchor | manifested_construct | math_node | field_emitter
    position: Vec3
    mass: float = 0.0
    energy: float = 0.0
    radius: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "entity_type": self.entity_type,
            "position": self.position.to_dict(),
            "mass": _round3(self.mass),
            "energy": _round3(self.energy),
            "radius": _round3(self.radius),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "PhysicalEntity":
        return cls(
            id=d["id"],
            entity_type=d["entity_type"],
            position=Vec3.from_dict(d["position"]),
            mass=float(d.get("mass", 0.0)),
            energy=float(d.get("energy", 0.0)),
            radius=float(d.get("radius", 0.5)),
            metadata=d.get("metadata", {}),
        )


@dataclass
class NullEntity:
    """A native agent of the void. Survives strictly on zero (E_null = 0.0)."""
    id: str
    position: Vec3
    operator_id: str = OPERATOR
    control_mode: str = "DirectUserControl"
    zero_deviation: float = 0.0
    collapse_threshold: float = 50.0
    void_resonance: float = 1.0
    nullification_rate: float = 0.8
    manifestation_count: int = 0
    ambient_void_purity: float = 1.0

    def update_state(self, nearby_matter: List[PhysicalEntity]) -> None:
        total_disturbance = 0.0
        for entity in nearby_matter:
            if entity.id == self.id:
                continue
            dist = self.position.distance_to(entity.position)
            if dist < 40.0:
                total_disturbance += (entity.mass + entity.energy * 0.05) / max(dist * dist, 1.0)
        if total_disturbance < 0.05:
            self.zero_deviation = max(0.0, self.zero_deviation - self.nullification_rate)
        else:
            self.zero_deviation += total_disturbance * 0.05
        self.void_resonance = max(0.0, min(1.0, 1.0 - (self.zero_deviation / self.collapse_threshold)))
        self.ambient_void_purity = max(0.0, min(1.0, 1.0 - (total_disturbance * 0.02)))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "position": self.position.to_dict(),
            "operator_id": self.operator_id,
            "control_mode": self.control_mode,
            "zero_deviation": _round3(self.zero_deviation),
            "void_resonance": _round3(self.void_resonance),
            "nullification_rate": self.nullification_rate,
            "manifestation_count": self.manifestation_count,
            "ambient_void_purity": _round3(self.ambient_void_purity),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "NullEntity":
        return cls(
            id=d["id"],
            position=Vec3.from_dict(d["position"]),
            operator_id=d.get("operator_id", OPERATOR),
            control_mode=d.get("control_mode", "DirectUserControl"),
            zero_deviation=float(d.get("zero_deviation", 0.0)),
            void_resonance=float(d.get("void_resonance", 1.0)),
            nullification_rate=float(d.get("nullification_rate", 0.8)),
            manifestation_count=int(d.get("manifestation_count", 0)),
            ambient_void_purity=float(d.get("ambient_void_purity", 1.0)),
        )


class NullUniverse:
    """The world. Starts as a pure void; everything else is manifested."""

    def __init__(self):
        self.tick = 0
        self.entropy = 0.0
        self.status = STATUS_PRIMORDIAL_VOID
        self.physical_entities: Dict[str, PhysicalEntity] = {}
        self.null_entities: Dict[str, NullEntity] = {}
        self.edges: List[Dict[str, str]] = []  # {"id", "a", "b", "graph"} for K_n
        self.chronicle: List[Dict[str, Any]] = []
        self._monolith_seq = 0
        self._graph_seq = 0
        self._entity_seq = 0
        self.log("Genesis: Primordial Void established (T=0). 0 entities, 0 mass, 0 energy.")

    # -- chronicle ---------------------------------------------------------
    def log(self, text: str) -> None:
        self.chronicle.append({"tick": self.tick, "text": text})
        self.chronicle = self.chronicle[-500:]

    # -- derived state ------------------------------------------------------
    def total_mass(self) -> float:
        return sum(e.mass for e in self.physical_entities.values())

    def total_energy(self) -> float:
        return sum(e.energy for e in self.physical_entities.values())

    def _activate(self) -> None:
        if self.status == STATUS_PRIMORDIAL_VOID:
            self.status = STATUS_ACTIVE

    def is_ticking(self) -> bool:
        return self.status in (STATUS_PRIMORDIAL_VOID, STATUS_ACTIVE)

    # -- null entities ------------------------------------------------------
    def spawn_null_entity(self, entity_id: str, position: Optional[Vec3] = None,
                          operator_id: str = OPERATOR) -> NullEntity:
        if entity_id in self.null_entities:
            raise ValueError(f"Null Entity '{entity_id}' already exists")
        pos = position or Vec3(0.0, 0.0, 0.0)
        entity = NullEntity(id=entity_id, position=pos, operator_id=operator_id)
        self.null_entities[entity_id] = entity
        self._activate()
        self.log(f"Null Entity born: '{entity_id}' at {pos.to_dict()} | Operator: '{operator_id}'")
        return entity

    def materialize_null_entity(self, name: str, operator_id: str = OPERATOR) -> NullEntity:
        """MaterializeNullEntity from the IPC protocol: a new native entity."""
        self._entity_seq += 1
        angle = (self._entity_seq * 2.39996) % (2 * math.pi)  # golden-angle spread
        pos = Vec3(math.cos(angle) * 6.0, 0.0, math.sin(angle) * 6.0)
        return self.spawn_null_entity(name, pos, operator_id)

    # -- manifestation ------------------------------------------------------
    def anchor(self, operator_id: str = OPERATOR) -> PhysicalEntity:
        """Set the void anchor at the genesis point (0,0,0). Idempotent."""
        existing = self.physical_entities.get("Void_Anchor")
        if existing is not None:
            return existing
        anchor = PhysicalEntity(
            id="Void_Anchor",
            entity_type="anchor",
            position=Vec3(0.0, 0.0, 0.0),
            mass=0.0,
            energy=0.0,
            radius=0.8,
            metadata={"creator": "Atlas", "authorized_by": operator_id, "is_fixed": True},
        )
        self.physical_entities[anchor.id] = anchor
        self._activate()
        self.log("Void anchor set at the genesis point (0, 0, 0).")
        return anchor

    def manifest_monolith(self, w: int = 3, h: int = 6, d: int = 3,
                          operator_id: str = OPERATOR) -> PhysicalEntity:
        """PhysicalConstruct cuboid, raised out of the void (was: deepslate bricks)."""
        self._monolith_seq += 1
        name = f"Monolith_{self._monolith_seq}"
        entity = PhysicalEntity(
            id=name,
            entity_type="manifested_construct",
            position=Vec3(0.0, 0.0, 5.0),
            mass=100.0,
            energy=0.0,
            radius=max(w, d) / 2.0,
            metadata={
                "shape": "Cuboid",
                "width": w, "height": h, "depth": d,
                "creator": "Atlas", "authorized_by": operator_id, "is_fixed": True,
            },
        )
        self.physical_entities[entity.id] = entity
        self.entropy += 0.05
        self._activate()
        self.log(f"Manifested {w}x{h}x{d} monolith '{name}' at (0, 0, 5).")
        return entity

    def manifest_graph(self, n: int = 5, radius: float = 5.0,
                       operator_id: str = OPERATOR) -> List[PhysicalEntity]:
        """DiscreteMathGraph: complete graph K_n in the void (was: sea lanterns + end rods)."""
        n = max(3, min(8, int(n)))
        radius = max(3.0, min(10.0, float(radius)))
        self._graph_seq += 1
        name = f"K{self._graph_seq}_{n}"
        origin = Vec3(12.0, 0.0, 0.0)
        nodes: List[PhysicalEntity] = []
        for i in range(n):
            angle = (i / n) * 2 * math.pi
            node = PhysicalEntity(
                id=f"{name}_Node_{i}",
                entity_type="math_node",
                position=Vec3(origin.x + math.cos(angle) * radius, 0.0,
                              origin.z + math.sin(angle) * radius),
                mass=1.0,
                energy=0.0,
                radius=0.3,
                metadata={"graph": name, "topology": "CompleteGraph_K_n",
                          "node_index": i, "authorized_by": operator_id},
            )
            self.physical_entities[node.id] = node
            nodes.append(node)
        for i in range(n):
            for j in range(i + 1, n):
                self.edges.append({
                    "id": f"{name}_Edge_{i}_{j}",
                    "a": nodes[i].id, "b": nodes[j].id, "graph": name,
                })
        self.entropy += 0.05
        self._activate()
        self.log(f"Materialized complete graph {name}: {n} nodes, {n * (n - 1) // 2} edges.")
        return nodes

    def manifest_field(self, field_type: str = "EntropyDampener", radius: float = 15.0,
                       intensity: float = 1.0, operator_id: str = OPERATOR) -> PhysicalEntity:
        """FieldEmitter from the blueprint vocabulary."""
        self._entity_seq += 1
        name = f"Field_{self._entity_seq}"
        entity = PhysicalEntity(
            id=name,
            entity_type="field_emitter",
            position=Vec3(-12.0, 0.0, 0.0),
            mass=0.0,
            energy=0.0,
            radius=radius,
            metadata={"field_type": field_type, "intensity": intensity,
                      "creator": "Atlas", "authorized_by": operator_id},
        )
        self.physical_entities[entity.id] = entity
        self._activate()
        self.log(f"Manifested field emitter '{name}' ({field_type}, radius {radius}).")
        return entity

    # -- nullification ------------------------------------------------------
    def nullify(self, target: Optional[str] = None,
                operator_id: str = OPERATOR) -> Dict[str, Any]:
        """Cleanse manifested matter back to nothingness.

        No target: dissolve every manifested construct, graph node and field
        (the anchor and the null entities remain — the genesis point endures).
        With a target id: dissolve just that entity (and its graph edges).
        """
        removed: List[str] = []
        if target:
            entity = self.physical_entities.get(target)
            if entity is None:
                raise ValueError(f"Nothing called '{target}' exists to nullify")
            if entity.entity_type == "anchor":
                raise ValueError("The void anchor cannot be nullified — it marks the genesis point")
            removed.append(entity.id)
            del self.physical_entities[target]
            self.edges = [e for e in self.edges if e["a"] != target and e["b"] != target]
        else:
            for entity_id in list(self.physical_entities):
                if self.physical_entities[entity_id].entity_type != "anchor":
                    removed.append(entity_id)
                    del self.physical_entities[entity_id]
            self.edges = []
        absorbed_mass = 0.0
        for ne in self.null_entities.values():
            ne.zero_deviation = max(0.0, ne.zero_deviation - len(removed) * 0.1)
        self.log(f"Nullified {len(removed)} manifested {'entity' if len(removed) == 1 else 'entities'} "
                 f"back to pure nothingness.")
        return {"removed": removed, "absorbed_mass": absorbed_mass}

    # -- time ----------------------------------------------------------------
    def pause(self) -> None:
        if self.status in (STATUS_ACTIVE, STATUS_PRIMORDIAL_VOID):
            self.status = STATUS_PAUSED
            self.log("Universe paused.")

    def resume(self) -> None:
        if self.status == STATUS_PAUSED:
            self.status = STATUS_ACTIVE if self.physical_entities else STATUS_PRIMORDIAL_VOID
            self.log("Universe resumed.")

    def freeze(self) -> None:
        self.status = STATUS_FROZEN
        self.log("Universe frozen.")

    def step(self) -> None:
        """One tick: entropy dynamics from harness.py; null entities sense the void."""
        if not self.is_ticking():
            return
        self.tick += 1
        entropy_damping = sum(ne.void_resonance * 0.002 for ne in self.null_entities.values())
        self.entropy = max(0.0, self.entropy + (0.0005 * len(self.physical_entities)) - entropy_damping)
        matter = list(self.physical_entities.values())
        for ne in self.null_entities.values():
            ne.update_state(matter)

    # -- reports / persistence ----------------------------------------------
    def report(self) -> dict:
        return {
            "tick": self.tick,
            "entropy": round(self.entropy, 4),
            "status": self.status,
            "physical_entities": len(self.physical_entities),
            "null_entities": len(self.null_entities),
            "total_mass": round(self.total_mass(), 2),
            "total_energy": round(self.total_energy(), 2),
            "total_manifestations": sum(ne.manifestation_count for ne in self.null_entities.values()),
            "null_energy_status": "Absolute Zero (Nothingness)",
        }

    def to_dict(self) -> dict:
        return {
            "tick": self.tick,
            "entropy": self.entropy,
            "status": self.status,
            "physical_entities": {k: v.to_dict() for k, v in self.physical_entities.items()},
            "null_entities": {k: v.to_dict() for k, v in self.null_entities.items()},
            "edges": list(self.edges),
            "chronicle": list(self.chronicle),
            "counters": {
                "monolith_seq": self._monolith_seq,
                "graph_seq": self._graph_seq,
                "entity_seq": self._entity_seq,
            },
            "report": self.report(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "NullUniverse":
        u = cls.__new__(cls)
        u.tick = int(d.get("tick", 0))
        u.entropy = float(d.get("entropy", 0.0))
        u.status = d.get("status", STATUS_PRIMORDIAL_VOID)
        u.physical_entities = {k: PhysicalEntity.from_dict(v)
                               for k, v in d.get("physical_entities", {}).items()}
        u.null_entities = {k: NullEntity.from_dict(v)
                           for k, v in d.get("null_entities", {}).items()}
        u.edges = list(d.get("edges", []))
        u.chronicle = list(d.get("chronicle", []))
        counters = d.get("counters", {})
        u._monolith_seq = int(counters.get("monolith_seq", 0))
        u._graph_seq = int(counters.get("graph_seq", 0))
        u._entity_seq = int(counters.get("entity_seq", 0))
        return u

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "NullUniverse":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))
