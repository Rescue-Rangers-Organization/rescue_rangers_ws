#!/usr/bin/env python3

import sys
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityCommander(Node):
    def __init__(self) -> None:
        super().__init__("velocity_commander")
        self.publisher_ = self.create_publisher(Twist, "/cmd_vel", 10)
        self.get_logger().info("Velocity commander started")

    def send_velocity(self, linear_x: float, angular_z: float) -> None:
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.angular.z = float(angular_z)
        self.publisher_.publish(msg)
        self.get_logger().info(
            f"Published cmd_vel: linear.x={linear_x:.3f}, angular.z={angular_z:.3f}"
        )

    def send_for_duration(
        self,
        linear_x: float,
        angular_z: float,
        duration_sec: float,
        rate_hz: float = 10.0,
    ) -> None:
        period = 1.0 / rate_hz
        end_time = time.time() + duration_sec

        while rclpy.ok() and time.time() < end_time:
            self.send_velocity(linear_x, angular_z)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(period)

        self.stop()

    def stop(self) -> None:
        msg = Twist()
        self.publisher_.publish(msg)
        self.get_logger().info("Published STOP command")


def main() -> None:
    rclpy.init()
    node = VelocityCommander()

    try:
        if len(sys.argv) < 2:
            node.get_logger().info(
                "Usage examples:\n"
                "  ros2 run robot_controls velocity_commander forward\n"
                "  ros2 run robot_controls velocity_commander backward\n"
                "  ros2 run robot_controls velocity_commander stop\n"
                "  ros2 run robot_controls velocity_commander custom 0.5 0.0 2.0"
            )
            return

        command = sys.argv[1].lower()

        if command == "forward":
            node.send_for_duration(0.5, 0.0, 2.0)
        elif command == "backward":
            node.send_for_duration(-0.5, 0.0, 2.0)
        elif command == "left":
            node.send_for_duration(0.0, 0.8, 2.0)
        elif command == "right":
            node.send_for_duration(0.0, -0.8, 2.0)
        elif command == "stop":
            node.stop()
        elif command == "custom":
            if len(sys.argv) != 5:
                raise ValueError("custom requires: linear_x angular_z duration_sec")
            linear_x = float(sys.argv[2])
            angular_z = float(sys.argv[3])
            duration_sec = float(sys.argv[4])
            node.send_for_duration(linear_x, angular_z, duration_sec)
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