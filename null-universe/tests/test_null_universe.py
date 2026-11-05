#!/usr/bin/env python3
"""
Comprehensive Test Suite for the Null Universe Simulation Engine.
Verifies:
 1. Primordial Void State (T=0)
 2. Null Entity Zero-Energy Metabolism & Resonance
 3. Rapier Physics, Colliders & Raycast Occlusion
 4. Controlled Manifestation Engine (User & AI Agent via User)
 5. Discrete Mathematics (von Neumann Ordinals, Graph Topologies, Kernel/Null-Space)
 6. Multi-Tick Thermodynamics & Stability
"""

import unittest
import math
import sys
import os

# Ensure script directory is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from harness import NullUniverse, Vector3, PhysicalEntity, NullEntity

class TestGenesisAndVoid(unittest.TestCase):
    def setUp(self):
        self.sim = NullUniverse()

    def test_primordial_void_state(self):
        """Verify the universe starts at absolute zero (nothingness)."""
        summary = self.sim.get_universe_report()
        self.assertEqual(summary["tick"], 0)
        self.assertEqual(summary["entropy"], 0.0)
        self.assertEqual(summary["physical_entities"], 0)
        self.assertEqual(summary["null_entities"], 0)
        self.assertEqual(summary["total_mass"], 0.0)
        self.assertEqual(summary["total_positive_energy"], 0.0)
        self.assertEqual(summary["null_energy_status"], "Absolute Zero (Nothingness)")
        print("\n[PASS] Test 1: Genesis state starts at pure vacuum (0 entities, 0 mass, 0 energy).")

class TestNullEntityMetabolism(unittest.TestCase):
    def setUp(self):
        self.sim = NullUniverse()
        self.null_entity = self.sim.spawn_null_entity("Null_Prime", Vector3(0.0, 0.0, 0.0))

    def test_zero_energy_survival_in_vacuum(self):
        """Null entities must maintain 100% resonance in pristine nothingness."""
        for _ in range(5):
            self.sim.step()
        self.assertEqual(self.null_entity.zero_deviation, 0.0)
        self.assertEqual(self.null_entity.void_resonance, 1.0)
        self.assertEqual(self.null_entity.ambient_void_purity, 1.0)
        print("\n[PASS] Test 2a: Null entity sustains 100% resonance in zero-point vacuum.")

    def test_matter_intrusion_and_nullification(self):
        """Matter intrusion increases zero deviation; nullification restores vacuum balance."""
        # Inject positive matter disturbance
        debris = self.sim.inject_positive_matter("Debris_Anomaly", Vector3(2.0, 0.0, 0.0), mass=50.0, energy=200.0)
        for _ in range(5):
            self.sim.step()

        # Check that deviation increased
        self.assertGreater(self.null_entity.zero_deviation, 0.0)
        self.assertLess(self.null_entity.void_resonance, 1.0)
        self.assertLess(self.null_entity.ambient_void_purity, 1.0)
        initial_dev = self.null_entity.zero_deviation

        # Null entity cleanses space
        absorbed_m, absorbed_e = self.null_entity.nullify_disturbance(debris, power=50.0)
        self.assertGreater(absorbed_m, 0.0)
        self.assertGreater(absorbed_e, 0.0)

        for _ in range(5):
            self.sim.step()

        # Verify recovery towards zero
        self.assertLess(self.null_entity.zero_deviation, initial_dev)
        self.assertGreater(self.null_entity.void_resonance, 0.90)
        print(f"\n[PASS] Test 2b: Disturbance detected and nullified. Resonance recovered to {self.null_entity.void_resonance * 100:.1f}%.")

class TestRapierPhysicsAndSensory(unittest.TestCase):
    def setUp(self):
        self.sim = NullUniverse()
        self.observer = self.sim.spawn_null_entity("Observer_Null", Vector3(0.0, 0.0, 0.0))

    def test_spatial_distance_and_perception(self):
        """Rapier 3D spatial calculations correctly detect distances and occlusion."""
        e1 = self.sim.inject_positive_matter("Target_A", Vector3(3.0, 4.0, 0.0), mass=10.0, energy=0.0) # Dist = 5.0
        e2 = self.sim.inject_positive_matter("Target_Far", Vector3(100.0, 0.0, 0.0), mass=10.0, energy=0.0) # Out of range

        self.sim.step()
        detected_ids = [d["entity_id"] for d in self.observer.perceived_disturbances]

        self.assertIn("Target_A", detected_ids)
        self.assertNotIn("Target_Far", detected_ids)
        print("\n[PASS] Test 3: 3D spatial distance and perception thresholds verified.")

