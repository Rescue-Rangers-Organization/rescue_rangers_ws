"""IK with Collision

Basic Inverse Kinematics with Collision Avoidance using PyRoKi.
"""

import json
import time
from pathlib import Path

import numpy as np
import pyroki as pk
import viser
from viser.extras import ViserUrdf

import solve_ik
from yourdfpy import URDF
import os


def main(urdf):
    """Main function for basic IK with collision."""

    # urdf = load_robot_description("panda_description")
    target_link_name = "frame"
    robot = pk.Robot.from_urdf(urdf)

    # Set up visualizer.
    server = viser.ViserServer()
    server.scene.add_grid("/ground", width=2, height=2, cell_size=0.1)
    urdf_vis = ViserUrdf(server, urdf, root_node_name="/robot")

    # Create interactive controller for IK target.
    ik_target_handle = server.scene.add_transform_controls(
        "/ik_target", scale=0.2, position=(0.5, 0.0, 0.5), wxyz=(0, 0, 1, 0)
    )

    timing_handle = server.gui.add_number("Elapsed (ms)", 0.001, disabled=True)

    while True:
        start_time = time.time()

        solution = solve_ik.solve_ik(
            robot=robot,
            target_link_name=target_link_name,
            target_position=np.array(ik_target_handle.position),
            target_wxyz=np.array(ik_target_handle.wxyz),
        )
        # print(solution)

        # Update timing handle.
        timing_handle.value = (time.time() - start_time) * 1000

        # Update visualizer - collision meshes inherit these transforms automatically.
        urdf_vis.update_cfg(solution)


if __name__ == "__main__":
    parent = os.path.dirname(os.path.abspath(__file__))
    urdf = (URDF.load((parent + "/rover_arm_urdf/RescueRangersArm.urdf"), 
                     mesh_dir=(parent + "/rover_arm_urdf/RescueRangersArmMeshes")))
    main(urdf)
