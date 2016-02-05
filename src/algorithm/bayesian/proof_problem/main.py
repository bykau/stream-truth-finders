'''
The implementation of Bayesian Model for streaming data truth detection presented in
Xin Luna Dong, Laure Berti-Equille, Divesh Srivastava
Data Fusion: Resolvnig Conflicts from Multiple Sources

@author: Evgeny Krivosheev (krivosheevevgeny@gmail.com)
'''

import os
import csv
import numpy as np
import copy
import random


s_number = 5
max_rounds = 30
eps = 0.001
numb_of_swaps = 101
truth_obj_list = [6, 8, 9, 15, 16, 10, 11, 7, 18, 20]
# All values are true
# data_init = [
#     [6, 8, None, 15, None, None, 11, 7, 18, 20],
#     [6, None, 9, 15, 16, 10, 11, None, None, 20],
#     [None, 8, 9, 15, None, 10, 11, 7, None, 20],
#     [6, None, 9, 15, None, 10, 11, 7, 18, None],
#     [None, 8, 9, 15, 16, 10, 11, None, None, 20]
# ]
# data_init = [
#     [6, 19, None, 15, None, 16, 11, 5, 18, 20],
#     [6, None, 9, 15, 16, 22, 21, None, None, 20],
#     [None, 8, 23, 15, None, 10, 11, 7, None, 24],
#     [13, None, 9, 15, None, 10, 11, 7, 18, None],
#     [None, 8, 9, 15, 16, 28, 12, None, None, 20]
# ]

# prob_gt = [
#     [1],
#     [0, 1],
#     [1, 0],
#     [0, 1],
#     [1],
#     [0, 0, 1],
#     [0, 0, 1],
#     [1, 0],
#     [0, 1],
#     [1, 0]
# ]


def generator():
    case = [[None, None, 6, 6, 0],
            [6, None, None, 8, 8]]
    k = 20
    markers = [True, True, None, None, False]
    for obj_ind, obj_gt in enumerate(truth_obj_list[2:]):
        rand_markers = sorted(markers, key=lambda k: random.random())
        values = []
        for i in rand_markers:
            if i == True:
               values.append(obj_gt)
            elif i == False:
                k += 1
                values.append(k)
            else:
                values.append(i)
        case.append(values)
    case = map(list, zip(*case))

    return case


def get_n_params(data):
    n_list = []
    for i in range(len(data[0])):
        observed_data = [obj[i] for obj in data]
        if None in observed_data:
            n = len(set(observed_data))-2
        else:
            n = len(set(observed_data))-1
        n_list.append(n)
    return n_list


def get_accuracy(data, prob):
    accuracy_list = []
    for s_index in range(s_number):
        p_sum = 0.
        size = 0.
        for obj_index in range(len(data[0])):
            observed_val = data[s_index][obj_index]
            if not observed_val:
                continue
            size += 1
            observed_values = sorted([obj[obj_index] for obj in data])
            possible_values = sorted(list(set(observed_values)-set([None])))
            for v_ind, v in enumerate(possible_values):
                if v == observed_val:
                    p_sum += prob[obj_index][v_ind]
                    break
        accuracy = p_sum/size
        accuracy_list.append(accuracy)
    return accuracy_list


def get_prob(data, accuracy):
    n_list = get_n_params(data)
    likelihood = []
    for obj_index in range(len(truth_obj_list)):
            likelihood.append([])
            n = n_list[obj_index]
            observed_values = sorted([obj[obj_index] for obj in data])
            possible_values = sorted(list(set(observed_values)-set([None])))
            if n == 0:
                likelihood[obj_index].append(1.)
                continue
            # break_flag = False
            for v_true in possible_values:
                a, b, b_sum = 1., 1., 0.
                a_not_completed = True
                for v_possible in possible_values:
                    # if break_flag:
                    #     break
                    for v, s_index in zip(observed_values, range(s_number)):
                        if v == None:
                            continue
                        accuracy = accuracy_list[s_index]
                        # if accuracy == 1.:
                            # if v == v_true:
                            #     likelihood[obj_index].append(1.)
                            #     break_flag = True
                            #     break
                            # else:
                            #     likelihood[obj_index].append(0.)
                            #     break_flag = True
                            #     break
                        if v == v_possible:
                            b *= n*accuracy/(1-accuracy)
                        if a_not_completed and v == v_true:
                            a *= n*accuracy/(1-accuracy)
                    a_not_completed = False
                    b_sum += b
                    b = 1
                # if break_flag:
                #     break_flag = False
                #     continue
                p = a/b_sum
                likelihood[obj_index].append(p)
    return likelihood


