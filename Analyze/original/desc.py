import time

from Analyze.point_calc import calc, as_attacker, as_midfield, as_defender, df_calc

# attr to calc, 33d without Composure
alla = [
    'Crossing', 'Finishing', 'Heading_Accuracy', 'Short_Passing', 'Volleys',
    'Dribbling', 'Curve', 'Free_Kick_Accuracy', 'Long_Passing', 'Ball_Control',
    'Acceleration', 'Sprint_Speed', 'Agility', 'Reactions', 'Balance',
    'Shot_Power', 'Jumping', 'Stamina', 'Strength', 'Long_Shots',
    'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties',
    'Marking', 'Standing_Tackle', 'Sliding_Tackle',
    'GK_Diving', 'GK_Handling', 'GK_Kicking', 'GK_Positioning', 'GK_Reflexes'
]

form = {
    '451ATTACK': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 1, 'WM': 2, 'AM': 2, 'WW': 0, 'CF': 0, 'ST': 1},
    '4141': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 1, 'CM': 2, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 1},
    '4231NARROW': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 2, 'CM': 0, 'WM': 0, 'AM': 3, 'WW': 0, 'CF': 0, 'ST': 1},
    '4231WIDE': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 2, 'CM': 0, 'WM': 2, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 1},
    '451FLAT': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 3, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 1},
    '4141MIDFIELD': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 2, 'WM': 2, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 1},
    '4141ATTACK': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 2, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 1, 'ST': 1},
    '442HOLDING': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 2, 'CM': 0, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 2},
    '442FLAT': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 2, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 2},
    '41212NARROW': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 1, 'CM': 2, 'WM': 0, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 2},
    '41212WIDE': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 1, 'CM': 0, 'WM': 2, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 2},
    '4222': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 2, 'CM': 0, 'WM': 0, 'AM': 2, 'WW': 0, 'CF': 0, 'ST': 2},
    '4312': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 3, 'WM': 0, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 2},
    '4132': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 1, 'CM': 1, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 2},
    '433FALSE9': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 1, 'CM': 2, 'WM': 0, 'AM': 0, 'WW': 2, 'CF': 1, 'ST': 0},
    '433ATTACK': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 2, 'WM': 0, 'AM': 1, 'WW': 2, 'CF': 0, 'ST': 1},
    '433DEFEND': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 2, 'CM': 1, 'WM': 0, 'AM': 0, 'WW': 2, 'CF': 0, 'ST': 1},
    '433HOLDING': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 1, 'CM': 2, 'WM': 0, 'AM': 0, 'WW': 2, 'CF': 0, 'ST': 1},
    '433FLAT': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 3, 'WM': 0, 'AM': 0, 'WW': 2, 'CF': 0, 'ST': 1},
    '4321': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 3, 'WM': 0, 'AM': 0, 'WW': 0, 'CF': 2, 'ST': 1},
    '424': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 2, 'WM': 0, 'AM': 0, 'WW': 2, 'CF': 0, 'ST': 2},
    '541DIAMOND': {'GK': 1, 'FB': 0, 'WB': 2, 'CB': 3, 'DM': 1, 'CM': 0, 'WM': 2, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 1},
    '541FLAT': {'GK': 1, 'FB': 0, 'WB': 2, 'CB': 3, 'DM': 0, 'CM': 2, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 1},
    '5212': {'GK': 1, 'FB': 0, 'WB': 2, 'CB': 3, 'DM': 0, 'CM': 2, 'WM': 0, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 2},
    '532': {'GK': 1, 'FB': 0, 'WB': 2, 'CB': 3, 'DM': 0, 'CM': 3, 'WM': 0, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 2},
    '523': {'GK': 1, 'FB': 0, 'WB': 2, 'CB': 3, 'DM': 0, 'CM': 2, 'WM': 0, 'AM': 0, 'WW': 2, 'CF': 0, 'ST': 1},
    '3142': {'GK': 1, 'FB': 0, 'WB': 0, 'CB': 3, 'DM': 1, 'CM': 2, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 2},
    '3412': {'GK': 1, 'FB': 0, 'WB': 0, 'CB': 3, 'DM': 0, 'CM': 2, 'WM': 2, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 2},
    '352': {'GK': 1, 'FB': 0, 'WB': 0, 'CB': 3, 'DM': 2, 'CM': 0, 'WM': 2, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 2},
    '3511': {'GK': 1, 'FB': 0, 'WB': 0, 'CB': 3, 'DM': 2, 'CM': 1, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 1, 'ST': 1},
    '3421': {'GK': 1, 'FB': 0, 'WB': 0, 'CB': 3, 'DM': 0, 'CM': 2, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 2, 'ST': 1},
    '343FLAT': {'GK': 1, 'FB': 0, 'WB': 0, 'CB': 3, 'DM': 0, 'CM': 2, 'WM': 2, 'AM': 0, 'WW': 2, 'CF': 0, 'ST': 1},
    '343DIAMOND': {'GK': 1, 'FB': 0, 'WB': 0, 'CB': 3, 'DM': 1, 'CM': 0, 'WM': 2, 'AM': 1, 'WW': 2, 'CF': 0, 'ST': 1}
}


