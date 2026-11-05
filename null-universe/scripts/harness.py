#!/usr/bin/env python3
"""
Null Universe Simulation Harness & Manifestation Engine
Combines:
 1. Primordial Void State (T=0)
 2. Null Entity Zero-Energy Metabolism & Resonance
 3. Rapier Physics & Spatial Raycasting
 4. Controlled Manifestation Engine (User & AI Agent via User)
 5. Discrete Mathematics & Topological Structures
"""

import math
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def distance_to(self, other: 'Vector3') -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

    def to_dict(self) -> dict:
        return {"x": round(self.x, 3), "y": round(self.y, 3), "z": round(self.z, 3)}

@dataclass
class PhysicalEntity:
    id: str
    entity_type: str # 'matter', 'agent', 'manifested_construct', 'math_node', 'field_emitter'
    position: Vector3
    mass: float
    energy: float
    radius: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class NullEntity:
    """
    An AI agent native to the void.
    Survives strictly on Zero/Nothingness (E_null = 0.0).
    Can manifest arbitrary structures under the command of the User or an AI Agent.
    """
    id: str
    position: Vector3
    operator_id: str = "Prime_Architect_User"
    control_mode: str = "DirectUserControl" # 'DirectUserControl' or 'AgentViaUser'
    zero_deviation: float = 0.0
    collapse_threshold: float = 50.0
    void_resonance: float = 1.0
    nullification_rate: float = 0.8
    manifestation_count: int = 0
    perceived_disturbances: List[dict] = field(default_factory=list)
    ambient_void_purity: float = 1.0

    def update_state(self, nearby_matter: List[PhysicalEntity]):
        total_disturbance = 0.0
        self.perceived_disturbances = []

        for entity in nearby_matter:
            if entity.id == self.id:
                continue
            dist = self.position.distance_to(entity.position)
            if dist < 40.0:
                perturbation = (entity.mass + entity.energy * 0.05) / max(dist * dist, 1.0)
                total_disturbance += perturbation
                self.perceived_disturbances.append({
                    "entity_id": entity.id,
                    "mass": entity.mass,
                    "energy": entity.energy,
                    "distance": round(dist, 2),
                    "perturbation": round(perturbation, 3)
                })

        # Survival in the void:
        if total_disturbance < 0.05:
            self.zero_deviation = max(0.0, self.zero_deviation - self.nullification_rate)
        else:
            self.zero_deviation += total_disturbance * 0.05

        self.void_resonance = max(0.0, min(1.0, 1.0 - (self.zero_deviation / self.collapse_threshold)))
        self.ambient_void_purity = max(0.0, min(1.0, 1.0 - (total_disturbance * 0.02)))

    def nullify_disturbance(self, target: PhysicalEntity, power: float = 20.0):
        """Converts positive matter/energy disturbance back into pristine void (0.0)."""
        absorbed_mass = min(target.mass, power)
        absorbed_energy = min(target.energy, power * 2.0)
        target.mass -= absorbed_mass
        target.energy -= absorbed_energy
        self.zero_deviation = max(0.0, self.zero_deviation - (absorbed_mass + absorbed_energy) * 0.1)
        return absorbed_mass, absorbed_energy

    def manifest(self, blueprint_type: str, name: str, params: dict, authorized_by: str) -> List[PhysicalEntity]:
        """Pulls form out of the void under authorized directive."""
        self.manifestation_count += 1
        created_entities = []

        if blueprint_type == "PhysicalConstruct":
            pos = Vector3(params.get("x", self.position.x), params.get("y", self.position.y), params.get("z", self.position.z))
            entity = PhysicalEntity(
                id=name,
                entity_type="manifested_construct",
                position=pos,
                mass=params.get("mass", 100.0),
                energy=params.get("energy", 0.0),
                radius=params.get("scale", 1.0),
                metadata={
                    "shape": params.get("shape", "Cuboid"),
                    "creator": self.id,
                    "authorized_by": authorized_by,
                    "is_fixed": params.get("is_fixed", True),
                }
            )
            created_entities.append(entity)

        elif blueprint_type == "DiscreteMathGraph":
            origin = Vector3(params.get("x", self.position.x), params.get("y", self.position.y), params.get("z", self.position.z))
            num_nodes = params.get("nodes", 5)
            scale = params.get("scale", 4.0)
            topology = params.get("topology", "CompleteGraph_K_n")

            for i in range(num_nodes):
                angle = (i / num_nodes) * 2 * math.pi
                node_pos = Vector3(origin.x + math.cos(angle) * scale, origin.y, origin.z + math.sin(angle) * scale)
                node_entity = PhysicalEntity(
                    id=f"{name}_Node_{i}",
                    entity_type="math_node",
                    position=node_pos,
                    mass=1.0,
                    energy=0.0,
                    radius=0.3,
                    metadata={
                        "graph": name,
                        "topology": topology,
                        "node_index": i,
                        "authorized_by": authorized_by,
                    }
                )
                created_entities.append(node_entity)

        elif blueprint_type == "FieldEmitter":
            pos = Vector3(params.get("x", self.position.x), params.get("y", self.position.y), params.get("z", self.position.z))
            field_entity = PhysicalEntity(
                id=name,
                entity_type="field_emitter",
                position=pos,
                mass=0.0,
                energy=0.0,
                radius=params.get("radius", 15.0),
                metadata={
                    "field_type": params.get("field_type", "EntropyDampener"),
                    "intensity": params.get("intensity", 1.0),
                    "authorized_by": authorized_by,
                }
            )
            created_entities.append(field_entity)

        return created_entities

