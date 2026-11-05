use bevy::prelude::*;
use serde::{Deserialize, Serialize};

/// Global universe state tracking ticks, entropy, and total conservation metrics.
#[derive(Resource, Debug, Clone, Serialize, Deserialize)]
pub struct NullUniverseState {
    pub tick: u64,
    pub entropy: f64,
    pub total_mass: f64,
    pub total_energy: f64,
    pub active_entities: usize,
    pub status: UniverseStatus,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum UniverseStatus {
    PrimordialVoid,
    ActiveSimulation,
    Paused,
    Frozen,
}

impl Default for NullUniverseState {
    fn default() -> Self {
        Self {
            tick: 0,
            entropy: 0.0,
            total_mass: 0.0,
            total_energy: 0.0,
            active_entities: 0,
            status: UniverseStatus::PrimordialVoid,
        }
    }
}

/// Setup system initializing the primordial void state (T=0).
pub fn setup_genesis(mut commands: Commands) {
    tracing::info!("Initializing Null Universe: Void state established (T=0)");
    commands.insert_resource(NullUniverseState::default());
}
