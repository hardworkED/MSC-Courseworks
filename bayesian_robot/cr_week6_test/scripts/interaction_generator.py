#!/usr/bin/env python

import rospy
from random import uniform
from std_msgs.msg import Int64
from cr_week6_test.msg import object_info, human_info

def interaction_generator():
    rospy.init_node('interaction_generator', anonymous=True)
    pub_object = rospy.Publisher('object_info', object_info, queue_size=0)
    pub_human = rospy.Publisher('human_info', human_info, queue_size=0)
    # generate and publish every 10 seconds
    rate = rospy.Rate(0.1)

    id_count = 1
    object_params = object_info()
    human_params = human_info()
    while not rospy.is_shutdown():
        # generate parameter values
        object_params.id = id_count
        object_params.object_size = round(uniform(0.5, 2.5))

        human_params.id = id_count
        human_params.human_expression = round(uniform(0.5, 3.5))
        human_params.human_action = round(uniform(0.5, 3.5))

        # publish parameters
        pub_object.publish(object_params)
        pub_human.publish(human_params)

        # id increment
        id_count += 1

        rate.sleep()

if __name__ == '__main__':
    try:
        interaction_generator()
    except rospy.ROSInterruptException:
        pass