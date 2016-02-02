'''
The implementation of Bayesian Model for streaming data truth detection presented in
Xin Luna Dong, Laure Berti-Equille, Divesh Srivastava
Data Fusion: Resolvnig Conflicts from Multiple Sources

@author: Evgeny Krivosheev (krivosheevevgeny@gmail.com)
'''

import os
import sys
import csv
import random
import numpy as np


s_number = 5
max_rounds = 30
eps = 0.01
truth_obj_list = [6, 8, 8, 15, 16, 10, 10, 7, 18, 20]
res_obj_list = [None]*len(truth_obj_list)
accuracy_list = [0.8]*s_number

data = [
    [6, 8, None, 15, 16, None, 10, 8, 16, 20],
    [6, None, 8, 15, 16, 7, 9, None, None, 20],
    [None, 6, 13, 15, None, 10, 10, 7, None, 21],
    [6, None, 8, 13, None, 10, 10, 7, 18, None],
    [None, 8, 8, 15, 16, 8, 2, None, None, 20]
]


def get_n_params(data):
    n_list = []
    for i in range(len(data[0])):
        observed_data = [obj[i] for obj in data]
        n = len(set(observed_data))-2
        n_list.append(n)
    return n_list


# def get_accuracy(data, obj_list):
#     accuracy_list = []
#     s_true_nubmer = 0.
#     size_of_val = len(obj_list)
#     for s_index in range(s_number):
#         for index, obj in enumerate(obj_list):
#             if obj == data[s_index][index]:
#                 s_true_nubmer += 1
#         accuracy = s_true_nubmer/(size_of_val+0.2*size_of_val)
#         accuracy_list.append(accuracy)
#         s_true_nubmer = 0.
#     return accuracy_list


def get_prob(data, accuracy):
    n_list = get_n_params(data)
    likelihood = []
    for obj_index in range(len(data[0])):
            likelihood.append([])
            n = n_list[obj_index]
            observed_values = sorted([obj[obj_index] for obj in data])
            possible_values = sorted(list(set(observed_values)-set([None])))
            # if n == 0:
            #     res_obj_list[obj_index] = possible_values[0]
            #     continue
            for v_true in possible_values:
                a, b, b_sum = 1., 1., 0.
                a_not_completed = True
                for v_possible in possible_values:
                    for v, s_index in zip(observed_values, range(s_number)):
                        accuracy = accuracy_list[s_index]
                        if v == v_possible:
                            b *= n*accuracy/(1-accuracy)
                        if a_not_completed and v == v_true:
                            a *= n*accuracy/(1-accuracy)
                    a_not_completed = False
                    b_sum += b
                    b = 1
                p = a/b_sum
                likelihood.update({p: v_true})
            max_likelihood_value = likelihood[max(likelihood.keys())]
            res_obj_list[obj_index] = max_likelihood_value



if __name__ == '__main__':
    accuracy_delta = 0.3
    iter_number = 0

    get_prob(data=data, accuracy=accuracy_list)

    while accuracy_delta > eps and iter_number < max_rounds:
        for obj_index in range(len(data[0])):
            likelihood = {}
            n = n_list[obj_index]
            observed_values = [obj[obj_index] for obj in data]
            possible_values = list(set(observed_values))
            if n == 0:
                res_obj_list[obj_index] = possible_values[0]
                continue
            for v_true in possible_values:
                a, b, b_sum = 1., 1., 0.
                a_not_completed = True
                for v_possible in possible_values:
                    for v, s_index in zip(observed_values, range(s_number)):
                        accuracy = accuracy_list[s_index]
                        if v == v_possible:
                            b *= n*accuracy/(1-accuracy)
                        if a_not_completed and v == v_true:
                            a *= n*accuracy/(1-accuracy)
                    a_not_completed = False
                    b_sum += b
                    b = 1
                p = a/b_sum
                likelihood.update({p: v_true})
            max_likelihood_value = likelihood[max(likelihood.keys())]
            res_obj_list[obj_index] = max_likelihood_value

        accuracy_prev = accuracy_list
        accuracy_list = get_accuracy(data, res_obj_list)
        accuracy_delta = max([abs(k-l) for k, l in zip(accuracy_prev, accuracy_list)])
        iter_number += 1
        print accuracy_delta

    # edit_distance = get_levenshtein_distance(truth_obj_list, obj_list)
    # headers = ['edit_dist', 'p_true', 'iter_number']
    # list_to_csv = [edit_distance, p_true, iter_number]
    # with open('proof_prob_output.csv', 'a') as stats_file:
    #     wr = csv.writer(stats_file,  dialect='excel')
    #     if os.stat("proof_prob_output.csv").st_size == 0:
    #         wr.writerows([headers, list_to_csv])
    #     else:
    #         wr.writerows([list_to_csv])
    #
    # print "acc:{}".format(accuracy_list)
    # print "obj:{}".format(obj_list)
    # print "gt :{}".format(truth_obj_list)
    # print "edit_dist: {}".format(edit_distance)
    # print "iter_numner:{}".format(iter_number)
