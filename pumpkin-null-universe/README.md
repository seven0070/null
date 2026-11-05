# Pumpkin-Hosted Null Universe

Host the **Null Universe** inside a blazingly fast [Pumpkin](https://github.com/Pumpkin-MC/Pumpkin) voxel world with **zero dependencies, no Java, and a single binary**.

---

## Why Pumpkin Replaces Heavy Toolchains

* **Single Executable**: No compiling massive Rust crates from source, no Docker, no Firecracker microVMs. Just one pre-compiled file: `./pumpkin`.
* **Instant 3D Voxel Void**: Automatically starts at $T_0$ in a pure vacuum world (air coordinates).
* **Cross-Play Out of the Box**: Supports both Minecraft Java Edition (PC/Mac/Linux) and Bedrock Edition (iOS/Android/Windows/Consoles) simultaneously.
* **Direct RCON Control**: Control Null Entities and manifest structures in real time via standard Python scripts.

---

## 1-Minute Setup Guide

### 1. Download the Standalone Pumpkin Binary
Download the pre-compiled binary for your operating system from [Pumpkin Releases](https://github.com/Pumpkin-MC/Pumpkin/releases) or [pumpkinmc.org](https://pumpkinmc.org/download/):

* **Linux (x86_64 / aarch64)**:
  ```bash
  curl -L -o pumpkin https://github.com/Pumpkin-MC/Pumpkin/releases/latest/download/pumpkin-linux-x86_64
  chmod +x pumpkin
  ```
* **macOS (Apple Silicon / Intel)**:
  ```bash
  curl -L -o pumpkin https://github.com/Pumpkin-MC/Pumpkin/releases/latest/download/pumpkin-darwin-arm64
  chmod +x pumpkin
  ```
* **Windows**:
  Download `pumpkin-windows-x86_64.exe` from the releases page.

---

### 2. Launch the Null Universe Server
Place the `pumpkin` executable inside this folder alongside `configuration.toml` and start it:

```bash
./pumpkin
```

The server will initialize immediately:
* **Java Server**: `127.0.0.1:25565`
* **Bedrock Server**: `127.0.0.1:19132`
* **RCON Gateway**: `127.0.0.1:25575`

---

### 3. Connect to the World
Open standard Minecraft on your PC, Mac, or phone:
* **Direct Connect**: `127.0.0.1` (or your local IP)
* You will spawn inside the pristine void at $(0, 64, 0)$.

---

### 4. Command the Null Entities
In a separate terminal, run the Null Entity controller:

```bash
python3 pumpkin_agent.py
```

This script connects via RCON and allows you or an AI agent to:
1. Initialize the void anchor at $(0, 64, 0)$.
2. Manifest physical monoliths and shelters out of obsidian or deepslate.
3. Materialize discrete math graphs (like a 3D Complete Graph $K_5$) using glowing sea lanterns and end rods.
4. Execute nullification pulses that cleanse physical matter back to pure air.
