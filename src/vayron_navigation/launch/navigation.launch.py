import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    nav2_dir = get_package_share_directory('nav2_bringup')
    package_dir = get_package_share_directory('vayron_navigation')

    nav_launch = os.path.join(
        nav2_dir, 'launch', 'navigation_launch.py'
    )
    params_file = os.path.join(
        package_dir, 'config', 'nav2_params.yaml'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    configured_params = RewrittenYaml(
        source_file=params_file,
        root_key='',
        param_rewrites={'use_sim_time': use_sim_time},
        convert_types=True,
    )

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav_launch),
        launch_arguments={
            'params_file': configured_params,
            'use_sim_time': use_sim_time,
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='True for simulation, false for physical hardware',
        ),
        nav2,
    ])
