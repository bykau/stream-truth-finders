import operator


def get_initial_value(observed, cef_measures):
    initial_values = []
    observed_keys = sorted(observed.keys())
    all_possible_values = []
    for s in observed_keys:
        observed_values = observed.get(s)[1]
        all_possible_values += observed_values
        for value in observed_values:
            if value:
                break
        if value not in initial_values:
            initial_values.append(value)

    all_possible_values = list(set(all_possible_values))
    if None in all_possible_values:
        all_possible_values.remove(None)
    likelihood = {}
    for value in initial_values:
        p = 1
        for s in observed_keys:
            m = len(all_possible_values)-1
            observed_values = observed.get(s)[1]
            for observed_value in observed_values:
                if observed_value:
                    break
            coverage = cef_measures.get(s)[0]
            exactness = cef_measures.get(s)[1]

            if observed_value == value:
                if value:
                    p *= exactness*coverage
                else:
                    p *= exactness
            elif observed_value != value and observed_value:
                p *= (1-exactness)/m
            else:
                p *= exactness*(1-coverage)

        likelihood.update({value: p})

    max_likelihood_value = max(likelihood.iteritems(), key=operator.itemgetter(1))[0]

    return max_likelihood_value, m


def get_life_span(observed, cef_measures):
    life_span = [[], []]
    initial_value, m = get_initial_value(observed, cef_measures)
    observation_len = len(observed.get(observed.keys()[0])[1])
    observed_keys = sorted(observed.keys())
    start_time = observed.get(observed_keys[0])[0][0]
    end_time = observed.get(observed_keys[0])[0][observation_len-1]
    life_span[0].append(start_time)
    life_span[1].append(initial_value)
    observation_time = observed.get(observed_keys[0])[0]

    tr_last = start_time
    tr_last_index = 0
    while tr_last < observation_time[-2]:
        likelihood = {}
        p_no_transition = 1.
        potential_values = []
        for s in observed_keys:
            s_values = observed.get(s)[1]
            for value in s_values:
                if value not in potential_values:
                    potential_values.append(value)
        if None in potential_values:
            potential_values.remove(None)
        life_span_pre_val = life_span[1][-1]
        life_span_pre_time = life_span[0][-1]
        if life_span_pre_val in potential_values:
                potential_values.remove(life_span_pre_val)
        if len(potential_values) == 0:
            break
        for tr_index, tr in enumerate(observation_time[tr_last_index+1:observation_len-1]):
            tr_index += tr_last_index+1
            for v in potential_values:
                p = 1
                for s in observed_keys:
                    coverage = cef_measures.get(s)[0]
                    exactness = cef_measures.get(s)[1]
                    freshness = cef_measures.get(s)[2]
                    freshness_keys = sorted(freshness.keys())
                    s_values = observed.get(s)[1]
                    observed_values = s_values[tr_index:]
                    for observed_val_index, observed_val in enumerate(observed_values):
                        tu = observation_time[tr_index+observed_val_index]
                        tu_1_index = tr_index+observed_val_index-1
                        while tu_1_index > 0:
                            val_tu_1 = s_values[tu_1_index]
                            prev_val = s_values[tu_1_index-1]
                            if val_tu_1 != prev_val:
                                tu_1 = observation_time[tu_1_index]
                                break
                            elif tu_1_index-1 == 0:
                                tu_1 = observation_time[0]
                                tu_1_index -= 1
                                break
                            tu_1_index -= 1
                        if observed_val == s_values[tu_1_index]:
                            if observed_val_index == len(observed_values)-1:
                                time_delta = end_time - tr
                                if tr == observation_time[tr_last_index+1] and observed_val == potential_values[0]:
                                    p_no_transition *= exactness
                                if len(freshness) == 1:
                                    f = 0.0
                                else:
                                    for t_index, t in enumerate(freshness_keys[:-1]):
                                        if time_delta >= t and time_delta < freshness_keys[t_index+1]:
                                            f = freshness.get(t)
                                            break
                                        elif t == freshness_keys[-2]:
                                            f = 1.
                                            break
                                p *= exactness*(1-coverage)*f
                            else:
                                continue
                        else:
                            # tu = observation_time[tr_index+observed_val_index]
                            # tu_1_index = tr_index+observed_val_index-1
                            # while tu_1_index > 0:
                            #     val_tu_1 = s_values[tu_1_index]
                            #     prev_val = s_values[tu_1_index-1]
                            #     if val_tu_1 != prev_val:
                            #         tu_1 = observation_time[tu_1_index]
                            #         break
                            #     elif tu_1_index-1 == 0:
                            #         tu_1 = observation_time[0]
                            #         tu_1_index -= 1
                            #         break
                            #     tu_1_index -= 1
                            if tr == observation_time[tr_last_index+1] and observed_val == potential_values[0]:
                                p_no_transition *= (1-exactness)*float((tu-tu_1).total_seconds()) \
                                                   /(m*float((end_time-life_span_pre_time).total_seconds()))
                            if observed_val == v:
                                time_delta = tu - tr
                                if len(freshness) == 1:
                                    f = 0.0
                                else:
                                    for t_index, t in enumerate(freshness_keys[:-1]):
                                        if time_delta >= t and time_delta < freshness_keys[t_index+1]:
                                            f = freshness.get(t)
                                            break
                                        elif t == freshness_keys[-2]:
                                            f = 1.
                                            break
                                p *= exactness*coverage*f
                            else:
                                p *= (1-exactness)*float((tu-tu_1).total_seconds()) \
                                     /(m*float((end_time-life_span_pre_time).total_seconds()))
                            break
                likelihood.update({p: [tr, v]})
        p_max = max(likelihood.keys())
        max_likelihood_value = likelihood.get(p_max)
        life_span[0].append(max_likelihood_value[0])
        life_span[1].append(max_likelihood_value[1])
        # if p_max > p_no_transition:
        #     life_span[0].append(max_likelihood_value[0])
        #     life_span[1].append(max_likelihood_value[1])
        # else:
        #     break

        tr_last = max_likelihood_value[0]
        tr_last_index = observation_time.index(tr_last)

    return life_span