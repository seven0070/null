use bevy::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Unique identifier for an agent or entity in the Null Universe.
#[derive(Component, Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct EntityId(pub String);

/// Agent brain metadata and classification.
#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct AgentBrain {
    pub model_id: String,
    pub generation: u64,
}

/// Matter properties for an entity condensed in the void.
#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct Matter {
    pub mass: f32,
    pub density: f32,
    pub energy: f32,
}

/// Inventory containing material resources and crafted tools.
#[derive(Component, Debug, Clone, Default, Serialize, Deserialize)]
pub struct Inventory {
    pub resources: HashMap<String, f32>,
    pub max_capacity: f32,
}

/// Standard energy store consumed by mechanical actions.
#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct EnergyStore {
    pub current: f32,
    pub max: f32,
    pub recharge_rate: f32,
}

// =========================================================================
// NULL ENTITY & MANIFESTATION ENGINE
// =========================================================================

/// Marker component denoting a native Null Entity born of the void.
#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct NullEntity {
    pub origin_tick: u64,
    pub consciousness_frequency: f32,
}

/// Operator authority binding a Null Entity to the real-world user or an AI agent acting via the user.
#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct OperatorBinding {
    pub operator_id: String,
    pub control_mode: ControlMode,
    pub authorized_manifestations: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ControlMode {
    /// Commanded directly by the user in real time
    DirectUserControl,
    /// Commanded by an AI agent acting via the user
    AgentViaUser,
    /// Autonomous entity proposing creations to the user for execution
    AutonomousWithUserOversight,
}

impl Default for OperatorBinding {
    fn default() -> Self {
        Self {
            operator_id: "Prime_Architect_User".into(),
            control_mode: ControlMode::DirectUserControl,
            authorized_manifestations: vec!["all".into()],
        }
    }
}

/// The Manifestation Engine power: enables an entity to pull form out of the void.
#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct ManifestationPower {
    pub creation_cooldown_ticks: u32,
    pub current_cooldown: u32,
    pub max_complexity: u32,
    pub total_manifestations_created: u64,
}

impl Default for ManifestationPower {
    fn default() -> Self {
        Self {
            creation_cooldown_ticks: 1,
            current_cooldown: 0,
            max_complexity: 1000,
            total_manifestations_created: 0,
        }
    }
}

/// Pending intent to manifest a structure, entity, or mathematical object.
#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct ManifestationIntent {
    pub source_entity: String,
    pub authorized_by: String,
    pub blueprint: ManifestationBlueprint,
}

/// Blueprint specifying what to manifest out of nothingness.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ManifestationBlueprint {
    /// Physical geometry with Rapier colliders (cubes, spheres, monoliths, barriers)
    PhysicalConstruct {
        name: String,
        shape: ConstructShape,
        position: [f32; 3],
        mass: f32,
        energy: f32,
        is_fixed: bool,
    },
    /// Discrete mathematical structure (graph nodes, lattices, topological matrices)
    DiscreteMathGraph {
        name: String,
        topology: GraphTopologyType,
        nodes: usize,
        origin: [f32; 3],
        scale: f32,
    },
    /// Cellular Automaton / Discrete field
    CellularLattice {
        name: String,
        dimensions: [u32; 2],
        origin: [f32; 3],
        rule_set: String,
    },
    /// Gravitational or Void Force Field (attractor, repulsor, tranquilizer)
    FieldEmitter {
        name: String,
        field_type: FieldType,
        center: [f32; 3],
        radius: f32,
        intensity: f32,
    },
    /// Custom computational agent / automated worker
    AgentAvatar {
        agent_id: String,
        role: String,
        position: [f32; 3],
    },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ConstructShape {
    Cuboid { half_extents: [f32; 3] },
    Sphere { radius: f32 },
    Capsule { half_height: f32, radius: f32 },
    Pyramid { base_width: f32, height: f32 },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum GraphTopologyType {
    CompleteGraph,   // K_n
    CycleGraph,      // C_n
    BinaryTree,      // Tree structure
    PlanarGrid,      // 2D grid graph
    HypercubeGraph,  // Q_d
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum FieldType {
    Attractor,
    Repulsor,
    EntropyDampener,
    VoidHarmonizer,
}

/// Metadata attached to any manifested entity.
#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct ManifestedMetadata {
    pub creator_id: String,
    pub operator_id: String,
    pub manifested_tick: u64,
    pub blueprint_type: String,
}

// =========================================================================
// NULL ENERGY & ZERO-STATE SURVIVAL
// =========================================================================

#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct NullEnergyBalance {
    pub zero_deviation: f32,
    pub collapse_threshold: f32,
    pub void_resonance: f32,
    pub nullification_rate: f32,
}

impl Default for NullEnergyBalance {
    fn default() -> Self {
        Self {
            zero_deviation: 0.0,
            collapse_threshold: 50.0,
            void_resonance: 1.0,
            nullification_rate: 0.5,
        }
    }
}

#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct VoidSensor {
    pub detection_radius: f32,
    pub sensitivity: f32,
}

impl Default for VoidSensor {
    fn default() -> Self {
        Self {
            detection_radius: 50.0,
            sensitivity: 0.001,
        }
    }
}

#[derive(Component, Debug, Clone, Default, Serialize, Deserialize)]
pub struct NullPerception {
    pub perceived_disturbances: Vec<VoidDisturbance>,
    pub ambient_void_purity: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VoidDisturbance {
    pub entity_id: String,
    pub perturbation_magnitude: f32,
    pub distance: f32,
    pub relative_position: [f32; 3],
}

// =========================================================================
// STANDARD SENSORY & OBSERVATION
// =========================================================================

#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct SensoryArray {
    pub num_rays: usize,
    pub range: f32,
    pub fov_radians: f32,
}

impl Default for SensoryArray {
    fn default() -> Self {
        Self {
            num_rays: 16,
            range: 30.0,
            fov_radians: std::f32::consts::PI * 0.75,
        }
    }
}

#[derive(Component, Debug, Clone, Default, Serialize, Deserialize)]
pub struct AgentPerception {
    pub visible_entities: Vec<ObservedEntity>,
    pub sensory_points: Vec<SensoryHit>,
    pub nearby_messages: Vec<ReceivedMessage>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ObservedEntity {
    pub id: String,
    pub distance: f32,
    pub relative_position: [f32; 3],
    pub entity_type: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SensoryHit {
    pub distance: f32,
    pub normal: [f32; 3],
    pub material: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReceivedMessage {
    pub from: String,
    pub content: String,
    pub distance: f32,
}
