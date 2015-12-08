from datetime import datetime
import re


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
    restaurants_list = []
    time_for_norm_obj = []
    with open('restaurants/restaurants_golden.txt') as f0:
        for line in f0:
            params = line.strip().split('\t')
            rest_name = re.sub(r'\W+', '', params[0])
            restaurants_list.append(rest_name)

    rest_list = []
    for i in time_point_list:
        with open('restaurants/' + i[0]) as f:
            t = i[1]
            time_for_norm_obj.append(t)
            for line in f:
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                source = re.sub(r'\W+', '', params[0])
                rest_name = re.sub(r'\W+', '', params[1]).lower()
                if rest_name in restaurants_list:
                    if rest_name not in rest_list:
                        rest_list.append(rest_name)
                addr = re.sub(r'\W+', '', params[2]).lower() if len(params) >= 3 else 'None'
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

    n = 0
    n_list = []
    with open('restaurants/restaurants_golden.txt') as f0:
        for line in f0:
            params = line.strip().split('\t')
            rest_name = re.sub(r'\W+', '', params[0])
            rest_val = re.sub(r'\W+', '', params[1])
            if rest_name in rest_list:
                if rest_val == 'N':
                    n += 1
                    n_list.append(rest_name)
    print 'n = {}'.format(n)
    rest_names = sorted(restaurants.keys())
    rest_values = [restaurants.get(name) for name in rest_names]
    return [normalizing_object] + rest_values, rest_names, n_list
