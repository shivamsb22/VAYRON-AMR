
#!/usr/bin/env python3

import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class CmdVelWatchdog(Node):
    def __init__(self):
        super().__init__('vayron_cmd_vel_watchdog')

        self.declare_parameter('input_topic', '/cmd_vel')
        self.declare_parameter('output_topic', '/cmd_vel_safe')
        self.declare_parameter('timeout_sec', 0.5)
        self.declare_parameter('max_linear_speed', 0.25)
        self.declare_parameter('max_angular_speed', 1.5)

        self.timeout = float(self.get_parameter('timeout_sec').value)
        self.max_linear = float(
            self.get_parameter('max_linear_speed').value
        )
        self.max_angular = float(
            self.get_parameter('max_angular_speed').value
        )

        self.last_msg_time = None
        self.latest_cmd = Twist()

        self.publisher = self.create_publisher(
            Twist, self.get_parameter('output_topic').value, 10
        )
        self.subscription = self.create_subscription(
            Twist,
            self.get_parameter('input_topic').value,
            self.command_callback,
            10,
        )
        self.timer = self.create_timer(0.05, self.publish_safe_command)

        self.get_logger().info('VAYRON command watchdog initialized.')

    def command_callback(self, msg):
        values = (
            msg.linear.x, msg.linear.y, msg.linear.z,
            msg.angular.x, msg.angular.y, msg.angular.z,
        )

        if not all(math.isfinite(value) for value in values):
            self.latest_cmd = Twist()
            self.last_msg_time = None
            self.get_logger().warning('Invalid command rejected.')
            return

        safe = Twist()
        safe.linear.x = max(
            -self.max_linear, min(self.max_linear, msg.linear.x)
        )
        safe.angular.z = max(
            -self.max_angular, min(self.max_angular, msg.angular.z)
        )

        self.latest_cmd = safe
        self.last_msg_time = self.get_clock().now()

    def publish_safe_command(self):
        output = Twist()

        if self.last_msg_time is not None:
            age = (
                self.get_clock().now() - self.last_msg_time
            ).nanoseconds / 1e9

            if age <= self.timeout:
                output = self.latest_cmd

        self.publisher.publish(output)


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelWatchdog()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.publisher.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
