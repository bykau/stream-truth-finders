from cef_measure import get_CEF
from life_span import get_life_span
from algorithm_competitors import majority_voting
from raw_value_preparation import cook_raw_value
from datetime import timedelta

from src.algorithm import get_observed_cases


def get_truth_overlap(truth, result):
    k = 0
    for index, value in enumerate(result):
        if value == truth[index]:
            k += 1

    return 100*k/len(truth)


def cef_initialization(c, e, observed):
    observed_keys = sorted(observed.keys())
    cef_measures = {}
    f_init = {}
    time_observation = observed.get(observed_keys[0])[0]
    delta_max = timedelta(seconds=0)
    for t_index, t in enumerate(observed.get(observed_keys[0])[0][:-1]):
        delta = time_observation[t_index+1]-t
        if delta > delta_max:
            delta_max = delta
    f = 0.
    f_item = 1./3
    t_item = delta_max/3
    delta = timedelta(seconds=0)
    # while delta <= delta_max:
    #     f_init.update({delta: f})
    #     f += f_item
    #     delta += t_item
    f_init = {timedelta(days=0): 0.1,
         timedelta(days=365): 0.2,
         timedelta(days=366): 0.2}
    for s in observed_keys:
        cef = [c, e, f_init]
        cef_measures.update({s: cef})

    return cef_measures


if __name__ == '__main__':
    # ground_truth = ['Wisc', 'MSR']

    observed_cases = cook_raw_value(get_observed_cases())
    observed_keys = sorted(observed_cases[0].keys())
    cef_measures = cef_initialization(c=0.99, e=0.95, observed=observed_cases[0])
    set_of_life_spans = []
    sources_number = len(observed_keys)
    cases_number = len(observed_cases)

    for case_number, observed in enumerate(observed_cases):
        iter_quantity = 0
        life_span = get_life_span(observed=observed, cef_measures=cef_measures)
        set_of_life_spans.append(life_span)

        # print initial info
        print 'OBJECT NUMBER: {}'.format(case_number)
        # print 'Ground truth: {}'.format(ground_truth)
        for key in observed_keys:
            print '{}: {}'.format(key, observed.get(key)[1])
        print 'Initial life span: {}'.format(life_span)
    print '---------------------'

    cef_for_each_s_old = [cef_measures.get(s) for s in observed_keys]
    ce_delta_sum = [1, 1]
    while max(ce_delta_sum) > 0.01*sources_number*cases_number:
        cef_for_each_s = []
        observed_cases_changed = [] + observed_cases
        for observed_case_index in range(cases_number):
            observed_cases_changed[observed_case_index].update({'life_span': set_of_life_spans[observed_case_index]})
        observed_cases_changed = cook_raw_value(observed_cases_changed)

        time_points = observed_cases_changed[0].get('life_span')[0]
        for s in observed_keys:
            life_span_set = []
            sources_data = []
            time_points = []
            for case in observed_cases_changed:
                life_span_set.append(case.get('life_span')[1])
                sources_data.append(case.get(s)[1])
                time_points.append(case.get('life_span')[0])
            cef = get_CEF(life_span_set=life_span_set,
                          sources_data=sources_data,
                          time_points=time_points)
            cef_measures.update({s: cef})
            cef_for_each_s.append(cef)

        set_of_life_spans = []
        for observed_changed in observed_cases_changed:
            del observed_changed['life_span']
            life_span = get_life_span(observed=observed_changed, cef_measures=cef_measures)
            set_of_life_spans.append(life_span)

        ce_delta_sum = [0, 0]
        for old, new in zip(cef_for_each_s_old, cef_for_each_s):
            diff_for_s = [abs(x-y) for x, y in zip(old[0:2], new[0:2])]
            for i in range(len(ce_delta_sum)):
                ce_delta_sum[i] += diff_for_s[i]
        cef_for_each_s_old = cef_for_each_s
        # majority_voting_result = majority_voting(observed)

        iter_quantity += 1
        print '---------------------'
        print 'iter={}'.format(iter_quantity)
        print 'ce_delta_sum: {}'.format(ce_delta_sum)
        for cef, s in zip(cef_for_each_s, observed_keys):
            print s, ': C={}, E={}, F={}'.format(cef[0], cef[1], cef[2])
        for case_index, life_span in enumerate(set_of_life_spans):
            list_to_print = []
            for t, val in zip(life_span[0], life_span[1]):
                list_to_print.append([t.strftime('%Y'), val])
            print "Object {} life span: {}".format(case_index, list_to_print)
        # print 'Majority voting results: {} {}%' \
        #     .format(majority_voting_result, get_truth_overlap(ground_truth, majority_voting_result))

    print 'iter_quantity={}'.format(iter_quantity)
    print "*********************************************************"
