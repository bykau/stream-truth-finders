from datetime import timedelta
from raw_value_preparation import cook_raw_value


def get_CEF(life_span_set, sources_data):
    """
    :param O:
    :param S:
    :return:
    cl(S,O): capturable
    c(S,O): captured
    ml(S,O): mis-capturable
    m(S,O): mis-captured
    covg: coverage
    exac: exactness
    fresh: freshness
    """
    cl = c = ml = m = 0
    data_for_freshness = []
    for s_life_span, s_data in zip(life_span_set, sources_data):
        synchronised_values = cook_raw_value([{'O': s_life_span, 'S': s_data}])[0]
        O = synchronised_values.get('O')[1]
        S = synchronised_values.get('S')[1]
        s_time_points = synchronised_values.get('S')[0]
        N = len(s_time_points)
        for i in range(N-1):
            if O[i] == S[i] and i == 0:
                c += 1
                cl += 1
                data_for_freshness.append(timedelta(seconds=0))
            elif O[i] == S[i] and O[i] != O[i-1] and S[i] != S[i-1]:
                c += 1
                cl += 1
                data_for_freshness.append(timedelta(seconds=0))

            ml += 1
            if O[i] != S[i]:
                cl += 1
                if O[i+1] == S[i+1]:
                    c += 1
                    data_for_freshness.append(s_time_points[i+1]-s_time_points[i])
                elif O[i+1] != S[i+1]:
                    m += 1

            # if O[i] == S[i] and O[i+1] != S[i+1]:
            #     m += 1

        ml += 1
        if O[N-1] != S[N-1]:
            cl += 1
        elif O[N-1] != O[N-2] and S[N-1] != S[N-2]:
                c += 1
                cl += 1
                data_for_freshness.append(timedelta(seconds=0))

    c = float(c)
    exac = 1 - float(m)/ml
    covg = float(c)/cl
    delta_for_freshness = sorted(list(set(data_for_freshness)))
    fresh = {timedelta(seconds=0): 0.0}
    for delta in delta_for_freshness:
        c_delta = len([k for k in data_for_freshness if delta >= k])
        fresh_delta = c_delta/c
        fresh.update({delta: fresh_delta})

    return [covg, exac, fresh]
