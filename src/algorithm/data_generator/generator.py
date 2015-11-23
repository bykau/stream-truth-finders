import random
import string
from datetime import datetime


time_points = ['2000-01-01 00:00:00', '2000-01-05 00:00:00', '2000-01-07 00:00:00',
               '2000-01-10 00:00:00', '2000-01-11 00:00:00', '2000-01-13 00:00:00',
               '2000-01-17 00:00:00', '2000-01-20 00:00:00', '2000-01-25 00:00:00',
               '2000-01-29 00:00:00', '2000-02-01 00:00:00', '2000-02-08 00:00:00',
               '2000-02-10 00:00:00', '2000-02-11 00:00:00', '2000-02-15 00:00:00',
               '2000-02-19 00:00:00', '2000-02-23 00:00:00', '2000-02-25 00:00:00',
               '2000-02-27 00:00:00', '2000-02-28 00:00:00']

number_of_object = 100
ground_truth_list = []
for i in range(number_of_object):
    t = [time_points[0]]
    v = [random.choice(string.ascii_uppercase)]
    number_of_v = random.choice(range(len(time_points)/2))
    for j in range(number_of_v):
        t.append(random.choice(list(set(time_points)-set(t))))
        v.append(random.choice(string.ascii_uppercase.replace(v[-1], '')))
    ground_truth_list.append([sorted(t), v])


p_i = 0.5
p_e = 0.2
p_o = 0.3

p_t = 0.75
p_f = 0.99
f0 = 0.1

number_of_sources = 10
observed_cases = []
for i in range(number_of_object):
    obj = {}
    gt_time_points = ground_truth_list[i][0]
    for s in range(number_of_sources):
        t = []
        v = []
        for t_index, t_point in enumerate(time_points):
            x = random.random()
            if t_index == 0:
                if x <= p_i:
                    t.append(t_point)
                else:
                    continue
            elif t_index == 19:
                if x <= p_e:
                    t.append(t_point)
                else:
                    continue
            else:
                if x <= p_o:
                    t.append(t_point)
                else:
                    continue

            for t_gt_index, t_gt in enumerate(gt_time_points):
                if t_gt > t_point:
                    t_gt_point = gt_time_points[t_gt_index-1]
                    break
                elif t_gt == t_point:
                    t_gt_point = t_gt
                    break
                elif len(gt_time_points) == 1:
                    t_gt_point = t_gt
                    break
                else:
                    t_gt_point = t_gt
                    break

            delta = datetime.strptime(t_point, '%Y-%m-%d %H:%M:%S') - datetime.strptime(t_gt_point, '%Y-%m-%d %H:%M:%S')
            normz_factor = datetime.strptime(time_points[-1], '%Y-%m-%d %H:%M:%S') - datetime.strptime(time_points[0], '%Y-%m-%d %H:%M:%S')
            delata_normalized = delta.total_seconds()/normz_factor.total_seconds()

        obj.update({'S{}'.format(s): [t, v]})
    observed_cases.append(obj)

with open('data.py', 'w') as f:
    f.write('ground_truth_list = ' + str(ground_truth_list) + '\n')
    f.write('observed_cases = ' + str(observed_cases) + '\n')
