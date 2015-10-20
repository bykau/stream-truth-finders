import datetime
# from data_for_tests import observed_cases


def cook_raw_value(observed_cases):
    observed_cases_new = []
    for test_case in observed_cases:
        time_set_new = []
        test_case_new = {}
        for s in test_case:
            time_set_new += (test_case.get(s)[0])
        time_set_new = sorted(list(set(time_set_new)))
        for s in test_case:
            s_values_new = []
            timestamp_set = []
            time_set_new_temp = [] + time_set_new
            s_values = test_case.get(s)[1]
            s_time_set = test_case.get(s)[0]
            for t_index, t in enumerate(s_time_set):
                for t_new_index, t_new in enumerate(time_set_new_temp):
                    try:
                        if t_new < t and t_index == 0:
                            s_values_new.append(None)
                            timestamp_set.append(t_new)
                        elif t_new < t:
                            s_values_new.append(s_values[t_index-1])
                            timestamp_set.append(t_new)
                        elif t_new == t and t_new_index != 0:
                            s_values_new.append(s_values[t_index])
                            timestamp_set.append(t_new)
                            if t_index == len(s_time_set)-1:
                                continue
                            del time_set_new_temp[0:t_new_index+1]
                            break
                        elif t_index == 0 and t_new < s_time_set[1]:
                                s_values_new.append(s_values[t_index])
                                timestamp_set.append(t_new)
                        elif t_index == (len(s_time_set)-1):
                            s_values_new.append(s_values[t_index])
                            timestamp_set.append(t_new)
                        else:
                            del time_set_new_temp[0:t_new_index]
                            break
                    except IndexError:
                        s_values_new.append(s_values[t_index])
                        timestamp_set.append(t_new)

            test_case_new.update({s: [sorted(timestamp_set), s_values_new]})
        observed_cases_new.append(test_case_new)

    return observed_cases_new
