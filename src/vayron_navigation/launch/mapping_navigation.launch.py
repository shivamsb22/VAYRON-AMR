import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    pkg_dir = get_package_share_directory('vayron_navigation')
    sim_time = LaunchConfiguration('use_sim_time')
    slam = os.path.join(pkg_dir, 'launch', 'slam.launch.py')
    nav = os.path.join(pkg_dir, 'launch', 'navigation.launch.py')
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(slam),
            launch_arguments={'use_sim_time': sim_time}.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav),
            launch_arguments={'use_sim_time': sim_time}.items(),
        ),
    ])
