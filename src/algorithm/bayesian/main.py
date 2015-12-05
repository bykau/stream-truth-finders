'''
The implementation of Bayesian Model for streaming data truth detection presented in
Xin Luna Dong, Laure Berti-Equille, Divesh Srivastava, (2012)
Truth Discovery and Copying Detection in a Dynamic World, http://www.vldb.org/pvldb/2/vldb09-335.pdf

@author: Evgeny Krivosheev (krivosheevevgeny@gmail.com)
'''

import os
import csv
import datetime
import numpy as np

from cef_measure import get_CEF
from life_span import get_life_span
from algorithm_competitors import majority_voting
from raw_value_preparation import cook_raw_value
from evaluation_methods import get_levenshtein_distance
from src.algorithm.data_generator import get_observed_cases,\
    ground_truth_list, p_t_mean, f0_mean
from restaurants.restaurants import get_restaurants


def cef_initialization(c, e, observed, sources):
    observed_keys = sorted(sources)
    cef_measures = {}
    f_init = {}
    time_observation = observed.values()[0][0]
    delta_max = datetime.timedelta(seconds=0)
    for t_index, t in enumerate(time_observation[:-1]):
        delta = time_observation[t_index+1]-t
        if delta > delta_max:
            delta_max = delta
    f_item = 1./6
    t_item = delta_max/5
    f = f_item
    delta = datetime.timedelta(seconds=0)
    while delta <= delta_max:
        f_init.update({delta: f})
        f += f_item
        delta += t_item
    for s in observed_keys:
        cef = [c, e, f_init]
        cef_measures.update({s: cef})

    return cef_measures

headers = ['Round', 'Life span',
            'S1.C', 'S1.E', 'S1.F, days',
            'S2.C', 'S2.E', 'S2.F, days',
            'S3.C', 'S3.E', 'S3.F, days',
            'S4.C', 'S4.E', 'S4.F, days',
            'S5.C', 'S5.E', 'S5.F, days',
            'S6.C', 'S6.E', 'S6.F, days',
            'S7.C', 'S7.E', 'S7.F, days',
            'S8.C', 'S8.E', 'S8.F, days',
            'S9.C', 'S9.E', 'S9.F, days',
            'S10.C', 'S10.E', 'S10.F, days']

