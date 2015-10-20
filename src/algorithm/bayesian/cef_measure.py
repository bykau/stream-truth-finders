from datetime import timedelta


def get_CEF(life_span, source_data):
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
    time_points = life_span[0]
    N = len(time_points)
    O = life_span[1]
    S = source_data[1]
    data_for_freshness = []
    for i in range(N-1):
        ml += 1
        if O[i] != S[i]:
            cl += 1
            if O[i+1] == S[i+1]:
                c += 1
                data_for_freshness.append(time_points[i+1]-time_points[i])
            elif O[i+1] != S[i+1]:
                m += 1

        if O[i] == S[i] and O[i+1] != S[i+1]:
            m += 1

    # cl += 1
    ml += 1
    # if O[0] == S[0]:
    #     c += 1
    # else:
    #     m += 1
    if O[N-1] != S[N-1]:
        cl += 1

    c = float(c)
    exac = 1 - float(m)/ml
    # !!!to do!!!`
    try:
        covg = float(c)/cl
    except ZeroDivisionError:
        covg = 1.
    delta_for_freshness = sorted(list(set(data_for_freshness)))
    fresh = {timedelta(seconds=0): 0.0}
    for delta in delta_for_freshness:
        c_delta = len([k for k in data_for_freshness if delta >= k])
        fresh_delta = c_delta/c
        fresh.update({delta: fresh_delta})

    return [covg, exac, fresh]
