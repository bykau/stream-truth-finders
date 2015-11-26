import itertools
import operator


def most_common(L):
  SL = sorted((x, i) for i, x in enumerate(L))
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]


def majority_voting(observed_cases):
    result_list = []
    for case in observed_cases:
        observed_keys = sorted(case.keys())
        observation_len = len(case.get(observed_keys[0])[0])
        maj_voting_obj_result = [[], []]
        for item in range(observation_len):
            l = []
            for s in observed_keys:
                l.append(case.get(s)[1][item])
            most_common_value = most_common(l)
            if item != 0 and most_common_value == maj_voting_obj_result[1][-1]:
                continue
            else:
                maj_voting_obj_result[1].append(most_common_value)
                maj_voting_obj_result[0].append(case.get(s)[0][item])
        result_list.append(maj_voting_obj_result)

    return result_list
