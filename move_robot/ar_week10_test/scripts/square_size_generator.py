# Goh Jun Huang
#!/usr/bin/env python

import rospy
from random import uniform
from std_msgs.msg import Float64
from ar_week10_test.msg import square_info

def square_size_generator():
    rospy.init_node('square_size_generator', anonymous=True)
    pub = rospy.Publisher('square_info', square_info, queue_size=0)
    # generate and publish every 20 seconds
    rate = rospy.Rate(0.05)

    params = square_info()
    while not rospy.is_shutdown():
        # generate parameter values
        params.length = uniform(0.05, 0.20)
        # publish parameters
        pub.publish(params)
        rospy.loginfo(params.length)
        rate.sleep()

if __name__ == '__main__':
    try:
        square_size_generator()
    except rospy.ROSInterruptException:
        pass
