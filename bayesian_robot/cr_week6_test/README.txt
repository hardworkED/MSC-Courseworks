Code developed by Goh Jun Huang, QMUL
220399308

Python version: 3.8.10
rosdistro: noetic
rosversion: 1.15.15

To run the package:

1)  unzip the 'cr_week6_test.zip' folder in your catkin workspace
2)  build the catkin workspace via 'catkin_make'
3)  run the 'human_robot_interaction.launch' launch file via 'roslaunch cr_week6_test human_robot_interaction.launch'
    (run 'roscore' if you have not do so)
4)  run 'rqt_graph' to view topic and nodes
    (refresh for latest graph)
5) run following commands to view the messages in the topic:
    - rostopic echo /object_info
    - rostopic echo /human_info
    - rostopic echo /perceived_info
    - rostopic echo /robot_info
