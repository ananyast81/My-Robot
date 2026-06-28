import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    urdf_path = os.path.join(
        get_package_share_directory('my_robot_description'),
        'urdf',
        'my_robot.urdf.xacro'
    )

    rviz_config_path = os.path.join(
        get_package_share_directory('my_robot_description'),
        'rviz',
        'camera_lidar_config.rviz'
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

    return LaunchDescription([
        # Uncomment if you want to run rviz indepently
        # robot_state_publisher_node,
        rviz2_node,
    ])