
#!/usr/bin/env python3

import select
import sys
import termios
import tty

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
        self.get_logger().info(
            f'Keyboard teleop ready. Publishing to {topic}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()

    settings = termios.tcgetattr(sys.stdin)

    try:
        tty.setcbreak(sys.stdin.fileno())
        print(
            '\nVAYRON Keyboard Teleop\n'
            'W: forward | S: backward\n'
            'A: left    | D: right\n'
            'Space: stop | Q: quit\n'
        )

        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.02)

            ready, _, _ = select.select([sys.stdin], [], [], 0.05)
            if not ready:
                continue

            key = sys.stdin.read(1).lower()
            msg = Twist()

            if key == 'w':
                msg.linear.x = node.linear_speed
            elif key == 's':
                msg.linear.x = -node.linear_speed
            elif key == 'a':
                msg.angular.z = node.angular_speed
            elif key == 'd':
                msg.angular.z = -node.angular_speed
            elif key in (' ', '\x03'):
                pass
            elif key == 'q':
                break
            else:
                continue

            node.publisher.publish(msg)

    except KeyboardInterrupt:
        pass
    finally:
        stop = Twist()
        node.publisher.publish(stop)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
