import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory, get_package_prefix

def generate_launch_description():

    urdf_path = os.path.join(
        get_package_share_directory('my_robot_description'),
        'urdf',
        'my_robot.urdf.xacro'
    )

    rviz_config_path = os.path.join(
        get_package_share_directory('my_robot_description'),
        'rviz',
        'map_config.rviz'
    )

    slam_params_path = os.path.join(
        get_package_share_directory('my_robot_bringup'),
        'config',
        'mapper_params_online_async.yaml'
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(f'xacro {urdf_path}')}]
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config_path]
    )

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('slam_toolbox'),
                'launch',
                'online_async_launch.py'
            )
        ),
        launch_arguments={
            'slam_params_file': slam_params_path,
            'use_sim_time': 'true'
        }.items()
    )

    return LaunchDescription([
        # Uncomment if you want to run rviz indepently
        # robot_state_publisher_node,
        rviz2_node,
        slam_toolbox_launch,
    ])