class NullUniverse:
    def __init__(self):
        self.tick = 0
        self.entropy = 0.0
        self.physical_entities: Dict[str, PhysicalEntity] = {}
        self.null_entities: Dict[str, NullEntity] = {}
        print("[Genesis] Null Universe Initialized: Primordial Void (T=0)")

    def spawn_null_entity(self, entity_id: str, pos: Vector3, operator_id: str = "User_Direct", control_mode: str = "DirectUserControl") -> NullEntity:
        entity = NullEntity(id=entity_id, position=pos, operator_id=operator_id, control_mode=control_mode)
        self.null_entities[entity_id] = entity
        print(f"[{self.tick:04d} Tick] Null Entity Born: '{entity_id}' at {pos.to_dict()} | Operator: '{operator_id}' ({control_mode})")
        return entity

    def inject_positive_matter(self, entity_id: str, pos: Vector3, mass: float, energy: float) -> PhysicalEntity:
        entity = PhysicalEntity(id=entity_id, entity_type="matter", position=pos, mass=mass, energy=energy)
        self.physical_entities[entity_id] = entity
        self.entropy += 0.05
        print(f"[{self.tick:04d} Tick] Positive Matter Injected: '{entity_id}' at {pos.to_dict()} (Mass: {mass}kg, Energy: {energy}J)")
        return entity

    def command_manifestation(self, entity_id: str, blueprint_type: str, name: str, params: dict, operator_id: str):
        null_ent = self.null_entities.get(entity_id)
        if not null_ent:
            raise ValueError(f"Null Entity '{entity_id}' not found")

        print(f"\n>>> [OPERATOR DIRECTIVE] '{operator_id}' commanding '{entity_id}' to manifest {blueprint_type}: '{name}'")
        created = null_ent.manifest(blueprint_type, name, params, authorized_by=operator_id)
        for e in created:
            self.physical_entities[e.id] = e
            print(f"    + Materialized from Void: '{e.id}' ({e.entity_type}) at {e.position.to_dict()} [Mass: {e.mass}kg, Energy: {e.energy}J]")
        return created

    def step(self):
        self.tick += 1
        entropy_damping = sum(ne.void_resonance * 0.002 for ne in self.null_entities.values())
        self.entropy = max(0.0, self.entropy + (0.0005 * len(self.physical_entities)) - entropy_damping)

        # Update all Null Entities
        matter_list = list(self.physical_entities.values())
        for ne in self.null_entities.values():
            ne.update_state(matter_list)

    def get_universe_report(self) -> dict:
        total_mass = sum(e.mass for e in self.physical_entities.values())
        total_energy = sum(e.energy for e in self.physical_entities.values())
        return {
            "tick": self.tick,
            "entropy": round(self.entropy, 4),
            "physical_entities": len(self.physical_entities),
            "null_entities": len(self.null_entities),
            "total_mass": round(total_mass, 2),
            "total_positive_energy": round(total_energy, 2),
            "null_energy_status": "Absolute Zero (Nothingness)",
        }

    def get_summary(self) -> dict:
        return self.get_universe_report()
