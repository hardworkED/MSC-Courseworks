#!/usr/bin/env python

from cr_week6_test.srv import predict_robot_expression
from cr_week6_test.msg import perceived_info, robot_info
import rospy
import numpy as np

def callback(data):
    pub = rospy.Publisher('robot_info', robot_info, queue_size=0)
    try:
        pred = rospy.ServiceProxy('predict_robot_expression', predict_robot_expression)
        # get cubic coeffs
        p = pred(data)

        params = robot_info()
        if not rospy.is_shutdown():
            # set parameters
            params.id = data.id
            params.p_happy = p.p_happy
            params.p_sad = p.p_sad
            params.p_neutral = p.p_neutral
            # publish robot info
            pub.publish(params)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def robot_controller():
    rospy.init_node('robot_controller', anonymous=True)
    rospy.Subscriber('perceived_info', perceived_info, callback)
    rospy.wait_for_service('predict_robot_expression')
    rospy.spin()

if __name__ == '__main__':
    try:
        robot_controller()
    except rospy.ROSInterruptException:
        pass