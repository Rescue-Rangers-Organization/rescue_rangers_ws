from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    front_node = Node(
        package="basicmicro_ros2",
        executable="basicmicro_node.py",
        namespace="front",
        name="basicmicro_node",
        output="screen",
        parameters=[
            {
                "port": "/dev/roboclaw_front",
                "baud": 38400,
                "address": 128,
                "wheel_radius": 0.1,
                "wheel_separation": 0.3,
                "encoder_counts_per_rev": 1000,
                "gear_ratio": 1.0,
            }
        ],
    )

    rear_node = Node(
        package="basicmicro_ros2",
        executable="basicmicro_node.py",
        namespace="rear",
        name="basicmicro_node",
        output="screen",
        parameters=[
            {
                "port": "/dev/roboclaw_rear",
                "baud": 38400,
                "address": 128,
                "wheel_radius": 0.1,
                "wheel_separation": 0.3,
                "encoder_counts_per_rev": 1000,
                "gear_ratio": 1.0,
            }
        ],
    )

    return LaunchDescription([
        front_node,
        rear_node,
    ])