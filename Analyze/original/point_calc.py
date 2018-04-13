all_attr = [
    'Crossing', 'Finishing', 'Heading_Accuracy', 'Short_Passing', 'Volleys',
    'Dribbling', 'Curve', 'Free_Kick_Accuracy', 'Long_Passing', 'Ball_Control',
    'Acceleration', 'Sprint_Speed', 'Agility', 'Reactions', 'Balance',
    'Shot_Power', 'Jumping', 'Stamina', 'Strength', 'Long_Shots',
    'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties',
    'Marking', 'Standing_Tackle', 'Sliding_Tackle',
    'GK_Diving', 'GK_Handling', 'GK_Kicking', 'GK_Positioning', 'GK_Reflexes'
]


# calculate the ova of a player at each position, just input a dataframe
def calc(p, do_round=True):
    
    ova = {'GK': 0, 'FB': 0, 'WB': 0, 'CB': 0, 'DM': 0, 'CM': 0, 'WM': 0, 'AM': 0, 'WW': 0, 'CF': 0, 'ST': 0}

    a = .11 * p['Reactions'] + \
        .21 * p['GK_Diving'] + \
        .21 * p['GK_Handling'] + \
        .05 * p['GK_Kicking'] + \
        .21 * p['GK_Positioning'] + \
        .21 * p['GK_Reflexes']
    ova['GK'] = a

    a = .04 * p['Acceleration'] + \
        .06 * p['Sprint_Speed'] + \
        .1 * p['Stamina'] + \
        .08 * p['Reactions'] + \
        .12 * p['Interceptions'] + \
        .08 * p['Ball_Control'] + \
        .12 * p['Crossing'] + \
        .04 * p['Dribbling'] + \
        .1 * p['Short_Passing'] + \
        .07 * p['Marking'] + \
        .08 * p['Standing_Tackle'] + \
        .11 * p['Sliding_Tackle']
    ova['WB'] = a

    a = .05 * p['Acceleration'] + \
        .07 * p['Sprint_Speed'] + \
        .08 * p['Stamina'] + \
        .08 * p['Reactions'] + \
        .12 * p['Interceptions'] + \
        .07 * p['Ball_Control'] + \
        .09 * p['Crossing'] + \
        .04 * p['Heading_Accuracy'] + \
        .07 * p['Short_Passing'] + \
        .08 * p['Marking'] + \
        .11 * p['Standing_Tackle'] + \
        .14 * p['Sliding_Tackle']
    ova['FB'] = a

    a = .02 * p['Sprint_Speed'] + \
        .03 * p['Jumping'] + \
        .1 * p['Strength'] + \
        .05 * p['Reactions'] + \
        .07 * p['Aggression'] + \
        .13 * p['Interceptions'] + \
        .04 * p['Ball_Control'] + \
        .1 * p['Heading_Accuracy'] + \
        .05 * p['Short_Passing'] + \
        .14 * p['Marking'] + \
        .17 * p['Standing_Tackle'] + \
        .1 * p['Sliding_Tackle']
    ova['CB'] = a

    a = .06 * p['Stamina'] + \
        .04 * p['Strength'] + \
        .07 * p['Reactions'] + \
        .05 * p['Aggression'] + \
        .14 * p['Interceptions'] + \
        .04 * p['Vision'] + \
        .1 * p['Ball_Control'] + \
        .1 * p['Long_Passing'] + \
        .14 * p['Short_Passing'] + \
        .09 * p['Marking'] + \
        .12 * p['Standing_Tackle'] + \
        .05 * p['Sliding_Tackle']
    ova['DM'] = a

    a = .07 * p['Acceleration'] + \
        .06 * p['Sprint_Speed'] + \
        .05 * p['Stamina'] + \
        .07 * p['Reactions'] + \
        .08 * p['Positioning'] + \
        .07 * p['Vision'] + \
        .13 * p['Ball_Control'] + \
        .1 * p['Crossing'] + \
        .15 * p['Dribbling'] + \
        .06 * p['Finishing'] + \
        .05 * p['Long_Passing'] + \
        .11 * p['Short_Passing']
    ova['WM'] = a

    a = .06 * p['Stamina'] + \
        .08 * p['Reactions'] + \
        .05 * p['Interceptions'] + \
        .06 * p['Positioning'] + \
        .13 * p['Vision'] + \
        .14 * p['Ball_Control'] + \
        .07 * p['Dribbling'] + \
        .02 * p['Finishing'] + \
        .13 * p['Long_Passing'] + \
        .17 * p['Short_Passing'] + \
        .04 * p['Long_Shots'] + \
        .05 * p['Standing_Tackle']
    ova['CM'] = a

    a = .04 * p['Acceleration'] + \
        .03 * p['Sprint_Speed'] + \
        .03 * p['Agility'] + \
        .07 * p['Reactions'] + \
        .09 * p['Positioning'] + \
        .14 * p['Vision'] + \
        .15 * p['Ball_Control'] + \
        .13 * p['Dribbling'] + \
        .07 * p['Finishing'] + \
        .04 * p['Long_Passing'] + \
        .16 * p['Short_Passing'] + \
        .05 * p['Long_Shots']
    ova['AM'] = a

    a = .05 * p['Acceleration'] + \
        .05 * p['Sprint_Speed'] + \
        .09 * p['Reactions'] + \
        .13 * p['Positioning'] + \
        .08 * p['Vision'] + \
        .15 * p['Ball_Control'] + \
        .14 * p['Dribbling'] + \
        .11 * p['Finishing'] + \
        .02 * p['Heading_Accuracy'] + \
        .09 * p['Short_Passing'] + \
        .05 * p['Shot_Power'] + \
        .04 * p['Long_Shots']
    ova['CF'] = a

    a = .07 * p['Acceleration'] + \
        .06 * p['Sprint_Speed'] + \
        .03 * p['Agility'] + \
        .07 * p['Reactions'] + \
        .09 * p['Positioning'] + \
        .06 * p['Vision'] + \
        .14 * p['Ball_Control'] + \
        .09 * p['Crossing'] + \
        .16 * p['Dribbling'] + \
        .1 * p['Finishing'] + \
        .09 * p['Short_Passing'] + \
        .04 * p['Long_Shots']
    ova['WW'] = a

    a = .04 * p['Acceleration'] + \
        .05 * p['Sprint_Speed'] + \
        .05 * p['Strength'] + \
        .08 * p['Reactions'] + \
        .13 * p['Positioning'] + \
        .1 * p['Ball_Control'] + \
        .07 * p['Dribbling'] + \
        .18 * p['Finishing'] + \
        .1 * p['Heading_Accuracy'] + \
        .05 * p['Short_Passing'] + \
        .1 * p['Shot_Power'] + \
        .03 * p['Long_Shots'] + \
        .02 * p['Volleys']
    ova['ST'] = a

    # decide whether to round, while comparing two players, do not round.
    if do_round:
        for k, v in ova.items():
            ova[k] = int(round(float(v)))
        return ova
    else:
        for k, v in ova.items():
            ova[k] = float(v)
        return ova


