import itertools
from multiprocessing.pool import Pool
from Analyze.point_calc import df_calc, calc

# all forms that in FIFA18, XD I manually write them all.
form = {
    '451ATTACK': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 1, 'WM': 2, 'AM': 2, 'WW': 0, 'CF': 0, 'ST': 1},
    '4141': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 1, 'CM': 2, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 1},
    '4231NARROW': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 2, 'CM': 0, 'WM': 0, 'AM': 3, 'WW': 0, 'CF': 0, 'ST': 1},
    '4231WIDE': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 2, 'CM': 0, 'WM': 2, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 1},
    '451FLAT': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 3, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 1},
    '4411MIDFIELD': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 2, 'WM': 2, 'AM': 1, 'WW': 0, 'CF': 0, 'ST': 1},
    '4411ATTACK': {'GK': 1, 'FB': 2, 'WB': 0, 'CB': 2, 'DM': 0, 'CM': 2, 'WM': 2, 'AM': 0, 'WW': 0, 'CF': 1, 'ST': 1},
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
# is at a high speed, but accuracy may not be so good for giants
# in put a team, thus select_club/nation(data,'club/nation')
def starting_eleven(p, ban_list=None, fm=form['433FLAT']):
    # the dict to  store the players of the form
    if ban_list is None:
        ban_list = []
    dictc = {}

    # firstly drop players in the ban_list
    p = p.drop(p[p['ID'].isin(ban_list)].index)

    # then calc the ova at all positions for all the players
    df = df_calc(p)

    # it's undoubtedly that starting GK is the best GK in the form, and there's only one GK
    # so select the player with the highest GK point
    tp = df.sort_values('ovaGK', ascending=False)
    # save to the dict as {ID:[Name,Position,ova]}
    dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
    dictc[tp['ID'].iloc[0]].append('GK')
    dictc[tp['ID'].iloc[0]].append(tp['ovaGK'].iloc[0])
    # remove the player selected
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

    # return the dict
    return dictc