def swap_random(data, n):
    for i in range(n):
        s_index = np.random.randint(5, size=1)[0]
        swapped = False
        while not swapped:
            obj_index = np.random.randint(10, size=1)[0]
            v = data[s_index][obj_index]
            if v:
                data[s_index][obj_index] = None
                while not swapped:
                    obj_index2 = np.random.randint(10, size=1)[0]
                    if obj_index2 == obj_index:
                        continue
                    if not data[s_index][obj_index2]:
                        data[s_index][obj_index2] = v
                        swapped = True
    return data


def get_swap_cases(data):
    possible_cases = []
    for s_ind in range(s_number):
        observed_values = copy.copy(data[s_ind])
        for v_ind, v in enumerate(observed_values):
            if not v:
                continue
            for v2_ind, v2 in enumerate(observed_values):
                if v2:
                    continue
                new_case = copy.deepcopy(data)
                new_case[s_ind][v2_ind] = v
                new_case[s_ind][v_ind] = None
                possible_cases.append(new_case)
    return possible_cases


def get_dist_metric(data, prob):
    prob_gt = []
    for obj_index in range(len(data[0])):
        observed_values = sorted([obj[obj_index] for obj in data])
        possible_values = sorted(list(set(observed_values)-set([None])))
        prob_gt.append(possible_values)
    for obj_ind, v_true in enumerate(truth_obj_list):
        for v_ind, v in enumerate(prob_gt[obj_ind]):
            if v == v_true:
                prob_gt[obj_ind][v_ind] = 1
            else:
                prob_gt[obj_ind][v_ind] = 0
    prob_gt_vector = []
    prob_vector = []
    for i in range(len(prob_gt)):
        prob_gt_vector += prob_gt[i]
        prob_vector += prob[i]
    dist_metric = np.dot(prob_gt_vector, prob_vector)
    return dist_metric


if __name__ == '__main__':
    for m in range(20):
        data_init = generator()
        possible_cases = []
        possible_cases.append(data_init)
        possible_cases += get_swap_cases(copy.deepcopy(data_init))
        dist_metric_list = []
        iter_number_list = []
        for data in possible_cases:
            accuracy_delta = 0.3
            iter_number = 0
            accuracy_list = [0.8]*s_number
            while accuracy_delta > eps and iter_number < max_rounds:
                prob = get_prob(data=data, accuracy=accuracy_list)
                accuracy_prev = accuracy_list
                accuracy_list = get_accuracy(data, prob)
                accuracy_delta = max([abs(k-l) for k, l in zip(accuracy_prev, accuracy_list)])
                iter_number += 1
            dist_metric = get_dist_metric(data, prob)
            dist_metric_list.append(dist_metric)
            iter_number_list.append(iter_number)
        iter_number_mean = np.mean(iter_number_list)
        iter_number_std = np.std(iter_number_list)
        true_swp_dist = dist_metric_list[1]
        dist_metric_list = sorted(dist_metric_list, reverse=True)
        true_swp_index = dist_metric_list.index(true_swp_dist)
        max_dist_metr = dist_metric_list[0]
        print 'max_dist_metr: {}'.format(max_dist_metr)
        print 'true_swp_dist: {}'.format(true_swp_dist)
        print 'true_swp_index: {}'.format(true_swp_index)
        print '------------'

        headers = ['true_swp_index', 'max_dist_metr', 'true_swp_dist', 'iter_number_mean', 'iter_number_std']
        list_to_csv = [true_swp_index, max_dist_metr, true_swp_dist, iter_number_mean, iter_number_std]
        with open('significance_testing_data.csv', 'a') as stats_file:
            wr = csv.writer(stats_file,  dialect='excel')
            if os.stat("significance_testing_data.csv").st_size == 0:
                wr.writerows([headers, list_to_csv])
            else:
                wr.writerows([list_to_csv])
