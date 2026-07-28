import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_nav2 = get_package_share_directory('ros2_course_nav2')
    pkg_robot = get_package_share_directory('ros2_course')
    pkg_gz = get_package_share_directory('ros_gz_sim')
    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')

    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    use_rviz = LaunchConfiguration('use_rviz')
    map_yaml = LaunchConfiguration('map')

    world_path = os.path.join(pkg_nav2, 'worlds', 'simple_nav_world.sdf')
    nav2_params = os.path.join(pkg_nav2, 'config', 'nav2_params.yaml')
    default_map = os.path.join(pkg_nav2, 'maps', 'course_map.yaml')
    lifecycle_nodes = [
        'controller_server',
        'smoother_server',
        'planner_server',
        'behavior_server',
        'bt_navigator',
        'waypoint_follower',
        'velocity_smoother',
    ]

    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_robot, 'launch', 'rsp.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gz, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_path}'}.items()
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-world', 'course_world',
            '-topic', 'robot_description',
            '-name', 'my_robot',
            '-x', '0.0',
            '-y', '1.8',
            '-z', '0.1'
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/camera/image@sensor_msgs/msg/Image[gz.msgs.Image'
        ],
        output='screen'
    )

    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_bringup, 'launch', 'localization_launch.py')
        ),
        launch_arguments={
            'map': map_yaml,
            'use_sim_time': use_sim_time,
            'params_file': nav2_params,
            'autostart': autostart,
            'use_composition': 'False'
        }.items()
    )

    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}, nav2_params],
        arguments=['--ros-args', '--log-level', 'info'],
        remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static'), ('cmd_vel', 'cmd_vel_nav')],
    )

    smoother_server = Node(
        package='nav2_smoother',
        executable='smoother_server',
        name='smoother_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}, nav2_params],
        arguments=['--ros-args', '--log-level', 'info'],
        remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')],
    )

    planner_server = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}, nav2_params],
        arguments=['--ros-args', '--log-level', 'info'],
        remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')],
    )

    behavior_server = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}, nav2_params],
        arguments=['--ros-args', '--log-level', 'info'],
        remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static'), ('cmd_vel', 'cmd_vel_nav')],
    )

    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}, nav2_params],
        arguments=['--ros-args', '--log-level', 'info'],
        remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')],
    )

    waypoint_follower = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}, nav2_params],
        arguments=['--ros-args', '--log-level', 'info'],
        remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')],
    )

    velocity_smoother = Node(
        package='nav2_velocity_smoother',
        executable='velocity_smoother',
        name='velocity_smoother',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}, nav2_params],
        arguments=['--ros-args', '--log-level', 'info'],
        remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static'), ('cmd_vel', 'cmd_vel_nav')],
    )

    lifecycle_manager_navigation = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        arguments=['--ros-args', '--log-level', 'info'],
        parameters=[
            {'use_sim_time': use_sim_time},
            {'autostart': autostart},
            {'node_names': lifecycle_nodes},
        ],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_nav2_bringup, 'rviz', 'nav2_default_view.rviz')],
        output='screen',
        condition=IfCondition(use_rviz)
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('autostart', default_value='true'),
        DeclareLaunchArgument('use_rviz', default_value='true'),
        DeclareLaunchArgument('map', default_value=default_map),
        rsp,
        gazebo,
        spawn_entity,
        bridge,
        localization,
        controller_server,
        smoother_server,
        planner_server,
        behavior_server,
        bt_navigator,
        waypoint_follower,
        velocity_smoother,
        lifecycle_manager_navigation,
        rviz,
    ])
