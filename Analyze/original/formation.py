import copy
import itertools

from Analyze.point_calc import df_calc, calc

# all forms that in FIFA18, XD I manually write them all.
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


# determine the fine starting eleven for team
# in put a team, thus select_club/nation(data,'club/nation')
def starting_eleven(p, fm=form['433FLAT']):
    dictc = {}
    df = df_calc(p)
    # it's undoubtedly that starting GK is the best GK in the form, and there's only one GK
    tp = df.sort_values('ovaGK', ascending=False)
    dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
    dictc[tp['ID'].iloc[0]].append('GK')
    dictc[tp['ID'].iloc[0]].append(tp['ovaGK'].iloc[0])
    tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for WB
    if fm['WB'] == 2:
        for i in range(fm['WB']):
            tp = tp.sort_values('ovaWB', ascending=False)
            dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
            dictc[tp['ID'].iloc[0]].append('WB')
            dictc[tp['ID'].iloc[0]].append(tp['ovaWB'].iloc[0])
            tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for FB
    for i in range(fm['FB']):
        tp = tp.sort_values('ovaFB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('FB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaFB'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for CB
    for i in range(fm['CB']):
        tp = tp.sort_values('ovaCB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('CB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaCB'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for DM
    for i in range(fm['DM']):
        tp = tp.sort_values('ovaDM', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('DM')
        dictc[tp['ID'].iloc[0]].append(tp['ovaDM'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for CM
    for i in range(fm['CM']):
        tp = tp.sort_values('ovaCM', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('CM')
        dictc[tp['ID'].iloc[0]].append(tp['ovaCM'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for WM
    for i in range(fm['WM']):
        tp = tp.sort_values('ovaWM', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('WM')
        dictc[tp['ID'].iloc[0]].append(tp['ovaWM'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for AM
    for i in range(fm['AM']):
        tp = tp.sort_values('ovaAM', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('AM')
        dictc[tp['ID'].iloc[0]].append(tp['ovaAM'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for WW
    for i in range(fm['WW']):
        tp = tp.sort_values('ovaWW', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('WW')
        dictc[tp['ID'].iloc[0]].append(tp['ovaWW'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for CF
    for i in range(fm['CF']):
        tp = tp.sort_values('ovaCF', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('CF')
        dictc[tp['ID'].iloc[0]].append(tp['ovaCF'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for ST
    for i in range(fm['ST']):
        tp = tp.sort_values('ovaST', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('ST')
        dictc[tp['ID'].iloc[0]].append(tp['ovaST'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    return dictc


# determine the better starting eleven for team
# in put a team, thus select_club/nation(data,'club/nation')
def better_eleven(p, fm=form['433FLAT'], add=1.5):
    dictc = {}
    df = df_calc(p)
    # it's undoubtedly that starting GK is the best GK in the form, and there's only one GK
    tp = df.sort_values('ovaGK', ascending=False)
    dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
    dictc[tp['ID'].iloc[0]].append('GK')
    dictc[tp['ID'].iloc[0]].append(tp['ovaGK'].iloc[0])
    tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for WB
    for i in range(fm['WB']):
        tp = tp.sort_values('ovaWB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('WB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaWB'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for FB
    for i in range(fm['FB']):
        tp = tp.sort_values('ovaFB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('FB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaFB'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for CB
    for i in range(fm['CB']):
        tp = tp.sort_values('ovaCB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('CB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaCB'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # use a deepcopy to ensure not to change the value of fm!!!
    dict_pos = copy.deepcopy(fm)
    dict_pos.pop('GK')
    dict_pos.pop('FB')
    dict_pos.pop('WB')
    dict_pos.pop('CB')
    tp['ovaFW'] = tp['ovaWW'] + tp['ovaCF'] + tp['ovaST']
    fw_num = fm['WW'] + fm['CF'] + fm['ST']
    p_list = tp.sort_values('ovaFW', ascending=False).iloc[0:int(fw_num * add)]
    name_list = set(p_list['ID'].values)
    a = 0
    ova = []
    form_list = []
    for ww in itertools.combinations(name_list, dict_pos['WW']):
        rest1 = name_list.difference(ww)
        ovaWW = df_calc(p_list[p_list['ID'].isin(ww)])['ovaWW'].sum()
        for cf in itertools.combinations(rest1, dict_pos['CF']):
            rest2 = rest1.difference(cf)
            ovaCF = df_calc(p_list[p_list['ID'].isin(cf)])['ovaCF'].sum()
            for st in itertools.combinations(rest2, dict_pos['ST']):
                ovaST = df_calc(p_list[p_list['ID'].isin(st)])['ovaST'].sum()
                ova_sum = ovaWW + ovaCF + ovaST
                form_list.append(ww + cf + st)
                ova.append(ova_sum)
                a += 1
    # print(a)
    pos_order = []
    dict_pos_fw = copy.deepcopy(dict_pos)
    dict_pos_fw.pop('DM')
    dict_pos_fw.pop('CM')
    dict_pos_fw.pop('WM')
    dict_pos_fw.pop('AM')
    for k in dict_pos_fw:
        for num in range(dict_pos_fw[k]):
            pos_order.append(k)
    for players in list(form_list[ova.index(max(ova))]):
        dictc[players] = [p_list[p_list['ID'] == players]['Name'].values[0]]
        pos = pos_order[list(form_list[ova.index(max(ova))]).index(players)]
        dictc[players].append(pos)
        dictc[players].append(calc(p_list[p_list['ID'] == players], False)[pos])
        tp = tp.drop(tp[tp['ID'] == players].index)
    dict_pos.pop('WW')
    dict_pos.pop('CF')
    dict_pos.pop('ST')
    tp['ovaMD'] = tp['ovaDM'] + tp['ovaCM'] + tp['ovaWM'] + tp['ovaAM']
    md_num = fm['DM'] + fm['CM'] + fm['WM'] + fm['AM']
    p_list = tp.sort_values('ovaMD', ascending=False).iloc[0:int(md_num * add)]
    name_list = set(p_list['ID'].values)
    a = 0
    ova = []
    form_list = []
    for dm in itertools.combinations(name_list, dict_pos['DM']):
        rest1 = name_list.difference(dm)
        ovaDM = df_calc(p_list[p_list['ID'].isin(dm)])['ovaDM'].sum()
        for cm in itertools.combinations(rest1, dict_pos['CM']):
            rest2 = rest1.difference(cm)
            ovaCM = df_calc(p_list[p_list['ID'].isin(cm)])['ovaCM'].sum()
            for wm in itertools.combinations(rest2, dict_pos['WM']):
                rest3 = rest2.difference(wm)
                ovaWM = df_calc(p_list[p_list['ID'].isin(wm)])['ovaWM'].sum()
                for am in itertools.combinations(rest3, dict_pos['AM']):
                    ovaAM = df_calc(p_list[p_list['ID'].isin(am)])['ovaAM'].sum()
                    ova_sum = ovaDM + ovaCM + ovaWM + ovaAM
                    form_list.append(dm + cm + wm + am)
                    ova.append(ova_sum)
                    a += 1
    # print(a)
    pos_order = []
    for k in dict_pos:
        for num in range(dict_pos[k]):
            pos_order.append(k)
    for players in list(form_list[ova.index(max(ova))]):
        dictc[players] = [p_list[p_list['ID'] == players]['Name'].values[0]]
        pos = pos_order[list(form_list[ova.index(max(ova))]).index(players)]
        dictc[players].append(pos)
        dictc[players].append(calc(p_list[p_list['ID'] == players], False)[pos])

    return dictc


# determine the best starting eleven for team
# in put a team, thus select_club/nation(data,'club/nation')
def best_eleven(p, fm=form['433FLAT']):
    dictc = {}
    df = df_calc(p)
    # it's undoubtedly that starting GK is the best GK in the form, and there's only one GK
    tp = df.sort_values('ovaGK', ascending=False)
    dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
    dictc[tp['ID'].iloc[0]].append('GK')
    dictc[tp['ID'].iloc[0]].append(tp['ovaGK'].iloc[0])
    tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)
    # fit for WB
    for i in range(fm['WB']):
        tp = tp.sort_values('ovaWB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('WB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaWB'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for FB
    for i in range(fm['FB']):
        tp = tp.sort_values('ovaFB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('FB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaFB'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # fit for CB
    for i in range(fm['CB']):
        tp = tp.sort_values('ovaCB', ascending=False)
        dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
        dictc[tp['ID'].iloc[0]].append('CB')
        dictc[tp['ID'].iloc[0]].append(tp['ovaCB'].iloc[0])
        tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # well... if there's DM in the formation, it's hard to say. Emmm... Assume that the best player of you is an Am,
    # it may gets higher point than your DMs, he may be send to the DM by greedy algorithm.
    # so we just use a strategy that might be of some stupid: calc it all and we can know how to combine the best
    # it's really time-costing but, emmm... really exact.
    dict_pos = fm
    dict_pos.pop('GK')
    dict_pos.pop('FB')
    dict_pos.pop('WB')
    dict_pos.pop('CB')
    # 8 is enough for a team, for example, the 8th or barca is A.Gomes, so might be enough.
    # the Time Complexity now is of O(n!), so, it takes about mintue while n=6,about 3 while 8 and over 10 while 8.
    p_list = tp.sort_values('ova', ascending=False).iloc[0:8]
    name_list = set(p_list['ID'].values)
    a = 0
    # first try 3cm 3cf
    ova = []
    form_list = []
    for dm in itertools.combinations(name_list, dict_pos['DM']):
        rest1 = name_list.difference(dm)
        ovaDM = df_calc(p_list[p_list['ID'].isin(dm)])['ovaDM'].sum()
        for cm in itertools.combinations(rest1, dict_pos['CM']):
            rest2 = rest1.difference(cm)
            ovaCM = df_calc(p_list[p_list['ID'].isin(cm)])['ovaCM'].sum()
            for wm in itertools.combinations(rest2, dict_pos['WM']):
                rest3 = rest2.difference(wm)
                ovaWM = df_calc(p_list[p_list['ID'].isin(wm)])['ovaWM'].sum()
                for am in itertools.combinations(rest3, dict_pos['AM']):
                    rest4 = rest3.difference(am)
                    ovaAM = df_calc(p_list[p_list['ID'].isin(am)])['ovaAM'].sum()
                    for ww in itertools.combinations(rest4, dict_pos['WW']):
                        rest5 = rest4.difference(ww)
                        ovaWW = df_calc(p_list[p_list['ID'].isin(ww)])['ovaWW'].sum()
                        for cf in itertools.combinations(rest5, dict_pos['CF']):
                            rest6 = rest5.difference(cf)
                            ovaCF = df_calc(p_list[p_list['ID'].isin(cf)])['ovaCF'].sum()
                            for st in itertools.combinations(rest6, dict_pos['ST']):
                                ovaST = df_calc(p_list[p_list['ID'].isin(st)])['ovaST'].sum()
                                ova_sum = ovaDM + ovaCM + ovaWM + ovaAM + ovaWW + ovaCF + ovaST
                                form_list.append(dm + cm + wm + am + ww + cf + st)
                                ova.append(ova_sum)
                                a += 1
    # print(ova[ova.index(max(ova))])
    # print(a)
    pos_order = []
    for k in dict_pos:
        for num in range(dict_pos[k]):
            pos_order.append(k)
    for players in list(form_list[ova.index(max(ova))]):
        dictc[players] = [p_list[p_list['ID'] == players]['Name'].values[0]]
        pos = pos_order[list(form_list[ova.index(max(ova))]).index(players)]
        dictc[players].append(pos)
        dictc[players].append(calc(p_list[p_list['ID'] == players], False)[pos])
    return dictc


# input some players, such as a club or a nation, you can also input the players you want.
# output a form makes up the highest ova
# well... due to using greedy algorithm in the function start_eleven(), the result may not be the best
# need to be optimized
def best_form(p):
    dict_form = {}
    for k in form:
        # print('now '+k)
        # # consume so much time that have to measure it
        # print(time.strftime('%H:%M:%S', time.localtime(time.time())))
        dictc = starting_eleven(p, fm=form[k])
        team_ova = 0
        for kc in dictc:
            team_ova += dictc[kc][2]
        dict_form[k] = [dictc, team_ova]
    ova_list = []
    key_list = []
    for k in dict_form:
        ova_list.append(dict_form[k][1])
        key_list.append(k)
    best_fm = key_list[ova_list.index(max(ova_list))]
    return dict_form[best_fm][0]
