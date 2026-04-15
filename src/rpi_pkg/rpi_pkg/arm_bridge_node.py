#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray, Bool
from adafruit_servokit import ServoKit

class ArmBridgeNode(Node):
    def __init__(self):
        # Initialize node with the name 'dummy_node'
        super().__init__('arm_bridge_node')
        self.get_logger().info('ArmBridgeNode has been started.')

        # list of dynamixel obj with correct ids and whatnot
        self.dynamixels = []
        self.arm_desired_angles = []

        # Servo gripper state / obj
        self.kit = ServoKit(channels=16)
        self.gripper = self.kit.servo[0] # TODO change ID
        self.want_grip = False
        self.gripper_released_pos = 90
        self.gripper_closed_pos = 0

        # Publishes String messages to 'dummy_topic' with a queue size of 10
        self.publisher_ = self.create_publisher(String, 'dummy_topic', 10)
        
        # 2. Dummy Timer
        # Calls 'timer_callback' every 1.0 second
        self.timer_period = 0.1  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.count = 0

        # 3. Dummy Subscriber
        # Listens to 'input_topic' and calls 'listener_callback' when data arrives
        self.subscription = self.create_subscription(
            Float64MultiArray,
            'arm_desired_angles_rad',
            self.arm_angle_callback,
            10)

        self.subscription = self.create_subscription(
            Bool,
            'want_grip',
            self.gipper_callback,
            10)

    def timer_callback(self):
        """Timer logic: creates and publishes a message."""
        # msg = String()
        # msg.data = f'Dummy message #{self.count}'
        # self.publisher_.publish(msg)
        # self.get_logger().info(f'Publishing: "{msg.data}"')
        if len(self.arm_desired_angles) == len(self.dynamixels):
            for i in range(len(self.dynamixels)):
                self.dynamixels[i].set(self.arm_desired_angles[i])
        
        if self.want_grip:
            self.gripper.angle = (self.gripper_closed_pos)
        else:
            self.gripper.angle = (self.gripper_released_pos)
        
        self.count += 1


    def arm_angle_callback(self, msg):
        """Subscriber logic: processes incoming messages."""
        self.get_logger().info(f'Arm angles requested: "{msg.data}"')

        self.arm_desired_angles = msg.data


    def gipper_callback(self, msg):
        """Subscriber logic: processes incoming messages."""
        self.get_logger().info(f'Grip requested: "{msg.data}"')
        self.want_grip = msg.data


def main(args=None):
    rclpy.init(args=args)
    node = ArmBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
