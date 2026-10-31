
#!/usr/bin/env python3

import math
import time

import rclpy
import serial

from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, UInt32
from rclpy.node import Node
from tf2_ros import TransformBroadcaster


class VayronSerialBridge(Node):
    """Serial interface for VAYRON Arduino motor controller."""

    def __init__(self):
        super().__init__('vayron_serial_bridge')

        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 115200)
        self.declare_parameter('wheel_separation', 0.3429)
        self.declare_parameter('wheel_radius', 0.0325)
        self.declare_parameter('max_linear_speed', 0.25)
        self.declare_parameter('cmd_vel_topic', '/cmd_vel_safe')
        self.declare_parameter('command_timeout', 0.5)
        self.declare_parameter('reconnect_interval', 2.0)
        self.declare_parameter('publish_odom', True)

        self.wheel_separation = float(
            self.get_parameter('wheel_separation').value
        )
        self.wheel_radius = float(
            self.get_parameter('wheel_radius').value
        )
        self.max_linear_speed = float(
            self.get_parameter('max_linear_speed').value
        )
        self.command_timeout = float(
            self.get_parameter('command_timeout').value
        )
        self.reconnect_interval = float(
            self.get_parameter('reconnect_interval').value
        )

        self.port = self.get_parameter('port').value
        self.baud_rate = int(
            self.get_parameter('baud_rate').value
        )

        self.serial_port = None
        self.last_reconnect = 0.0
        self.last_command_time = time.monotonic()
        self.last_odom_time = time.monotonic()

        self.linear = 0.0
        self.angular = 0.0

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.pulse_count = 0
        self.front_left_rpm = 0.0

        self.odom_pub = self.create_publisher(
            Odometry, '/odom', 10
        )

        self.rpm_pub = self.create_publisher(
            Float32, '/wheel_rpm/front_left', 10
        )

        self.ticks_pub = self.create_publisher(
            UInt32, '/wheel_ticks/front_left', 10
        )

        self.tf_broadcaster = TransformBroadcaster(self)

        self.create_subscription(
            Twist,
            self.get_parameter('cmd_vel_topic').value,
            self.cmd_callback,
            10,
        )

        self.timer = self.create_timer(0.05, self.update)

        self.get_logger().info(
            'VAYRON serial bridge initialized.'
        )

    def connect_serial(self):
        if self.serial_port is not None:
            return

        now = time.monotonic()

        if now - self.last_reconnect < self.reconnect_interval:
            return

        self.last_reconnect = now

        try:
            self.serial_port = serial.Serial(
                self.port,
                self.baud_rate,
                timeout=0.01,
                write_timeout=0.1,
            )

            self.get_logger().info(
                f'Connected to Arduino: {self.port}'
            )

        except (serial.SerialException, OSError, ValueError) as exc:
            self.get_logger().warning(
                f'Arduino connection unavailable: {exc}'
            )

    def disconnect_serial(self):
        if self.serial_port is not None:
            try:
                self.serial_port.close()
            except (serial.SerialException, OSError):
                pass

            self.serial_port = None

    def cmd_callback(self, msg):
        values = (
            msg.linear.x,
            msg.angular.z,
        )

        if not all(math.isfinite(value) for value in values):
            self.linear = 0.0
            self.angular = 0.0
            return

        self.linear = max(
            -self.max_linear_speed,
            min(self.max_linear_speed, msg.linear.x),
        )

        self.angular = max(
            -1.5,
            min(1.5, msg.angular.z),
        )

        self.last_command_time = time.monotonic()

    def send_motor_command(self):
        age = time.monotonic() - self.last_command_time

        if age > self.command_timeout:
            left = 0.0
            right = 0.0
        else:
            half_track = self.wheel_separation / 2.0

            left = (
                self.linear - self.angular * half_track
            ) / self.max_linear_speed

            right = (
                self.linear + self.angular * half_track
            ) / self.max_linear_speed

            scale = max(1.0, abs(left), abs(right))

            left /= scale
            right /= scale

        if self.serial_port is None:
            return

        packet = f'M,{left:.3f},{right:.3f}\n'

        try:
            self.serial_port.write(packet.encode('ascii'))

        except (serial.SerialException, OSError) as exc:
            self.get_logger().error(
                f'Serial transmission failed: {exc}'
            )
            self.disconnect_serial()

    def read_sensor_feedback(self):
        if self.serial_port is None:
            return

        try:
            while self.serial_port.in_waiting:
                line = self.serial_port.readline().decode(
                    'ascii', errors='ignore'
                ).strip()

                if not line:
                    continue

                fields = line.split(',')

                if len(fields) == 3 and fields[0] == 'E':
                    count = int(fields[1])
                    rpm = float(fields[2])

                    if count < 0 or not math.isfinite(rpm):
                        continue

                    if count > 0xFFFFFFFF:
                        continue

                    self.pulse_count = count
                    self.front_left_rpm = rpm

                    ticks = UInt32()
                    ticks.data = self.pulse_count
                    self.ticks_pub.publish(ticks)

                    rpm_msg = Float32()
                    rpm_msg.data = self.front_left_rpm
                    self.rpm_pub.publish(rpm_msg)

                elif line.startswith('S,'):
                    self.get_logger().debug(
                        f'Arduino status: {line}'
                    )

        except (serial.SerialException, OSError) as exc:
            self.get_logger().error(
                f'Serial reception failed: {exc}'
            )
            self.disconnect_serial()

        except (ValueError, IndexError):
            self.get_logger().warning(
                'Malformed Arduino feedback ignored.'
            )

    def publish_odometry(self, dt):
        if dt <= 0.0 or dt > 0.2:
            return

        age = time.monotonic() - self.last_command_time

        v = self.linear if age <= self.command_timeout else 0.0
        w = self.angular if age <= self.command_timeout else 0.0

        self.x += v * math.cos(self.yaw) * dt
        self.y += v * math.sin(self.yaw) * dt

        self.yaw = math.atan2(
            math.sin(self.yaw + w * dt),
            math.cos(self.yaw + w * dt),
        )

        stamp = self.get_clock().now().to_msg()

        odom = Odometry()
        odom.header.stamp = stamp
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y

        odom.pose.pose.orientation.z = math.sin(self.yaw / 2.0)
        odom.pose.pose.orientation.w = math.cos(self.yaw / 2.0)

        odom.twist.twist.linear.x = v
        odom.twist.twist.angular.z = w

        # Command-derived estimate, not encoder-measured odometry.
        odom.pose.covariance[0] = 0.1
        odom.pose.covariance[7] = 0.1
        odom.pose.covariance[35] = 0.2

        self.odom_pub.publish(odom)

        transform = TransformStamped()
        transform.header.stamp = stamp
        transform.header.frame_id = 'odom'
        transform.child_frame_id = 'base_footprint'

        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y

        transform.transform.rotation.z = math.sin(self.yaw / 2.0)
        transform.transform.rotation.w = math.cos(self.yaw / 2.0)

        self.tf_broadcaster.sendTransform(transform)

    def update(self):
        now = time.monotonic()

        dt = now - self.last_odom_time
        self.last_odom_time = now

        self.connect_serial()
        self.send_motor_command()
        self.read_sensor_feedback()

        if self.get_parameter('publish_odom').value:
            self.publish_odometry(dt)

    def destroy_node(self):
        if self.serial_port is not None:
            try:
                self.serial_port.write(
                    b'M,0.000,0.000\n'
                )
            except (serial.SerialException, OSError):
                pass

            self.disconnect_serial()

        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = VayronSerialBridge()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
