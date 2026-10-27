from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    package_dir = get_package_share_directory('vayron_description')
    xacro_file = os.path.join(
        package_dir, 'urdf', 'vayron', 'vayron.urdf.xacro'
    )

    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            xacro_file
        ]),
        value_type=str
    )

    state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    watchdog = Node(
        package='vayron_description',
        executable='cmd_vel_watchdog.py',
        name='cmd_vel_watchdog',
        output='screen',
        parameters=[{
            'timeout_sec': 0.5,
            'publish_rate': 20.0
        }],
        respawn=True,
        respawn_delay=0.2
    )
    gazebo = ExecuteProcess(
        cmd=[
            'gazebo',
            '--verbose',
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so'
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
            '-z', '0.02'
        ],
        output='screen'
    )

    rviz_config = os.path.join(package_dir, 'rviz', 'vayron.rviz')

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        state_publisher,
        watchdog,
        gazebo,
        rviz,
        TimerAction(
            period=5.0,
            actions=[spawn_robot]
        )
    ])
