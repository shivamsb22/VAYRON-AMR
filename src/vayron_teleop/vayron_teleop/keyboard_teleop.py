
#!/usr/bin/env python3

import select
import sys
import termios
import tty
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('vayron_keyboard_teleop')

        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('linear_speed', 0.25)
        self.declare_parameter('angular_speed', 0.8)

        topic = self.get_parameter('cmd_vel_topic').value
        self.linear_speed = float(
            self.get_parameter('linear_speed').value
        )
        self.angular_speed = float(
            self.get_parameter('angular_speed').value
        )

        self.publisher = self.create_publisher(Twist, topic, 10)

        self.active_key = None
        self.last_key_time = 0.0
        self.key_timeout = 0.2

        self.timer = self.create_timer(
            0.05,
            self.publish_velocity
        )

        self.get_logger().info(
            f'Keyboard teleop ready. Publishing to {topic}'
        )

    def publish_velocity(self):
        msg = Twist()

        if time.monotonic() - self.last_key_time <= self.key_timeout:

            if self.active_key == 'w':
                msg.linear.x = self.linear_speed

            elif self.active_key == 's':
                msg.linear.x = -self.linear_speed

            elif self.active_key == 'a':
                msg.angular.z = self.angular_speed

            elif self.active_key == 'd':
                msg.angular.z = -self.angular_speed

        self.publisher.publish(msg)

    def process_key(self, key):
        key = key.lower()

        if key == 'q':
            return False

        if key in ('w', 'a', 's', 'd'):
            self.active_key = key
            self.last_key_time = time.monotonic()

        elif key == ' ':
            self.active_key = None
            self.last_key_time = 0.0
            self.publisher.publish(Twist())

        return True


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()

    settings = termios.tcgetattr(sys.stdin)

    print(
        '\nVAYRON KEYBOARD TELEOP\n'
        'W: Forward | S: Reverse\n'
        'A: Left    | D: Right\n'
        'Space: Stop | Q: Quit\n'
    )

    try:
        tty.setcbreak(sys.stdin.fileno())

        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.01)

            ready, _, _ = select.select(
                [sys.stdin], [], [], 0.02
            )

            if ready:
                key = sys.stdin.read(1)

                if not node.process_key(key):
                    break

    except KeyboardInterrupt:
        pass

    finally:
        # Publish stop only while ROS is still active
        if rclpy.ok():
            try:
                node.active_key = None
                node.publisher.publish(Twist())
            except Exception as exc:
                print(f"Stop command warning: {exc}")

        # Restore terminal settings
        try:
            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                settings
            )
        except Exception:
            pass

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
