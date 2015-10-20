import itertools
import operator


def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]


def majority_voting(observed):
    observed_keys = sorted(observed.keys())
    observation_len = len(observed.get("S1"))

    result_list = []
    for item in range(observation_len):
        l = []
        for s in observed_keys:
            l.append(observed.get(s)[item])
        result_list.append(most_common(l))

    return result_list
