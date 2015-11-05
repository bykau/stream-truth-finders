__all__ = ['get_observed_cases']

import datetime

observed_cases = [
    # case 0 from article
    # normalisation
    # # normalisation
    # {
    #     'S1': [['2000-01-01 00:00:00', '2001-01-01 00:00:00', '2002-01-01 00:00:00',
    #             '2003-01-01 00:00:00', '2004-01-01 00:00:00', '2005-01-01 00:00:00',
    #             '2006-01-01 00:00:00', '2007-01-01 00:00:00', '2008-01-01 00:00:00',
    #             '2009-01-01 00:00:00'],
    #            ['UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT']],
    #     'S2': [['2000-01-01 00:00:00', '2001-01-01 00:00:00', '2002-01-01 00:00:00',
    #             '2003-01-01 00:00:00', '2004-01-01 00:00:00', '2005-01-01 00:00:00',
    #             '2006-01-01 00:00:00', '2007-01-01 00:00:00', '2008-01-01 00:00:00',
    #             '2009-01-01 00:00:00'],
    #            ['UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT']],
    #     'S3': [['2000-01-01 00:00:00', '2001-01-01 00:00:00', '2002-01-01 00:00:00',
    #             '2003-01-01 00:00:00', '2004-01-01 00:00:00', '2005-01-01 00:00:00',
    #             '2006-01-01 00:00:00', '2007-01-01 00:00:00', '2008-01-01 00:00:00',
    #             '2009-01-01 00:00:00'],
    #            ['UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT']],
    #     'S4': [['2000-01-01 00:00:00', '2001-01-01 00:00:00', '2002-01-01 00:00:00',
    #             '2003-01-01 00:00:00', '2004-01-01 00:00:00', '2005-01-01 00:00:00',
    #             '2006-01-01 00:00:00', '2007-01-01 00:00:00', '2008-01-01 00:00:00',
    #             '2009-01-01 00:00:00'],
    #            ['UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT']],
    #     'S5': [['2000-01-01 00:00:00', '2001-01-01 00:00:00', '2002-01-01 00:00:00',
    #             '2003-01-01 00:00:00', '2004-01-01 00:00:00', '2005-01-01 00:00:00',
    #             '2006-01-01 00:00:00', '2007-01-01 00:00:00', '2008-01-01 00:00:00',
    #             '2009-01-01 00:00:00'],
    #            ['UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT', 'UCB', 'MIT']]
    # },
    {
        'S1': [['2003-01-01 00:00:00'],
               ['MIT']],
        'S2': [['2000-01-01 00:00:00'],
               ['UCB']],
        'S3': [['2001-01-01 00:00:00', '2006-01-01 00:00:00'],
               ['UCB', 'MIT']],
        'S4': [['2005-01-01 00:00:00'],
               ['MIT']],
        'S5': [['2003-01-01 00:00:00', '2005-01-01 00:00:00'],
               ['UCB', 'MS']],
    },
    {
        'S1': [['2000-01-01 00:00:00', '2009-01-01 00:00:00'],
               ['Wisc', 'MSR']],
        'S2': [['2000-01-01 00:00:00', '2001-01-01 00:00:00', '2008-01-01 00:00:00'],
               ['UW', 'Wisc', 'MSR']],
        'S3': [['2001-01-01 00:00:00', '2002-01-01 00:00:00'],
               ['UW', 'Wisc']],
        'S4': [['2005-01-01 00:00:00'],
               ['Wisc']],
        'S5': [['2003-01-01 00:00:00', '2005-01-01 00:00:00', '2007-01-01 00:00:00'],
               ['UW', 'None', 'Wisc']],
    },
    {
        'S1': [['2000-01-01 00:00:00'],
               ['MSR']],
        'S2': [['2000-01-01 00:00:00'],
               ['MSR']],
        'S3': [['2001-01-01 00:00:00'],
               ['MSR']],
        'S4': [['2007-01-01 00:00:00'],
               ['MSR']],
        'S5': [['2003-01-01 00:00:00'],
               ['MSR']],
    },
    {
        'S1': [['2004-01-01 00:00:00', '2009-01-01 00:00:00'],
               ['BEA', 'UCI']],
        'S2': [['2005-01-01 00:00:00'],
               ['AT&T']],
        'S3': [['2006-01-01 00:00:00'],
               ['BEA']],
        'S4': [['2007-01-01 00:00:00'],
               ['BEA']],
        'S5': [['2007-01-01 00:00:00'],
               ['BEA']],
    },
    {
        'S1': [['2000-01-01 00:00:00', '2007-01-01 00:00:00'],
               ['UW', 'Google']],
        'S2': [['2000-01-01 00:00:00', '2002-01-01 00:00:00', '2005-01-01 00:00:00'],
               ['Wisc', 'UW', 'Google']],
        'S3': [['2001-01-01 00:00:00', '2006-01-01 00:00:00'],
               ['Wisc', 'UW']],
        'S4': [['2005-01-01 00:00:00'],
               ['UW']],
        'S5': [['2003-01-01 00:00:00', '2005-01-01 00:00:00', '2007-01-01 00:00:00'],
               ['Wisc', 'Google', 'UW']],
    },
    # # case 1
    # # S1: 714288990
    # # S2: 2427161196
    # # Lazio vs Juventus 5/20
    # {
    #     'S1': [['2003-01-01 19:01:30', '2003-01-01 19:03:15', '2003-01-01 21:08:40'],
    #            [1, 2, 3]],
    #     'S2': [['2003-01-01 19:36:03', '2003-01-01 21:24:43'],
    #            [2, 3]],
    # },
    # # Real vs Espanyol 5/17
    # {
    #     'S1': [['2003-01-01 17:58:15', '2003-01-01 18:30:24', '2003-01-01 18:37:23',
    #             '2003-01-01 18:39:39', '2003-01-01 18:47:02', '2003-01-01 18:49:41'],
    #            [0, 1, 2, 3, 4, 5]],
    #     'S2': [['2003-01-01 17:04:47', '2003-01-01 18:23:54', '2003-01-01 18:30:20',
    #             '2003-01-01 18:40:57', '2003-01-01 18:41:17', '2003-01-01 18:59:52'],
    #            [0, 1, 2, 3, 4, 5]]
    # },
    # # Real vs Juventus 5/13
    # {
    #     'S1': [['2003-01-01 18:47:32', '2003-01-01 19:10:43'],
    #            [0, 1]],
    #     'S2': [['2003-01-01 18:49:04', '2003-01-01 19:36:17', '2003-01-01 20:46:26'],
    #            [0, 1, 2]]
    # }
    # case 2
    # {
    #     'S1': [['2000-01-01 00:00:00', '2002-01-01 00:00:00'],
    #            ['Wisc', 'MIT']],
    #     'S2': [['2000-01-01 00:00:00', '2002-01-01 00:00:00'],
    #            ['Wisc', 'MIT']],
    #     'S3': [['2000-01-01 00:00:00', '2002-01-01 00:00:00'],
    #            ['Wisc', 'MIT']],
    #     'S4': [['2000-01-01 00:00:00', '2002-01-01 00:00:00'],
    #            ['Wisc', 'MIT']],
    #     'S5': [['2000-01-01 00:00:00', '2002-01-01 00:00:00'],
    #            ['Wisc', 'MIT']],
    # },
    # {
    #     'S1': [['2000-01-01 00:00:00'],
    #            ['MSR']],
    #     'S2': [['2000-01-01 00:00:00'],
    #            ['MSR']],
    #     'S3': [['2000-01-01 00:00:00'],
    #            ['MSR']],
    #     'S4': [['2000-01-01 00:00:00'],
    #            ['MSR']],
    #     'S5': [['2000-01-01 00:00:00'],
    #            ['MSR']],
    # },
    # {
    #     'S1': [['2002-01-01 00:00:00', '2008-01-01 00:00:00'],
    #            ['BEA', 'UCI']],
    #     'S2': [['2002-01-01 00:00:00', '2008-01-01 00:00:00'],
    #            ['BEA', 'UCI']],
    #     'S3': [['2002-01-01 00:00:00', '2008-01-01 00:00:00'],
    #            ['BEA', 'UCI']],
    #     'S4': [['2002-01-01 00:00:00', '2008-01-01 00:00:00'],
    #            ['BEA', 'UCI']],
    #     'S5': [['2002-01-01 00:00:00', '2008-01-01 00:00:00'],
    #            ['BEA', 'UCI']],
    # },
    # {
    #     'S1': [['2000-01-01 00:00:00', '2005-01-01 00:00:00'],
    #            ['UW', 'Google']],
    #     'S2': [['2000-01-01 00:00:00', '2005-01-01 00:00:00'],
    #            ['UW', 'Google']],
    #     'S3': [['2000-01-01 00:00:00', '2005-01-01 00:00:00'],
    #            ['UW', 'Google']],
    #     'S4': [['2000-01-01 00:00:00', '2005-01-01 00:00:00'],
    #            ['UW', 'Google']],
    #     'S5': [['2000-01-01 00:00:00', '2005-01-01 00:00:00'],
    #            ['UW', 'Google']],
    # },
    ]


def get_observed_cases():
    observed_cases_new = []
    for case in observed_cases:
        case_new = {}
        for s in case:
            t_new = []
            for t in case.get(s)[0]:
                t_new.append(datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S'))
            case_new.update({s: [t_new, case.get(s)[1]]})
        observed_cases_new.append(case_new)

    return observed_cases_new