if __name__ == '__main__':
    # raw_cases = get_observed_cases()
    raw_cases = get_restaurants()
    observed_cases = cook_raw_value(raw_cases)
    observed_keys = sorted(['MenuPages', 'TasteSpace', 'NYMag', 'NYTimes', 'ActiveDiner', 'TimeOut',
                            'SavoryCities', 'VillageVoice', 'FoodBuzz', 'NewYork', 'OpenTable', 'DiningGuide'])
    cef_measures = cef_initialization(c=0.7, e=0.7, observed=observed_cases[0], sources=observed_keys)
    set_of_life_spans = []
    sources_number = len(observed_keys)
    cases_number = len(observed_cases)

    iter_quantity = 0
    data_for_csv = {}
    for case_number, observed in enumerate(observed_cases):
        life_span = get_life_span(observed=observed, cef_measures=cef_measures)
        set_of_life_spans.append(life_span)

        # print initial info
        life_span_to_csv = []
        for t, val in zip(life_span[0], life_span[1]):
            life_span_to_csv.append([t.strftime('%Y-%m-%d'), val])
        cef_for_csv = []
        for s in observed_keys:
            try:
                cef = cef_measures[s]
            except TypeError:
                pass
            f_for_print = ['{}: {}'.format(t.days, cef[2][t]) for t in sorted(cef[2].keys())]
            cef_for_csv += [round(cef[0], 3), round(cef[1], 3), f_for_print]
        data_for_csv.update({case_number: [headers, [0] + [life_span_to_csv] + cef_for_csv]})
    print '---------------------'

    # # for testing cef measures
    # ground_truth = [set_of_life_spans[0]]
    # for i in ground_truth_list:
    #     time_i = []
    #     for j in i[0]:
    #         time_i.append(datetime.datetime.strptime(j, '%Y-%m-%d %H:%M:%S'))
    #     ground_truth.append([time_i, i[1]])
    # cef_gt = []
    # observed_cases_changed = [] + observed_cases
    # for observed_case_index in range(cases_number):
    #     observed_cases_changed[observed_case_index].update({'life_span': ground_truth[observed_case_index]})
    # observed_cases_changed = cook_raw_value(observed_cases_changed)
    #
    # for s in observed_keys:
    #     sources_data = []
    #     for case in raw_cases:
    #         sources_data.append(case.get(s))
    #     cef = get_CEF(life_span_set=ground_truth,
    #                   sources_data=sources_data)
    #     cef_gt.append(cef)
    # # end testing cef measures

    cef_for_each_s_old = [cef_measures.get(s) for s in observed_keys]
    ce_delta_sum = [1, 1]
    while max(ce_delta_sum) > 0.01*sources_number:
        cef_for_each_s = []
        observed_cases_changed = [] + observed_cases
        for observed_case_index in range(cases_number):
            observed_cases_changed[observed_case_index].update({'life_span': set_of_life_spans[observed_case_index]})
        observed_cases_changed = cook_raw_value(observed_cases_changed)

        time_points = observed_cases_changed[0].get('life_span')[0]
        for s in observed_keys:
            sources_data = []
            time_points = []
            for case in raw_cases:
                s_data = case.get(s)
                if not s_data:
                    continue
                sources_data.append(s_data)
            cef = get_CEF(life_span_set=set_of_life_spans,
                          sources_data=sources_data)
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
        # majority_voting_result = majority_voting(observed_cases_changed)
        # levenshtein_distance = get_levenshtein_distance(ground_truth_list, set_of_life_spans[1:])
        # levenshtein_distance_m_voting = get_levenshtein_distance(ground_truth_list, majority_voting_result[1:])

        # from src.algorithm.data_generator.data import observed_cases as print_cases
        iter_quantity += 1
        # print '---------------------'
        # print 'round={}'.format(iter_quantity)
        # print 'ce_delta_sum: {}'.format(ce_delta_sum)
        # cef_for_csv = []
        # for cef, s in zip(cef_for_each_s, observed_keys):
        #     print s, ': C={}, E={}, F={}'.format(cef[0], cef[1], cef[2])
        #     f_for_print = ['{}: {}'.format(t.days, cef[2][t]) for t in sorted(cef[2].keys())]
        #     cef_for_csv += [round(cef[0], 3), round(cef[1], 3), f_for_print]
        # for case_index, life_span in enumerate(set_of_life_spans[1:]):
        #     list_to_print = []
        #     for t, val in zip(life_span[0], life_span[1]):
        #         list_to_print.append([t.strftime('%Y-%m-%d'), val])
        #     print '---------------------'
        #     print "Object {}, ed.dist={}, ed.dist_mv={} life span: {}".format(case_index, levenshtein_distance[case_index],
        #                                                                     levenshtein_distance_m_voting[case_index], list_to_print)
        #     # print "Gtound Truth:                                   {}".format([[tm[0:10], vl] for tm, vl in zip(ground_truth_list[case_index][0], ground_truth_list[case_index][1])])
        #     list_to_csv = [] + ['{}, {}'.format(str(iter_quantity), levenshtein_distance[case_index])] + [str(list_to_print)] + cef_for_csv
        #     data = data_for_csv[case_index] + [list_to_csv]
        #     data_for_csv.update({case_index: data})

    print 'iter_quantity={}'.format(iter_quantity)
    print "*********************************************************"
    #
    # with open('output_data.csv', 'w') as result_file:
    #     wr = csv.writer(result_file,  dialect='excel')
    #     for obj, name in zip(data_for_csv, range(len(observed_cases))):
    #             wr.writerows([['Object {}'.format(name)]] + data_for_csv[obj] + [''] + [''])
    #
    # cov_delta = []
    # exac_delta = []
    # for s in range(sources_number):
    #     cov_delta.append(abs(cef_gt[s][0]-cef_for_each_s[s][0]))
    #     exac_delta.append(abs(cef_gt[s][1]-cef_for_each_s[s][1]))
    # headers_statistics = ['p_t mean', 'f0 mean', 'edit dist', 'edit std',
    #                       'edit dist mv', 'edit std mv', 'cov delta',
    #                       'cov std', 'exac delta', 'exac std']
    # stat_list = [p_t_mean, f0_mean, round(np.mean(levenshtein_distance), 3), round(np.std(levenshtein_distance), 3),
    #              round(np.mean(levenshtein_distance_m_voting), 3), round(np.std(levenshtein_distance_m_voting), 3),
    #              round(np.mean(cov_delta), 3), round(np.std(cov_delta), 3),
    #              round(np.mean(exac_delta), 3), round(np.std(exac_delta), 3)]
    # with open('statistics_data.csv', 'a') as stats_file:
    #     wr = csv.writer(stats_file,  dialect='excel')
    #     if os.stat("statistics_data.csv").st_size == 0:
    #         wr.writerows([headers_statistics, stat_list])
    #     else:
    #         wr.writerows([stat_list])