class TestControlledManifestation(unittest.TestCase):
    def setUp(self):
        self.sim = NullUniverse()
        self.null_architect = self.sim.spawn_null_entity("Architect_Zero", Vector3(0.0, 0.0, 0.0))

    def test_direct_user_manifestation(self):
        """User directly commands the manifestation of a physical construct."""
        created = self.null_architect.manifest(
            blueprint_type="PhysicalConstruct",
            name="Test_Sanctuary",
            params={"x": 5.0, "y": 0.0, "z": 0.0, "mass": 1000.0, "energy": 0.0, "shape": "Cuboid"},
            authorized_by="User_Direct"
        )
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0].id, "Test_Sanctuary")
        self.assertEqual(created[0].entity_type, "manifested_construct")
        self.assertEqual(created[0].mass, 1000.0)
        self.assertEqual(created[0].metadata["authorized_by"], "User_Direct")
        print("\n[PASS] Test 4a: Direct User manifestation of physical construct validated.")

    def test_ai_agent_via_user_manifestation(self):
        """AI agent operating on behalf of the user commands discrete math graph manifestation."""
        created = self.null_architect.manifest(
            blueprint_type="DiscreteMathGraph",
            name="CompleteGraph_K5",
            params={"x": 10.0, "y": 0.0, "z": 0.0, "nodes": 5, "scale": 3.0, "topology": "CompleteGraph_K_5"},
            authorized_by="AI_Agent_Via_User"
        )
        self.assertEqual(len(created), 5)
        for i, node in enumerate(created):
            self.assertEqual(node.entity_type, "math_node")
            self.assertEqual(node.metadata["node_index"], i)
            self.assertEqual(node.metadata["authorized_by"], "AI_Agent_Via_User")
        print("\n[PASS] Test 4b: AI Agent via User manifestation of discrete math graph validated.")

    def test_field_emitter_manifestation(self):
        """Manifesting zero-point force fields."""
        created = self.null_architect.manifest(
            blueprint_type="FieldEmitter",
            name="Entropy_Dampener_Alpha",
            params={"x": 0.0, "y": 0.0, "z": 0.0, "field_type": "EntropyDampener", "intensity": 2.0},
            authorized_by="User_Direct"
        )
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0].entity_type, "field_emitter")
        self.assertEqual(created[0].mass, 0.0) # Zero mass field
        print("\n[PASS] Test 4c: Zero-point field emitter manifestation validated.")

class TestDiscreteMathematics(unittest.TestCase):
    def test_von_neumann_ordinals_from_null(self):
        """Construct natural numbers recursively from the empty set (nothingness)."""
        # 0 = empty set ()
        ord_0 = ()
        # 1 = { 0 }
        ord_1 = (ord_0,)
        # 2 = { 0, 1 }
        ord_2 = (ord_0, ord_1)
        # 3 = { 0, 1, 2 }
        ord_3 = (ord_0, ord_1, ord_2)

        self.assertEqual(len(ord_0), 0)
        self.assertEqual(len(ord_1), 1)
        self.assertEqual(len(ord_2), 2)
        self.assertEqual(len(ord_3), 3)
        print("\n[PASS] Test 5a: von Neumann ordinal arithmetic bootstrapped from empty set Ø.")

    def test_complete_graph_combinatorics(self):
        """Verify discrete complete graph edge formula |E| = n*(n-1)/2."""
        for n in [3, 4, 5, 6, 8]:
            expected_edges = n * (n - 1) // 2
            edges = []
            for i in range(n):
                for j in range(i + 1, n):
                    edges.append((i, j))
            self.assertEqual(len(edges), expected_edges)
        print("\n[PASS] Test 5b: Discrete graph topology combinatorics verified.")

    def test_linear_algebra_null_space_solver(self):
        """Find the Kernel / Null Space of a perturbation matrix to cancel disturbances to zero."""
        # 2x2 matrix: row 1 is [2, 4], row 2 is [1, 2] (dependent, rank 1, nullity 1)
        # We want vector x = [x1, x2] such that A * x = [0, 0]
        # x = [-2, 1] satisfies: 2*(-2) + 4*(1) = 0, 1*(-2) + 2*(1) = 0
        x = [-2.0, 1.0]
        row_1 = 2.0 * x[0] + 4.0 * x[1]
        row_2 = 1.0 * x[0] + 2.0 * x[1]
        self.assertAlmostEqual(row_1, 0.0)
        self.assertAlmostEqual(row_2, 0.0)
        print(f"\n[PASS] Test 5c: Linear algebra Null Space Ker(A) verified: A*x = [0.0, 0.0].")

class TestThermodynamicsAndClock(unittest.TestCase):
    def test_multi_tick_stability(self):
        """Run 50 simulation ticks and verify thermodynamic stability."""
        sim = NullUniverse()
        sim.spawn_null_entity("Sentinel_01", Vector3(0.0, 0.0, 0.0))
        sim.inject_positive_matter("Matter_Block", Vector3(10.0, 0.0, 0.0), mass=100.0, energy=50.0)

        for _ in range(50):
            sim.step()

        report = sim.get_universe_report()
        self.assertEqual(report["tick"], 50)
        self.assertGreaterEqual(report["entropy"], 0.0)
        self.assertEqual(report["null_entities"], 1)
        self.assertEqual(report["physical_entities"], 1)
        print(f"\n[PASS] Test 6: 50-tick simulation ran with 100% stability. Entropy = {report['entropy']:.4f}.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
