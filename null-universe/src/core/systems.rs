use bevy::prelude::*;
use bevy_rapier3d::prelude::*;
use crate::core::components::*;
use crate::core::genesis::NullUniverseState;

/// System that executes approved manifestation intents into real Bevy + Rapier entities.
pub fn manifestation_execution_system(
    mut commands: Commands,
    mut universe: ResMut<NullUniverseState>,
    mut intents: Query<(Entity, &ManifestationIntent)>,
    mut powers: Query<(&mut ManifestationPower, &OperatorBinding)>,
) {
    for (intent_entity, intent) in &mut intents {
        // Find matching manifestation power for the creator
        for (mut power, operator) in &mut powers {
            if operator.operator_id == intent.authorized_by || operator.authorized_manifestations.contains(&"all".into()) {
                power.total_manifestations_created += 1;

                match &intent.blueprint {
                    ManifestationBlueprint::PhysicalConstruct {
                        name,
                        shape,
                        position,
                        mass,
                        energy,
                        is_fixed,
                    } => {
                        let pos = Vec3::new(position[0], position[1], position[2]);
                        let body_type = if *is_fixed {
                            RigidBody::Fixed
                        } else {
                            RigidBody::Dynamic
                        };

                        let collider = match shape {
                            ConstructShape::Cuboid { half_extents } => {
                                Collider::cuboid(half_extents[0], half_extents[1], half_extents[2])
                            }
                            ConstructShape::Sphere { radius } => Collider::ball(*radius),
                            ConstructShape::Capsule { half_height, radius } => {
                                Collider::capsule_y(*half_height, *radius)
                            }
                            ConstructShape::Pyramid { base_width, height } => {
                                Collider::cone(*height, *base_width / 2.0)
                            }
                        };

                        commands.spawn((
                            Transform::from_translation(pos),
                            body_type,
                            collider,
                            EntityId(name.clone()),
                            Matter {
                                mass: *mass,
                                density: 1.0,
                                energy: *energy,
                            },
                            ManifestedMetadata {
                                creator_id: intent.source_entity.clone(),
                                operator_id: intent.authorized_by.clone(),
                                manifested_tick: universe.tick,
                                blueprint_type: "PhysicalConstruct".into(),
                            },
                        ));

                        tracing::info!(
                            "[{:04} Tick] Manifested Physical Construct '{}' at {:?} via Operator '{}'",
                            universe.tick,
                            name,
                            pos,
                            intent.authorized_by
                        );
                    }
                    ManifestationBlueprint::DiscreteMathGraph {
                        name,
                        topology,
                        nodes,
                        origin,
                        scale,
                    } => {
                        let center = Vec3::new(origin[0], origin[1], origin[2]);
                        let node_count = *nodes;

                        // Spawn graph nodes along geometric topology
                        for i in 0..node_count {
                            let angle = (i as f32 / node_count as f32) * std::f32::consts::TAU;
                            let node_pos = center + Vec3::new(angle.cos() * scale, 0.0, angle.sin() * scale);

                            commands.spawn((
                                Transform::from_translation(node_pos),
                                RigidBody::Fixed,
                                Collider::ball(0.2),
                                EntityId(format!("{}_Node_{}", name, i)),
                                ManifestedMetadata {
                                    creator_id: intent.source_entity.clone(),
                                    operator_id: intent.authorized_by.clone(),
                                    manifested_tick: universe.tick,
                                    blueprint_type: format!("MathGraph::{:?}", topology),
                                },
                            ));
                        }

                        tracing::info!(
                            "[{:04} Tick] Manifested Discrete Math Graph '{}' ({:?}, {} nodes) via Operator '{}'",
                            universe.tick,
                            name,
                            topology,
                            node_count,
                            intent.authorized_by
                        );
                    }
                    ManifestationBlueprint::FieldEmitter {
                        name,
                        field_type,
                        center,
                        radius,
                        intensity,
                    } => {
                        let pos = Vec3::new(center[0], center[1], center[2]);
                        commands.spawn((
                            Transform::from_translation(pos),
                            Collider::ball(*radius),
                            Sensor,
                            EntityId(name.clone()),
                            ManifestedMetadata {
                                creator_id: intent.source_entity.clone(),
                                operator_id: intent.authorized_by.clone(),
                                manifested_tick: universe.tick,
                                blueprint_type: format!("FieldEmitter::{:?} (intensity: {})", field_type, intensity),
                            },
                        ));

                        tracing::info!(
                            "[{:04} Tick] Manifested Field Emitter '{}' ({:?}) via Operator '{}'",
                            universe.tick,
                            name,
                            field_type,
                            intent.authorized_by
                        );
                    }
                    _ => {}
                }
            }
        }

        // Clean up intent entity once fulfilled
        commands.entity(intent_entity).despawn();
    }
}

