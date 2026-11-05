# Null Universe

A headless, deterministic simulation world running inside [OpenSandbox](https://github.com/opensandbox-group/OpenSandbox), powered by [Bevy](https://github.com/bevyengine/bevy) (ECS) and [Rapier](https://github.com/dimforge/rapier) (2D/3D physics).

## Core Architecture

- **Substrate**: OpenSandbox Firecracker microVM with snapshot/restore capabilities.
- **World Engine**: Headless Bevy ECS (tick schedule, entity registry, components, systems).
- **Physical Fabric**: Rapier 3D with rigid bodies, colliders, character controllers, and raycast sensory probing.
- **Agent IPC Bridge**: JSON-RPC and Unix domain sockets for agent perception streaming and action actuation.

## Directory Structure

```
null-universe/
├── Cargo.toml                  # Rust dependencies (Bevy, Rapier3D, Tokio, Serde)
├── Dockerfile                  # Multi-stage container build for OpenSandbox
├── sandbox.toml                # OpenSandbox deployment & snapshot config
├── README.md                   # Project overview & documentation
├── src/
│   ├── main.rs                 # Simulation engine entry point
│   ├── core/
│   │   ├── mod.rs              # Core simulation plugin
│   │   ├── genesis.rs          # Void state (T=0) & universe metrics
│   │   ├── components.rs       # ECS components (Matter, Agent, Sensory, Inventory)
│   │   └── systems.rs          # Thermodynamic tick & energy metabolism
│   ├── physics/
│   │   ├── mod.rs              # Physics plugin
│   │   ├── rapier_setup.rs     # Rapier 30Hz fixed timestep configuration
│   │   └── sensory.rs          # Raycast line-of-sight & obstacle occlusion
│   └── ipc/
│       ├── mod.rs              # IPC plugin
│       ├── protocol.rs         # Inbound actions & outbound state frames
│       └── server.rs           # Channel & socket processing system
└── scripts/
    └── harness.py              # Runnable test harness & prototype
```

## Running the Test Harness

```bash
python3 scripts/harness.py
```
