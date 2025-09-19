#!/bin/bash
# build workspace
colcon build --symlink-install

# source setup (important!)
source install/setup.bash

# reset turtlesim
ros2 service call /reset std_srvs/srv/Empty {}
ros2 service call /turtle1/teleport_absolute turtlesim/srv/TeleportAbsolute "{x: 2.0, y: 8.0, theta: -1.57}"
ros2 service call /clear std_srvs/srv/Empty {}

# run your node
ros2 run second_part Writer
