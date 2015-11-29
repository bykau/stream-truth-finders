import sys
import random
import string
import math
from datetime import datetime
import numpy as np


time_points = ['2000-01-01 00:00:00', '2000-01-05 00:00:00', '2000-01-07 00:00:00',
               '2000-01-10 00:00:00', '2000-01-11 00:00:00', '2000-01-13 00:00:00',
               '2000-01-17 00:00:00', '2000-01-20 00:00:00', '2000-01-25 00:00:00',
               '2000-01-29 00:00:00', '2000-02-01 00:00:00', '2000-02-08 00:00:00',
               '2000-02-10 00:00:00', '2000-02-11 00:00:00', '2000-02-15 00:00:00',
               '2000-02-19 00:00:00', '2000-02-23 00:00:00', '2000-02-25 00:00:00',
               '2000-02-27 00:00:00', '2000-02-28 00:00:00']

p_i = 0.7
p_e = 0.1
p_o = 0.1

number_of_sources = 10
number_of_object = 100


def get_ground_truth(number_of_object):
    ground_truth_list = []
    for i in range(number_of_object):
        t = [time_points[0]]
        v = [random.choice(string.ascii_uppercase)]
        # number_of_v = random.choice(range(len(time_points)/6))
        number_of_v = random.choice([1, 2])
        for j in range(number_of_v):
            t.append(random.choice(list(set(time_points)-set(t))))
            v.append(random.choice(string.ascii_uppercase.replace(v[-1], '')))
        ground_truth_list.append([sorted(t), v])

    return ground_truth_list


def get_s_parameters(p_t_mean, f0_mean):
    parameters_for_s = []
    for s in range(number_of_sources):
        p_t = np.random.normal(p_t_mean, 0.1, 1)[0]
        if p_t < 0:
            p_t = 0.01
        elif p_t > 1:
            p_t = 1.
        f0 = np.random.normal(f0_mean, 0.1, 1)[0]
        if f0 < 0:
            f0 = 0.1
        elif f0 > 1:
            f0 = 1.
        parameters_for_s.append([p_t, f0])

    return parameters_for_s


def get_observed_cases(ground_truth_list, parameters_for_s):
    observed_cases = []
    for i in range(number_of_object):
        obj = {}
        gt_time_points = ground_truth_list[i][0]
        gt_values = ground_truth_list[i][1]
        for s in range(number_of_sources):
            t = []
            v = []
            while not t:
                for t_index, t_point in enumerate(time_points):
                    x = random.random()
                    if t_index == 0:
                        if x > p_i:
                            continue
                    elif t_index == 19:
                        if x > p_e:
                            continue
                    else:
                        if x > p_o:
                            continue

                    for t_gt_index, t_gt in enumerate(gt_time_points):
                        if t_gt > t_point:
                            t_gt_point = gt_time_points[t_gt_index-1]
                            gt_prev_val = gt_values[t_gt_index-1]
                            break
                        elif t_gt == t_point:
                            t_gt_point = t_gt
                            gt_prev_val = gt_values[t_gt_index]
                            break
                        elif len(gt_time_points) == 1:
                            t_gt_point = t_gt
                            gt_prev_val = gt_values[t_gt_index]
                            break
                        elif t_gt_index == len(gt_time_points)-1:
                            t_gt_point = t_gt
                            gt_prev_val = gt_values[t_gt_index]
                            break

                    delta = datetime.strptime(t_point, '%Y-%m-%d %H:%M:%S') - datetime.strptime(t_gt_point, '%Y-%m-%d %H:%M:%S')
                    normz_factor = datetime.strptime(time_points[-1], '%Y-%m-%d %H:%M:%S') - datetime.strptime(time_points[0], '%Y-%m-%d %H:%M:%S')
                    delta_normalized = delta.total_seconds()/normz_factor.total_seconds()
                    p_t = parameters_for_s[s][0]
                    f0 = parameters_for_s[s][1]
                    if delta_normalized <= -math.log10(f0):
                        p_t_observ = p_t*f0*math.pow(2, delta_normalized)
                    else:
                        p_t_observ = p_t
                    if np.random.choice(2, 1, p=[1-p_t_observ, p_t_observ])[0]:
                        if len(v) != 0 and gt_prev_val == v[-1]:
                            continue
                        else:
                            v.append(gt_prev_val)
                    else:
                        if len(v) != 0:
                            v.append(random.choice(string.ascii_uppercase
                                                   .replace(gt_prev_val, '')
                                                   .replace(v[-1], '')))
                        else:
                            v.append(random.choice(string.ascii_uppercase
                                                   .replace(gt_prev_val, '')))
                    t.append(t_point)
                obj.update({'S{}'.format(s): [t, v]})
        observed_cases.append(obj)

    return observed_cases


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 2:
        print '** Parameters error **'
        sys.exit(1)
    p_t = args[0]
    f0 = args[1]
    ground_truth_list = get_ground_truth(number_of_object)
    parameters_for_s = get_s_parameters(p_t, f0)
    observed_cases = get_observed_cases(ground_truth_list, parameters_for_s)

    with open('data.py', 'w') as f:
        f.write('ground_truth_list = ' + str(ground_truth_list) + '\n')
        f.write('observed_cases = ' + str(observed_cases) + '\n')
        f.write('p_t_mean = {}'.format(f0) + '\n')
        f.write('f0_mean = {}'.format(f0) + '\n')
