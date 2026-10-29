import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    nav2_dir = get_package_share_directory('nav2_bringup')
    package_dir = get_package_share_directory('vayron_navigation')

    localization_launch = os.path.join(
        nav2_dir, 'launch', 'localization_launch.py'
    )
    params_file = os.path.join(
        package_dir, 'config', 'nav2_params.yaml'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    map_file = LaunchConfiguration('map')

    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(localization_launch),
        launch_arguments={
            'map': map_file,
            'params_file': params_file,
            'use_sim_time': use_sim_time,
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            description='Absolute path to the saved map YAML file',
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='True for simulation, false for physical hardware',
        ),
        localization,
    ])
