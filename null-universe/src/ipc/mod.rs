pub mod protocol;
pub mod server;

use bevy::prelude::*;

pub struct IpcPlugin;

impl Plugin for IpcPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, server::setup_ipc_channels)
            .add_systems(FixedUpdate, server::process_inbound_actions);
    }
}
