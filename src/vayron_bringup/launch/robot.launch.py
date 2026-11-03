import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def launch_robot(context, *args, **kwargs):
    mode = LaunchConfiguration('mode').perform(context)

    bringup_dir = get_package_share_directory('vayron_bringup')

    if mode == 'hardware':
        launch_file = os.path.join(
            bringup_dir,
            'launch',
            'hardware.launch.py'
        )
        launch_arguments = {}

    elif mode == 'simulation':
        simulation_dir = get_package_share_directory(
            'vayron_simulation'
        )

        default_world = os.path.join(
            simulation_dir,
            'worlds',
            'indoor_test_facility',
            'indoor_test_facility.world'
        )

        launch_file = os.path.join(
            bringup_dir,
            'launch',
            'simulation.launch.py'
        )

        launch_arguments = {
            'world': LaunchConfiguration('world')
        }

    else:
        raise RuntimeError(
            f"Invalid VAYRON mode: '{mode}'. "
            "Choose 'hardware' or 'simulation'."
        )

    return [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(launch_file),
            launch_arguments=launch_arguments.items()
        )
    ]


def generate_launch_description():

    simulation_dir = get_package_share_directory(
        'vayron_simulation'
    )

    default_world = os.path.join(
        simulation_dir,
        'worlds',
        'indoor_test_facility',
        'indoor_test_facility.world'
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'mode',
            default_value='hardware',
            description='VAYRON operating mode: hardware or simulation'
        ),

        DeclareLaunchArgument(
            'world',
            default_value=default_world,
            description='Gazebo world file used in simulation mode'
        ),

        OpaqueFunction(function=launch_robot),

    ])
