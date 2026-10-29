
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    simulation_dir = get_package_share_directory('vayron_simulation')

    indoor_launch = os.path.join(
        simulation_dir, 'launch', 'vayron_indoor.launch.py'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(indoor_launch)
        ),
    ])
