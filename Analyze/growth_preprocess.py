from multiprocessing.pool import Pool

import pandas as pd

from Analyze import desc
from Analyze.point_calc import as_attacker, as_defender, as_midfield

data_all = pd.DataFrame(pd.read_csv('data/all.csv'))
comp = ['ID', 'ver', 'Name', 'Weight', 'Height', 'year', 'month', 'date', 'Age', 'Club', 'Nation', 'Pfoot', 'Wfoot',
        'IR', 'SM ', 'ova', 'potential', 'value', 'wage',
        'Crossing', 'Finishing', 'Heading_Accuracy', 'Short_Passing', 'Volleys',
        'Dribbling', 'Curve', 'Free_Kick_Accuracy', 'Long_Passing', 'Ball_Control',
        'Acceleration', 'Sprint_Speed', 'Agility', 'Reactions', 'Balance',
        'Shot_Power', 'Jumping', 'Stamina', 'Strength', 'Long_Shots',
        'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties',
        'Marking', 'Standing_Tackle', 'Sliding_Tackle',
        'GK_Diving', 'GK_Handling', 'GK_Kicking', 'GK_Positioning', 'GK_Reflexes',
        'pointPAC', 'pointSHO', 'pointPAS', 'pointDRI', 'pointDEF', 'pointPHY',
        'ova+5', 'growth']
alla = desc.alla


def switcher(p=[]):
    li = [as_attacker(p), as_midfield(p), as_defender(p)]
    return li.index(max(li))


def growth_calc(start_age=20, end_age=25):
    mates_1 = data_all[data_all['Age'] == start_age]
    mates_2 = data_all[data_all['Age'] == end_age]

    data_5 = pd.DataFrame(columns=comp)
    a = 0
    for i in range(mates_1['ID'].count()):
        if mates_1.iloc[i, 0] in mates_2['ID'].values:
            a += 1
            data_5.loc[a, :] = mates_1.iloc[i, :]
            data_5['ova+5'][a] = mates_2[mates_2['ID'] == mates_1.iloc[i, 0]]['ova'].values[0]
            data_5['growth'][a] = data_5['ova+5'][a] - data_5['ova'][a]

    data_5.to_csv('data/' + str(start_age) + 'to' + str(end_age) + '.csv', encoding='utf-8')

    # data_5.to_csv('data/data_5.csv', encoding='utf-8')
    #
    # data_att = pd.DataFrame(columns=comp)
    # data_mid = pd.DataFrame(columns=comp)
    # data_def = pd.DataFrame(columns=comp)
    #
    # data_5.reset_index()
    # data5a = data_5[alla]
    #
    # a = b = c = 0
    # for x in range(1, data_5['ID'].count() + 1):
    #     if switcher(data5a.loc[x, :]) == 0:
    #         data_att.loc[a, :] = data_5.loc[x, :]
    #         a += 1
    #     elif switcher(data5a.loc[x, :]) == 1:
    #         data_mid.loc[b, :] = data_5.loc[x, :]
    #         b += 1
    #     else:
    #         data_def.loc[c, :] = data_5.loc[x, :]
    #         c += 1
    #
    # data_att.to_csv('data/att.csv', encoding='utf-8')
    # data_mid.to_csv('data/mid.csv', encoding='utf-8')
    # data_def.to_csv('data/def.csv', encoding='utf-8')


def multi_task(name, sa, ea):
    growth_calc(sa, ea)


if __name__ == '__main__':
    p = Pool(8)
    for i in range(18, 26, 1):
        p.apply_async(multi_task, args=(i, i, i + 1))
    p.close()
    p.join()
