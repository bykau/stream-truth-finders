from datetime import datetime


time_point_list = [
    ['restaurants_2009_1_22.txt', datetime(2009, 1, 22)],
    ['restaurants_2009_1_29.txt', datetime(2009, 1, 29)],
    ['restaurants_2009_2_05.txt', datetime(2009, 2, 5)],
    ['restaurants_2009_2_12.txt', datetime(2009, 2, 12)],
    ['restaurants_2009_2_19.txt', datetime(2009, 2, 19)],
    ['restaurants_2009_2_26.txt', datetime(2009, 2, 26)],
    ['restaurants_2009_3_05.txt', datetime(2009, 3, 5)],
    ['restaurants_2009_3_12.txt', datetime(2009, 3, 12)]]

f0_list = []
with open(time_point_list[0][0]) as f0:
    for line in f0:
        params = line.strip().split('\t')
        f0_list.append(params)