# determine the best starting eleven for team
# cost more time, but accuracy is graet
# in put a team, thus select_club/nation(data,'club/nation')
def best_eleven(p, ban_list=None, fm=form['433FLAT']):
    # the dict to  store the players of the form
    if ban_list is None:
        ban_list = []
    dictc = {}

    # firstly drop players in the ban_list
    p = p.drop(p[p['ID'].isin(ban_list)].index)

    # then calc the ova at all positions for all the players
    df = df_calc(p)

    # it's undoubtedly that starting GK is the best GK in the form, and there's only one GK
    # so select the player with the highest GK point
    tp = df.sort_values('ovaGK', ascending=False)
    # save to the dict as {ID:[Name,Position,ova]}
    dictc[tp['ID'].iloc[0]] = [tp['Name'].iloc[0]]
    dictc[tp['ID'].iloc[0]].append('GK')
    dictc[tp['ID'].iloc[0]].append(tp['ovaGK'].iloc[0])
    # remove the player selected
    tp = tp.drop(tp[tp['ID'] == tp['ID'].iloc[0]].index)

    # as for the rest players, firstly fit for the defenders
    # if a player performs better at DM than AM, we believe he is a defender than an attacker. And select them.
    p_list = tp[tp['ovaDM'] > tp['ovaAM']].sort_values('ova', ascending=False
                                                       # and to be effective, just select 2 times of actually defenders
                                                       # for we are going to use a way in low effect to calc
                                                       ).head(
        int(round((fm['FB'] + fm['WB'] + fm['CB'] + fm['DM']) * 2)))

    # get the set of players above for the combinations calc
    name_set = set(p_list['ID'].values)
    # lists to record ova and defenders
    ova = []
    def_list = []

    # then, get all combinations and append ova and set of IDs to the lists above
    for wb in itertools.combinations(name_set, fm['WB']):
        rest1 = name_set.difference(wb)
        ovaWB = sum(p_list[p_list['ID'].isin(wb)]['ovaWB'].values)
        for fb in itertools.combinations(rest1, fm['FB']):
            rest2 = rest1.difference(fb)
            ovaFB = sum(p_list[p_list['ID'].isin(fb)]['ovaFB'].values)
            for cb in itertools.combinations(rest2, fm['CB']):
                rest3 = rest2.difference(cb)
                ovaCB = sum(p_list[p_list['ID'].isin(cb)]['ovaCB'].values)
                for dm in itertools.combinations(rest3, fm['DM']):
                    ovaDM = sum(p_list[p_list['ID'].isin(dm)]['ovaDM'].values)
                    ova_sum = ovaWB + ovaFB + ovaCB + ovaDM
                    def_list.append(wb + fb + cb + dm)
                    ova.append(ova_sum)
    # get the pos_order in order
    pos_order = []
    for k in fm:
        for num in range(fm[k]):
            pos_order.append(k)

    # get the defenders with the max ova
    for player in list(def_list[ova.index(max(ova))]):
        # get the pos of the current player
        pos = pos_order[list(def_list[ova.index(max(ova))]).index(player) + 1]
        # save to the dict as {ID:[Name,Position,ova]}
        dictc[player] = [p_list[p_list['ID'] == player]['Name'].values[0]]
        dictc[player].append(pos)
        dictc[player].append(calc(p_list[p_list['ID'] == player], False)[pos])
        # remove the player selected
        tp = tp.drop(tp[tp['ID'] == player].index)

    # next, attackers
    p_list = tp[tp['ovaCM'] >= tp['ovaCB']].sort_values('ova', ascending=False).head(
        int(round((fm['CM'] + fm['WM'] + fm['AM'] + fm['CF'] + fm['WW'] + fm['ST']) * 1.5)))
    name_set = set(p_list['ID'].values)
    ova = []
    att_list = []
    for cm in itertools.combinations(name_set, fm['CM']):
        rest2 = name_set.difference(cm)
        ovaCM = sum(p_list[p_list['ID'].isin(cm)]['ovaCM'].values)
        for wm in itertools.combinations(rest2, fm['WM']):
            rest3 = rest2.difference(wm)
            ovaWM = sum(p_list[p_list['ID'].isin(wm)]['ovaWM'].values)
            for am in itertools.combinations(rest3, fm['AM']):
                rest4 = rest3.difference(am)
                ovaAM = sum(p_list[p_list['ID'].isin(am)]['ovaAM'].values)
                for ww in itertools.combinations(rest4, fm['WW']):
                    rest5 = rest4.difference(ww)
                    ovaWW = sum(p_list[p_list['ID'].isin(ww)]['ovaWW'].values)
                    for cf in itertools.combinations(rest5, fm['CF']):
                        rest6 = rest5.difference(cf)
                        ovaCF = sum(p_list[p_list['ID'].isin(cf)]['ovaCF'].values)
                        for st in itertools.combinations(rest6, fm['ST']):
                            ovaST = sum(p_list[p_list['ID'].isin(st)]['ovaST'].values)
                            ova_sum = ovaCM + ovaWM + ovaAM + ovaWW + ovaCF + ovaST
                            att_list.append(cm + wm + am + ww + cf + st)
                            ova.append(ova_sum)

    pos_order = []
    for k in fm:
        for num in range(fm[k]):
            pos_order.append(k)
    for player in list(att_list[ova.index(max(ova))]):
        pos = pos_order[
            list(att_list[ova.index(max(ova))]).index(player) + (fm['FB'] + fm['WB'] + fm['CB'] + fm['DM'] + 1)]
        dictc[player] = [p_list[p_list['ID'] == player]['Name'].values[0]]
        dictc[player].append(pos)
        dictc[player].append(calc(p_list[p_list['ID'] == player], False)[pos])

    return dictc


# input some players, such as a club or a nation, you can also input the players you want.
# output a form makes up the highest ova
# well... you can decide which algorithm to use either best_eleven or starting_eleven
# while using the best_eleven(),you may get the result at once, but with lower accuracy
# while using the best_eleven(),you may get the best result, but cost much more time
def best_form(p, ban_list=None):
    if ban_list is None:
        ban_list = []
    dict_form = {}
    for k in form:
        dictc = best_eleven(p, ban_list=ban_list, fm=form[k])
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
    ret = {best_fm: dict_form[best_fm][0]}
    return ret


def multi_form(k, p, ban=None):
    if ban is None:
        ban = []
    dict_form = {}
    dictc = best_eleven(p, ban_list=ban, fm=form[k])
    team_ova = 0
    for kc in dictc:
        team_ova += dictc[kc][2]
    dict_form[k] = [dictc, team_ova]
    return dict_form


# use a multiprocess to get a 3x speed for calc
def best_form_multi(p, ban_list=None):
    if ban_list is None:
        ban_list = []
    pool = Pool(5)
    res = []
    dict_form = {}
    for k in form:
        res.append(pool.apply_async(multi_form, args=(k, p, ban_list)))
    for i in res:
        dict_form.update(i.get())
    pool.close()
    pool.join()
    ova_list = []
    key_list = []
    for k in dict_form:
        ova_list.append(dict_form[k][1])
        key_list.append(k)
    best_fm = key_list[ova_list.index(max(ova_list))]
    ret = {best_fm: dict_form[best_fm][0]}
    return ret
