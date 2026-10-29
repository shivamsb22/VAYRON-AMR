import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    package_dir = get_package_share_directory('vayron_navigation')

    localization = os.path.join(
        package_dir, 'launch', 'localization.launch.py'
    )
    navigation = os.path.join(
        package_dir, 'launch', 'navigation.launch.py'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    map_file = LaunchConfiguration('map')

    return LaunchDescription([
        DeclareLaunchArgument('map'),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(localization),
            launch_arguments={
                'map': map_file,
                'use_sim_time': use_sim_time,
            }.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(navigation),
            launch_arguments={
                'use_sim_time': use_sim_time,
            }.items(),
        ),
    ])
