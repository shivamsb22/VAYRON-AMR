import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    simulation_dir = get_package_share_directory(
        'vayron_simulation'
    )

    simulation_launch = os.path.join(
        simulation_dir,
        'launch',
        'simulation.launch.py'
    )

    default_world = os.path.join(
        simulation_dir,
        'worlds',
        'indoor_test_facility',
        'indoor_test_facility.world'
    )

    world = LaunchConfiguration('world')

    return LaunchDescription([

        DeclareLaunchArgument(
            'world',
            default_value=default_world,
            description='Gazebo world file'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(simulation_launch),
            launch_arguments={
                'world': world
            }.items()
        ),
    ])
