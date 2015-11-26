__all__ = ['get_observed_cases']


import datetime
from .data import observed_cases


def get_observed_cases():
    observed_cases_new = []
    time_for_norm_obj = []
    for case in observed_cases:
        case_new = {}
        for s in case:
            t_new = []
            for t in case.get(s)[0]:
                t_new.append(datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S'))
                time_for_norm_obj.append(datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S'))
            case_new.update({s: [t_new, case.get(s)[1]]})
        observed_cases_new.append(case_new)

    time_for_norm_obj = sorted(list(set(time_for_norm_obj)))
    values_for_norm_obj = ['Test_{}'.format(index) for index in range(len(time_for_norm_obj))]
    normalizing_object = {}
    for s in sorted(observed_cases[0].keys()):
        normalizing_object.update({s: [time_for_norm_obj, values_for_norm_obj]})

    return [normalizing_object] + observed_cases_new
