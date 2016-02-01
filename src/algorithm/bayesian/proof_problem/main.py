'''
The implementation of Bayesian Model for streaming data truth detection presented in
Xin Luna Dong, Laure Berti-Equille, Divesh Srivastava
Data Fusion: Resolvnig Conflicts from Multiple Sources

@author: Evgeny Krivosheev (krivosheevevgeny@gmail.com)
'''

import random
import numpy as np


p_true = 0.7
s_number = 5
max_rounds = 30
eps = 0.01
truth_obj_list = [10, 13, 18, 20, 20, 21, 23, 26, 30, 31]
obj_list = [None]*len(truth_obj_list)
accuracy_list = [0.8]*s_number


def get_data():
    observed_data = []
    for s in range(s_number):
        s_data = []
        for i in range(len(truth_obj_list)):
            ground_truth = truth_obj_list[i]
            r = random.random()
            if r <= p_true:
                s_data.append(ground_truth)
            else:
                w_value = int(np.random.normal(ground_truth, 2, 1)[0])
                s_data.append(w_value)
        observed_data.append(s_data)
    return observed_data


def get_n_params(data):
    n_list = []
    for i in range(len(data[0])):
        observed_data = [obj[i] for obj in data]
        n = len(set(observed_data))-1
        n_list.append(n)
    return n_list


def get_accuracy(data, obj_list):
    accuracy_list = []
    s_true_nubmer = 0.
    size_of_val = len(obj_list)
    for s_index in range(s_number):
        for index, obj in enumerate(obj_list):
            if obj == data[s_index][index]:
                s_true_nubmer += 1
        accuracy = s_true_nubmer/size_of_val
        accuracy_list.append(accuracy)
        s_true_nubmer = 0.
    return accuracy_list


if __name__ == '__main__':
    data = get_data()
    n_list = get_n_params(data)
    accuracy_delta = 0.3
    iter_number = 0

    for i in data:
        print i

    while accuracy_delta > eps or iter_number < max_rounds:
        for obj_index in range(len(data[0])):
            likelihood = {}
            n = n_list[obj_index]
            observed_values = [obj[obj_index] for obj in data]
            possible_values = list(set(observed_values))
            if n == 0:
                obj_list[obj_index] = possible_values[0]
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
            obj_list[obj_index] = max_likelihood_value

        accuracy_prev = accuracy
        accuracy = get_accuracy(data, obj_list)
