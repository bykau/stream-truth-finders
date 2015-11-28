import datetime
from raw_value_preparation import cook_raw_value


def get_combained_values(truth_list, result_list):
    combained_values = []
    for truth, result in zip(truth_list, result_list):
        t_truth = [datetime.datetime.strptime(truth_point, '%Y-%m-%d %H:%M:%S') for truth_point in truth[0]]
        dict_item = {'GT': [t_truth, truth[1]],
                     'LS': result}
        combained_values.append(dict_item)
    combained_values = cook_raw_value(combained_values)

    return combained_values


def get_truth_overlap(truth_list, result_list):
    combained_values = get_combained_values(truth_list, result_list)
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


def get_levenshtein_distance(truth_list, result_list):
    combained_values = get_combained_values(truth_list, result_list)
    levenshtein_distance = []
    for obj_item in combained_values:
        gt = obj_item.get('GT')[1]
        ls = obj_item.get('LS')[1]
        len_gt = len(gt)
        len_ls = len(ls)
        dist = [[0 for j in range(len_ls+1)] for i in range(len_gt+1)]
        for i in range(len_gt+1):
            for j in range(len_ls+1):
                if i == 0:
                    dist[i][j] = j
                elif j == 0:
                    dist[i][j] = i
                if i > 0 and j > 0:
                    a = dist[i-1][j-1] if gt[i-1] == ls[j-1] else dist[i-1][j-1] + 1
                    dist[i][j] = min(dist[i][j-1] + 1, dist[i-1][j] + 1, a)
        levenshtein_distance.append(dist[len_gt][len_ls])

    return levenshtein_distance

