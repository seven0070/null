use bevy::prelude::*;
use bevy_rapier3d::prelude::*;

/// Configures Rapier 3D physics for headless, deterministic sandbox execution.
pub fn configure_rapier(mut config: ResMut<RapierConfiguration>) {
    // Gravitational constant inside the Null Universe
    config.gravity = Vec3::new(0.0, -9.81, 0.0);
    // Deterministic fixed timestep at 30 Hz with 2 sub-steps
    config.timestep_mode = TimestepMode::Fixed {
        dt: 1.0 / 30.0,
        substeps: 2,
    };
    tracing::info!("Rapier physics configured with deterministic fixed timestep (30 Hz)");
}
