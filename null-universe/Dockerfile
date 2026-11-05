# Stage 1: Build Null Universe Engine with Rust & Cargo
FROM rust:1.80-slim as builder

WORKDIR /usr/src/null-universe
COPY Cargo.toml ./
# Cache dependencies
RUN mkdir src && echo "fn main() {}" > src/main.rs && cargo build --release || true

# Copy actual source code and compile
COPY src ./src
RUN cargo build --release

# Stage 2: Minimal OpenSandbox runtime image
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /usr/src/null-universe/target/release/null-universe /app/null-universe

# Expose IPC socket mount directory
VOLUME ["/var/run/null-universe"]

ENV RUST_LOG=info
ENTRYPOINT ["/app/null-universe"]