# directly calc all in the dataframe, and return as df, so it is at a very high effect
def df_calc(p):
    p = p.copy()

    p['ovaGK'] = (.11 * p['Reactions'] +
                  .21 * p['GK_Diving'] +
                  .21 * p['GK_Handling'] +
                  .05 * p['GK_Kicking'] +
                  .21 * p['GK_Positioning'] +
                  .21 * p['GK_Reflexes'])

    p['ovaWB'] = (.04 * p['Acceleration'] +
                  .06 * p['Sprint_Speed'] +
                  .1 * p['Stamina'] +
                  .08 * p['Reactions'] +
                  .12 * p['Interceptions'] +
                  .08 * p['Ball_Control'] +
                  .12 * p['Crossing'] +
                  .04 * p['Dribbling'] +
                  .1 * p['Short_Passing'] +
                  .07 * p['Marking'] +
                  .08 * p['Standing_Tackle'] +
                  .11 * p['Sliding_Tackle'])

    p['ovaFB'] = (.05 * p['Acceleration'] +
                  .07 * p['Sprint_Speed'] +
                  .08 * p['Stamina'] +
                  .08 * p['Reactions'] +
                  .12 * p['Interceptions'] +
                  .07 * p['Ball_Control'] +
                  .09 * p['Crossing'] +
                  .04 * p['Heading_Accuracy'] +
                  .07 * p['Short_Passing'] +
                  .08 * p['Marking'] +
                  .11 * p['Standing_Tackle'] +
                  .14 * p['Sliding_Tackle'])

    p['ovaCB'] = (.02 * p['Sprint_Speed'] +
                  .03 * p['Jumping'] +
                  .1 * p['Strength'] +
                  .05 * p['Reactions'] +
                  .07 * p['Aggression'] +
                  .13 * p['Interceptions'] +
                  .04 * p['Ball_Control'] +
                  .1 * p['Heading_Accuracy'] +
                  .05 * p['Short_Passing'] +
                  .14 * p['Marking'] +
                  .17 * p['Standing_Tackle'] +
                  .1 * p['Sliding_Tackle'])

    p['ovaDM'] = (.06 * p['Stamina'] +
                  .04 * p['Strength'] +
                  .07 * p['Reactions'] +
                  .05 * p['Aggression'] +
                  .14 * p['Interceptions'] +
                  .04 * p['Vision'] +
                  .1 * p['Ball_Control'] +
                  .1 * p['Long_Passing'] +
                  .14 * p['Short_Passing'] +
                  .09 * p['Marking'] +
                  .12 * p['Standing_Tackle'] +
                  .05 * p['Sliding_Tackle'])

    p['ovaWM'] = (.07 * p['Acceleration'] +
                  .06 * p['Sprint_Speed'] +
                  .05 * p['Stamina'] +
                  .07 * p['Reactions'] +
                  .08 * p['Positioning'] +
                  .07 * p['Vision'] +
                  .13 * p['Ball_Control'] +
                  .1 * p['Crossing'] +
                  .15 * p['Dribbling'] +
                  .06 * p['Finishing'] +
                  .05 * p['Long_Passing'] +
                  .11 * p['Short_Passing'])

    p['ovaCM'] = (.06 * p['Stamina'] +
                  .08 * p['Reactions'] +
                  .05 * p['Interceptions'] +
                  .06 * p['Positioning'] +
                  .13 * p['Vision'] +
                  .14 * p['Ball_Control'] +
                  .07 * p['Dribbling'] +
                  .02 * p['Finishing'] +
                  .13 * p['Long_Passing'] +
                  .17 * p['Short_Passing'] +
                  .04 * p['Long_Shots'] +
                  .05 * p['Standing_Tackle'])

    p['ovaAM'] = (.04 * p['Acceleration'] +
                  .03 * p['Sprint_Speed'] +
                  .03 * p['Agility'] +
                  .07 * p['Reactions'] +
                  .09 * p['Positioning'] +
                  .14 * p['Vision'] +
                  .15 * p['Ball_Control'] +
                  .13 * p['Dribbling'] +
                  .07 * p['Finishing'] +
                  .04 * p['Long_Passing'] +
                  .16 * p['Short_Passing'] +
                  .05 * p['Long_Shots'])

    p['ovaCF'] = (.05 * p['Acceleration'] +
                  .05 * p['Sprint_Speed'] +
                  .09 * p['Reactions'] +
                  .13 * p['Positioning'] +
                  .08 * p['Vision'] +
                  .15 * p['Ball_Control'] +
                  .14 * p['Dribbling'] +
                  .11 * p['Finishing'] +
                  .02 * p['Heading_Accuracy'] +
                  .09 * p['Short_Passing'] +
                  .05 * p['Shot_Power'] +
                  .04 * p['Long_Shots'])

    p['ovaWW'] = (.07 * p['Acceleration'] +
                  .06 * p['Sprint_Speed'] +
                  .03 * p['Agility'] +
                  .07 * p['Reactions'] +
                  .09 * p['Positioning'] +
                  .06 * p['Vision'] +
                  .14 * p['Ball_Control'] +
                  .09 * p['Crossing'] +
                  .16 * p['Dribbling'] +
                  .1 * p['Finishing'] +
                  .09 * p['Short_Passing'] +
                  .04 * p['Long_Shots'])

    p['ovaST'] = (.04 * p['Acceleration'] +
                  .05 * p['Sprint_Speed'] +
                  .05 * p['Strength'] +
                  .08 * p['Reactions'] +
                  .13 * p['Positioning'] +
                  .1 * p['Ball_Control'] +
                  .07 * p['Dribbling'] +
                  .18 * p['Finishing'] +
                  .1 * p['Heading_Accuracy'] +
                  .05 * p['Short_Passing'] +
                  .1 * p['Shot_Power'] +
                  .03 * p['Long_Shots'] +
                  .02 * p['Volleys'])
    # not to do a round, because there is no need to do so
    return p


