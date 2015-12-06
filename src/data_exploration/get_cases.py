import datetime
import csv
from src.data_exploration.data import observed_cases, games_name_list


def get_game_cases():
    observed_cases_new = []
    time_for_norm_obj = []
    for case in observed_cases:
        case_new = {}
        for s in case:
            t_new = []
            for t in case.get(s)[0]:
                t_new.append(datetime.datetime.strptime(t, '%a %b %d %H:%M:%S %Y'))
                time_for_norm_obj.append(datetime.datetime.strptime(t, '%a %b %d %H:%M:%S %Y'))
            case_new.update({s: [t_new, case.get(s)[1]]})
        observed_cases_new.append(case_new)

    time_for_norm_obj = sorted(list(set(time_for_norm_obj)))
    values_for_norm_obj = ['Test_{}'.format(index) for index in range(len(time_for_norm_obj))]
    normalizing_object = {}

    football_sources = []
    with open('../../data_mining_twitter/accounts.csv', 'rb') as f:
        clubs = csv.reader(f)
        for club in clubs:
            football_sources.append(club[0].split(';')[0])

    for s in football_sources:
        normalizing_object.update({s: [time_for_norm_obj, values_for_norm_obj]})

    return normalizing_object, observed_cases_new, games_name_list, football_sources
