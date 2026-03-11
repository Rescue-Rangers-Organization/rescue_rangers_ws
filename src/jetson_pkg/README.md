## Mapping & Odometry
Launching mapping node:
```[bash]
ros2 launch rtabmap_launch rtabmap.launch.py \
    rtabmap_args:="--delete_db_on_start" \
    use_sim_time:=false \
    rgbd_sync:=false \
    subscribe_scan:=true \
    frame_id:=base_link \
    scan_topic:=/scan \
    map_frame_id:=map \
    Grid/FromDepth:=false \
    rtabmapviz:=false
```

Use ```rtabmap-databaseViewer``` to open ```~/.ros/rtabmap.db``` to visualize or export the map.
