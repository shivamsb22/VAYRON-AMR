
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    hardware_dir = get_package_share_directory('vayron_hardware')
    control_dir = get_package_share_directory('vayron_control')
    description_dir = get_package_share_directory('vayron_description')
    perception_dir = get_package_share_directory('vayron_perception')

    hardware_config = os.path.join(
        hardware_dir, 'config', 'hardware.yaml'
    )
    control_config = os.path.join(
        control_dir, 'config', 'control.yaml'
    )
    xacro_file = os.path.join(
        description_dir, 'urdf', 'vayron', 'vayron.urdf.xacro'
    )
    rviz_file = os.path.join(description_dir, 'rviz', 'vayron.rviz')
    sensors_launch = os.path.join(
        perception_dir, 'launch', 'hardware_sensors.launch.py'
    )

    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            xacro_file,
            ' ',
            'simulation:=false',
        ]),
        value_type=str,
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': False,
        }],
        output='screen',
    )

    watchdog = Node(
        package='vayron_control',
        executable='cmd_vel_watchdog',
        name='vayron_cmd_vel_watchdog',
        parameters=[control_config],
        output='screen',
    )

    serial_bridge = Node(
        package='vayron_hardware',
        executable='serial_bridge',
        name='vayron_serial_bridge',
        parameters=[hardware_config],
        output='screen',
    )

    sensors = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(sensors_launch)
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_file],
        parameters=[{'use_sim_time': False}],
        output='screen',
    )

    return LaunchDescription([
        robot_state_publisher,
        watchdog,
        serial_bridge,
        sensors,
        rviz,
    ])
