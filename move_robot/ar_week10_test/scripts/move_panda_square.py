# Goh Jun Huang
#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from ar_week10_test.msg import square_info
import moveit_msgs.msg
import moveit_commander
import sys
import copy
from math import pi

# code reference from moveit_tutorials
class MovePandaSquare():

    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        group_name = 'panda_arm'
        move_group = moveit_commander.MoveGroupCommander(group_name)
        display_trajectory_publisher = rospy.Publisher(
            '/move_group/display_planned_path',
            moveit_msgs.msg.DisplayTrajectory,
            queue_size=0,
        )

        planning_frame = move_group.get_planning_frame()
        eef_link = move_group.get_end_effector_link()
        group_names = robot.get_group_names()

        self.box_name = ''
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names

    # 2a
    def go_to_joint_state(self):
        start_conf = [0, -pi / 4, 0, -pi / 2, 0, pi / 3, 0]

        self.move_group.go(start_conf, wait=True)
        self.move_group.stop()

    # 2b
    def plan_cartesian_path(self, data):
        waypoints = []

        wpose = self.move_group.get_current_pose().pose
        wpose.position.x += data
        waypoints.append(copy.deepcopy(wpose))
        wpose.position.y += data
        waypoints.append(copy.deepcopy(wpose))
        wpose.position.x -= data
        waypoints.append(copy.deepcopy(wpose))
        wpose.position.y -= data
        waypoints.append(copy.deepcopy(wpose))
        
        (plan, fraction) = self.move_group.compute_cartesian_path(
            waypoints, 0.01, 0.0
        )

        return plan, fraction

    # 2c
    def display_trajectory(self, plan):
        display_trajectory = moveit_msgs.msg.DisplayTrajectory()
        display_trajectory.trajectory_start = self.robot.get_current_state()
        display_trajectory.trajectory.append(plan)
        self.display_trajectory_publisher.publish(display_trajectory)

    # 2d
    def execute_plan(self, plan):
        self.move_group.execute(plan, wait=True)

move = MovePandaSquare()

def callback(data):
    global move

    print('\n\nReceived square size: {}'.format(data.length))

    print('Start configuration')
    move.go_to_joint_state()
    rospy.sleep(2)
    print('Plan Cartesian path')
    plan, fraction = move.plan_cartesian_path(data.length)
    print('Show planned trajectory')
    move.display_trajectory(plan)
    rospy.sleep(6)
    print('Execute planned trajectory')
    move.execute_plan(plan)
    print('Wait for next message')


def move_panda_square():
    rospy.init_node('move_panda_square', anonymous=True)
    rospy.Subscriber('square_info', square_info, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        move_panda_square()
    except rospy.ROSInterruptException:
        pass