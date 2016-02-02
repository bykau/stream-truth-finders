'''
The implementation of Bayesian Model for streaming data truth detection presented in
Xin Luna Dong, Laure Berti-Equille, Divesh Srivastava
Data Fusion: Resolvnig Conflicts from Multiple Sources

@author: Evgeny Krivosheev (krivosheevevgeny@gmail.com)
'''

import os
import sys
import csv
import numpy as np
import copy


s_number = 5
max_rounds = 30
eps = 0.01
numb_of_swaps = 101
truth_obj_list = [6, 8, 8, 15, 16, 10, 10, 7, 18, 20]

data_init = [
    [6, 8, None, 15, 16, None, 10, 8, 16, 20],
    [6, None, 8, 15, 16, 7, 9, None, None, 20],
    [None, 6, 13, 15, None, 10, 10, 7, None, 21],
    [6, None, 8, 13, None, 10, 10, 7, 18, None],
    [None, 8, 8, 15, 16, 8, 2, None, None, 20]
]
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
                    try:
                        p_sum += prob[obj_index][v_ind]
                    except IndexError:
                        pass
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
                likelihood[obj_index].append(0.99)
                continue
            for v_true in possible_values:
                a, b, b_sum = 1., 1., 0.
                a_not_completed = True
                for v_possible in possible_values:
                    for v, s_index in zip(observed_values, range(s_number)):
                        if v == None:
                            continue
                        accuracy = accuracy_list[s_index]
                        if v == v_possible:
                            b *= n*accuracy/(1-accuracy)
                        if a_not_completed and v == v_true:
                            a *= n*accuracy/(1-accuracy)
                    a_not_completed = False
                    b_sum += b
                    b = 1
                p = a/b_sum
                likelihood[obj_index].append(p)
    return likelihood


def swap_data(data, n):
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
    for i in range(numb_of_swaps):
        dist_metric_list = []
        for j in range(10):
            accuracy_delta = 0.3
            iter_number = 0
            accuracy_list = [0.8]*s_number
            data = copy.deepcopy(data_init)
            data = swap_data(data, i)
            while accuracy_delta > eps and iter_number < max_rounds:
                try:
                    prob = get_prob(data=data, accuracy=accuracy_list)
                except ZeroDivisionError:
                    print i
                accuracy_prev = accuracy_list
                accuracy_list = get_accuracy(data, prob)
                accuracy_delta = max([abs(k-l) for k, l in zip(accuracy_prev, accuracy_list)])
                iter_number += 1
            dist_metric = get_dist_metric(data, prob)
            dist_metric_list.append(dist_metric)
            print "dist_metric: {}".format(dist_metric)

        dist_metric_mean = np.mean(dist_metric_list)
        dist_metric_std = np.std(dist_metric_list)
        headers = ['dist_metric_mean', 'dist_metric_std', 'number_of_swaps']
        list_to_csv = [dist_metric_mean, dist_metric_std, i]
        with open('proof_prob_output.csv', 'a') as stats_file:
            wr = csv.writer(stats_file,  dialect='excel')
            if os.stat("proof_prob_output.csv").st_size == 0:
                wr.writerows([headers, list_to_csv])
            else:
                wr.writerows([list_to_csv])

