use serde::{Deserialize, Serialize};
use crate::core::components::{
    AgentPerception, EnergyStore, Inventory, ManifestationBlueprint, NullEnergyBalance,
    NullPerception, OperatorBinding,
};

/// Inbound action from an operator (User or AI Agent) into the Null Universe.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "payload")]
pub enum AgentAction {
    /// Materialize standard agent
    Materialize {
        agent_id: String,
        position: [f32; 3],
    },
    /// Materialize a native Null Entity
    MaterializeNullEntity {
        entity_id: String,
        position: [f32; 3],
        consciousness_frequency: f32,
        operator: Option<OperatorBinding>,
    },
    /// Direct command from the user or an AI agent via the user to manifest a blueprint
    CommandManifestation {
        entity_id: String,
        operator_id: String,
        blueprint: ManifestationBlueprint,
    },
    /// Kinematic movement
    Move {
        agent_id: String,
        direction: [f32; 3],
        speed: f32,
    },
    /// Null Entity: Cleanses local space back to zero
    NullifyDisturbance {
        entity_id: String,
        target_entity_id: String,
        absorption_power: f32,
    },
    /// Null Entity: Phase into pure vacuum state
    PhaseIntoVoid {
        entity_id: String,
        duration_ticks: u32,
    },
    /// Broadcast a message
    Broadcast {
        agent_id: String,
        message: String,
        radius: f32,
    },
}

/// Outbound state frame streamed from the simulation to an operator or agent.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AgentStateFrame {
    pub tick: u64,
    pub agent_id: String,
    pub position: [f32; 3],
    pub energy: EnergyStore,
    pub inventory: Inventory,
    pub perception: AgentPerception,
}

/// Outbound state frame streamed specifically to a Null Entity and its Operator.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NullEntityStateFrame {
    pub tick: u64,
    pub entity_id: String,
    pub operator_id: String,
    pub position: [f32; 3],
    pub null_balance: NullEnergyBalance,
    pub perception: NullPerception,
    pub total_manifestations: u64,
}
