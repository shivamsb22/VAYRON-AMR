import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    TimerAction,
)
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    description_dir = get_package_share_directory(
        'vayron_description'
    )

    simulation_dir = get_package_share_directory(
        'vayron_simulation'
    )

    control_dir = get_package_share_directory(
        'vayron_control'
    )

    xacro_file = os.path.join(
        description_dir,
        'urdf',
        'vayron',
        'vayron.urdf.xacro'
    )

    rviz_file = os.path.join(
        description_dir,
        'rviz',
        'vayron.rviz'
    )

    control_config = os.path.join(
        control_dir,
        'config',
        'control.yaml'
    )

    default_world = os.path.join(
        simulation_dir,
        'worlds',
        'indoor_test_facility',
        'indoor_test_facility.world'
    )

    world = LaunchConfiguration('world')

    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            xacro_file,
            ' ',
            'simulation:=true',
        ]),
        value_type=str
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }]
    )

    watchdog = Node(
        package='vayron_control',
        executable='cmd_vel_watchdog',
        name='vayron_cmd_vel_watchdog',
        output='screen',
        parameters=[
            control_config,
            {'use_sim_time': True}
        ],
        respawn=True,
        respawn_delay=1.0
    )

    gazebo = ExecuteProcess(
        cmd=[
            'gazebo',
            '--verbose',
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so',
            world,
        ],
        output='screen'
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'vayron',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.10',
        ],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='vayron_rviz',
        arguments=['-d', rviz_file],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'world',
            default_value=default_world,
            description='Absolute path to the Gazebo world file'
        ),

        robot_state_publisher,

        watchdog,

        gazebo,

        rviz,

        TimerAction(
            period=5.0,
            actions=[spawn_robot]
        ),
    ])
