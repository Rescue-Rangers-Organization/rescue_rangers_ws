```bash
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
cd DynamixelSDK/python
pip3 install .

# Verify
python3 -c "import dynamixel_sdk; print('ok')"

cd rescue_rangers_ws
colcon build
source install/setup.bash
export ROS_DOMAIN_ID=10

# Check port
ls /dev/ttyUSB*

ros2 run rpi_pkg arm_motor_node

ros2 topic pub --once /arm_motor_command std_msgs/msg/Float32MultiArray "{data: [700.0, 5.0]}"
```

- Note: velocity = 700 and time = 5 secs
  
## Testing ik node
After installing pyroki, setting up venv, activating
```[bash]
python3 -m colcon build --symlink-install
source install/setup.bash
ros2 run rpi_pkg ik_node

# in one terminal
ros2 topic echo /arm_desired_angles_rad

# in another terminal
ros2 topic pub --once /arm_desired_pos_ori std_msgs/msg/Float64MultiArray "{data: [0.5, 0.0, 0.5, 0, 0, 1, 0]}"
```

You should see something similar to the following:
```[bash]
layout:
  dim: []
  data_offset: 0
data:
- 0.15377405285835266
- 1.572248935699463
- -0.14610835909843445
- -1.5708003044128418
- -0.148228719830513
- 1.4170541763305664
---
```