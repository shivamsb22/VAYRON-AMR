#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CmdVelWatchdog(Node):

    def __init__(self):
        super().__init__('cmd_vel_watchdog')

        self.declare_parameter('timeout_sec', 0.5)
        self.declare_parameter('publish_rate', 20.0)

        self.timeout_sec = float(
            self.get_parameter('timeout_sec').value
        )
        publish_rate = float(
            self.get_parameter('publish_rate').value
        )

        self.last_command_time = None
        self.last_command = Twist()
        self.timed_out = True

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.command_callback,
            10
        )

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel_safe',
            10
        )

        self.timer = self.create_timer(
            1.0 / publish_rate,
            self.publish_safe_command
        )

        self.get_logger().info(
            f'Watchdog active: timeout={self.timeout_sec:.2f}s'
        )

    def command_callback(self, msg):
        self.last_command = msg
        self.last_command_time = time.monotonic()
        self.timed_out = False

    def publish_safe_command(self):
        now = time.monotonic()

        expired = (
            self.last_command_time is None
            or now - self.last_command_time > self.timeout_sec
        )

        if expired:
            if not self.timed_out:
                self.get_logger().warning(
                    'Command timeout: publishing zero velocity'
                )

            self.timed_out = True
            self.publisher.publish(Twist())
            return

        safe_command = Twist()

        # Limit forward/reverse speed
        safe_command.linear.x = max(
            -0.10, min(0.10, self.last_command.linear.x)
        )

        # Limit turning speed
        safe_command.angular.z = max(
            -0.30, min(0.30, self.last_command.angular.z)
        )

        self.publisher.publish(safe_command)

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelWatchdog()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Send several zero commands before shutdown.
        for _ in range(3):
            node.publisher.publish(Twist())
            time.sleep(0.05)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