/// Advance universe clock and metrics.
pub fn universe_tick_system(
    mut universe: ResMut<NullUniverseState>,
    query: Query<(&Matter, Option<&EnergyStore>)>,
    null_entities: Query<&NullEnergyBalance>,
) {
    universe.tick += 1;

    let mut total_mass = 0.0f64;
    let mut total_energy = 0.0f64;
    let mut entity_count = 0;

    for (matter, energy_opt) in &query {
        total_mass += matter.mass as f64;
        let eng = energy_opt.map_or(0.0, |e| e.current);
        total_energy += (matter.energy + eng) as f64;
        entity_count += 1;
    }

    universe.total_mass = total_mass;
    universe.total_energy = total_energy;
    universe.active_entities = entity_count + null_entities.iter().count();

    let null_damping: f64 = null_entities
        .iter()
        .map(|b| (b.void_resonance * 0.0005) as f64)
        .sum();

    let entropy_increase = (0.0001 * (entity_count as f64)) - null_damping;
    universe.entropy = (universe.entropy + entropy_increase).max(0.0);
}

/// Metabolism system for Null Entities.
pub fn null_entity_metabolism_system(
    matter_query: Query<(&GlobalTransform, &Matter)>,
    mut null_query: Query<(
        Entity,
        &GlobalTransform,
        &VoidSensor,
        &mut NullEnergyBalance,
        &mut NullPerception,
    )>,
) {
    for (_null_ent, null_trans, sensor, mut balance, mut perception) in &mut null_query {
        let null_pos = null_trans.translation();
        let mut local_disturbance = 0.0f32;
        let mut disturbances = Vec::new();

        for (matter_trans, matter) in &matter_query {
            let matter_pos = matter_trans.translation();
            let dist = null_pos.distance(matter_pos);

            if dist <= sensor.detection_radius && dist > 0.001 {
                let perturbation = (matter.mass + matter.energy * 0.1) / (dist * dist);
                local_disturbance += perturbation;

                disturbances.push(VoidDisturbance {
                    entity_id: "matter_perturbation".into(),
                    perturbation_magnitude: perturbation,
                    distance: dist,
                    relative_position: [
                        matter_pos.x - null_pos.x,
                        matter_pos.y - null_pos.y,
                        matter_pos.z - null_pos.z,
                    ],
                });
            }
        }

        if local_disturbance < 0.01 {
            balance.zero_deviation = (balance.zero_deviation - balance.nullification_rate).max(0.0);
        } else {
            balance.zero_deviation += local_disturbance * sensor.sensitivity;
        }

        balance.void_resonance = (1.0 - (balance.zero_deviation / balance.collapse_threshold)).clamp(0.0, 1.0);
        perception.ambient_void_purity = (1.0 - (local_disturbance * 0.05)).clamp(0.0, 1.0);
        perception.perceived_disturbances = disturbances;
    }
}

/// Standard energy metabolism for positive-matter entities.
pub fn energy_metabolism_system(
    mut query: Query<&mut EnergyStore>,
) {
    for mut energy in &mut query {
        if energy.current < energy.max {
            energy.current = (energy.current + energy.recharge_rate).min(energy.max);
        }
    }
}
