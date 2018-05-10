from multiprocessing.pool import Pool
import pandas as pd
from Analyze import desc
from Analyze.point_calc import as_attacker, as_defender, as_midfield


# get all players from 2011 to now
data_all = pd.DataFrame(pd.read_csv('data/all.csv'))
# get alla for position calc
alla = desc.alla
# we use those features to do ML, ova+ means ova next period and growth is itself. Definitely 'ova+'='ova'+'growth'
comp = ['ID', 'ver', 'Name', 'Weight', 'Height', 'year', 'month', 'date', 'Age', 'Club', 'Nation', 'Pfoot', 'Wfoot',
        'IR', 'SM ', 'ova', 'potential', 'value', 'wage',
        'Crossing', 'Finishing', 'Heading_Accuracy', 'Short_Passing', 'Volleys',
        'Dribbling', 'Curve', 'Free_Kick_Accuracy', 'Long_Passing', 'Ball_Control',
        'Acceleration', 'Sprint_Speed', 'Agility', 'Reactions', 'Balance',
        'Shot_Power', 'Jumping', 'Stamina', 'Strength', 'Long_Shots',
        'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties',
        'Marking', 'Standing_Tackle', 'Sliding_Tackle',
        'GK_Diving', 'GK_Handling', 'GK_Kicking', 'GK_Positioning', 'GK_Reflexes',
        'ova+', 'growth']


# calc the growth and ova+ of players in the period of age
def growth_calc(start_age=20, end_age=25):
    # one part of the players are at the age of the start age
    mates_1 = data_all[data_all['Age'] == start_age]
    # the others are at the end age
    mates_2 = data_all[data_all['Age'] == end_age]
    # # only select those whose ova+ is over 70
    # mates_2 = mates_2[mates_2['ova']>70]
    # new a df to store those players fit the conditions
    data_p = pd.DataFrame(columns=comp)
    # count of players in data_p
    a = 0

    for i in range(mates_1['ID'].count()):
        # if player is recorded at both ages
        if mates_1.iloc[i, 0] in mates_2['ID'].values:
            # count of player ++
            a += 1
            # append player_info to data_p
            data_p.loc[a, :] = mates_1.iloc[i, :]
            # set ova+ as ova at end_age
            data_p['ova+'][a] = mates_2[mates_2['ID'] == mates_1.iloc[i, 0]]['ova'].values[0]
            # growth=ova+-ova
            data_p['growth'][a] = data_p['ova+'][a] - data_p['ova'][a]
    return data_p

    # data_5.to_csv('data/' + str(start_age) + 'to' + str(end_age) + '.csv', encoding='utf-8', index=None)

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


# use multi_task to speed up
def multi_task(name, sa, ea):
    return growth_calc(sa, ea)


# calc all the players' growth and ova+ every year in the period from start to end
def calc_every_year(start_age=20, end_age=25):
    data_e = pd.DataFrame(columns=comp)
    p = Pool(8)
    res=[]
    for i in range(start_age, end_age, 1):
        res.append(p.apply_async(multi_task, args=(i, i, i + 1)))
    for i in res:
        data_e=data_e.append(i.get())
    p.close()
    p.join()
    return data_e



if __name__ == '__main__':
    # calc every year growths form 18 to 25
    df = calc_every_year(18,25)
    df.to_csv('data/annual_18to25.csv', encoding='utf-8', index=None)
    print(df)
    # # or just calc 20 to 25
    # df = growth_calc(20,25)
