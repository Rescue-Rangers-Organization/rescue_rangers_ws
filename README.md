# rescue_rangers_ws
ROS2 workspace for Rice University Rescue Rangers Senior Design Team's rover robot. 

## Workspace Structure
rescue_rangers_ws
-  (ignored) build :arrow_right: where intermediate files are stored on colcon build
- (ignored) install :arrow_right: where each package will be installed to on colcon build
- (ignored) log :arrow_right: logs - kinda useless
- src :arrow_right: where we write code that will be compiled on colcon build

## Package Structure (under development)
- rover_description :arrow_right: URDF / Mujoco Files for Simulation & IK. Note this is an imported repo! Link to repo can be found [here](https://github.com/Rescue-Rangers-Organization/rover_description)
- rpi_pkg :arrow_right: package containing nodes for the rpi, such as drivetrain & arm control
- jetson_pkg :arrow_right: package containing nodes for the jetson, such as mapping & camera streaming
- station_pkg :arrow_right: package containing nodes for the control station, such as xbox controller


## Building and Running
Setup / Sourcing:
```[bash]
git clone <this repo>
cd rescue_rangers_ws
colcon build
source install/setup.bash
```
