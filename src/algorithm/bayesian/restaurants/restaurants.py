from datetime import datetime


def get_restaurants():
    time_point_list = [
        ['restaurants_2009_1_22.txt', datetime(2009, 1, 22)],
        ['restaurants_2009_1_29.txt', datetime(2009, 1, 29)],
        ['restaurants_2009_2_05.txt', datetime(2009, 2, 5)],
        ['restaurants_2009_2_12.txt', datetime(2009, 2, 12)],
        ['restaurants_2009_2_19.txt', datetime(2009, 2, 19)],
        ['restaurants_2009_2_26.txt', datetime(2009, 2, 26)],
        ['restaurants_2009_3_05.txt', datetime(2009, 3, 5)],
        ['restaurants_2009_3_12.txt', datetime(2009, 3, 12)]]

    restaurants = {}
    time_for_norm_obj = []
    for i in time_point_list:
        with open('restaurants/' + i[0]) as f:
            t = i[1]
            time_for_norm_obj.append(t)
            for line in f:
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                source = params[0]
                rest_name = params[1]
                addr = params[2] if len(params) >= 3 else 'None'
                rest_obj = restaurants.get(rest_name)
                if not rest_obj:
                    rest_obj = {}
                s_val = rest_obj.get(source)
                if s_val:
                    if s_val[1][-1] == addr:
                        continue
                    s_val[0].append(t)
                    s_val[1].append(addr)
                else:
                    s_val = [[], []]
                    s_val[0].append(t)
                    s_val[1].append(addr)
                rest_obj.update({source: s_val})
                restaurants.update({rest_name: rest_obj})

    time_for_norm_obj = sorted(time_for_norm_obj)
    values_for_norm_obj = ['Test_{}'.format(index) for index in range(len(time_for_norm_obj))]
    observed_keys = sorted(['MenuPages', 'TasteSpace', 'NYMag', 'NYTimes', 'ActiveDiner', 'TimeOut',
                            'SavoryCities', 'VillageVoice', 'FoodBuzz', 'NewYork', 'OpenTable', 'DiningGuide'])
    normalizing_object = {}
    for s in observed_keys:
        normalizing_object.update({s: [time_for_norm_obj, values_for_norm_obj]})
    return [normalizing_object] + restaurants.values()
