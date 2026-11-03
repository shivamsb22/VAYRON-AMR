from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    perception_share = get_package_share_directory('vayron_perception')

    lidar_launch = os.path.join(
        perception_share,
        'launch',
        'lidar_c1.launch.py'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'serial_port',
            default_value='/dev/ttyUSB0',
            description='Serial port for RPLIDAR C1'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(lidar_launch),
            launch_arguments={
                'serial_port': LaunchConfiguration('serial_port')
            }.items()
        )
    ])
