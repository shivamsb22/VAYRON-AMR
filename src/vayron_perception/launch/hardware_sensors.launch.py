
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    lidar = Node(
        package='rplidar_ros',
        executable='rplidar_node',
        name='vayron_lidar',
        output='screen',
        parameters=[{
            'serial_port': '/dev/ttyUSB0',
            'serial_baudrate': 115200,
            'frame_id': 'rplidar_link',
            'angle_compensate': True,
            'scan_mode': 'Standard',
        }],
        remappings=[
            ('/scan', '/scan'),
        ],
    )

    camera = Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        name='vayron_camera',
        output='screen',
        parameters=[{
            'video_device': '/dev/video0',
            'camera_frame_id': 'camera_optical_frame',
            'image_size': [640, 480],
            'time_per_frame': [1, 30],
        }],
    )

    return LaunchDescription([lidar, camera])
