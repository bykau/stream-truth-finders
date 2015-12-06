import csv
from collections import defaultdict
from dateutil import parser
import numpy as np


def get_score_sum(score):
    scores = score.replace('[','').replace(']','').replace('\'','').split(',')[0].split('-')
    return int(scores[0]) + int(scores[1])


def data_preparation(games):
    games_name_list = []
    obj_list = []
    for game in games.keys():
        obj = {}
        for t in sorted(games[game], key=lambda tup: parser.parse(tup[2])):
            s = t[0]
            score_sum = get_score_sum(t[5])
            time = t[2].replace('+0000', '')
            obj_s_val = obj.get(s)
            if obj_s_val:
                if obj_s_val[1][-1] != score_sum:
                    obj_s_val[0].append(time)
                    obj_s_val[1].append(score_sum)
                else:
                    continue
            else:
                obj_s_val = [[time], [score_sum]]
            obj.update({s: obj_s_val})

        games_name_list.append(game)
        obj_list.append(obj)

    with open('data.py', 'w') as f:
        f.write('games_name_list = ' + str(games_name_list) + '\n')
        f.write('observed_cases = ' + str(obj_list) + '\n')


if __name__ == '__main__':
    games = defaultdict(list)
    with open('../data_mining_twitter/data.txt') as data_file:
        data_reader = csv.reader(data_file, delimiter=';')
        for row in data_reader:
            if len(row) > 6:
                game_date = parser.parse(row[2])
                team1 = row[3]
                team2 = row[4]
                if team1 > team2:
                    games[team1+' vs '+team2 + ' ' + str(game_date.month)+'/'+str(game_date.day)].append(row[:6])
                else:
                    games[team2+' vs '+team1 + ' ' + str(game_date.month)+'/'+str(game_date.day)].append(row[:6])
                    
    delays = defaultdict(list)
    for game in games.keys():        
        is_ordered = True
        prev_sum = -1
        for t in sorted(games[game], key=lambda tup: parser.parse(tup[2])):
            score_sum = get_score_sum(t[5])
            if score_sum < prev_sum:
                is_ordered = False
            prev_sum = score_sum
        
        if not is_ordered:
            print game
            for t in sorted(games[game], key=lambda tup: parser.parse(tup[2])):
                print t[0], t[2], t[5], get_score_sum(t[5])
            print
        else:
            prev_time = None
            prev_score_sum = None
            for t in sorted(games[game], key=lambda tup: parser.parse(tup[2])):
                if prev_time is not None:
                    cur_score_sum = get_score_sum(t[5])
                    if prev_score_sum == cur_score_sum:
                        cur_time = parser.parse(t[2])
                        delays[t[0]].append((cur_time - prev_time).total_seconds())
                prev_time = parser.parse(t[2])
                prev_score_sum = get_score_sum(t[5])
    
    for source in delays.keys():
        print "{}\t{}\t{:.1f}\t{:.1f}".format(source, len(delays[source]), np.average(delays[source]), np.std(delays[source]))

    data_preparation(games)
