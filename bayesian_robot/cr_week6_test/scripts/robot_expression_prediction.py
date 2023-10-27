#!/usr/bin/env python

from cr_week6_test.srv import predict_robot_expression, predict_robot_expressionResponse
import numpy as np
from operator import itemgetter
import rospy

def handle_prediction(req):
    params = req.params
    curr_cond = '{}{}{}'.format(params.human_expression, params.human_action, params.object_size)

    # probability given for HE, HA, O
    p = [1 / 3, 1 / 3, 1 / 2]
    # possible parameters for HE, HA, O
    pp = [3, 3, 2]
    # defining CPTs
    # keys = 'HE HA O'
    RE = [
        {   # H
            '111': 0.8,
            '112': 1.0,
            '121': 0.8,
            '122': 1.0,
            '131': 0.6,
            '132': 0.8,
            '211': 0.0,
            '212': 0.0,
            '221': 0.0,
            '222': 0.1,
            '231': 0.0,
            '232': 0.2,
            '311': 0.7,
            '312': 0.8,
            '321': 0.8,
            '322': 0.9,
            '331': 0.6,
            '332': 0.7,
        },
        {   # S
            '111': 0.2,
            '112': 0.0,
            '121': 0.2,
            '122': 0.0,
            '131': 0.2,
            '132': 0.2,
            '211': 0.0,
            '212': 0.0,
            '221': 0.1,
            '222': 0.1,
            '231': 0.2,
            '232': 0.2,
            '311': 0.3,
            '312': 0.2,
            '321': 0.2,
            '322': 0.1,
            '331': 0.2,
            '332': 0.2,
        },
        {  # N
            '111': 0.0,
            '112': 0.0,
            '121': 0.0,
            '122': 0.0,
            '131': 0.2,
            '132': 0.0,
            '211': 1.0,
            '212': 1.0,
            '221': 0.9,
            '222': 0.8,
            '231': 0.8,
            '232': 0.6,
            '311': 0.0,
            '312': 0.0,
            '321': 0.0,
            '322': 0.0,
            '331': 0.2,
            '332': 0.1,
        },
    ]

    rslts = []
    # get exact p if observation is complete
    if '0' not in curr_cond:
        rslts = [RE[i][curr_cond] for i in range(len(RE))]
    # calculate p if there is no observation
    elif int(curr_cond) == 0:
        c = np.prod([p[i] for i in range(len(p))])
        rslts = [(np.array(list(RE[i].values())) * c).sum() for i in range(len(RE))]
    # calculate p if there is missing observation
    else:
        l = list(curr_cond)
        # find index of missing observation
        inds = [i for i in range(len(l)) if l[i] == '0']
        # calculate scalar to be multiplied in the calculation
        c = np.prod([p[i] for i in inds])
        conds = [curr_cond]
        # get all combinations of probabilities needed for the calculation
        for ind in inds:
            tmp = [cond.replace('0', str(i + 1), 1) for i in range(pp[ind]) for cond in conds]
            conds = tmp
        # calculate for p
        rslts = [sum(np.array(itemgetter(*conds)(RE[i])) * c) for i in range(len(RE))]
    
    # return probability of happy, sad, neutral
    return predict_robot_expressionResponse(rslts[0], rslts[1], rslts[2])

def robot_expression_prediction():
    rospy.init_node('robot_expression_prediction')
    s = rospy.Service('predict_robot_expression', predict_robot_expression, handle_prediction)
    rospy.spin()

if __name__ == "__main__":
    robot_expression_prediction()