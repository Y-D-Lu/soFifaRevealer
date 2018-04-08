# select first league of a nation, return
def select_first(c):
    cs=c
    for i in range(c['ID'].count()):
        if c.iloc[i,2].find('(1)') == -1:
            cs=cs.drop(i)

    return cs
