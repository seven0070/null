pub mod rapier_setup;
pub mod sensory;

use bevy::prelude::*;
use bevy_rapier3d::prelude::*;

pub struct PhysicsSimulationPlugin;

impl Plugin for PhysicsSimulationPlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins(RapierPhysicsPlugin::<NoUserData>::default().in_fixed_schedule())
            .add_systems(Startup, rapier_setup::configure_rapier)
            .add_systems(FixedUpdate, sensory::sensory_raycast_system);
    }
}
