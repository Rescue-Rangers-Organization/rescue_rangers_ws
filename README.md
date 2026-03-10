# rescue_rangers_ws
ROS2 workspace for Rice University Rescue Rangers Senior Design Team's rover robot. 

## Workspace Structure
rescue_rangers_ws
-  (ignored) build :right_arrow: where intermediate files are stored on colcon build
- (ignored) install :right_arrow: where each package will be installed to on colcon build
- (ignored) log :right_arrow: logs - kinda useless
- src :right_arrow: where we write code that will be compiled on colcon build

## Package Structure (under development)
- rover_description :right_arrow: URDF / Mujoco Files for Simulation & IK
- rpi_pkg :right_arrow: package containing nodes for the rpi, such as drivetrain &amp arm control
- jetson_pkg :right_arrow: package containing nodes for the jetson, such as mapping & camera streaming
- station_pkg :right_arrow: package containing nodes for the control station, such as xbox controller
