# ros2_course_nav2

Autonomous navigation package for `ros2_course` robot using Gazebo Harmonic, SLAM Toolbox, and Nav2.

## Online Mapping + Navigation

```bash
ros2 launch ros2_course_nav2 autonomous_sim.launch.py
```

## Save Map

```bash
ros2 launch ros2_course_nav2 save_map.launch.py map_name:=course_map
```

This saves:
- `maps/course_map.pgm`
- `maps/course_map.yaml`

## Localization + Saved Map Navigation

```bash
ros2 launch ros2_course_nav2 localization_sim.launch.py
```

To load a different map file:

```bash
ros2 launch ros2_course_nav2 localization_sim.launch.py map:=/absolute/path/to/map.yaml
```
