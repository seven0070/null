use bevy::prelude::*;
use std::sync::mpsc::{channel, Receiver, Sender};
use crate::ipc::protocol::AgentAction;

#[derive(Resource)]
pub struct ActionReceiver(pub Receiver<AgentAction>);

#[derive(Resource)]
pub struct ActionSender(pub Sender<AgentAction>);

/// Sets up the in-memory/IPC queue for receiving agent requests.
pub fn setup_ipc_channels(mut commands: Commands) {
    let (tx, rx) = channel::<AgentAction>();
    commands.insert_resource(ActionReceiver(rx));
    commands.insert_resource(ActionSender(tx));
    tracing::info!("IPC event channels initialized for OpenSandbox integration");
}

/// Drains incoming actions and applies them to Bevy entities and Rapier components.
pub fn process_inbound_actions(
    receiver: Res<ActionReceiver>,
    mut commands: Commands,
) {
    while let Ok(action) = receiver.0.try_recv() {
        match action {
            AgentAction::Materialize { agent_id, position } => {
                tracing::info!("Materializing agent {} at {:?}", agent_id, position);
                // Spawning agent in Bevy ECS with Rapier collider
                commands.spawn((
                    Transform::from_xyz(position[0], position[1], position[2]),
                    crate::core::components::EntityId(agent_id),
                    crate::core::components::SensoryArray::default(),
                    crate::core::components::AgentPerception::default(),
                    crate::core::components::EnergyStore {
                        current: 100.0,
                        max: 100.0,
                        recharge_rate: 0.1,
                    },
                    crate::core::components::Inventory::default(),
                    crate::core::components::Matter {
                        mass: 70.0,
                        density: 1.0,
                        energy: 100.0,
                    },
                ));
            }
            _ => {
                // Action handling for movement and construction
            }
        }
    }
}
