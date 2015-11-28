import datetime
from raw_value_preparation import cook_raw_value


def get_truth_overlap(truth_list, result_list):
    combained_values = []
    for truth, result in zip(truth_list, result_list):
        t_truth = [datetime.datetime.strptime(truth_point, '%Y-%m-%d %H:%M:%S') for truth_point in truth[0]]
        dict_item = {'GT': [t_truth, truth[1]],
                     'LS': result}
        combained_values.append(dict_item)
    combained_values = cook_raw_value(combained_values)

    distance_to_gt = []
    for obj_item in combained_values:
        k = 0
        gt = obj_item.get('GT')[1]
        ls = obj_item.get('LS')[1]
        for truth, result in zip(gt, ls):
            if truth == result:
                k += 1
        dist = 100*k/len(gt)
        distance_to_gt.append(dist)

    return distance_to_gt
