import random
import numpy as np


truth_obj_list = [10, 13, 18, 20, 20, 21, 23, 26, 30, 31]
p_true = 0.7


def get_data():
    observed_data = []
    for s in range(5):
        s_data = []
        for i in range(10):
            ground_truth = truth_obj_list[i]
            r = random.random()
            if r <= p_true:
                s_data.append(ground_truth)
            else:
                w_value = int(np.random.normal(ground_truth, 2, 1)[0])
                s_data.append(w_value)
        observed_data.append(s_data)
    return observed_data

if __name__ == '__main__':
    data = get_data()
    for i in data:
        print i
