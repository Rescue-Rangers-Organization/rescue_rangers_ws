#!/usr/bin/env python3

import sys
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SyncVelocityCommander(Node):
    def __init__(self) -> None:
        super().__init__("sync_velocity_commander")
        self.front_pub = self.create_publisher(Twist, "/front/cmd_vel", 10)
        self.rear_pub = self.create_publisher(Twist, "/rear/cmd_vel", 10)
        self.get_logger().info("Sync velocity commander started")

    def publish_both(self, linear_x: float, angular_z: float) -> None:
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.angular.z = float(angular_z)
        self.front_pub.publish(msg)
        self.rear_pub.publish(msg)

    def send_for_duration(self, linear_x: float, angular_z: float, duration: float, rate_hz: float = 10.0) -> None:
        period = 1.0 / rate_hz
        end_time = time.time() + duration
        while rclpy.ok() and time.time() < end_time:
            self.publish_both(linear_x, angular_z)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(period)
        self.stop()

    def stop(self) -> None:
        self.publish_both(0.0, 0.0)


def main() -> None:
    rclpy.init()
    node = SyncVelocityCommander()

    try:
        if len(sys.argv) < 2:
            node.get_logger().info(
                "Usage:\n"
                "  ros2 run robot_controls sync_velocity_commander forward\n"
                "  ros2 run robot_controls sync_velocity_commander backward\n"
                "  ros2 run robot_controls sync_velocity_commander stop\n"
                "  ros2 run robot_controls sync_velocity_commander custom 0.4 0.0 2.0"
            )
            return

        command = sys.argv[1].lower()

        if command == "forward":
            node.send_for_duration(0.4, 0.0, 2.0)
        elif command == "backward":
            node.send_for_duration(-0.4, 0.0, 2.0)
        elif command == "left":
            node.send_for_duration(0.0, 0.8, 4.0)
        elif command == "right":
            node.send_for_duration(0.0, -0.8, 4.0)
        elif command == "stop":
            node.stop()
        elif command == "custom":
            linear_x = float(sys.argv[2])
            angular_z = float(sys.argv[3])
            duration = float(sys.argv[4])
            node.send_for_duration(linear_x, angular_z, duration)
        else:
            raise ValueError(f"Unknown command: {command}")

    except Exception as exc:
        node.get_logger().error(str(exc))
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()