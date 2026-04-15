#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import numpy as np
import pyroki as pk

from rpi_pkg import solve_ik
from yourdfpy import URDF
import os

from ament_index_python.packages import get_package_share_directory
import os

class IKNode(Node):
    def __init__(self):
        # Initialize node with the name 'dummy_node'
        super().__init__('ik_node')
        self.get_logger().info('IKNode has been started.')


        # Publishes String messages to 'dummy_topic' with a queue size of 10
        self.publisher_ = self.create_publisher(Float64MultiArray, 'arm_desired_angles_rad', 10)

        package_path = get_package_share_directory('rpi_pkg')
        workspace_root = os.path.abspath(os.path.join(package_path, '..', '..', '..', '..'))
        self.get_logger().info(workspace_root)
        urdf = URDF.load(fname_or_file=str(workspace_root + "/lib/rover_arm_urdf/RescueRangersArm.urdf"), 
                     mesh_dir=str(workspace_root + "/lib/rover_arm_urdf/RescueRangersArmMeshes"))
        self.robot = pk.Robot.from_urdf(urdf)
        self.target_link_name = "frame"
        

        self.subscription = self.create_subscription(
            Float64MultiArray,
            'arm_desired_pos_ori', # [x_pos, y_pos, z_pos, ori_w, ori_x, ori_y, ori_z]
            self.ik_callback,
            10)


    def ik_callback(self, msg):
        """Subscriber logic: processes incoming messages."""
        self.get_logger().info(f'Got target pos: {msg.data}')

        angles_rad : np.ndarray = solve_ik.solve_ik(
            robot=self.robot, target_link_name=self.target_link_name, target_position=np.array(msg.data[:3]), target_wxyz=np.array(msg.data[3:])
            )
        self.get_logger().info(f'Found target angles: {angles_rad.tolist()}')

        pub_msg = Float64MultiArray()
        pub_msg.data = angles_rad.tolist()
        self.publisher_.publish(pub_msg)
        

def main(args=None):
    rclpy.init(args=args)
    node = IKNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
