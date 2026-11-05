pub mod components;
pub mod genesis;
pub mod systems;

use bevy::prelude::*;

pub struct CoreSimulationPlugin;

impl Plugin for CoreSimulationPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, genesis::setup_genesis)
            .add_systems(
                FixedUpdate,
                (
                    systems::universe_tick_system,
                    systems::null_entity_metabolism_system,
                    systems::energy_metabolism_system,
                    systems::manifestation_execution_system,
                ),
            );
    }
}
