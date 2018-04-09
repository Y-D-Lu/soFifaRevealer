import copy
import time
import itertools

from scipy.spatial.distance import pdist, squareform

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


# the attr that related with WingBack
WB = ['Acceleration', 'Sprint_Speed', 'Stamina', 'Reactions', 'Interceptions', 'Ball_Control', 'Crossing',
      'Dribbling', 'Short_Passing', 'Marking', 'Standing_Tackle', 'Sliding_Tackle']
# the attr that related with FullBack
FB = ['Acceleration', 'Sprint_Speed', 'Stamina', 'Reactions', 'Interceptions', 'Ball_Control', 'Crossing',
      'Heading_Accuracy', 'Short_Passing', 'Marking', 'Standing_Tackle', 'Sliding_Tackle']
# the attr that related with CenterBack
CB = ['Sprint_Speed', 'Jumping', 'Strength', 'Reactions', 'Aggression', 'Interceptions', 'Ball_Control',
      'Heading_Accuracy', 'Short_Passing', 'Marking', 'Standing_Tackle', 'Sliding_Tackle']
# the attr that related with DefenceMidfield
DM = ['Stamina', 'Strength', 'Reactions', 'Aggression', 'Interceptions', 'Vision', 'Ball_Control',
      'Long_Passing', 'Short_Passing', 'Marking', 'Standing_Tackle', 'Sliding_Tackle']
# the attrs that related with WingMidfield
WM = ['Acceleration', 'Sprint_Speed', 'Stamina', 'Reactions', 'Positioning', 'Vision', 'Ball_Control',
      'Crossing', 'Dribbling', 'Finishing', 'Long_Passing', 'Short_Passing']
# the attr that related with CenterMidfield
CM = ['Stamina', 'Reactions', 'Interceptions', 'Positioning', 'Vision', 'Ball_Control', 'Dribbling',
      'Finishing', 'Long_Passing', 'Short_Passing', 'Long_Shots', 'Standing_Tackle']
# the attr that related with AttackMidfield
AM = ['Acceleration', 'Sprint_Speed', 'Agility', 'Reactions', 'Positioning', 'Vision', 'Ball_Control',
      'Dribbling', 'Finishing', 'Long_Passing', 'Short_Passing', 'Long_Shots']
# the attr that related with CenterForward
CF = ['Acceleration', 'Sprint_Speed', 'Reactions', 'Positioning', 'Vision', 'Ball_Control', 'Dribbling',
      'Finishing', 'Heading_Accuracy', 'Short_Passing', 'Shot_Power', 'Long_Shots']
# the attr that related with Winger
WW = ['Acceleration', 'Sprint_Speed', 'Agility', 'Reactions', 'Positioning', 'Vision', 'Ball_Control', 'Crossing',
      'Dribbling', 'Finishing', 'Short_Passing', 'Long_Shots']
# the attr that related with Striker
ST = ['Acceleration', 'Sprint_Speed', 'Strength', 'Reactions', 'Positioning', 'Ball_Control', 'Dribbling',
      'Finishing', 'Heading_Accuracy', 'Short_Passing', 'Shot_Power', 'Long_Shots', 'Volleys']


# select top players, input the df contains the target players, condition you want to compare with ,
# and the top percentage you want, output the players' info's df
def select_top(p, cond='ova', percentage=0.1):
    pt = p[p[cond] > p[cond].describe(percentiles=[1 - percentage / 100])[5]].sort_values(cond, ascending=False)
    return pt


# select rank of attr of a player, input the df contains the target player, the  id of the target player,
# and condition you want to compare, output the target player's rank of the condition
def select_rank(p, pid=41, cond='ova'):
    # firstly sort by condition given
    sort = p.sort_values(cond, ascending=False)
    # then get the player's rank
    rk = sort[cond].rank(ascending=False, method='min')[sort[sort['ID'] == pid][cond].index[0]]
    return int(rk)


# determine best position for a player, input a slice of a player, thus df[alla].iloc[0, :]
# output the position at which the player get the highest OVA as string.
def best_pos(p):
    # get dict of pos
    calc_dict = calc(p, False)
    # get key whose value is the max one
    pos = max(calc_dict, key=calc_dict.get)
    return pos


# select the top player for the field
# at a extremely low effect, takes days and hours to do an analyze
# never use it unless the input is at a very low num
def top_pos(p, pos='CM'):
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


# get similar players that similar to the player input
def similar(p=[], tid=41, num=10):
    # determine the best position for the target player and accordingly set the player_s
    player_s = p[eval(best_pos(p[p['ID'] == tid][alla].iloc[0, :]))]
    pid = p['ID']
    name = p['Name']

    dis = []
    IDs = []
    Names = []

    # get distance among players
    player_dis = pdist(player_s, 'euclidean')
    player_dis = squareform(player_dis)

    for i in range(player_s.count()[0]):
        if pid[i] == tid:
            target = i
    for i in range(player_s.count()[0]):
        if pid[i] != tid:
            dis.append(player_dis[i][target])
            IDs.append(pid[i])
            Names.append(name[i])
    distemp = copy.deepcopy(dis)
    distemp.sort()
    dict_s = {}
    # it may be wise to include the target player in the return dict
    dict_s[0] = [tid, p[p['ID'] == tid]['Name'].values[0]]
    for i in range(num):
        dict_s[i + 1] = [IDs[dis.index(distemp[i])], Names[dis.index(distemp[i])]]

    return dict_s
