use bevy::prelude::*;
use bevy_rapier3d::prelude::*;
use crate::core::components::*;

/// Raycasting perception system that simulates sensory probing of physical surroundings.
pub fn sensory_raycast_system(
    rapier_context: Query<&RapierContext>,
    mut agents: Query<(Entity, &GlobalTransform, &SensoryArray, &mut AgentPerception)>,
    targets: Query<(Entity, &GlobalTransform, &EntityId), Without<SensoryArray>>,
) {
    let Ok(context) = rapier_context.get_single() else {
        return;
    };

    for (agent_entity, transform, sensor, mut perception) in &mut agents {
        let origin = transform.translation();
        let forward = transform.forward();
        let mut hits = Vec::new();
        let mut visible = Vec::new();

        // 1. Arc-based sensory raycasting
        for i in 0..sensor.num_rays {
            let angle = if sensor.num_rays > 1 {
                -sensor.fov_radians / 2.0
                    + (sensor.fov_radians / (sensor.num_rays as f32 - 1.0)) * (i as f32)
            } else {
                0.0
            };

            let ray_dir = Quat::from_rotation_y(angle) * forward;

            if let Some((_hit_entity, intersection)) = context.cast_ray_and_get_normal(
                origin,
                ray_dir,
                sensor.range,
                true,
                QueryFilter::default().exclude_collider(agent_entity),
            ) {
                hits.push(SensoryHit {
                    distance: intersection.time_of_impact,
                    normal: [
                        intersection.normal.x,
                        intersection.normal.y,
                        intersection.normal.z,
                    ],
                    material: "solid".into(),
                });
            }
        }

        // 2. Line-of-sight check to nearby entities
        for (target_entity, target_transform, target_id) in &targets {
            let target_pos = target_transform.translation();
            let dist = origin.distance(target_pos);

            if dist <= sensor.range {
                let dir = (target_pos - origin).normalize();
                if let Some((hit_entity, _)) = context.cast_ray(
                    origin,
                    dir,
                    dist,
                    true,
                    QueryFilter::default().exclude_collider(agent_entity),
                ) {
                    if hit_entity == target_entity {
                        visible.push(ObservedEntity {
                            id: target_id.0.clone(),
                            distance: dist,
                            relative_position: [
                                target_pos.x - origin.x,
                                target_pos.y - origin.y,
                                target_pos.z - origin.z,
                            ],
                            entity_type: "object".into(),
                        });
                    }
                }
            }
        }

        perception.sensory_points = hits;
        perception.visible_entities = visible;
    }
}
