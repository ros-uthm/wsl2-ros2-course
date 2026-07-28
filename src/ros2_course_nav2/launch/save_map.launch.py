import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    pkg_nav2 = get_package_share_directory('ros2_course_nav2')

    map_name = LaunchConfiguration('map_name')
    maps_dir = os.path.join(pkg_nav2, 'maps')
    map_path = PathJoinSubstitution([maps_dir, map_name])

    return LaunchDescription([
        DeclareLaunchArgument('map_name', default_value='course_map'),
        Node(
            package='nav2_map_server',
            executable='map_saver_cli',
            arguments=['-f', map_path],
            output='screen'
        )
    ])
