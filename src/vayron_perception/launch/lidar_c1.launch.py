from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    config_file = os.path.join(
        get_package_share_directory('vayron_perception'),
        'config',
        'lidar_c1.yaml'
    )

    serial_port = LaunchConfiguration('serial_port')

    lidar_node = Node(
        package='sllidar_ros2',
        executable='sllidar_node',
        name='sllidar_node',
        output='screen',
        parameters=[
            config_file,
            {
                'serial_port': serial_port
            }
        ],
        remappings=[
            ('/scan', '/scan_real')
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'serial_port',
            default_value='/dev/ttyUSB0',
            description='Serial device connected to RPLIDAR C1'
        ),
        lidar_node
    ])
