Code developed by Goh Jun Huang, QMUL
220399308

Python version: 3.8.10
rosdistro: noetic
rosversion: 1.15.15

To run the package:

1)  Download and install the following packages: (for noetic distro)
    git clone https://github.com/ros-planning/moveit_tutorials.git -b master
    git clone https://github.com/ros-planning/panda_moveit_config.git -b noetic-devel
2)  unzip the 'ar_week10_test.zip' folder in your catkin workspace
3)  build the catkin workspace with 'catkin_make'
4)  run the following on four different terminals:
    roslaunch panda_moveit_config demo.launch
    rosrun ar_week10_test square_size_generator.py
    rosrun ar_week10_test move_panda_square.py
    rosrun rqt_plot rqt_plot