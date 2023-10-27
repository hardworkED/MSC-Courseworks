#!/usr/bin/env python

import rospy
from random import randint
from cr_week6_test.msg import object_info, human_info, perceived_info

cache_obj = dict()
cache_human = dict()

def random_filter(params):
    rslt = params.copy()
    # define which info to be filtered
    acts = {
        1: [0],
        2: [1],
        3: [2],
        8: []
    }
    acts[4] = acts[1] + acts[2]
    acts[5] = acts[1] + acts[3]
    acts[6] = acts[2] + acts[3]
    acts[7] = acts[4] + acts[3]

    for act in acts[randint(1, 8)]:
        rslt[act] = 0
    return rslt

def combine_msg():
    global cache_obj
    global cache_human

    # find if there is corresponding id in both list
    intersect = sorted(list(cache_obj.keys() & cache_human.keys()))

    if intersect:
        pub = rospy.Publisher('perceived_info', perceived_info, queue_size=0)
        params = perceived_info()
        obj_params = cache_obj[intersect[0]]
        human_params = cache_human[intersect[0]]

        # filter params
        filtered_params = random_filter([obj_params.object_size, human_params.human_action, human_params.human_expression])

        # insert params
        params.id = obj_params.id
        params.object_size = filtered_params[0]
        params.human_action = filtered_params[1]
        params.human_expression = filtered_params[2]

        # publish params
        pub.publish(params)

        # delete published data from cache
        del cache_obj[intersect[0]]
        del cache_human[intersect[0]]

def callback_obj(data):
    cache_obj[data.id] = data
    combine_msg()

def callback_human(data):
    cache_human[data.id] = data
    combine_msg()

def perception_filter():
    rospy.init_node('perception_filter', anonymous=True)
    obj_sub = rospy.Subscriber('object_info', object_info, callback_obj)
    human_sub = rospy.Subscriber('human_info', human_info, callback_human)
    rospy.spin()

if __name__ == '__main__':
    try:
        perception_filter()
    except rospy.ROSInterruptException:
        pass