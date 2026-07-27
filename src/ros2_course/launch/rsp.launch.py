import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    # 1. Mendapatkan laluan ke folder pakej ros2_course
    pkg_share = get_package_share_directory('ros2_course')

    # 2. Memproses fail robot.urdf.xacro
    xacro_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)

    # 3. Tetapan parameter robot_description
    params = {
        'robot_description': robot_description_config.toxml(),
        'use_sim_time': True
    }

    # 4. Nod Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    return LaunchDescription([node_robot_state_publisher])
