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
  