# select top players
def select_top(p, cond='ova', percentage=0.1):
    pt = p[p[cond] > p[cond].describe(percentiles=[1 - percentage / 100])[5]].sort_values(cond, ascending=False)
    return pt


# select rank of attr of a player
def select_rank(p, pid=41, cond='ova'):
    sort = p.sort_values(cond, ascending=False)
    rk = sort[cond].rank(ascending=False, method='min')[sort[sort['ID'] == pid][cond].index[0]]
    return int(rk)


# determine best position for a player, a slice of a player
def best_pos(p):
    calc_dict = calc(p, False)
    pos = max(calc_dict, key=calc_dict.get)
    return pos


# select the top player for the field
# at a extremely low effect, takes days and hours to do an analyze
# never use it unless the input is at a very low num
def top_pos(p, pos='CM', num=1):
    p = p.copy()
    p['point' + pos] = p['ova']
    for i in range(p['ID'].count()):
        calc_dict = calc(p.iloc[i, :], False)
        p.iloc[i, -1] = calc_dict[pos]
    return p.sort_values('point' + pos, ascending=False)


# select players with the same team
def select_team(p, club='FC Barcelona'):
    mates = p[p['Club'] == club]
    return mates


# select players with the same nation
def select_nation(p, nation='Spain'):
    mates = p[p['Nation'] == nation]
    return mates


# determine the fine starting eleven for team
# in put a team, thus select_club/nation(data,'club/nation')
def starting_eleven(p, fm=form['433FLAT']):
    tm = p
    dictc = {}
    # fit for ST
    for i in range(fm['ST']):
        tp = df_calc(tm).sort_values('ovaST', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('ST')
        dictc[tp['ID'].iloc[0]].append(tp['ovaST'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    # fit for CF
    for i in range(fm['CF']):
        tp = df_calc(tm).sort_values('ovaCF', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('CF')
        dictc[tp['ID'].iloc[0]].append(tp['ovaCF'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    # fit for WW
    for i in range(fm['WW']):
        tp = df_calc(tm).sort_values('ovaWW', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('WW')
        dictc[tp['ID'].iloc[0]].append(tp['ovaWW'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    # fit for AM
    for i in range(fm['AM']):
        tp = df_calc(tm).sort_values('ovaAM', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('AM')
        dictc[tp['ID'].iloc[0]].append(tp['ovaAM'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    # fit for WM
    for i in range(fm['WM']):
        tp = df_calc(tm).sort_values('ovaWM', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('WM')
        dictc[tp['ID'].iloc[0]].append(tp['ovaWM'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    # fit for CM
    for i in range(fm['CM']):
        tp = df_calc(tm).sort_values('ovaCM', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('CM')
        dictc[tp['ID'].iloc[0]].append(tp['ovaCM'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    # fit for DM
    for i in range(fm['DM']):
        tp = df_calc(tm).sort_values('ovaDM', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('DM')
        dictc[tp['ID'].iloc[0]].append(tp['ovaDM'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    # fit for CB
    for i in range(fm['CB']):
        tp = df_calc(tm).sort_values('ovaCB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('CB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaCB'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    # fit for WB
    for i in range(fm['WB']):
        tp = df_calc(tm).sort_values('ovaWB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('WB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaWB'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    # fit for FB
    for i in range(fm['FB']):
        tp = df_calc(tm).sort_values('ovaFB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('FB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaFB'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    for i in range(fm['GK']):
        tp = df_calc(tm).sort_values('ovaGK', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('GK')
        dictc[tp['ID'].iloc[0]].append(tp['ovaGK'].iloc[0])
        tm = tm.drop(tm[tm['ID'] == tp['ID'].iloc[0]].index)

    return dictc


# input some players, such as a club or a nation, you can also input the players you want.
# output a form makes up the highest ova
# well... due to using greedy algorithm in the function start_eleven(), the result may not be the best
# need to be optimized
def best_form(p):
    dict_form={}
    for k in form:
        # print('now '+k)
        # # consume so much time that have to measure it
        # print(time.strftime('%H:%M:%S', time.localtime(time.time())))
        dictc = starting_eleven(p, fm=form[k])
        team_ova = 0
        for kc in dictc:
            team_ova += dictc[kc][2]
        dict_form[k] = [dictc,team_ova]
    ova_list=[]
    key_list=[]
    for k in dict_form:
        ova_list.append(dict_form[k][1])
        key_list.append(k)
    best_fm=key_list[ova_list.index(max(ova_list))]
    return dict_form[best_fm][0]
