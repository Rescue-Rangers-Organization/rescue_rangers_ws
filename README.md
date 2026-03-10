# rescue_rangers_ws
ROS2 workspace for Rice University Rescue Rangers Senior Design Team's rover robot. 

## Workspace Structure
rescue_rangers_ws
-  (ignored) build :arrow_right: where intermediate files are stored on colcon build
- (ignored) install :arrow_right: where each package will be installed to on colcon build
- (ignored) log :arrow_right: logs - kinda useless
- src :arrow_right: where we write code that will be compiled on colcon build

## Package Structure (under development)
- rover_description :arrow_right: URDF / Mujoco Files for Simulation & IK
- rpi_pkg :arrow_right: package containing nodes for the rpi, such as drivetrain &amp arm control
- jetson_pkg :arrow_right: package containing nodes for the jetson, such as mapping & camera streaming
- station_pkg :arrow_right: package containing nodes for the control station, such as xbox controller
