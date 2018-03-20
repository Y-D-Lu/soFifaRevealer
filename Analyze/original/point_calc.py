# input should be a list with 28 elements in order:
# Crossing, Finishing, Heading_Accuracy, Short_Passing, Volleys,
# Dribbling, Curve, Free_Kick_Accuracy, Long_Passing, Ball_Control,
# Acceleration, Sprint_Speed, Agility, Reactions, Balance,
# Shot_Power, Jumping, Stamina, Strength, Long_Shots,
# Aggression, Interceptions, Positioning, Vision, Penalties,
# Marking, Standing_Tackle, Sliding_Tackle


# calculate the ova of a player at each position
def calc(p=[], do_round=True):
    pos = []
    a = .04 * p[10] + \
        .06 * p[11] + \
        .1 * p[17] + \
        .08 * p[13] + \
        .12 * p[21] + \
        .08 * p[9] + \
        .12 * p[0] + \
        .04 * p[5] + \
        .1 * p[3] + \
        .07 * p[25] + \
        .08 * p[26] + \
        .11 * p[27]
    pos.append('WB')
    pos.append(a)
    a = .05 * p[10] + \
        .07 * p[11] + \
        .08 * p[17] + \
        .08 * p[13] + \
        .12 * p[21] + \
        .07 * p[9] + \
        .09 * p[0] + \
        .04 * p[2] + \
        .07 * p[3] + \
        .08 * p[25] + \
        .11 * p[26] + \
        .14 * p[27]
    pos.append('FB')
    pos.append(a)
    a = .02 * p[11] + \
        .03 * p[16] + \
        .1 * p[18] + \
        .05 * p[13] + \
        .07 * p[20] + \
        .13 * p[21] + \
        .04 * p[9] + \
        .1 * p[2] + \
        .05 * p[3] + \
        .14 * p[25] + \
        .17 * p[26] + \
        .1 * p[27]
    pos.append('CB')
    pos.append(a)
    a = .06 * p[17] + \
        .04 * p[18] + \
        .07 * p[13] + \
        .05 * p[20] + \
        .14 * p[21] + \
        .04 * p[23] + \
        .1 * p[9] + \
        .1 * p[8] + \
        .14 * p[3] + \
        .09 * p[25] + \
        .12 * p[26] + \
        .05 * p[27]
    pos.append('DM')
    pos.append(a)
    a = .07 * p[10] + \
        .06 * p[11] + \
        .05 * p[17] + \
        .07 * p[13] + \
        .08 * p[22] + \
        .07 * p[23] + \
        .13 * p[9] + \
        .1 * p[0] + \
        .15 * p[5] + \
        .06 * p[1] + \
        .05 * p[8] + \
        .11 * p[3]
    pos.append('WM')
    pos.append(a)
    a = .06 * p[17] + \
        .08 * p[13] + \
        .05 * p[21] + \
        .06 * p[22] + \
        .13 * p[23] + \
        .14 * p[9] + \
        .07 * p[5] + \
        .02 * p[1] + \
        .13 * p[8] + \
        .17 * p[3] + \
        .04 * p[19] + \
        .05 * p[26]
    pos.append('CM')
    pos.append(a)
    a = .04 * p[10] + \
        .03 * p[11] + \
        .03 * p[12] + \
        .07 * p[13] + \
        .09 * p[22] + \
        .14 * p[23] + \
        .15 * p[9] + \
        .13 * p[5] + \
        .07 * p[1] + \
        .04 * p[8] + \
        .16 * p[3] + \
        .05 * p[19]
    pos.append('AM')
    pos.append(a)
    a = .05 * p[10] + \
        .05 * p[11] + \
        .09 * p[13] + \
        .13 * p[22] + \
        .08 * p[23] + \
        .15 * p[9] + \
        .14 * p[5] + \
        .11 * p[1] + \
        .02 * p[2] + \
        .09 * p[3] + \
        .05 * p[15] + \
        .04 * p[19]
    pos.append('CF')
    pos.append(a)
    a = .07 * p[10] + \
        .06 * p[11] + \
        .03 * p[12] + \
        .07 * p[13] + \
        .09 * p[22] + \
        .06 * p[23] + \
        .14 * p[9] + \
        .09 * p[0] + \
        .16 * p[5] + \
        .1 * p[1] + \
        .09 * p[3] + \
        .04 * p[19]
    pos.append('WW')
    pos.append(a)
    a = .04 * p[10] + \
        .05 * p[11] + \
        .05 * p[18] + \
        .08 * p[13] + \
        .13 * p[22] + \
        .1 * p[9] + \
        .07 * p[5] + \
        .18 * p[1] + \
        .1 * p[2] + \
        .05 * p[3] + \
        .1 * p[15] + \
        .03 * p[19] + \
        .02 * p[4]
    pos.append('ST')
    pos.append(a)
    # decide whether to round, while comparing two players, do not round.
    if do_round:
        for i in range(1, 21, 2):
            pos[i] = round(pos[i])
        return pos
    else:
        return pos


# point as an attacker
def as_attacker(p=[]):
    return (calc(p)[15] + calc(p)[17] + calc(p)[19]) / 3


# point as a midfield
def as_midfield(p=[]):
    return (calc(p)[9] + calc(p)[7] + calc(p)[11] + calc(p)[13]) / 4


# point as a defender
def as_defender(p=[]):
    return (calc(p)[1] + calc(p)[3] + calc(p)[5]) / 3


# calc six dimension as pointPAC,pointSHO,pointPAS,pointDRI,pointDEF,pointPHY
def six_d(p=[], do_round=True):
    pt = []
    pt.append(0.45 * p[10] + 0.55 * p[11])
    pt.append(0.45 * p[1] + 0.05 * p[4] + 0.2 * p[15] + 0.2 * p[19] + 0.05 * p[22] + 0.05 * p[24])
    pt.append(0.2 * p[0] + 0.35 * p[3] + 0.05 * p[6] + 0.05 * p[7] + 0.15 * p[8] + 0.2 * p[23])
    pt.append(0.5 * p[5] + 0.3 * p[9] + 0.1 * p[12] + 0.05 * p[13] + 0.05 * p[14])
    pt.append(0.1 * p[2] + 0.2 * p[21] + 0.3 * p[25] + 0.3 * p[26] + 0.1 * p[27])
    pt.append(0.05 * p[16] + 0.25 * p[17] + 0.5 * p[18] + 0.2 * p[20])
    if do_round:
        for i in range(6):
            pt[i] = round(pt[i])
        return pt
    else:
        return pt
