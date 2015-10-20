from random import sample, choice


def generator(exactness, ground_truth):
    ml = len(ground_truth)
    m = int(round((1 - exactness) * ml))
    new_set = [None] * ml
    change_value_indexes = sample(range(ml), m)
    for i in range(ml):
        if i in change_value_indexes:
            temp_list = [x for x in ground_truth if x != ground_truth[i]]
            temp_list = list(set(temp_list))
            if None not in temp_list:
                temp_list.append(None)
            temp_list.append('UCB')
            temp_list.append('BEA')
            new_set[i] = choice(temp_list)
        else:
            new_set[i] = ground_truth[i]

    return new_set