
#!/usr/bin/env python3

import math

import rclpy
import serial
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry
from rclpy.node import Node
from tf2_ros import TransformBroadcaster


class VayronSerialBridge(Node):
    """Send skid-steer commands to Arduino and estimate open-loop odometry."""

    def __init__(self):
        super().__init__('vayron_serial_bridge')

        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 115200)
        self.declare_parameter('wheel_separation', 0.19)
        self.declare_parameter('max_linear_speed', 0.25)
        self.declare_parameter('cmd_vel_topic', '/cmd_vel_safe')
        self.declare_parameter('publish_odom', True)

        self.wheel_separation = float(
            self.get_parameter('wheel_separation').value
        )
        self.max_linear_speed = float(
            self.get_parameter('max_linear_speed').value
        )
        self.publish_odom = bool(
            self.get_parameter('publish_odom').value
        )

        self.serial_port = None
        self.last_cmd_time = self.get_clock().now()
        self.last_odom_time = self.get_clock().now()
        self.linear = 0.0
        self.angular = 0.0
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.create_subscription(
            Twist,
            self.get_parameter('cmd_vel_topic').value,
            self.cmd_callback,
            10,
        )

        try:
            self.serial_port = serial.Serial(
                self.get_parameter('port').value,
                int(self.get_parameter('baud_rate').value),
                timeout=0.02,
                write_timeout=0.1,
            )
            self.get_logger().info('Arduino serial connection opened.')
        except (serial.SerialException, ValueError) as exc:
            self.get_logger().error(
                f'Cannot open Arduino serial port: {exc}. '
                'Restart the node after resolving the connection.'
            )

        self.timer = self.create_timer(0.05, self.update)

    def cmd_callback(self, msg):
        self.last_cmd_time = self.get_clock().now()

        if not all(math.isfinite(v) for v in (
            msg.linear.x, msg.angular.z
        )):
            self.linear = 0.0
            self.angular = 0.0
            return

        self.linear = max(-self.max_linear_speed,
                          min(self.max_linear_speed, msg.linear.x))
        self.angular = max(-1.5, min(1.5, msg.angular.z))

    def update(self):
        now = self.get_clock().now()
        dt = (now - self.last_odom_time).nanoseconds / 1e9
        self.last_odom_time = now

        age = (now - self.last_cmd_time).nanoseconds / 1e9
        v = self.linear if age < 0.5 else 0.0
        w = self.angular if age < 0.5 else 0.0

        if self.serial_port and self.serial_port.is_open:
            half_track = self.wheel_separation / 2.0
            left = (v - w * half_track) / self.max_linear_speed
            right = (v + w * half_track) / self.max_linear_speed
            scale = max(1.0, abs(left), abs(right))
            left /= scale
            right /= scale

            try:
                # Firmware protocol: M,<left -1..1>,<right -1..1>\n
                packet = f'M,{left:.3f},{right:.3f}\n'
                self.serial_port.write(packet.encode('ascii'))
            except (serial.SerialException, OSError) as exc:
                self.get_logger().error(f'Serial write failed: {exc}')
                self.linear = 0.0
                self.angular = 0.0
                return

        if not self.publish_odom or dt <= 0.0 or dt > 0.2:
            return

        # Command-based estimate only; no encoders measure actual movement.
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

    def destroy_node(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(b'M,0.000,0.000\n')
                self.serial_port.close()
            except (serial.SerialException, OSError):
                pass
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