# point as an attacker
def as_attacker(p):
    return (calc(p, False)['WW'] + calc(p, False)['CF'] + calc(p, False)['ST']) / 3


# point as a midfield
def as_midfield(p):
    return (calc(p, False)['DM'] + calc(p, False)['CM'] + calc(p, False)['AM'] + calc(p, False)['WM']) / 4


# point as a defender
def as_defender(p):
    return (calc(p, False)['FB'] + calc(p, False)['WB'] + calc(p, False)['CB']) / 3


def as_gk(p):
    return calc(p)['GK']


# calc six dimension as pointPAC,pointSHO,pointPAS,pointDRI,pointDEF,pointPHY
# or might pointDIV,pointHAN,pointKIC,pointREF,pointSPD,pointPOS => add it in the future
def six_d(p, do_round=True):
    p = p[all_attr].values[0]
    pt = [0.45 * p[10] + 0.55 * p[11],
          0.45 * p[1] + 0.05 * p[4] + 0.2 * p[15] + 0.2 * p[19] + 0.05 * p[22] + 0.05 * p[24],
          0.2 * p[0] + 0.35 * p[3] + 0.05 * p[6] + 0.05 * p[7] + 0.15 * p[8] + 0.2 * p[23],
          0.5 * p[5] + 0.3 * p[9] + 0.1 * p[12] + 0.05 * p[13] + 0.05 * p[14],
          0.1 * p[2] + 0.2 * p[21] + 0.3 * p[25] + 0.3 * p[26] + 0.1 * p[27],
          0.05 * p[16] + 0.25 * p[17] + 0.5 * p[18] + 0.2 * p[20]]
    if do_round:
        return list(map(lambda x: int(round(x)), pt))
    else:
        return pt
