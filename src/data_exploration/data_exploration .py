import csv
from collections import defaultdict
import pandas as pd
import datetime
from dateutil import parser
import numpy as np

def get_score_sum(score):
    scores = score.replace('[','').replace(']','').replace('\'','').split(',')[0].split('-')
    return int(scores[0]) + int(scores[1])
    

if __name__ == '__main__':
    games = defaultdict(list)
    with open('../data/data.txt') as data_file:
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
            