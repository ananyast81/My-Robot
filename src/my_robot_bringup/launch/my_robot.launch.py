import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Package directories
    pkg_my_robot_description = get_package_share_directory('my_robot_description')
    pkg_my_robot_bringup = get_package_share_directory('my_robot_bringup')
    pkg_ros_ign_gazebo = get_package_share_directory('ros_ign_gazebo')
    
    # Paths
    urdf_path = os.path.join(pkg_my_robot_description, 'urdf', 'my_robot.urdf.xacro')
    world_path = os.path.join(pkg_my_robot_bringup, 'worlds', 'bot_world.sdf')
    gazebo_config_path = os.path.join(pkg_my_robot_bringup, 'config', 'gazebo_bridge.yaml')
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', urdf_path]),
            'use_sim_time': True
        }],
        output='screen'
    )
    
    # Ignition Gazebo
    ignition_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_ign_gazebo, 'launch', 'ign_gazebo.launch.py')
        ),
        launch_arguments={'ign_args': f'-r {world_path}'}.items()
    )
    
    # Spawn Robot
    spawn_robot = Node(
        package='ros_ign_gazebo',
        executable='create',
        arguments=['-topic', 'robot_description'],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
    
    # Bridge
    bridge = Node(
        package='ros_ign_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': gazebo_config_path,
            'use_sim_time': True
        }],
        output='screen'
    )
    
    return LaunchDescription([
        robot_state_publisher,
        ignition_gazebo,
        spawn_robot,
        bridge,
    ])