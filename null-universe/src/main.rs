use bevy::prelude::*;

mod core;
mod physics;
mod ipc;

use crate::core::CoreSimulationPlugin;
use crate::physics::PhysicsSimulationPlugin;
use crate::ipc::IpcPlugin;

fn main() {
    tracing_subscriber::fmt::init();
    tracing::info!(">>> Starting Null Universe Simulation Engine <<<");

    App::new()
        // Headless execution: minimal runner, no window, no GPU context required
        .add_plugins(MinimalPlugins)
        // Core Null Universe genesis, state tracking, and metabolism
        .add_plugins(CoreSimulationPlugin)
        // Rapier 3D physics, collision handling, and raycast perception
        .add_plugins(PhysicsSimulationPlugin)
        // OpenSandbox IPC bridge for agent interaction
        .add_plugins(IpcPlugin)
        .run();
}
