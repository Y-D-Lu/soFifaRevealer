from Analyze.desc import *
from Analyze.plotting import *
data = pd.DataFrame(pd.read_csv('data/18.csv'))
club = pd.DataFrame(pd.read_csv('data/club18.csv'))

# # show the player counts of every ova, can see form the chart that it almost obey the Gaussian distribution
# plot_num(data,x='ova',y='ID')

# # the players' count of every age, clearly, is right skewed
# plot_num(data,x='Age',y='ID')

# # then let's see the trend of ova and potential by Ages, it's high time to grow from 17 to 26.
# plot_age(data,x='Age',y=['ova','potential'],method=map_method['mean'])

# # as for the players have a higher socre than the 3rd Quartile, is 18 to 25.
# plot_age(data,x='Age',y=['ova','potential'],method=map_method['0.75'])

# # we draw a density map to see more clearly, the relation between Age and ova, or something else.
# plot_density(data, x='Age', y='ova')

# # i know it's crazy, but yes, we did, use a candlestick chart in the analyzing for soccer player, just see the trend.
# # well, i set 3rd Quartile as high and 1st Quartile as low, and if a right skewed print if green, red versa.
# # see from that: before 28 is the golden age of a player, maybe get a sudden active in 31,32.
# plot_candlestick(data)

# # well, Iniesta is leaving FCB and may need to find a replacer for him, his ID in FIFA is 41
# # just print the dict returned by the func
# print(similar(data, 41, 10))
# # as {0: [41, 'Andrés Iniesta Luján ', 0.0], 1: [176635, 'Mesut Özil ', 11.0], 2: [186942, 'İlkay Gündoğan ', 13.0],..

# # so we may want to know the differfence between those players, it's a good idea to get a radar map.(as FIFA default)
# # we add Iniesta, Özil and Gündoğan. From that we can see, Gündoğan is almost the best choice, if not consider more.
# plot_radar6d(select_player_by_list(data,[41,176635,186942]))
