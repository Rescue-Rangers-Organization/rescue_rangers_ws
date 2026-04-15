cd rescue_rangers_ws
colcon build
source install/setup.bash
ros2 run rpi_pkg arm_motor_node
