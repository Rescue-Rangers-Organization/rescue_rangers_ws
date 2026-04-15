import threading
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

from dynamixel_sdk import PortHandler, PacketHandler


class ArmMotorNode(Node):
    def __init__(self):
        super().__init__('arm_motor_node')

        # -------- User settings --------
        self.device_name = '/dev/ttyUSB0'
        self.baudrate = 57600
        self.protocol_version = 2.0
        self.motor_ids = [6, 7, 8]

        # -------- Control table --------
        self.addr_operating_mode = 11
        self.addr_torque_enable = 512
        self.addr_goal_velocity = 552

        self.velocity_mode = 1
        self.torque_enable = 1
        self.torque_disable = 0

        # -------- SDK setup --------
        self.port = PortHandler(self.device_name)
        self.packet = PacketHandler(self.protocol_version)

        self.lock = threading.Lock()
        self.worker = None
        self.stop_event = threading.Event()

        self.open_and_setup_bus()

        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/arm_motor_command',
            self.command_callback,
            10
        )

        self.get_logger().info('arm_motor_node ready')

    def open_and_setup_bus(self):
        if not self.port.openPort():
            raise RuntimeError(f'Failed to open {self.device_name}')

        if not self.port.setBaudRate(self.baudrate):
            raise RuntimeError(f'Failed to set baudrate {self.baudrate}')

        for dxl_id in self.motor_ids:
            self.write1(dxl_id, self.addr_torque_enable, self.torque_disable)
            self.write1(dxl_id, self.addr_operating_mode, self.velocity_mode)
            self.write1(dxl_id, self.addr_torque_enable, self.torque_enable)

    def write1(self, dxl_id, addr, value):
        comm_result, dxl_error = self.packet.write1ByteTxRx(
            self.port, dxl_id, addr, value
        )
        if comm_result != 0:
            raise RuntimeError(
                f'ID {dxl_id} write1 failed: {self.packet.getTxRxResult(comm_result)}'
            )
        if dxl_error != 0:
            raise RuntimeError(
                f'ID {dxl_id} write1 packet error: {self.packet.getRxPacketError(dxl_error)}'
            )

    def write4(self, dxl_id, addr, value):
        comm_result, dxl_error = self.packet.write4ByteTxRx(
            self.port, dxl_id, addr, int(value)
        )
        if comm_result != 0:
            raise RuntimeError(
                f'ID {dxl_id} write4 failed: {self.packet.getTxRxResult(comm_result)}'
            )
        if dxl_error != 0:
            raise RuntimeError(
                f'ID {dxl_id} write4 packet error: {self.packet.getRxPacketError(dxl_error)}'
            )

    def set_all_velocities(self, velocity):
        for dxl_id in self.motor_ids:
            self.write4(dxl_id, self.addr_goal_velocity, velocity)

    def stop_all(self):
        for dxl_id in self.motor_ids:
            self.write4(dxl_id, self.addr_goal_velocity, 0)

    def command_callback(self, msg):
        if len(msg.data) < 2:
            self.get_logger().error('Expected [velocity, duration_seconds]')
            return

        velocity = float(msg.data[0])
        duration = float(msg.data[1])

        self.get_logger().info(
            f'Received arm command velocity={velocity}, duration={duration}'
        )

        self.stop_event.set()
        if self.worker is not None and self.worker.is_alive():
            self.worker.join(timeout=1.0)

        self.stop_event.clear()
        self.worker = threading.Thread(
            target=self.run_command,
            args=(velocity, duration),
            daemon=True
        )
        self.worker.start()

    def run_command(self, velocity, duration):
        try:
            with self.lock:
                self.set_all_velocities(velocity)

            start = time.time()
            while time.time() - start < duration:
                if self.stop_event.is_set():
                    break
                time.sleep(0.05)

        except Exception as e:
            self.get_logger().error(str(e))

        finally:
            try:
                with self.lock:
                    self.stop_all()
            except Exception as e:
                self.get_logger().error(f'Failed to stop motors: {e}')

    def destroy_node(self):
        try:
            with self.lock:
                self.stop_all()
                for dxl_id in self.motor_ids:
                    self.write1(dxl_id, self.addr_torque_enable, self.torque_disable)
                self.port.closePort()
        except Exception:
            pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ArmMotorNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
        



if __name__ == '__main__':
    main()